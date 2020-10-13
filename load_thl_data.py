def load_thl_data(url, kunta_stat, thl_area_dict, indicator, region, year, data, org = None):

    import json
    import pandas as pd
    import urllib.request

    url = url + str(indicator)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    try:
        with urllib.request.urlopen(req) as f:
            f = urllib.request.urlopen(req)
    except:
        return(data)
    desc=json.loads(f.read().decode('utf-8'))
    if not region.capitalize() in desc['classifications']['region']['values']:
        return(data)
    if org != None:
        if desc['sources'][0]['organization']['title']['fi'] not in org:
            return(data)
    
    available = 0
    while available == 0:
        column_name = desc['title']['fi'] + " (" + desc['sources'][0]['organization']['title']['fi'] + " " + str(year) + ")"
        url = "https://sotkanet.fi/rest/1.1/csv?indicator=" + str(indicator) +  "&region=" + region + "&years=" + str(year) + "&genders=total"
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        try:
            with urllib.request.urlopen(req) as f:
                f = urllib.request.urlopen(req)
        except:
            return(data)
        
        thl_data = pd.read_csv(f, sep=';',decimal = ',', encoding = 'utf-8', header = 0, usecols=[1, 4], names = ['0','id','2','3',column_name,'5'])
        available = len(thl_data[column_name].unique())
        thl_data.loc[:, column_name] = thl_data[column_name].astype(float)
                
        year = year - 1
    if data.empty:
        data=kunta_stat[['muncipality_code']].copy()
    for i in thl_area_dict:
        thl_data.loc[thl_data['id'] == i, "muncipality_code"] = thl_area_dict[i]
    thl_data.dropna(inplace=True)
    thl_data=thl_data.merge(kunta_stat['muncipality_code'], on='muncipality_code', how='right').copy()
    thl_data.drop(['id'], axis=1, inplace = True)
    thl_data.fillna(0, inplace=True)

    data=pd.merge(data, thl_data, on='muncipality_code').copy()
    #data[:, 'muncipality_code'] = data['muncipality_code'].astype(int)
    return(data)



def read_all_sotka(year, kunta_stat,  region='Kunta', org=None):
    
    import urllib.request
    import json
    import pandas as pd

    import urllib.request
    import json
    import pandas as pd
    
    url = "https://sotkanet.fi/rest//1.1/indicators"

    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    with urllib.request.urlopen(req) as f:
        f = urllib.request.urlopen(req)
    list_of_datas = json.loads(f.read().decode('utf-8'))

    number_list =[]
    for i in range(len(list_of_datas)):
        number_list.append(list_of_datas[i]['id'])


    url = "https://sotkanet.fi/rest//1.1/regions"
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    with urllib.request.urlopen(req) as f:
        f = urllib.request.urlopen(req)
    desc=json.loads(f.read().decode('utf-8'))

    thl_area_dict = {}
    for i in desc:
        if i['category'] == 'KUNTA':
            thl_area_dict[i['id']] =  i['code']
    
    for keys in thl_area_dict: 
        thl_area_dict[keys] = int(thl_area_dict[keys])
    
    data =  pd.DataFrame()
    url = "https://sotkanet.fi/rest/1.1/indicators/"
    for i in range(len(list_of_datas)):
        indicator = i
        data = load_thl_data(url, kunta_stat, thl_area_dict, indicator, region, year, data, org = org)
    kunta_stat = pd.merge(left=kunta_stat, right=data, on = 'muncipality_code')
    return(kunta_stat)

def read_covid(kunta_stat):
    import json
    import pandas as pd
    import urllib.request

    url = 'https://sampo.thl.fi/pivot/prod/fi/epirapo/covid19case/fact_epirapo_covid19case.json?column=hcdmunicipality2020-445268L'
    
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    try:
        with urllib.request.urlopen(req) as f:
            f = urllib.request.urlopen(req)
    except:
        print('err')
    desc=json.loads(f.read().decode('utf-8'))

    Kunnat = list(desc['dataset']['dimension']['hcdmunicipality2020']['category']['label'].values())
    Tapaukset = list(desc['dataset']['value'].values())
    d = {'muncipality_name': Kunnat, 'Covid': Tapaukset}
    covid = pd.DataFrame(data=d)
    covid.loc[covid['Covid']=='..', 'Covid']= 0
    covid.loc[:, 'Covid']= covid['Covid'].astype(int)
    kunta_stat = pd.merge(left=kunta_stat, right=covid, on = 'muncipality_name')
    kunta_stat.loc[:, 'Covid_ilmaantuvuus'] = 10000*kunta_stat['Covid']/kunta_stat['Asukkaat yhteensä, 2017 (PT)']

    return(kunta_stat)