#This file is part stock_lot_quantity_location module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.pool import PoolMeta
from trytond.pyson import PYSONEncoder

__all__ = ['LotByLocationStart', 'LotByLocation']
__metaclass__ = PoolMeta


class LotByLocationStart(ModelView):
    'Lot By Location'
    __name__ = 'lot.by.location.start'
    location = fields.Many2One('stock.location', 'Location', required=True)


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
