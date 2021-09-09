#!/usr/bin/env python
# coding: utf-8

# In[17]:


get_ipython().system('pip install bs4')
from bs4 import BeautifulSoup
import requests
import pandas as pd


# In[31]:

## Url split in order to webscrape the required 800 pages

url1 = "https://arcticinfrastructure.wilsoncenter.org/arctic-infrastructure-inventory-0?_page="
url2 = "&keywords=&_limit=10&microsite=6&countries=775,722,761,763,789,854,871,903,928&projects=947,944,948,945,942,943,946,941,950,949,957,956,954,955,952,953,951,961,959,962,960,958"


# In[32]:

## To ensure url properly concatenates

for x in range(1, 2):
    main_url = url1 + str(x) + url2
    print(main_url)


# In[33]:

## Extract the data by column rather than row, assigning each attribute its own list (type, title, country)
### Variable 'info' held data that was needed (cost and completion), but could not be extracted without extracting the project name as well

info_list=[]
type_list=[]
title_list=[]
country_list=[]

for x in range(1, 800):
    main_url = url1 + str(x) + url2
    
    data = requests.get(main_url).text
    soup = BeautifulSoup(data, "html.parser")
   
    projects = soup.find_all("div",class_="faceted-search-results")
      
    for project in projects:

        info = project.find_all("div", class_="teaser-column")
        type = project.find_all("div", class_="teaser-type")
        title = project.find_all("div", class_="teaser-title")
        country = project.find_all("div", class_="teaser-topic")
        
        for info_data in info:
            info_list.append(info_data.text)

        for title_data in title:
            title_list.append(title_data.text)
            
        for type_data in type:
            type_list.append(type_data.text)
            
        for country_data in country:
            country_list.append(country_data.text)
            


# In[34]:

## Removing the attached project name from data in 'info' (as I already have title_list), and splitting the list into two seperate list (cost_list, completion_list)

info_list_copy1 = info_list[:]
info_list_copy2 = info_list[:]

def cleaning_cost():
    del info_list_copy1[0::3]
    del info_list_copy1[0::2]
    global cost_list
    cost_list = info_list_copy1
    
def cleaning_completion():
    del info_list_copy2[0::3]
    del info_list_copy2[1::2]
    global completion_list
    completion_list = info_list_copy2
    
# In[35]:

cleaning_cost()
cleaning_completion()


# In[36]:


data = {'Name': title_list, 'Type': type_list, 'Country': country_list, 'Cost': cost_list, 'Completion': completion_list}


# In[37]:

## Ensuring the length for each list is the same in order to place the data into a Pandas Data Frame

print(len(title_list), len(type_list), len(country_list), len(cost_list), len(completion_list))


# In[38]:


df = pd.DataFrame(data)
print(df.head)


# In[39]:


df.to_csv(r'C:\Users\###\###\arctic_infrastructure_df.csv', index = False)


# In[ ]:




