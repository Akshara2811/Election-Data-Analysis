#!/usr/bin/env python
# coding: utf-8

# # Election Data analysis - Polls and Donors

# In this project, we analyzed two datasets. The first data set will be the results of political polls for the 2016 general elections.
# 
# Some of the questions answered are:
# 
# 1.) Who was being polled and what was their party affiliation?
# 2.) Did the poll results favor Trump or Clinton?
# 3.) How do undecided voters effect the poll?
# 4.) Can we account for the undecided voters?
# 5.) How did voter sentiment change over time?
# 6.) Can we see an effect in the polls from the debates?

# In[1]:


import pandas as pd
from pandas import Series, DataFrame
import numpy as np


# In[43]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().magic(u'matplotlib inline')


# In[5]:


from __future__ import division


# In[7]:


import requests


# In[8]:


from StringIO import StringIO 


# In[9]:


url = 'https://elections.huffingtonpost.com/pollster/2016-general-election-trump-vs-clinton.csv'

source = requests.get(url).text

poll_data = StringIO(source)


# In[10]:


poll_df = pd.read_csv(poll_data)


# In[11]:


poll_df.info()


# In[12]:


poll_df.head()


# In[15]:


sns.countplot('Affiliation',data=poll_df)


# Overall it's mostly neutral, but is leaning towards Democratic affliation. 

# By sorting it by population, we get the following results.

# In[16]:


sns.countplot('Affiliation',data=poll_df,hue='Population')


# In[17]:


poll_df.head()


# In[20]:


avg = pd.DataFrame(poll_df.mean()) 

avg.drop('Number of Observations',axis=0,inplace=True)


# In[21]:


avg.head()


# In[22]:


std = pd.DataFrame(poll_df.std())

std.drop('Number of Observations',axis=0,inplace=True)


# In[23]:


std.head()


# In[24]:


avg.plot(yerr=std,kind='bar',legend=False)


# The polls seem to be very close, especially considering the undecided votes.

# In[25]:


poll_avg = pd.concat([avg,std],axis=1)


# In[27]:


poll_avg.columns = ['Average','STD']


# In[28]:


poll_avg


# In[29]:


poll_df.head(5)


# In[30]:


poll_df.plot(x='End Date',y=['Trump','Clinton','Undecided'],marker='o',linestyle='')


# In[31]:


from datetime import datetime


# In[32]:


poll_df['Difference'] = (poll_df.Trump - poll_df.Clinton)/100

poll_df.head()


# In[33]:


poll_df = poll_df.groupby(['Start Date'],as_index=False).mean()

poll_df.head()


# In[34]:


fig = poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple')


# In[36]:


row_in = 0
xlimit = []

for date in poll_df['Start Date']:
    if date[0:7] == '2016-10':
        xlimit.append(row_in)
        row_in +=1
    else:
        row_in += 1
        
print min(xlimit)
print max(xlimit)


# In[44]:


fig = poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple',xlim=(232,262))

plt.axvline(232+8, linewidth=4, color='grey')
plt.axvline(232+18, linewidth=4, color='grey')


# There isn't any immediate dip in the differnce after the debates which means both candistes did pretty good in the debate. 

# # Donar Data Set
# 
# Now, the further data anaylsed is from the donor data set from 2012 general elections.
# 
# The questions we will be trying to answer while looking at this Data Set is:
# 
# 1.) How much was donated and what was the average donation?
# 2.) How did the donations differ between candidates?
# 3.) How did the donations differ between Democrats and Republicans?
# 4.) What were the demographics of the donors?
# 5.) Is there a pattern to donation amounts?

# In[70]:


donor_df = pd.read_csv('Election_Donor_Data.csv')


# In[71]:


donor_df.info()


# In[72]:


donor_df.head()


# In[66]:


donor_df['contb_receipt_amt'].value_counts()


# In[53]:


don_mean = donor_df['contb_receipt_amt'].mean()

don_std = donor_df['contb_receipt_amt'].std()

print 'The average donation was %.2f with a std of %.2f' %(don_mean,don_std)


# In[55]:


top_donor = donor_df['contb_receipt_amt'].copy()

top_donor.sort_values (ascending=True, inplace=True)

top_donor


# In[67]:


top_donor = top_donor[top_donor >0]

top_donor.sort_values (ascending=True, inplace=True)

top_donor.value_counts().head(10)


# In[68]:


com_don = top_donor[top_donor < 2500]

com_don.hist(bins=100)


# In[69]:


candidates = donor_df.cand_nm.unique()
#Show
candidates


# In[73]:


party_map = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

donor_df['Party'] = donor_df.cand_nm.map(party_map)


# In[74]:


'''
for i in xrange(0,len(donor_df)):
    if donor_df['cand_nm'][i] == 'Obama,Barack':
        donor_df['Party'][i] = 'Democrat'
    else:
        donor_df['Party'][i] = 'Republican'
'''


# In[75]:


# Clear refunds
donor_df = donor_df[donor_df.contb_receipt_amt >0]

# Preview DataFrame
donor_df.head()


# In[76]:


donor_df.groupby('cand_nm')['contb_receipt_amt'].count()


# In[77]:


donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()


# In[78]:


cand_amount = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()

# Our index tracker
i = 0

for don in cand_amount:
    print " The candidate %s raised %.0f dollars " %(cand_amount.index[i],don)
    print '\n'
    i += 1


# In[79]:


cand_amount.plot(kind='bar')


# In[80]:


donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar')


# In[81]:


occupation_df = donor_df.pivot_table('contb_receipt_amt',
                                index='contbr_occupation',
                                columns='Party', aggfunc='sum')


# In[82]:


occupation_df.head()


# In[83]:


occupation_df.shape


# In[84]:


occupation_df = occupation_df[occupation_df.sum(1) > 1000000]


# In[85]:


occupation_df.shape


# In[86]:


occupation_df.plot(kind='bar')


# In[87]:


occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[88]:


occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS','INFORMATION REQUESTED'],axis=0,inplace=True)


# In[89]:


# Set new ceo row as sum of the current two
occupation_df.loc['CEO'] = occupation_df.loc['CEO'] + occupation_df.loc['C.E.O.']
# Drop CEO
occupation_df.drop('C.E.O.',inplace=True)


# In[90]:


occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[ ]:




