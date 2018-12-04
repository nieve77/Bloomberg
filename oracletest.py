import cx_Oracle

con = cx_Oracle.connect('TPO/npi0708@10.0.1.30:1521/PNIDB')

cur=con.cursor()


cur.execute("select * from ent_issuinfom where std_dt='20161231'")
for result in cur:
    print(result)
con.close()