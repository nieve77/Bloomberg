import unittest
import pybbg
import datetime
import cx_Oracle
import pandas as pd
from dateutil.relativedelta import relativedelta



class Bloomberg_Beta(unittest.TestCase):
    #베타풀 데이터 블룸버그 API를 통해 RAW_ BETA,DEBT/EQUITY, ADJUSTED BETA데이터를 가져와 상장기업정보내역 테이블(ENT_LSTENT_INFO)에 저장
    def test_beta_bdp(self):
        ent_code=[]
        ent_code_num=[]
        data_ex = []
        data_value = []

        # TPO 데이터베이스 계정 접속
        con = cx_Oracle.connect('TPO/npi0708@10.0.1.30:1521/PNIDB')
        cur = con.cursor()


        # cur.execute("select * from ent_lstentinfo where std_dt='20181031' and rownum<4") 테스트용
        cur.execute("select * from ent_lstentinfo where std_dt=TO_CHAR(SYSDATE,'YYYYMMDD')")
        # 데이터가이드에서 당일에 가져온 기업들의 데이터를 리스트로 가져온다
        for result in cur:
            ent_code.append(result[1] + ' KS EQUITY') # 블룸버그 API에 사용될 상장기업코드
            ent_code_num.append(result[1])  #상장기업코드
            data_ex.append(result[1]) #상장기업코드
            data_ex.append(result[2]) #등록일자
            data_ex.append(result[3]) #등록자ID
            data_ex.append(result[4]) #수정일자
            data_ex.append(result[5]) #수정자ID
            data_ex.append(result[6]) #상장기업명
            data_ex.append(result[7]) #영문기업명
            data_ex.append(result[31]) #상장일자
            data_value.append(data_ex)
            data_ex = []

        index = pd.Index(ent_code)
        # 상장기업코드를 데이터프레임으로 만들어 블룸버그상장기업코드를 인덱스로 지정
        ent_code_num= pd.DataFrame({'ent_code_num' :ent_code_num})
        ent_code_num.index=index

        # cur.executemany("INSERT INTO ENT_LSTENTINFO(STD_DT, LSTENT_CD, REG_DTM, REGR_ID, MDFY_DTM, MDFY_ID, ENT_NM, ENT_ENG_NM, LIST_DT) VALUES (TO_CHAR(SYSDATE-300,'YYYYMMDD'), :1, :2, :3, :4, :5, :6, :7, :8)",data_value)
        # con.commit()

        #RAW_ BETA, ADJUSTED BETA 가져오는 함수
        beta_ar = pybbg.Pybbg()
        df = beta_ar.bdp(ent_code, ['BETA_ADJ_OVERRIDABLE', 'BETA_RAW_OVERRIDABLE'])
        # print(df)

        # BETA,DEBT/EQUITY 가져오는 함수
        beta_tot = pybbg.Pybbg()
        df1 = beta_tot.bdp(ent_code, ['TOT_DEBT_TO_TOT_EQY'], overrides={'FUND_PER': 'Q'})
        # print(df1)

        #세 항목을 병합하고 기업코드 행추가
        df_result = pd.concat([df, df1])
        df_result = df_result.append(ent_code_num.transpose())
        # print(df_result)


        rows = [tuple(x) for x in df_result.transpose().values]
        # print(rows)

        cur.executemany("UPDATE ENT_LSTENTINFO SET RAW_BETA=:1, ADJE_BETA=:2, DEBT_EQUITY=:3 WHERE STD_DT=TO_CHAR(SYSDATE,'YYYYMMDD') AND LSTENT_CD=:4", rows)
        con.commit()

        con.close()


    # WACC추정 데이터 블룸버그 API를 통해 배당수익률, 성장률, 배당금분배율, 시장수익률, 무위험이자율, 시장위험프리미엄데이터를 가져와 가중평균자본비용내역 테이블(ENT_WAGCOCP)에 저장
    def test_country_risk_bdh(self):

        # 최근 2~3일치의 기업가치가중치평균자본비용 데이터를 리스트로 가져온다
        wacc_etc = pybbg.Pybbg()
        dr = wacc_etc.bdh(['005930 KS Equity'],['COUNTRY_RISK_DIVIDEND_YIELD', 'COUNTRY_RISK_GROWTH_RATE', 'COUNTRY_RISK_PAYOUT_RATIO', 'COUNTRY_RISK_MARKET_RETURN'],
                          datetime.datetime.now().date() + datetime.timedelta(days=-4), datetime.datetime.now().date() + datetime.timedelta(days=-1))

        # 위에서 COUNTRY_RISK_RFR로 값이 나와야하는데 어떤때는 나오고 어떤때는 나오지 않아 따로 분리해 다른 값 전달
        wacc_rfr = pybbg.Pybbg()
        dr1 = wacc_rfr.bdh(['GVSK10YR Index'], ['PX_LAST'],
                            datetime.datetime.now().date() + datetime.timedelta(days=-4), datetime.datetime.now().date() + datetime.timedelta(days=-1))
        print(dr1)

        wacc_prem = pybbg.Pybbg()
        dr2 =wacc_prem.bdh("005930 KS Equity", ["COUNTRY_RISK_PREMIUM"],
                           datetime.datetime.now().date() + datetime.timedelta(days=-4), datetime.datetime.now().date() + datetime.timedelta(days=-1))
        print(dr2)

        #dr,dr1,d2 세 항목을 병합해서 처리
        dr_result = pd.concat([dr, dr1, dr2],axis=1)

        dr_result=dr_result.reset_index()
        dr_result.rename(columns={'index' : 'std_dt'}, inplace=True)
        dr_result['std_dt'] = dr_result['std_dt'].apply(lambda x: x.strftime('%Y%m%d'))
        print(dr_result)


        rows = [tuple(x) for x in dr_result.values]
        print(rows)

        # TPO 데이터베이스 계정 접속
        con = cx_Oracle.connect('TPO/npi0708@10.0.1.30:1521/PNIDB')
        cur = con.cursor()

        # Merge문을 이용해 값이 있으면 Update 값이 없으면 Inseert구문 실행
        str = """MERGE INTO ENT_WAGCOCP USING DUAL ON
             ( STD_DT = :1 )
          WHEN MATCHED THEN
            UPDATE
            SET MDFY_DTM    = SYSDATE
            , DIVD_ERNR    = :2
            , GRW_RT    = :3
            , DIVDAM_SHR_RT = :4
            , MKT_ERNR = :5
            , RF_INT_RT = :6
            , RSK_PREM = :7
          WHEN NOT MATCHED THEN
            INSERT
             ( STD_DT
             , REG_DTM
             , REGR_ID
             , MDFY_DTM
             , MDFY_ID
             , DIVD_ERNR
             , GRW_RT
             , DIVDAM_SHR_RT
             , MKT_ERNR
             , RF_INT_RT
             , RSK_PREM
             )
             VALUES
             ( :1
             , SYSDATE
             , 'SYSTEM'
             , SYSDATE
             , 'SYSTEM'
             , :2
             , :3
             , :4
             , :5
             , :6
             , :7
             )""".replace('\n',' ')

        cur.executemany(str, rows)
        con.commit()
        con.close()


if __name__ == '__main__':
    unittest.main()





