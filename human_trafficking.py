# -*- coding: utf-8 -*-
"""Human Trafficking_MK.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cZLzpTXXzV2RGl8SHiI-ToS5rMYZUXX5
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
path = "/content/drive/MyDrive/Colab/The Global Dataset 14 Apr 2020 (2).csv"
humantrafficking = pd.read_csv(path)
import numpy as np
import seaborn as sns
import plotly
import os
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


!pip install matplotlib

print(humantrafficking.shape)

"""# **DATA CLEANING**

"""

humantrafficking.head()

"""# **Removing the first column as it is not a part of our dataset.**

"""

humantrafficking = humantrafficking.drop('By using this data you agree to the Terms of Use: https://www.ctdatacollaborative.org/terms-use', 1)

humantrafficking.head()

"""# **Lets look at our Age Group column**

"""

humantrafficking['ageBroad'].unique()

humantrafficking[humantrafficking['ageBroad']=='-99'].shape

humantrafficking["ageBroad"].replace({"-99": "Unknown"}, inplace=True)

"""Replacing '-99' in age group with 'Unkown'. We are doing this primarily due the follwing reasons:
*  There are 12362 records under 'ageBroad' listed as -99 or missing, which is almost 1/4th of total number of records in our dataset.
*   Ignoring such a large chunk of victim data in our analysis could lead to incorrect analysis.
*  By putting 'Unknown' we also not speculating any particular age group for the missing data as that would also be incorect.

# **Lets look at the Year of Registration column**
"""

humantrafficking[humantrafficking['yearOfRegistration']==2019].shape

humantrafficking['yearOfRegistration'].value_counts()

"""As we can see we do not have sufficient data for the year 2019. Hence, we will be removing those records from the scope of our analysis"""

humantrafficking = humantrafficking[humantrafficking['yearOfRegistration']!=2019]

humantrafficking.shape

"""# **Lets look at the Citizenship and Country of Exploitation columns**"""

humantrafficking['citizenship'].sort_values().value_counts()

humantrafficking['CountryOfExploitation'].sort_values().value_counts()

"""In both the columns, '00' is neither a country nor a missing value. It indicates that the details regarding the country was not known when the case was registered for the victim. Therefore, we will replace '00' with 'Not Known' for sake of clarity of our audience."""

humantrafficking['citizenship'].replace({'00': 'Not Known'}, inplace=True)

humantrafficking['citizenship'].unique()

humantrafficking['CountryOfExploitation'].replace({'00': 'Not Known'}, inplace=True)

humantrafficking['CountryOfExploitation'].unique()

"""We can also observe that there's missing data in both columns indicated as '-99'.
We can safely remove the records where we have missing data in both 'citizenship' (which is country of origin) and 'country of exploitation' as they don't add any value to our geographical analysis.
"""

humantrafficking = humantrafficking[(humantrafficking['citizenship'] != '-99')]

humantrafficking['citizenship'].unique()

humantrafficking['CountryOfExploitation'].replace('-99', 'NaN', inplace=True)

humantrafficking['CountryOfExploitation'].unique()

print(humantrafficking.shape)

"""# **Adding a newly calculated conditional column for Victim Group based on Age group & Gender**"""

for ind, row in humantrafficking.iterrows():
  if (humantrafficking.loc[ind, 'ageBroad'] == '0--8') or (humantrafficking.loc[ind, 'ageBroad'] == '9--17'):
      if humantrafficking.loc[ind, 'gender'] == 'Male':
        humantrafficking.loc[ind,'Victim Group'] = 'Boys (Minor Males)'
      else:
        humantrafficking.loc[ind,'Victim Group'] = 'Girls (Minor Females)'
  elif humantrafficking.loc[ind, 'ageBroad'] == 'Unknown':
     humantrafficking.loc[ind,'Victim Group'] = 'Unknown'
  else:
      if humantrafficking.loc[ind, 'gender'] == 'Male':
        humantrafficking.loc[ind,'Victim Group'] = 'Men (Adult Males)'
      else:
        humantrafficking.loc[ind,'Victim Group'] = 'Women (Adult Females)'

