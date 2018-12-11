import cx_Oracle

con = cx_Oracle.connect('TPO/npi0708@10.0.1.30:1521/PNIDB')

cur=con.cursor()

data_ex=[]
data=[]

cur.execute("select * from ent_lstentinfo where std_dt='20181031'")

for result in cur:
     data_ex.append(result[1])
     data_ex.append(result[2])
     data_ex.append(result[3])
     data_ex.append(result[4])
     data_ex.append(result[5])
     data_ex.append(result[6])
     data_ex.append(result[7])
     data_ex.append(result[31])
     data.append(data_ex)
     data_ex=[]
print(data)

# cur.executemany("INSERT INTO ENT_LSTENTINFO(STD_DT, LSTENT_CD, REG_DTM, REGR_ID, MDFY_DTM, MDFY_ID, ENT_NM, ENT_ENG_NM, LIST_DT) VALUES (TO_CHAR(SYSDATE,'YYYYMMDD'), :1, :2, :3, :4, :5, :6, :7, :8)",data)

con.commit()
con.close()