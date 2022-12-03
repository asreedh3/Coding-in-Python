import pandas as pd
import matplotlib
import numpy as np

df = pd.read_csv("/Users/asreedhar/Downloads/browsing_audience.csv")
df = df.drop_duplicates()

'''Stratify the 2 types of Audience Segmentation'''
df_regular = df.loc[df['Audience Segment']=='Regular'].copy(deep=True)
df_ba = df.loc[df['Audience Segment']=='Browsing'].copy(deep=True)

'''Adoption Rate Calculations'''

#Get all the data points for the month of May
df_may = df.loc[df['Month']=='May'].copy(deep=True)
df_may_ba = df.loc[(df['Month']=='May') & (df['Audience Segment'] == 'Browsing')].copy(deep=True)

#Get the list of the Unique User IDs for the month of May
may_uq_ids = list(set(df_may['Account ID'].to_list()))
may_uq_ids_ba = list(set(df_may_ba['Account ID'].to_list()))
adoption_rate_may = len(may_uq_ids_ba)/len(may_uq_ids)

#Get all the data points for the month of June
df_june = df.loc[df['Month']=='June'].copy(deep=True)
df_june_ba = df.loc[(df['Month']=='June') & (df['Audience Segment'] == 'Browsing')].copy(deep=True)

#Get the list of the Unique User IDs for the month of June
june_uq_ids = list(set(df_june['Account ID'].to_list()))
june_uq_ids_ba = list(set(df_june_ba['Account ID'].to_list()))

#Need to get all the IDs in June that used BA for the first time
june_uq_ids_ba_new = list(set(june_uq_ids_ba)-set(may_uq_ids_ba))
adoption_rate_june = len(june_uq_ids_ba_new)/len(june_uq_ids)

#Put everything together
df_adoption_rates = pd.DataFrame([[adoption_rate_may],[adoption_rate_june]],columns =['Adoption Rate'],index=['May','June'])

#Get the Adoption Rate Percentage
df_adoption_rates = df_adoption_rates.multiply(100)
df_adoption_rates.reset_index(inplace=True)
df_adoption_rates.columns = ['Month','Adoption Rate']
df_adoption_rates.to_csv("adoption_rates.csv",header=True,index=False)


'''
Reasoning here is we want to see the adoption rate of June from the perspective of new adopters
Excluding those users who have tried it out already in May
'''

'''High Potential Users for Future Adoption'''

#Users who have been using BA consistently for 2 months.
intersection_uq_ba = list(set(may_uq_ids_ba).intersection(set(june_uq_ids_ba)))

#Users who have run Multiple Campaigns using BA Segmentation
df_ba_cuq = df_ba.drop_duplicates(subset=['Account ID','Campaign ID']).copy(deep=True)
df_ba_agg = df_ba_cuq.groupby(by=['Account ID']).agg(['count'])['Campaign ID']
df_ba_agg.sort_values(by=['count'],ascending=False,inplace=True)
#Take the top 3 users
df_ba_agg_top = df_ba_agg.head(3).reset_index()
ba_agg_top = df_ba_agg_top['Account ID'].to_list()

#Users who have the most Media Cost for BA campaigns
df_ba_cost_agg = df_ba.groupby(by=['Account ID']).agg(['sum'])['Media Cost']
df_ba_cost_agg.sort_values(by=['sum'],ascending=False,inplace=True)
#Take the top 3 users
df_ba_cost_agg_top = df_ba_cost_agg.head(3).reset_index()
ba_cost_agg_top = df_ba_cost_agg_top['Account ID'].to_list()

#Find the Union between the 3 criterion to identify the top potential users
top_potential_users = list(set(intersection_uq_ba).union(set(ba_agg_top),set(ba_cost_agg_top)))
df_top_potential_users = pd.DataFrame(top_potential_users,columns=['Users with High Potential'])
df_top_potential_users.sort_values(by=['Users with High Potential'],ascending=True,inplace=True,ignore_index=True)
df_top_potential_users.to_csv("top_potential_users.csv",header=True,index=False)


'''
Here we use 3 different criterion to find the top users. We look at users that have been consistently
using the product, Users that have extensively used the product by running more campaigns with
this segmentation. We also look at the users that have opened by their wallets to pay 
the associated media for capaigns with this segementation selection.
We then take a union of the top potential users.

'''

'''Performance BA vs Regular'''

