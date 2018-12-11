import pandas as pd

data={
   'BETA_RAW_OVERRIDABLE' : [1.002866, 0.5914072, 1.568849],
   'BETA_ADJ_OVERRIDABLE' : [1.0019, 0.7275975, 1.379219]
}

data1={
   'TOT_DEBT_TO_TOT_EQY'  : [41.609143, 330.58945, 339.60199]
}

df=pd.DataFrame(data)
df1=pd.DataFrame(data1)

data=[]
data1=[]

df_result=pd.concat([df,df1],axis=1)
# print(df_result)
#
#
# print(df_result.transpose())


rows = [tuple(x) for x in df_result.values]
print(rows)









#-------------------------------------------------------------

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import font_manager, rc
#
# data={
#     'year' : [2016,2017,2018],
#     'GDP rate' : [2.8,3.1,3.0],
#     'GDP' : ['1.637M','1.73M','1.83M']
# }
#
# df=pd.DataFrame(data)
#
# print(df)
# print()
# print(df.describe())
# font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
# rc('font', family=font_name)
# df=pd.read_excel('C:\\Users\\ysyoon\\PycharmProjects\\Bloomberg_Project\\1.xlsx')
#
# plt.bar(df.ID,df["국어"])
# plt.show()




#-------------------------------------------------------------

# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib import font_manager, rc
#
# font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
# rc('font', family=font_name)
#
# industry = ['통신업', '의료정밀', '운수창고업', '의약품', '음식료품', '전기가스업', '서비스업', '전기전자', '종이목재', '증권']
# fluctuations = [1.83, 1.30, 1.30, 1.26, 1.06, 0.93, 0.77, 0.68, 0.65, 0.61]
#
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111)
#
# ypos = np.arange(10)
# rects = plt.barh(ypos, fluctuations, align='center', height=0.5)
# plt.yticks(ypos, industry)
#
# plt.xlabel('등락률')
# plt.show()

#-------------------------------------------------------------