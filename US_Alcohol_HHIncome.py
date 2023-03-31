#!/usr/bin/env python
# coding: utf-8

# <h3>Requirements:</h3> 
# 
# These are also written in the Requirements.txt file 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


# <h1> Clean Up Data </h1>

# <h2> Dataset 1 </h2>

# This data comes from tables published by the United States Census Bureau and is the Median Household Income By State for years 1984 to 2021. It can be found here:  https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html

# If look at the original CSV file, h08.csv, the first few rows are messed up and there are some nested columns. After some trial and error, and to make it easier to be able to separate the data, I set the header to 3 to drop the first few rows and start the dataframe fresh.

# In[2]:


# Reading in the CSV file for Household Income. I named it HHIncome for clarity, and set the header to 3.

HHIncome = pd.read_csv('h08.csv', header=3)
HHIncome


# In[3]:


#looking at the data to get an idea of what it looks like 

print(HHIncome.shape)
print(HHIncome.head())
HHIncome


# In[4]:


# I'm not going to be using the Standard Error columns, so let's drop those

HHIncome.drop(HHIncome.columns[HHIncome.columns.str.contains('unnamed',case = False)],
              axis = 1, inplace = True)
HHIncome


# In[5]:


# let's drop the rows past the years that we aren't looking for in the other dataset
# we'll be keeping 2021 - 2019

HHIncome.drop(HHIncome.iloc[:, 4:41], axis=1, inplace=True)
print(HHIncome)


# In[6]:


#let's rename the 2020 column to make it easier

HHIncome.rename(columns={"2020 (41)" : "2020"}, inplace=True)
print(HHIncome)


# In[7]:


# we can also just drop the row that says 'Median Income'
#since we know that's what this data is

HHIncome.drop(HHIncome.index[0], axis=0, inplace=True)
HHIncome


# When I glanced at the datatype for this dataframe, I noticed that every column was Object, which was weird. I realized that because the year columns, 2019 2020 and 2021, have a comma within the value, they are being counted as strings rather than integers. I converted those to integers for clarity.

# In[8]:


# replacing the commas, and then converting the datatypes to a integer 

HHIncome.replace(',','', regex=True, inplace=True)

HHIncome[['2019', '2020', '2021']] = HHIncome[['2019', '2020', '2021']].astype('int')

HHIncome.dtypes


# I knew that I wanted to merge the datasets on the State column, but the way the year columns were formatted made it possible that the merged dataframe would look odd. After doing some research I stumbled into pandas.melt, which unpivoted the Dataframe from wide to long format and allowed me to have a Year column that would match nicely with Dataset 2. 

# In[9]:


#using pandas.melt, which unpivots the DataFrame from wide to long format and gives me a Year column

HHIncomeM = HHIncome.melt(id_vars=["State"], 
        var_name="Year", 
        value_name="HHIncome")
print(HHIncomeM)


# <h2> Dataset 2 </h2>

# This data set is provided by the US government as part of their Surveillance Reports from the National Institute on Alcohol Abuse and Alcoholism. It contains per capita alcohol sales between the years of 2017-2021 of beer, wine and spirits during the pandemic for 13 states so far. The link can be found here: https://pubs.niaaa.nih.gov/publications/surveillance-covid-19/COVSALES.htm
# 

# In[10]:


#read in CSV file for US Alcohol Sales

Alcohol = pd.read_csv('Data-Table1.csv')
Alcohol


# In[11]:


#looking at the data to get an idea of what it looks like

print(Alcohol.shape)
print(Alcohol.head())


# In[12]:


#we are working with years 2019-2021, so let's drop the rows that include the other years

Alcohol.drop(Alcohol[Alcohol['Year'] <= 2018].index, inplace = True)
Alcohol


# In[13]:


# the last two columns are mostly empty of data so they can be dropped as well
# I will also not be using the PerCapita or Ethanol columns at the moment so I'll drop those too

Alcohol.drop(Alcohol.columns[[5, 7, 8, 9]], axis = 1, inplace=True)
Alcohol


# In[14]:


#let's make sure we get rid of all null entries and drop those too
#once we do these we go from 1664 rows to 1248 rows

Alcohol.dropna(inplace=True)
print(Alcohol)


# In the Assets/ folder, the Definitions.csv file shows a table that details the pairing of the numerical values with their string counterparts for the State names, and the alcoholic Beverages.

# In[15]:


#Rename FIPS column to State, so that it's more clear

