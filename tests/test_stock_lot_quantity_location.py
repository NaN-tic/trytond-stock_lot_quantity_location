# This file is part of the stock_lot_quantity_location module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class StockLotQuantityLocationTestCase(ModuleTestCase):
    'Test Stock Lot Quantity Location module'
    module = 'stock_lot_quantity_location'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockLotQuantityLocationTestCase))
    return suite
