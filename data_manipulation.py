import pandas as pd
import numpy as np

#Reading the dataset in
df = pd.read_csv("/Users/asreedhar/Downloads/census.csv",\
    names=['age','workclass','fnlwgt','education','education-num','marital-status',\
        'occupation','relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country'
        ],index_col=False)

#Subset the dataset to ony columns that are required
df = df[['workclass','marital-status','capital-gain','capital-loss','hours-per-week']].copy(deep=True)

#Adding a default value column to the df
df['default'] = 'Default'

#Iterating through a DataFrame
for index, row in df.iterrows():
    print (index,row)
    break

#Subset or slicing based o index
ilocdf = df.iloc[:,0:3]
ilocdf_row = df.iloc[0:10,:]

#Reset index and drop it
df.reset_index(drop=True,inplace=True)

#Add a column for ids for merging
df['id'] = np.arange(df.shape[0])

#Create 2 df's for merging
df_1 = df[['id','workclass','marital-status','capital-gain']].copy(deep=True)
df_2 = df[['id','capital-loss']].copy(deep=True)
df_3 = df[['id','hours-per-week']].copy(deep=True)

#Merge into a new df
df_total = pd.merge(df_1,df_2,on=['id'],how='inner')

#Do a merge using left on and right on keyword arguments
df_total = pd.merge(df_1,df_2,left_on=['id'],right_on=['id'],how='inner').copy(deep=True)

#Do a merge to the left df and put it into a new df and merge another df to it
df_interim = df_1.merge(df_2,on='id',how='inner')
fulldf = df_interim.merge(df_3,on=['id'],how='inner')

#Groupby and get the sum of the data over 2 columns
sumdf = fulldf.groupby(['workclass']).sum()[['capital-gain','capital-loss']]

#Groupby and get the min/max over few columns
min_max_df = fulldf.groupby(['marital-status']).agg(['min','max'])[['capital-gain','capital-loss']]

#Groupby and specify individual functions over columns
aggdf = fulldf.groupby(['workclass']).agg({'capital-gain':['min','max'],'capital-loss':'min'})[['capital-gain','capital-loss']]

#Groupby and find the mean,min,median
avgdf = fulldf.groupby(['workclass']).agg(['mean','sum','median'])[['capital-gain','capital-loss']]

#Find the rank over partition and put it into a column
fulldf['rank'] = fulldf.groupby(['workclass'])['capital-gain'].rank(method='first',ascending=True).astype(int)
#Sort the df to get the paritioned df with ranks sorted in partitioned groups 
rankdf = fulldf.sort_values(by=['workclass','rank'],ascending=True)

#Sort over 2 columns but in different orientations
new_rankdf = rankdf.sort_values(by=['workclass','rank'],ascending=[False,True]).copy(deep=True)

#Extract only the top row of each group
topdf = rankdf.loc[rankdf['rank']==1].copy(deep=True)

#Find the groupby over 2 columns and do the ranking
fulldf['new_rank'] = fulldf.groupby(['workclass','marital-status'])['hours-per-week'].rank(method='first',ascending=True).astype(int)

#Find the groupby and then the rank ordering partition by 2 columns
fulldf = fulldf.sort_values(by=['hours-per-week','marital-status'],ascending=True)
fulldf['new_ranking'] = tuple(zip(fulldf['hours-per-week'],fulldf['marital-status']))
fulldf['new_ranking'] = fulldf.groupby(['workclass'],sort=False)['new_ranking'].apply(lambda x: pd.Series(pd.factorize(x)[0])).values

#Pivot tables allow aggregation
pivot_table_df = pd.pivot_table(fulldf,values=['hours-per-week'],index=['workclass'],columns=['marital-status'],aggfunc=np.mean,fill_value=0)
#index is horizontal axis categories
#columns is vertical axis categories
#values is the numeric column you want the aggregation off in each category combination

#Pivot the dataframe. No aggregation just flipping things around
list_1 = ['car','cat','dog']
list_2 = [1,2,3]
list_3 = ['new', 'old','new']
test_df = pd.DataFrame(list(zip(list_1,list_2,list_3)),columns=['image_name','count','image_type'])
pivot_df = test_df.pivot(index=['image_name'],columns=['image_type'],values=['count'])

#Replace values in the df based on some condition. This adjusts the value in place.
test_df.loc[test_df['count']>2,'count'] = 0
#.loc[condition for selection,column needed to modify]

#Series sort 
series_workclass = fulldf['workclass'].copy(deep=True)
series_workclass.sort_values(ascending=True,inplace=True)

#Get value counts for Series
series_workclass.value_counts()

#Get value counts for Df
df_workclass = fulldf[['workclass']]
df_workclass.value_counts()

#Subset rows based on conditions
hours_df = fulldf.loc[fulldf['hours-per-week'] == 60]
hours_capital_df = fulldf.loc[(fulldf['hours-per-week'] == 60) & (fulldf['capital-loss'] ==0)]
hours_multiple_df = fulldf.loc[fulldf['hours-per-week'].isin([40,60])]

