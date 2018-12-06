import unittest
import pybbg
import datetime
from dateutil.relativedelta import relativedelta

class Bloomberg_Beta(unittest.TestCase):
    def test_bdp(self):
        beta_tot = pybbg.Pybbg()
        data = beta_tot.bdp(['060310 KS Equity', '095570 KS Equity', '068400 KS Equity'],
                          ['BETA_ADJ_OVERRIDABLE', 'BETA_RAW_OVERRIDABLE'])
        print(data)

    def beta_bdp_tot(self):
        beta_tot = pybbg.Pybbg()
        data = beta_tot.bdp(['060310 KS Equity', '095570 KS Equity','068400 KS Equity'],['TOT_DEBT_TO_TOT_EQY'],overrides={'FUND_PER':'Q'})
        print(data)

    def country_risk_bdh(self):
        country_risk = pybbg.Pybbg()
        data = country_risk.bdh(['005930 KS Equity'], ['COUNTRY_RISK_DIVIDEND_YIELD','COUNTRY_RISK_GROWTH_RATE','COUNTRY_RISK_PAYOUT_RATIO','COUNTRY_RISK_MARKET_RETURN','COUNTRY_RISK_RFR','COUNTRY_RISK_PREMIUM'],
                          datetime.datetime.now().date() + datetime.timedelta(days=-4), datetime.datetime.now().date() + datetime.timedelta(days=-1))
        print(data)

if __name__ == '__main__':
    unittest.main()