#Avg Conversions for May
may_avg_conversions_ba = df_may_ba['Conversions'].mean()
df_may_regular = df.loc[(df['Month']=='May') & (df['Audience Segment'] == 'Regular')].copy(deep=True)
may_avg_conversions_regular = df_may_regular['Conversions'].mean()

#Avg Conversions for June
june_avg_conversions_ba = df_june_ba['Conversions'].mean()
df_june_regular = df.loc[(df['Month']=='June') & (df['Audience Segment'] == 'Regular')].copy(deep=True)
june_avg_conversions_regular = df_june_regular['Conversions'].mean()

#Avg Impressions for May
may_avg_impression_ba = df_may_ba['Impression'].mean()
may_avg_impression_regular = df_may_regular['Impression'].mean()

#Avg Impressions for June
june_avg_impression_ba = df_june_ba['Impression'].mean()
june_avg_impression_regular = df_june_regular['Impression'].mean()

#Conversion Rates for April, May and June
## Conversion Rate = avg Conversion/ avg Impression

#Conversion Rates May
may_conversion_rate_ba = may_avg_conversions_ba/may_avg_impression_ba
may_conversion_rate_regular = may_avg_conversions_regular/may_avg_impression_regular

#Conversion Rates June
june_conversion_rate_ba = june_avg_conversions_ba/june_avg_impression_ba
june_conversion_rate_regular = june_avg_conversions_regular/june_avg_impression_regular

#Conversion Rate April
df_april_regular = df.loc[(df['Month']=='April') & (df['Audience Segment'] == 'Regular')].copy(deep=True)
april_avg_conversions_regular = df_april_regular['Conversions'].mean()
april_avg_impression_regular = df_april_regular['Impression'].mean()
april_conversion_rate_regular = april_avg_conversions_regular/april_avg_impression_regular

#Create the DataFrame for Conversion Rates
df_conversion_rates = pd.DataFrame([[april_conversion_rate_regular,np.NaN],[may_conversion_rate_regular,may_conversion_rate_ba],\
                      [june_conversion_rate_regular,june_conversion_rate_ba]],columns =['Regular', 'Browsing Audience'],index=['April','May','June'])
df_conversion_rates= df_conversion_rates.multiply(100)
df_conversion_rates.reset_index(inplace=True)
df_conversion_rates.columns = ['Month','Regular','Browsing Audience']
df_conversion_rates.to_csv("conversion_rates.csv",header=True,index=False)


'''
Reasoning here is you track the conversion rate which will tell you the rate of conversion 
you can expect per view of the campaign ad. Rationale behind the use of the metric is you want to
track how many conversions you get per view because BA is effectively another segmentation method 
of getting the right ad in front of the right audience that is most likely to interact with it. 
Atleast that is the goal.So this metric would go a long way in assessing just that.

BA performs marginally better than regular in the 2 months its been active and comapring it to
the Aprl benchmark for the conversion rate. We need a few more months of data to
decisively conclude which one is the better perfomer especially since May seems to be a slower
month for both groups.

'''

'''Other Insights from the Dataset'''

#Start with May for campaigns that have run both

df_may_ba_camp_conv = df_may_ba.groupby(['Campaign ID']).agg(['mean'])['Conversions'].copy(deep=True)
df_may_ba_camp_conv.reset_index(inplace=True)
df_may_ba_camp_conv.columns = ['Campaign ID', 'Browsing Audience Conversion']
df_may_regular_camp_conv = df_may_regular.groupby(['Campaign ID']).agg(['mean'])['Conversions'].copy(deep=True)
df_may_regular_camp_conv.reset_index(inplace=True)
df_may_regular_camp_conv.columns = ['Campaign ID', 'Regular Conversion']
df_may_camp_conv = pd.merge(df_may_ba_camp_conv,df_may_regular_camp_conv,on=['Campaign ID'],how='inner')

df_june_ba_camp_conv = df_june_ba.groupby(['Campaign ID']).agg(['mean'])['Conversions'].copy(deep=True)
df_june_ba_camp_conv.reset_index(inplace=True)
df_june_ba_camp_conv.columns = ['Campaign ID', 'Browsing Audience Conversion']
df_june_regular_camp_conv = df_june_regular.groupby(['Campaign ID']).agg(['mean'])['Conversions'].copy(deep=True)
df_june_regular_camp_conv.reset_index(inplace=True)
df_june_regular_camp_conv.columns = ['Campaign ID', 'Regular Conversion']
df_june_camp_conv = pd.merge(df_june_ba_camp_conv,df_june_regular_camp_conv,on=['Campaign ID'],how='inner')



########Conversion Rate Across the Months####################

