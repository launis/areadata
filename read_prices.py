# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:06:03 2020

read prices and return dataframe of houses
@author: risto
"""


def read_prices(post):

    from bs4 import BeautifulSoup
    import requests
    import pandas as pd

    """
    #used straightly
    
    import read_post as rp
    post = rp.read_post()
    post = post[post['muncipality_name']=='Tampere']
    
    df = read_prices(post)
    
    input dataframe
    
    post - Data columns (total 3 columns):
        postcode_name       36 non-null object
        muncipality_code    36 non-null int64
        muncipality_name    36 non-null object
    
    return list of individual houses
    """

    req=0

    house_df = pd.DataFrame(columns=['city',
                                     'postcode',
                                     'area',
                                     'rooms',
                                     'house',
                                     'size',
                                     'price',
                                     'pricesq',
                                     'year',
                                     'house_describtion',
                                     'elevator',
                                     'own',
                                     'floors', 
                                     'floor',
                                     'condition'])
    
    
    for city, postcode in zip(post['muncipality_name'], post.index):
        for rooms in range(1,5):
                c=city
                ps=postcode
                url = "https://asuntojen.hintatiedot.fi/haku/?c={}&cr=1&ps={}&nc=167&r={}&amin=&amax=&renderType=renderTypeTable&search=1"
                newurl = url.format(city, postcode, rooms)

 
                response = requests.get(newurl)
   
                content = response.content
                parser = BeautifulSoup(content, 'html.parser')
                # Monitor the requests and printing 
                req += 1
                
                
                # Throw a warning for non-200 status codes
                if response.status_code != 200:
                    print('Request: {}; Status code: {}'.format(req, response.status_code))
                print(req)                    
                
                
                #go all td sections through with beautiful soap after 
                #class_="neighborhood"
                #data is found through next sibling
                
                for link in parser.find_all("td", class_="neighborhood"):
                    try:
                        area = link.string.strip()
                    except:
                        print("Something went wrong 0")
                        
                        area = None
                        break
                    
                    sib = link.find_next_sibling("td", class_="houseType")
                    try:
                        if sib.text.startswith("kt"):
                            house = 1
                        elif sib.text.startswith("rt"):
                            house = 2
                        else:
                            house = 3
                    except:
                        print("Something went wrong 1")
                        house = None
                        break
    
                    sib = link.find_next_sibling("td", class_="cellAlignRight")
                    try:
                        size = float(sib.text.replace(",", ".").replace(" ", ""))
                    except:
                        print("Something went wrong 2")
                        size = None
                        break
                    
                    sib2 = sib.find_next_sibling("td", class_="cellAlignRight")
                    try:
                        price = float(sib2.text.replace(",", ".").replace(" ", ""))
                    except:
                        print("Something went wrong 3")
                        price = None
                        break
    
                    sib3 = sib2.find_next_sibling("td", class_="cellAlignRight")
                    try:
                        pricesq = float(sib3.text.replace(",", ".").replace(" ", ""))
                    except:
                        print("Something went wrong 4")
                        pricesq = None
                        break

                    sib4 = sib3.find_next_sibling("td", class_="cellAlignRight")
                    try:
                        year = int(sib4.text.replace(",", ".").replace(" ", ""))
                    except:
                        print("Something went wrong 5")
                        year = None
                        break

                    #next is in different section
                    sib = link.find_next_sibling("td", class_="")
                    try:
                        house_describtion = sib.text.strip()
                    except:
                        print("Something went wrong 6")
                        house_describtion = None
                        break
            
                    sib2 = sib.find_next_sibling("td", class_="")
                    try:
                        floor  = sib2.text.strip()
                        floors = floor.split("/")[1]
                        floor  = floor.split("/")[0].replace("-", "")
                    except:
                        print("Something went wrong 7")
                        floor = None
                        break
            
                    sib3 = sib2.find_next_sibling("td", class_="")
                    try:
                        if sib3.text.strip()=="on": 
                            elevator=True 
                        else: elevator=False
                    except:
                        print("Something went wrong 8", sib3.text)
                        elevator = None
                        break
            
                    sib4 = sib3.find_next_sibling("td", class_="")
                    try:
                        if sib4.text.startswith("hyvä"):
                            condition = 1
                        elif sib4.text.startswith("tyyd."):
                            condition = 2
                        else:
                            condition = 3
                    except:
                        print("Something went wrong 9")
                        condition = None
                        break
                    
                    sib5 = sib4.find_next_sibling("td", class_="")
                    try:
                        if sib5.text.startswith("oma"): 
                            own=True 
                        else: own=False
                    except:
                        print("Something went wrong 10")
                        own = None
                        break
                    
                    #after all lines are read create a data row
                    new_row =  {'city' : city,
                                'postcode' : postcode, 
                                'area' : area,
                                'rooms' : rooms,
                                'house' : house,
                                'size' : size,
                                'price' : price,
                                'pricesq' : pricesq,
                                'year' : year,
                                'house_describtion' : house_describtion,
                                'elevator' : elevator,
                                'own' : own,
                                'floor' : floor,
                                'floors' : floors,
                                'condition' : condition}


                    #append row to the dataframe
                    house_df = house_df.append(new_row, ignore_index=True)
    
    house_df['rooms']=pd.to_numeric(house_df['rooms'], errors='ignore')
    house_df['house']=pd.to_numeric(house_df['house'], errors='ignore')
    house_df['size']=pd.to_numeric(house_df['size'], errors='ignore')
    house_df['price']=pd.to_numeric(house_df['price'], errors='ignore')
    house_df['floor']=pd.to_numeric(house_df['floor'], errors='ignore')
    house_df['floors']=pd.to_numeric(house_df['floors'], errors='ignore')
    house_df['pricesq']=pd.to_numeric(house_df['pricesq'], errors='ignore')
    house_df['year']=pd.to_numeric(house_df['year'], errors='ignore')
    house_df['elevator']=pd.to_numeric(house_df['elevator'], errors='ignore')
    house_df['condition']=pd.to_numeric(house_df['condition'], errors='ignore')
    house_df['own']=pd.to_numeric(house_df['own'], errors='ignore')
    return(house_df)