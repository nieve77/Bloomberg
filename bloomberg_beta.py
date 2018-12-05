import unittest
import pybbg
import datetime
from dateutil.relativedelta import relativedelta

class TestPybbg(unittest.TestCase):
    def test_bdp(self):
        tester = pybbg.Pybbg()
        data = tester.bdp(['060310 KS Equity', '095570 KS Equity','068400 KS Equity'], ['BETA_ADJ_OVERRIDABLE', 'BETA_RAW_OVERRIDABLE'])
        print(data)

    def test_bdh(self):
        tester = pybbg.Pybbg()
        data = tester.bdh(['005930 KS Equity'], ['COUNTRY_RISK_RFR','COUNTRY_RISK_PREMIUM'],
                          datetime.datetime.today() + datetime.timedelta(days=-5), datetime.datetime.today() + datetime.timedelta(days=-1))
        print(data)

    def test_bdp_tot(self):
        tester = pybbg.Pybbg()
        data = tester.bdp(['060310 KS Equity', '095570 KS Equity','068400 KS Equity'],['TOT_DEBT_TO_TOT_EQY'],overrides={'FUND_PER':'Q'})
        print(data)

if __name__ == '__main__':
    unittest.main()
