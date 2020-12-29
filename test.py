import pandas as pd

df = pd.DataFrame({'A': list('AAA'), 'B': range(3), 'C': range(3), 'D': range(3), 'E': range(3), 'F': range(3)}, index=list('xyz'))

df.insert(0, 'index', pd.datetime.now().replace(microsecond=0))
# print (df['TimeStamp'])

df.rename(columns={'index':'std_dt'},inplace=True)
# print(df)

df['std_dt']=df['std_dt'].apply(lambda x: x.strftime('%Y%m%d'))
# print(df['F'])
# print(df['A'])

rows = [tuple(x) for x in df.values]
print(rows)