humantrafficking['Victim Group'].value_counts()

"""# **Replace all -99 with NaN**"""

humantrafficking=humantrafficking.replace('-99','NaN')

humantrafficking=humantrafficking.replace(-99,np.NaN)

humantrafficking.head()

humantrafficking['CountryOfExploitation'].unique()

"""Replace all'-99' with 'NaN' across the dataframe. We are doing this primarily due the follwing reasons:

*    In the dataframe, we have only '0' and '1' which represent True and False respectively 
*  Making sure the '-99' values do not interfere with the arithmatic data analysis

# **Analysis Questions: Based on Victim Demographics**

Based on our dataframe, we would like to clarify the following:
 

1.   All columns that starts with 'is' is refering to the type of exploitation. For example, isForcedLabour. isSexualExploit etc.
2.   All columns that starts with 'meansOfControl' is refering to the means of control used on the victim to commit the crime. For example, meansOfControlWithholdsDocuments, meansOfControlSexualAbuse etc.
3.   All columns that starts with 'typeOfLabour' is refering to the 
further sub-type of labour exploitation faced by the victim. For example, typeOfLabourAgriculture, typeOfLabourAquafarming etc.
4.   All columns that starts with 'typeOfSex' is refering to the further sub-type of sexual exploitation faced by the victim. For example, typeOfSexProstitution, typeOfSexPornography etc.
5.   All columns that starts with 'recruiterRelation' is refering to the relationship the expoliter/recruiter had with the victim. For example, recruiterRelationFriend, recruiterRelationIntimatePartner etc.
6.   These columns capture True/False or Yes/No value using numerical 1 & 0. 1 indicates True or Yes, whereas 0 indicates False or No.

**Question 1: What are the most prevalent types of exploitations in each victim group?**
"""

#Lets group our humantrafficking dataframe based on the 'Victim Group' using the sum function

ht = humantrafficking.groupby(['Victim Group']).sum().reset_index()
ht

#Dropping 'yearOfRegistration' as it doesn't makes sense to group and sum 'year of registration'
ht.drop('yearOfRegistration', 1, inplace=True)
ht

#Setting 'Victim Group' as the index for the dataframe
ht = ht.set_index('Victim Group')
ht

#Tranposing our dataframe for easier analysis
htt = ht.transpose()
htt

#Subsetting 'htt' dataframe to include rows related to 'type of exploitation'
htt_exploit = htt.iloc[18:26]
htt_exploit

#Updating the Index Names
htt_exploit.index = ['Forced Labour', 'Sexual Exploitation', 'Other Exploitation', 'Sex And Labour', 'Forced Marriage', 'Forced Military', 'Organ Removal', 'Slavery And Practices']
htt_exploit

#Plotting Exploiatation Types across different Victim Groups

htt_exploit.plot.barh(y=['Boys (Minor Males)','Girls (Minor Females)', 'Men (Adult Males)', 'Women (Adult Females)'],
                      subplots=True, sharex=False, figsize=(10, 22), fontsize=12,
                      xlabel="Exploitation Type", ylabel="Count",
                      title = "Exploitation across different Victim Groups")

"""From the above plot it is clear that:
*   Boys (Minor Males) were most subjected to Forced Labour, followed by Sexual Exploitation.
*   Girls (Minor Females) were most subjected to Sexual Exploitation.
*   Men (Adult Males) were most subjected to Forced Labour.
*   Women (Adult Females) were most subjected to Sexual Exploitation.

**Question 2: What are the means of control used for such exploitations in each victim group?**
"""

#Lets continue to use our transposed humantrafficing dataframe for the sake our analysis
htt

#Subsetting 'htt' dataframe to include rows related to 'means of control'
htt_moc = htt.iloc[0:18]
htt_moc

"""If the means of control which is 'not specified' will not add any value to our analysis. Hence, we can safely disregard those cases."""

