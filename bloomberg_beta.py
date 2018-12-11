import unittest
import pybbg
import datetime
import cx_Oracle
import pandas as pd
from dateutil.relativedelta import relativedelta



class Bloomberg_Beta(unittest.TestCase):
    def test_beta_bdp(self):
        ent_code=[]
        data_ex = []
        data_value = []
        con = cx_Oracle.connect('TPO/npi0708@10.0.1.30:1521/PNIDB')
        cur = con.cursor()

        cur.execute("select * from ent_lstentinfo where std_dt='20181031'")
        for result in cur:
            ent_code.append(result[1]+ ' KS EQUITY')
            data_ex.append(result[1])
            data_ex.append(result[2])
            data_ex.append(result[3])
            data_ex.append(result[4])
            data_ex.append(result[5])
            data_ex.append(result[6])
            data_ex.append(result[7])
            data_ex.append(result[31])
            data_value.append(data_ex)
            data_ex = []

        # cur.executemany("INSERT INTO ENT_LSTENTINFO(STD_DT, LSTENT_CD, REG_DTM, REGR_ID, MDFY_DTM, MDFY_ID, ENT_NM, ENT_ENG_NM, LIST_DT) VALUES (TO_CHAR(SYSDATE+100,'YYYYMMDD'), :1, :2, :3, :4, :5, :6, :7, :8)",data_value)
        # con.commit()

        beta_ar = pybbg.Pybbg()
        df = beta_ar.bdp(ent_code, ['BETA_ADJ_OVERRIDABLE', 'BETA_RAW_OVERRIDABLE'])
        print(df)

        beta_tot = pybbg.Pybbg()
        df1 = beta_tot.bdp(ent_code, ['TOT_DEBT_TO_TOT_EQY'], overrides={'FUND_PER': 'Q'})
        print(df1)

        df_result = pd.concat([df, df1])
        # df_result.pivot(index='')
        rows = [tuple(x) for x in df_result.transpose().values]
        print(rows)

        # cur.executemany('''UPDATE ENT_LSTENTINFO SET RAW_BETA=:1, ADJE_BETA=:2, DEBT_EQUITY=:3 WHERE STD_DT=TO_CHAR(SYSDATE+100,'YYYYMMDD')''', rows)
        # con.commit()

        con.close()


    # def test_beta_bdp_tot(self):
    #     beta_tot = pybbg.Pybbg()
    #     data = beta_tot.bdp(['ent_code'],['TOT_DEBT_TO_TOT_EQY'],overrides={'FUND_PER':'Q'})
    #     print(data)


    # def test_country_risk_bdh(self):
    #     country_risk = pybbg.Pybbg()
    #     data = country_risk.bdh(['005930 KS Equity'], ['COUNTRY_RISK_DIVIDEND_YIELD','COUNTRY_RISK_GROWTH_RATE','COUNTRY_RISK_PAYOUT_RATIO','COUNTRY_RISK_MARKET_RETURN','COUNTRY_RISK_RFR','COUNTRY_RISK_PREMIUM'],
    #                       datetime.datetime.now().date() + datetime.timedelta(days=-4), datetime.datetime.now().date() + datetime.timedelta(days=-1))
    #     print(data)

if __name__ == '__main__':
    unittest.main()