#Selecting a cell
cell = fulldf.iloc[0]['workclass']
cell_index = fulldf.iloc[0][1]

#concat multiple df into one horizontally
c_df_1 = fulldf.iloc[0:100,:].copy(deep=True)
c_df_2 = fulldf.iloc[100:200,:].copy(deep=True)
c_df_3 = fulldf.iloc[200:300,:].copy(deep=True)

concat_df = pd.concat([c_df_1,c_df_2,c_df_3]) #Horizonatal concatenation

#Concat multiple df into one vertically
h_df_1 = df[['id','workclass','marital-status','capital-gain']].copy(deep=True)
h_df_2 = df[['capital-loss']].copy(deep=True)
h_df_3 = df[['hours-per-week']].copy(deep=True)

hconcat_df = pd.concat([h_df_1,h_df_2,h_df_3],axis= 1)

#Reading a list into a df
list_1 = ['car','cat','dog']
ldf_1 = pd.DataFrame(list_1,columns=['image_name'])

#Reading 2 parellel lists into a df
list_2 = [1,2,3]
ldf_2 = pd.DataFrame(list(zip(list_1,list_2)),columns=['image_name','count'])

#Reading a list of lists into a df
list_3 = [['cat',2],['dog',3],['cow',4]]
ldf_3 = pd.DataFrame(list_3, columns=['image_name','count'])

#Reading a dictionary into a df
dict_1 = {'image_name':['cat','dog','cow'],'count':[1,2,3]}
ddf_1 = pd.DataFrame.from_dict(dict_1)
dict_2 = {0:['cat',2],1:['dog',3],2:['cow',3]}
ddf_2 = pd.DataFrame.from_dict(dict_2,orient='index',columns=['image_name','count'])

#Converting Series to list
series_list_1 = fulldf['workclass'].to_list()

#Converting df to list Converts it into a list of lists
df_list_1 = fulldf[['workclass']].values.tolist()
df_list_2 = fulldf[['workclass','marital-status']].values.tolist()

#Converting df to a dictionary
r_dict=fulldf.to_dict(orient='records')
l_dict = fulldf.to_dict(orient='list')
s_dict = fulldf.to_dict(orient='series')
d_dict = fulldf.to_dict(orient='dict')
i_dict = fulldf.to_dict(orient='index')

#Converting all the stuff back
r_df = pd.DataFrame.from_dict(r_dict)
l_df = pd.DataFrame.from_dict(l_dict)
i_df = pd.DataFrame.from_dict(i_dict,orient='index')

#Looping through a dictionary
for key, value in dict_1.items():
    print(key,value)

#Get min, max values out of a dictionary
dict_3 = {'west':5,'east':2,'north':1,'south':8}
min(dict_3,key=dict_3.get)
max(dict_3,key=dict_3.get)

#Get min and max of a list
list_4 = [1,2,3,4]
min(list_4)
max(list_4)


arr = np.array([1,2,3])

#Enumerating for ndarray
for idx, value in np.ndenumerate(arr):
    print(idx,value)
    break

#Convert 2 list into dictionary
list_key = ['north','south']
list_values = [2,3]
list_dict = dict(zip(list_key,list_values))

#Convert single list into dict
dict_list = ['north',2,'south',3]
it = iter(dict_list)
dict_new = dict(zip(it,it))

#Convert dict to list
new_list = list(dict_new.items()) #Create a list of tuples (key,value)
new_keys = list(dict_new.keys())
new_values = list(dict_new.values())

#Make copy of the table for easier manipulation
df_sql = df.copy(deep=True)
df_sql.columns = ['workclass','marital_status','capital_gain','capital_loss','hours_per_week','default','id']

#Trying some sql based connections
from sqlite3 import connect
conn = connect(':memory:')
df_sql.to_sql('df_table',conn)

#Reading some sql from the df_table in memory
pd.read_sql('Select workclass, marital_status from df_table limit 10',conn)

#Select statement with where
pd.read_sql("Select workclass from df_table where workclass like '%Private%'",conn)

#Select the partition over
sql_string = "Select * from (Select workclass, id, marital_status, row_number() over(partition by workclass order by capital_gain asc) as ranking from df_table) as table1 where ranking = 1"
sql_df = pd.read_sql(sql_string,conn)
#rank_over_partition_df = sql_df.loc[sql_df['ranking'] == 1]

rank_pandas_df = df_sql.copy(deep=True)
rank_pandas_df['rank']= df_sql.groupby(by=['workclass'])['capital_gain'].rank(method='first',ascending=True).astype(int)
rank_pandas_df = rank_pandas_df.loc[rank_pandas_df['rank']==1].copy(deep=True)

#Drop Duplicates
rank_pandas_df.drop_duplicates(inplace=True,subset=['workclass'],keep='first')