#Removing 'meansOfControlNotSpecified' from our dataframe
htt_moc = htt.iloc[0:17]
htt_moc

#Updating the Index Names
htt_moc.index = ['Debt Bondage','Takes Earnings','Restricts Financial Access','Threats','Psychological Abuse','Physical Abuse','Sexual Abuse','False Promises','Psychoactive Substances','Restricts Movement','Restricts Medical Care','Excessive Working Hours','Uses Children','Threat Of Law Enforcement','Withholds Necessities','Withholds Documents','Other']
htt_moc

#Plotting 'Means Of Contol' used against different Victim Groups

htt_moc.plot.barh(y=['Boys (Minor Males)','Girls (Minor Females)', 'Men (Adult Males)', 'Women (Adult Females)'],
                      figsize=(10, 24), fontsize=12, subplots=True, sharex=False, 
                      xlabel="Means Of Control", ylabel="Count",
                      title = "Means Of Contol used against different Victim Groups")

"""It is clear from the above graph that:
*   For Boys (Minor Males), the most common means of control was Psychological Abuse, followed by False Promises & Sexual Abuse.
*   For Girls (Minor Females), the most common means of control was Psychological Abuse, followed by Psychoactive Substances & Restricted Movements.
*   For Men (Adult Males), the most common means of control was Taken Earnings, followed by False Promises & Excessive Working Hours.
*   For Women (Adult Females), the most common means of control was Psychological Abuse, followed by Restricted Movements & Physical Abuse.

**Question 3: What are the most common types of exploiter relationships with victim in each group?**
"""

#Again, lets continue to use our transposed humantrafficing dataframe for the sake our analysis
htt

#Subsetting 'htt' dataframe to include rows related to 'Recruiter Relation'
htt_rr = htt.iloc[44:49]
htt_rr

#Removing 'recruiterRelationUnknown' from our dataframe as it won't be adding any value to our analysis
htt_rr = htt.iloc[44:48]
htt_rr

#Updating the Index Names
htt_rr.index = ['Intimate Partner','Friend','Family','Other']
htt_rr

#Plotting 'Recruiter Relationship' against different Victim Groups

htt_rr.plot.bar(y=['Boys (Minor Males)','Girls (Minor Females)', 'Men (Adult Males)', 'Women (Adult Females)'],
                      figsize=(12, 8), fontsize=14, rot=45,
                      xlabel="Recruiter Relation", ylabel="Count",
                      title = "Recruiter Relationship against different Victim Groups")

"""From the above plot it is clear that:
*  Boys (Minor Males) are more often exploited by their Family Members.
*   Girls (Minor Females) are more often exploited by their Family Members.
*   Men (Adult Males) are more often exploied by Other acquaintances (outside family).
*   Women (Adult Females) are more often exploied by their Intimate Partners.

**Question 4: What are the most common types of forced labor & sexual exploitation carried out in each victim group?**
"""

#Again, lets continue to use our transposed humantrafficing dataframe for the sake our analysis
htt

#Subsetting 'htt' dataframe to include rows related to 'Type of Sexual Exploitation' and 'Type of Labour Exploitation'
htt_sl = htt.iloc[26:43]
htt_sl.drop('typeOfLabourNotSpecified', axis=0, inplace=True)     #If Labour type is Not Specified, we keep them out of our scope of analysis
htt_sl

#Updating the Index Names
htt_sl.index = ['Labour: Agriculture','Labour: Aquafarming','Labour: Begging','Labour: Construction','Labour: Domestic Work','Labour: Hospitality','Labour: Illicit Activities', 'Labour: Manufacturing', 'Labour: Mining Or Drilling', 'Labour: Peddling', 'Labour: Transportation', 'Labour: Other', 'Sex: Prostitution', 'Sex: Pornography', 'Sex: Remote Interactive Services','Sex: Private Sexual Services']
htt_sl

#Plotting 'Types of Labour & Sexual Exploitation' against different Victim Groups

