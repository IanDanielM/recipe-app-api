from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    """tests the calc module"""

    def test_add_number(self):
        """testing the add function"""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """Testing the subtract function"""

        res = calc.subtract(15, 10)
        self.assertEqual(res, 5)
