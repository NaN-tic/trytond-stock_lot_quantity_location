# This file is part stock_lot_quantity_location module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import stock

def register():
    Pool.register(
        stock.Lot,
        stock.Move,
        stock.LotByLocationStart,
        module='stock_lot_quantity_location', type_='model')
    Pool.register(
        stock.LotByLocation,
        module='stock_lot_quantity_location', type_='wizard')