htt_sl.plot.barh(y=['Boys (Minor Males)','Girls (Minor Females)', 'Men (Adult Males)', 'Women (Adult Females)'],
                      figsize=(10, 24), fontsize=12, subplots=True, sharex=False, 
                      xlabel="Types of Labour & Sexual Exploitation", ylabel="Count",
                      title = "Types of Labour & Sexual Exploitation against different Victim Groups")

"""From the above graph it is clear that:
*   Boys (Minor Males) are more exploited through Labour such as Begging and Other forms of Labour Exploitations (not listed here).
*   Girls (Minor Females) are more sexually exploited through Prostitution.
*   Men (Adult Males) are more exploited through Labour such as Construction.
*   Women (Adult Females) are more sexually exploited through Prostitution

# **Analysis Question: Based on Trend Analysis over time series**

**Question 1: What is the trend of exploitation numbers over the years?**
"""

humantrafficking_year = humantrafficking.groupby(['gender','yearOfRegistration']).size().reset_index()
humantrafficking_year.rename(columns = {0:'Number of Trafficked Individuals'}, inplace=True)


fig = px.bar(humantrafficking_year, x = 'yearOfRegistration', y = 'Number of Trafficked Individuals', color="gender",barmode="group",title="Trend of exploitation over the years", labels={"yearOfRegistration":"Year"},color_discrete_sequence=px.colors.qualitative.Safe,template="none",
            )
fig.show()

"""As seen in the grouped bar graph above, it is evident that the number of trafficked individuals have seen arised over the years. Although, the year 2016 shows a large number of female individuals affected, all the other years from 2005 to 2018 exhibit a rise in the total number of individuals affected. It is apparent from the graph that the number of female individuals trafficked have always been more than the number of male individuals each year.

:**Question 2: What is the distribution of various age groups exploited over the years?**
"""

humantrafficking1=humantrafficking[(humantrafficking['ageBroad']!='Unknown')]
humantrafficking_age = humantrafficking1.groupby(['ageBroad','yearOfRegistration']).size().reset_index()
humantrafficking_age.rename(columns = {0:'Number of Trafficked Individuals'}, inplace=True)


fig = px.bar(humantrafficking_age, x = 'yearOfRegistration', y = 'Number of Trafficked Individuals',labels={"yearOfRegistration":"Year"},facet_col='ageBroad',color_discrete_sequence=px.colors.qualitative.Set2,title="Various age group exploited over the years",barmode="stack", template="seaborn",
            category_orders = {'ageBroad': ['0--8', '9--17', '18--20', '21--23', '24--26', '27--29', '30--38', '39--47', '48+']})
fig.show()

"""Based on the classified age groups, it is discernible the age groups 9-17 and 30-38 have been targeted comparatively more than any other age groups. In this bar chart, to make the visualization more decipherable we have got rid of the 'Unknown' value.

**Question 3: Which are the most common type of exploitations in the last four years?**
"""

humantrafficking2=humantrafficking[(humantrafficking['typeOfExploitConcatenated']!='Other')]
humantrafficking_year_expl = humantrafficking2.groupby(['yearOfRegistration','typeOfExploitConcatenated']).size().reset_index()
humantrafficking_year_expl.rename(columns = {0:'Number of Trafficked Individuals'}, inplace=True)
humantrafficking_year_expl_sort= humantrafficking_year_expl.sort_values(by="Number of Trafficked Individuals",ascending=False)[:5]

fig = px.bar(humantrafficking_year_expl_sort, x = 'yearOfRegistration', y = 'Number of Trafficked Individuals', color="typeOfExploitConcatenated",color_discrete_sequence=px.colors.qualitative.Pastel, barmode="group",title="Most common type of exploitations in the last four years", labels={"yearOfRegistration":"Year"},template="none",text='Number of Trafficked Individuals'
            )
fig.show()

"""The above bar chart shows us sexual exploitation and forced labour are the most common type of exploitations that had occured in the last four years of our dataset around the world. It is clearly evident that the sexual exploitation has been the most common way in which individuals have been affected.

**Question 4: People of which citizenship had been most affected in the last 5 years ?**
"""

