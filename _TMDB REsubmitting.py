#!/usr/bin/env python
# coding: utf-8

# Project: Investigate a Dataset (TMDb_Movies Dataset)
#     

# Table of Contents
# Introduction
# Data Wrangling
# Exploratory Data Analysis
# Conclusions

# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>
# 

#  <a id='intro'></a>
# 
# ### over view
# 
# > **Tip**: this report is about data analysis of movies according to genres , revenue,budget and rating and it help us to find the best of movies that people attracted to them and how much the production team pay for that we get data from this link https://www.kaggle.com/tmdb/tmdb-movie-metadata

#  ### Question(s) for Analysis
#      1-what's the most produces year of movies?
#      2-what's the most profitable according to year?
#      3-what's the most productive type of movies?
#      4-what's the most profitable type of movies ?
#      5-what's the most popular movies genre?
#      

# In[44]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbs
import pandas as pd


#  ### General proporties
#  1-importing data and check it
#  2-look at data an choose from it the coloumns we need 
#  3-delete from the table the coloumns that we willn't use
#  4-check the coloums that have unknown value and if it will affect on analysis we will remove this coloums
#  5-check data with less missing value we will clean it
#  6-remove the duplicated row
# 
#    
#  

# importing data and check it,look at data and choose from coloums we need.

# In[46]:


df=pd.read_csv('tmdb-movies.csv')
df.head()


# 1-cleaning data by convert nan value in numerical coloums to zero
# 2-check null value
# 3-drop coloumns which has more null value and willn't be benfit for analysis
# 4-check null value again and drop it 
# 5-check duplicates row and drop it
# 6-check data types and covert numerical value from float to integer and convert object to string 

# In[48]:



movies_tmdb_rev=['budget_adj','revenue_adj','runtime']
df[movies_tmdb_rev]=df[movies_tmdb_rev].replace(0,np.nan)
df.head()


# delete from the table the coloumns that we willn't need

# In[50]:


df.isnull().sum()


# In[102]:


df_movies=df.drop(['imdb_id','cast','homepage','tagline','overview','release_date','director','keywords','production_companies'],axis=1)
df_movies.head()
 


# In[103]:


df_movies.isnull().sum()


# In[104]:


movies_tmdb=df_movies.dropna()
movies_tmdb.head()


# In[105]:


print(movies_tmdb.shape)


# In[106]:


movies_tmdb.isnull().sum()


# In[107]:


movies_tmdb.duplicated().sum()


# In[108]:


movies_tmdb=movies_tmdb.drop_duplicates()
movies_tmdb.head()


# In[109]:


movies_tmdb.dtypes


# In[110]:


integer=['revenue_adj','budget_adj']
movies_tmdb[integer]=movies_tmdb[integer].applymap(np.int64)
movies_tmdb.head()


# In[118]:


movies_tmdb['profit'] = movies_tmdb['revenue']-movies_tmdb['budget_adj']
movies_tmdb['profit'] = movies_tmdb['profit'].apply(np.int64)
movies_tmdb.head()


# In[112]:


movies_tmdb['genres']=movies_tmdb['genres'].apply(np.str_)


# In[119]:


movies_tmdb.dtypes


# In[114]:


print(movies_tmdb.shape)


# In[115]:


movies_tmdb.duplicated().sum()


# In[116]:


movies_tmdb.hist(figsize=(10,8))


# what's the most year of producation of movies?

# what's the most produces year of movies ? 
# it appears for us that number of movies increases gradully by year

# In[66]:


movies_tmdb['release_year'].value_counts().plot(kind='bar',figsize=(16,8))


# tmdb_genres=tmdb
# 

# what's the most profitable according to year? we found the profit of movies increases gradually by year

# In[123]:


movies_tmdb.groupby('release_year').profit.mean().plot()
movies_tmdb.head()


# we can estimate the profit mean as below

# In[188]:


movies_tmdb['profit'].describe()


# In[185]:


movies_tmdb['profit'].plot(kind='box',figsize=(16,8))


# we can check the relation between profit and budget from this plot 

# In[197]:


movies_tmdb.plot(x='budget_adj',y='profit',kind='scatter')
plt.title('budget Vs profit')
plt.xlabel('budget')
plt.ylabel('profit');


# we use split to split coloumn of genres to make it easy for analysing data
# and add the column after splitting to table to make more analysis

# In[198]:


genres_df = movies_tmdb['genres'].str.split("|", expand=True)


# In[199]:


genres_movies = genres_df.stack()

genres_movies = pd.DataFrame(genres_df)
genres_movies.head()


# In[200]:



genres_movies_count = genres_df.stack()

genres_movies_count= pd.DataFrame(genres_movies_count)
genres_movies_count.head()


# what's the most productive type of movies? from the table we find drama movies is the most productive type of movies

# In[159]:


genres_movies_count.rename(columns={0:'genres'}, inplace=True)
genres_movies_count.genres.value_counts()


# In[160]:


genres_movies_count.genres.value_counts().plot(kind='pie',figsize=(20,20))


# In[184]:


movies_tmdb['genres_new']=genres_df
movies_tmdb.head(10)


# what's the most profitable type of movies according to genre? we found that animation is the most profitable type of movies

# In[182]:


revenue_mean =movies_tmdb.groupby('genres_new')['profit'].mean()
revenue_mean.plot(kind='bar', title='Average profit according to genres', alpha=0.7);
plt.xlabel('genres', fontsize=20)
plt.ylabel('profit', fontsize=20)


# what's the most popular type of movies according to genre? we found that animation and adventure is the most popular type of movie

# In[202]:


vote_average=movies_tmdb.groupby('genres_new')['vote_count'].mean()
vote_average.plot(kind='bar', title='Average vote according to genres', alpha=0.7);
plt.xlabel('genres', fontsize=20)
plt.ylabel('vote average', fontsize=20)


# ### conclusion 
# from this data study we know alot of things that will be benefit for producer we found that a great number of people vote on animation and adventure and science fiction movies and a few number of people vote on documentry and this also appears obviously when we revise the profit for each type of movies we found that animation and adventure movies are movies which get high profit commparing to other movies and from this data analysis we found that number of movies produces is increasing gradullyby years which means that the production of movies by year play an important role in income for country and this also appear when we check the profit according to years