df_april = df.loc[(df['Month']=='April')].copy(deep=True)
april_avg_conversions = df_april['Conversions'].mean()
april_avg_impression = df_april['Impression'].mean()
april_conversion_rate = april_avg_conversions/april_avg_impression

may_avg_conversions = df_may['Conversions'].mean()
may_avg_impression = df_may['Impression'].mean()
may_conversion_rate = may_avg_conversions/may_avg_impression

june_avg_conversions = df_june['Conversions'].mean()
june_avg_impression = df_june['Impression'].mean()
june_conversion_rate = june_avg_conversions/june_avg_impression

df_conversion_rates_mom = pd.DataFrame([[april_conversion_rate],[may_conversion_rate],[june_conversion_rate]],columns =['Conversion Rate'],index=['April','May','June'])
df_conversion_rates_mom= df_conversion_rates_mom.multiply(100)


'''Media Cost Per Conversion'''

#Find the avg media cost and avg conversion cost for each type of segmentation
avg_media_cost_ba = df_ba['Media Cost'].mean()
avg_conversions_ba = df_ba['Conversions'].mean()
avg_media_cost_regular = df_regular['Media Cost'].mean()
avg_conversions_regular = df_regular['Conversions'].mean()

#Find the media cost per conversion for each type of segmentation
media_cost_conversion_ba = avg_media_cost_ba/avg_conversions_ba
media_cost_conversion_regular = avg_media_cost_regular/avg_conversions_regular

media_cost_per_conversion = pd.DataFrame([[media_cost_conversion_regular],[media_cost_conversion_ba]],\
                            columns =['Media Cost per Conversion'],index=['Regular','Browsing Audience'])
media_cost_per_conversion.reset_index(inplace=True)
media_cost_per_conversion.columns = ['Type of Segmentation','Media Cost per Conversion']
media_cost_per_conversion.sort_values(ignore_index=True,by=['Media Cost per Conversion'],ascending=True,inplace=True)
media_cost_per_conversion.to_csv('media_cost_conversion.csv',header=True,index=False)


'''
The media cost per conversion for BA based data points seems to be lower than the 
regular segmentation option. Which probably is driven by placement of the right type of ads
in front of the right type of viewer that is more likely to lead to a conversion
'''

'''High Performing Campaigns in June'''

#Find the top 2 performing BA campaigns for June
june_high_perf_ba = df_june_ba.sort_values(by=['Conversions'],ascending=False).head(2)
june_high_perf_ba.to_csv("june_high_performance.csv",header=True,index=False)


'''
We are seeing an uptick of BA performance in June which is 4 times the regular performance 
for the month. This is mainly driven by 2 campaigns that have chosen BA as the segmentation approach
The conversions are in the order of manitude of the 1000s.
Further exploration of these campaigns and why BA was so successful there would help drive
in better performance of the BA segmentation option moving forward and create a 
clear demarkation between the BA segmentation approach and the Regular segmentation approach

'''

'''Descriptive Statistics'''

#Find the avg and max Conversions and Impression
avg_conversions_ba = df_ba['Conversions'].mean()
max_conversions_ba = df_ba['Conversions'].max()
avg_conversions_regular = df_regular['Conversions'].mean()
max_conversions_regular = df_regular['Conversions'].max()

avg_impression_ba = df_ba['Impression'].mean()
max_impression_ba = df_ba['Impression'].max()
avg_impression_regular = df_regular['Impression'].mean()
max_impression_regular = df_regular['Impression'].mean()

#Campaigns that used BA
ba_campaign_count = df_ba_agg['count'].sum()

#Users who have run Multiple Campaigns using Regular Segmentation
df_regular_cuq = df_regular.drop_duplicates(subset=['Account ID','Campaign ID']).copy(deep=True)
df_regular_agg = df_regular_cuq.groupby(by=['Account ID']).agg(['count'])['Campaign ID']
df_regular_agg.sort_values(by=['count'],ascending=False,inplace=True)

#Campaigns that used Regular
regular_campaign_count = df_regular_agg['count'].sum()

#Users in Beta Cohort
beta_cohort_count = len(list(set(df['Account ID'].to_list())))

#Users that used BA
ba_cohort_count = len(list(set(df_ba['Account ID'].to_list())))

#Users that used both
both_cohort_count = []
for x in list(set(df_regular['Account ID'].to_list())):
    if x in list(set(df_ba['Account ID'].to_list())):
        both_cohort_count.append(x)

both_cohort_count = len(both_cohort_count)