humantrafficking_year= humantrafficking.groupby(['citizenship','yearOfRegistration']).size().reset_index()
humantrafficking_year.rename(columns = {0:'Number of Trafficked Individuals'}, inplace=True)
humantrafficking_year_sort= humantrafficking_year.sort_values(by="Number of Trafficked Individuals",ascending=False)[:10]

fig = px.bar(humantrafficking_year_sort, x = 'yearOfRegistration', y = 'Number of Trafficked Individuals', color="citizenship",color_discrete_sequence=px.colors.qualitative.Set3, barmode="stack",title="Citzenship of vitctims most affected in last 5 years", labels={"yearOfRegistration":"Year"}, color_discrete_map={ "Male": "RebeccaPurple", "Female": "MediumPurple"},template="none",text='Number of Trafficked Individuals',    
            )
fig.show()



"""The bar chart represents the citizenship of the victims that have been most affected in the last five years with highest frequency. These countries are PH(Philippines), ID(Indonesia), US(United States), UA(Ukraine), MM(Myanmar) and KH(Cambodia). Amongst the known countries, it is clearly evident that Philippines has seen the largest number of individuals affected in the year 2016. However, in 2017 and 2018 the highest number of victims had been from the people who did not disclose their citizenship.

# **Analysis Question: Based on Geography**

**Question 1: Which are Top 10 most affected countries?**
"""

humantrafficking['CountryOfExploitation'].sort_values().value_counts(ascending= False).head(10).plot.barh(color= 'green')
plt.title('Top 10 Most Affected Countries',size=15)
plt.xlabel('Number of Victims',size=13)
plt.ylabel('Country',size=13)
plt.show()

"""In the above graph shows top 10 countries where there are maximum number of cases. Also, we can observe that United States has the highest number of human trafficking cases i.e. 12512. On the other hand, UAE, MD (Moldava), Russia, Phillipines, Indonesia, Myanmar has most of the cases of human trafficking.

**Question 2: What are the most prevalent types of exploitation in each of those countries?**
"""

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
mm = humantrafficking.groupby('CountryOfExploitation')['typeOfExploitConcatenated']
mm1= mm.value_counts()
df5 = pd.DataFrame(mm1)
df7 = df5.rename(columns={'CountryOfExploitation': 'Country', 'typeOfExploitConcatenated': 'TypeOfExploitation','typeOfExploitConcatenated': 'NumberOfExploitaton'})
ff= df7.sort_values(by=['NumberOfExploitaton'],ascending=False).head(15)
ff.plot(kind='bar', stacked=True,color='red',title='Country & Prevalent Type of Exploitation',figsize=(7,7))
plt.xlabel('Country & Type of Exploitation',size=13)
plt.ylabel('Number of Victims',size=13)
plt.title('Country & Prevalent Type of Exploitation',size=15)
plt.show()

"""This picture shows what type of exploit is more prevalent in top 10 countries. Here, in USA, sexual exploitation has the highest number of cases as compared to forced labour. Furthermore, in Russia, forced labour has more cases when compared to other types of exploitation. Also, in Myanmar, Ghana and Phillipines we have more cases of forced labour rather than sexual exploitation.

**Question 3: To determine whether victims were mostly immigrants or citizen**
"""

conditions = [
    (humantrafficking['citizenship'] == humantrafficking ['CountryOfExploitation']),
    (humantrafficking['citizenship'] != humantrafficking['CountryOfExploitation']),
    ]

values = ['Citizen', 'Immigrant']

humantrafficking['status'] = np.select(conditions, values)

humantrafficking['status'].sort_values().value_counts().plot.barh(color= 'purple')
plt.title('Status of Victim(Immigrant or Citizen)',size=15)
plt.xlabel('Number of Victims',size=13)
plt.ylabel('Status',size=13)
plt.show()

"""By looking at the above graph, one can undoubtedly say that most of the victims were migrated from different countries maybe by making false promises of job offer, by giving psychoactive substances, for prostitution, etc."""