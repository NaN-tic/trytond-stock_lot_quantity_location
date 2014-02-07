#This file is part stock_lot_quantity_location module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.pool import Pool
from .stock import *


def register():
    Pool.register(
        LotByLocationStart,
        module='stock_lot_quantity_location', type_='model')
    Pool.register(
        LotByLocation,
        module='stock_lot_quantity_location', type_='wizard')