Alcohol.rename(columns={"FIPS" : "State"}, inplace=True)
print(Alcohol)


# In[16]:


# These are lists for the State and Beverage columns

statelist = ['Alaska','Colorado','Connecticut','Delaware','Florida','Illinois','Kentucky',
             'Massachusetts','Minnesota','Missouri','North Dakota','Tennessee','Texas' ]
print(statelist)

alclist = ['spirits','wine','beer']

print(alclist)


# In order to change this data, we'll have to change the dtype of those columns to string, since we're replacing numerical data with a word. 

# In[17]:


# converting dtypes  

Alcohol[['State', 'Beverage', 'Year']] = Alcohol[['State', 'Beverage', 'Year']].astype('str')


Alcohol['Gallons'] = Alcohol['Gallons'].astype(int)

print(Alcohol.dtypes)


# In[18]:


#using the lists we made earlier for the Beverages and States, we can now replace the values 
# in the dataframe using the pandas.DataFrame.replace function

Alcohol['Beverage'] = Alcohol['Beverage'].replace(['1', '2', '3'], alclist)
Alcohol['State'] = Alcohol['State'].replace(['2','8','9','10','12','17','21','25','27','29','38','47','48'], 
                                  statelist)

Alcohol


# <h1> Merging Datasets </h1>

# Let's merge these two datasets on the columns of State and Year. I chose an inner join because I felt it worked best with this data. 
# 
# This first join is the generic panda merge, to see what it would look like. 
# 
# Then I try to specifically merge these datasets, Alcohol and HHIncomeM, using an inner join on the columns State and Year. 

# In[19]:


merged_df = pd.merge(HHIncomeM, Alcohol)
merged_df


# In[20]:


merged_df = Alcohol.merge(HHIncomeM, on=['State', 'Year'], how='inner')
merged_df


# I wanted a way to really be able to look at all of the data in this merged dataframe, so I figured out a way to export it as an Excel sheet. I feel like that's a piece of code that I'm definitely going to take with me for future use.  

# In[21]:


# code to export dataframe as an Excel sheet; it should generate in the same folder that this notebook is in. 

writer = pd.ExcelWriter('output.xlsx')
merged_df.to_excel(writer)

writer.save()


# <h1> Data Analysis </h1>

# Let's do some exploratory data analysis to see what we have with this merged dataset of Alcohol Sales and Median Household income. 

# In[22]:


# let's look at the dtypes of the merged dataframe

merged_df.dtypes


# In[23]:


#total gallons of alcohol sold per state, per year

gallons_state_year = merged_df.groupby(['State', 'Year'])['Gallons'].sum()

print(gallons_state_year)


# In[24]:


#average gallons of alcohol sold by state

gallonavg = merged_df.groupby('State')['Gallons'].aggregate(['mean'])
print(gallonavg)


# In[25]:


#expression for the smallest (Min) and largest (Max) amount of gallons sold per state

gallonminmax = merged_df.groupby('State')['Gallons'].aggregate(['min', 'max'])
print(gallonminmax)


# Just looking at this, it's fairly easy to see that Florida and Texas have the lead when it comes to alcohol sales

# In[26]:


#expression for smallest (Min) and largest (Max) median Household Income per state

incomeminmax = merged_df.groupby('State')['HHIncome'].aggregate(['min', 'max'])
print(incomeminmax)


# In my opinion, the median household incomes don't differ on a huge amount. Most of the states are in the 60-70k range. Interestingly enough, Massachusetts seems to have an abundance of wealth with 86k.

# In[27]:


# average median household income per state

incomeavg = merged_df.groupby('State')['HHIncome'].aggregate(['mean'])
print(incomeavg)


# This expression shows the average median household income over the 3 years that we were looking at, 2019, 2020 and 2021. 

# In[28]:


# average median household income by year

income_year_avg = merged_df.groupby('Year')['HHIncome'].aggregate(['mean'])
print(income_year_avg)


# This expression really shows that overall the median household income wasn't changed much by the pandemic. There was a slight dip in 2020, but it looks like in 2021 the US did better than they had the previous 2 years. 

# In[29]:


#correlation of alcohol sold and income

corr=merged_df['Gallons'].corr(merged_df['HHIncome'])
print(corr)


# When we correlate the Gallons and HHIncome columns, we get a correlation coefficient of -0.135. This indicates that there is a negative correlation between the two values, meaning that as the amount of Gallons increases, the household income decreases. However, since the number is so close to 0, that indicates that the relationship is not very strong. 

