import unittest
import pybbg
import datetime
from dateutil.relativedelta import relativedelta

class TestPybbg(unittest.TestCase):
    def test_bdp(self):
        tester = pybbg.Pybbg()
        data = tester.bdp(['060310 KS Equity', '299170 KS Equity'], ['BETA_RAW_OVERRIDABLE', 'TOT_DEBT_TO_TOT_EQY', 'BETA_ADJ_OVERRIDABLE'])
        print(data)


if __name__ == '__main__':
    unittest.main()
