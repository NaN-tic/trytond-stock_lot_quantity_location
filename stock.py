# This file is part stock_lot_quantity_location module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import datetime
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.pool import Pool, PoolMeta
from trytond.pyson import PYSONEncoder, If, Eval, Bool, Date
from trytond.transaction import Transaction


class Lot(metaclass=PoolMeta):
    __name__ = 'stock.lot'

    @classmethod
    def get_quantity(cls, lots, name):
        Location = Pool().get('stock.location')

        if 'locations' not in Transaction().context:
            warehouses = Location.search([('type', '=', 'warehouse')])
            location_ids = [w.storage_location.id for w in warehouses]
            with Transaction().set_context(locations=location_ids):
                return super(Lot, cls).get_quantity(lots, name)
        return super(Lot, cls).get_quantity(lots, name)

    @classmethod
    def search_quantity(cls, name, domain=None):
        Location = Pool().get('stock.location')

        if 'locations' not in Transaction().context:
            warehouses = Location.search([('type', '=', 'warehouse')])
            location_ids = [w.storage_location.id for w in warehouses]
            with Transaction().set_context(locations=location_ids):
                return super(Lot, cls).search_quantity(name, domain)
        return super(Lot, cls).search_quantity(name, domain)


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'

    @classmethod
    def __setup__(cls):
        super(Move, cls).__setup__()
        cls.lot.context.update({
            'locations': If(Bool(Eval('from_location')),
                [Eval('from_location')], []),
            })


class LotByLocationStart(ModelView):
    'Lot By Location'
    __name__ = 'lot.by.location.start'
    location = fields.Many2One('stock.location', 'Location', required=True)
    forecast_date = fields.Date(
        'At Date', help=('Allow to compute expected '
            'stock quantities for this date.\n'
            '* An empty value is an infinite date in the future.\n'
            '* A date in the past will provide historical values.'))
    lot = fields.Many2One('stock.lot', 'Lot',)

    @staticmethod
    def default_location():
        Location = Pool().get('stock.location')
        locations = Location.search([('type', '=', 'warehouse')])
        if len(locations) == 1:
            return locations[0].id

    @staticmethod
    def default_forecast_date():
        Date_ = Pool().get('ir.date')
        return Date_.today()

    @staticmethod
    def default_lot():
        model = Transaction().context.get('active_model')
        if model == 'stock.lot':
            return Transaction().context.get('active_id')
        return None


class LotByLocation(Wizard):
    'Lot By Location'
    __name__ = 'lot.by_location'
    start = StateView('lot.by.location.start',
        'stock_lot_quantity_location.lot_by_location_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Get quantities', 'open', 'tryton-ok', default=True),
            ])
    open = StateAction('stock_lot_quantity_location.act_lot_by_location_tree')

    def do_open(self, action):
        location = self.start.location

        context = {}
        date = self.start.forecast_date or datetime.date.max
        context['stock_date_end'] = Date(date.year, date.month, date.day)
        context['locations'] = [self.start.location.id]
        action['pyson_context'] = PYSONEncoder().encode(context)
        action['name'] += ' - %s' % (location.rec_name)
        if self.start.lot:
            domain = [('id', '=', self.start.lot.id)]
            action['pyson_domain'] = PYSONEncoder().encode(domain)
        return action, {}