# In[30]:


# this exresssion shows the correlation between all columns in the dataset
merged_df.corr()


# Looking at this chart we can see again that Gallons and HHIncome have a weak negative relationship. 
# We can also tell that : 
# - Population and Gallons has a moderately strong positive relationship, which means that as the population increases, the amount of alcohol sold increases as well. 
# - Population and HHIncome have a negative relationship; as the population increases, the median household income will decrease. This correlation is slightly stronger than the one between Gallons and HHIncome, but still fairly weak.
#        

# <h1> Visualizations </h1>

# In[31]:


# heatmap to show the correlation between the columns of the merged dataframe

corrmat = merged_df.corr()
mask= np.zeros_like(corrmat)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corrmat,
            vmax=1, vmin=-1,
            annot=True, annot_kws={'fontsize':7},
            mask=mask,
            cmap=sns.diverging_palette(10,600,as_cmap=True))


# This chart demonstrates visually the correlation between all of the columns in the merged dataframe.
# Remember:
# - 1 is a strong positive relationship; both values increase because they are directly related.
# - -1 is a strong negative relationship; as one value increases, the other will decrease. 
# - 0 means that there is no correlation. 

# <h3> Tableau Visuals </h3>

# I attempted to make some Tableau charts with the merged data frame. I put those all in a dashboard as well, which is listed below. 
# 
# These are embedded using the Tableau public links. If for some reason there is trouble viewing these, I have them linked as both the workbooks and the images in the Tableau folder as well. 

# In[32]:


get_ipython().run_cell_magic('html', '', "<div class='tableauPlaceholder' id='viz1680187942824' style='position: relative'><noscript><a href='#'><img alt='Average Gallons Sold Per State, by Beverage ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ga&#47;GallonsHHIncome&#47;Graph2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='GallonsHHIncome&#47;Graph2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ga&#47;GallonsHHIncome&#47;Graph2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1680187942824');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# This table shows that overall, beer is winning with alcohol sales. It's the majority of the sales in every state, and we can really see that Florida and Texas are beating the other states by far. 

# In[33]:


get_ipython().run_cell_magic('html', '', "<div class='tableauPlaceholder' id='viz1680188197465' style='position: relative'><noscript><a href='#'><img alt='Total Gallons Sold Per State By Year ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ga&#47;GallonsHHIncome2&#47;Graph3&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='GallonsHHIncome2&#47;Graph3' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ga&#47;GallonsHHIncome2&#47;Graph3&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1680188197465');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# This table breaks down visually the alcohol sales for every year, for every state. In the majority of the states we can see that 2019 and 2020 are usually pretty close, and then drops off in 2021. Obviously with this data we can't tell the reason for that drop off but it's interesting to see by state rather than just the average for each year.

# In[34]:


get_ipython().run_cell_magic('html', '', "<div class='tableauPlaceholder' id='viz1680188253402' style='position: relative'><noscript><a href='#'><img alt='Average Gallons Sold and Household Income per State ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ga&#47;GallonsHHIncome1&#47;Graph1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='GallonsHHIncome1&#47;Graph1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ga&#47;GallonsHHIncome1&#47;Graph1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1680188253402');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# This chart overlays the Average of Gallons sold and Average Household Income, by state. Obviously we are working with different ranges, with Gallons being measured in Millions and Income being measured in Thousands. However, you can kind of see that the positions of the values by state are fairly similar, which echoes that -0.135 correlation coefficient we got earlier in our calculations. 

# In[35]:


get_ipython().run_cell_magic('html', '', "<div class='tableauPlaceholder' id='viz1680224238490' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ga&#47;GallonsHHIncome_D&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='GallonsHHIncome_D&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ga&#47;GallonsHHIncome_D&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1680224238490');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1366px';vizElement.style.height='795px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1366px';vizElement.style.height='795px';} else { vizElement.style.width='100%';vizElement.style.height='1027px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>")


# This is the dashboard of the Tableau images put together.

# <h1> Summary </h1>

# In merging these datasets I wanted to see if income would have a huge effect on the total alcohol sales. It appears that there's a slight negative relationship, but it's not the biggest factor or indicator of a state's total sales. 
# Obviously there are limitations with the data collected; the Alcohol dataset only collects for 13 states. In the future I would want to see if I could find other factors, perhaps other datasets that would help account for why alcohol sales differ within each state (other than population). 

# In[ ]:




