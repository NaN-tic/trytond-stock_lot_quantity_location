#This file is part stock_lot_quantity_location module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.pool import Pool, PoolMeta
from trytond.pyson import PYSONEncoder, If, Eval, Bool

__all__ = ['Move', 'LotByLocationStart', 'LotByLocation']
__metaclass__ = PoolMeta


class Move:
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

    @classmethod
    def default_location(cls):
        Location = Pool().get('stock.location')
        locations = Location.search([('type', '=', 'warehouse')])
        if len(locations) == 1:
            return locations[0].id


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
        context['locations'] = [self.start.location.id]
        action['pyson_context'] = PYSONEncoder().encode(context)
        action['name'] += ' - %s' % (location.rec_name)
        return action, {}
