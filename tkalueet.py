def tkalueet(url, stat):
    
    """Reads licensed bars and shops right to sell alco
    url: data from register
    stat: data from postcodes
    example url url="https://www.stat.fi/fi/luokitukset/corrmaps/export/kunta_1_20200101%23tyossakayntial_1_20200101/"
    

    """

    import pandas as pd
    
    def etaisyys(pnro):
        import utm
        from geopy import distance
    
        a = stat[stat['Postinumero'] == pnro]['X-koordinaatti metreinä'].values
        b = stat[stat['Postinumero'] == pnro]['Y-koordinaatti metreinä'].values
    
        kuntanro  = stat[stat['Postinumero'] == pnro]['muncipality_code'].values[0]
        if tkalue[tkalue['Kuntanumero']==kuntanro]['Tkalue'].values[0] == 'Ei tk-alue':
            return(pd.Series([0, 0]))
        else:
            c = tkalue[tkalue['Kuntanumero']==kuntanro]['X-koordinaatti metreinä'].values
            d = tkalue[tkalue['Kuntanumero']==kuntanro]['Y-koordinaatti metreinä'].values
        some_list = ['22240', '22270']
        if any(pnro in s for s in some_list):
            return(pd.Series([20, 1]))
        start = utm.to_latlon(a, b, 32, 'U')
        end = utm.to_latlon(c, d, 32, 'U')
        return(pd.Series([distance.distance(start, end).km, 1]))
    
    def keskus_koordinaatit(tkalue, alue, postinumero):
        tkalue.loc[tkalue['Tkalue']==alue,'X-koordinaatti metreinä'] = stat[stat['Postinumero']==postinumero]['X-koordinaatti metreinä'].item()
        tkalue.loc[tkalue['Tkalue']==alue,'Y-koordinaatti metreinä'] = stat[stat['Postinumero']==postinumero]['Y-koordinaatti metreinä'].item()
        return(tkalue)
    
    tkalue = pd.DataFrame()
    

    conv = lambda x : (x.replace("'", ""))
    tkalue=pd.read_csv(url, sep=";", encoding="ISO-8859-1", skiprows=4, 
                low_memory=False, names=['Kuntanumero', 'Kunta', 'Tkaluenumero', 'Tkalue'],
                converters = {'Kuntanumero':conv, 'Tkaluenumero':conv})
    tkalue = tkalue.apply(pd.to_numeric, errors='ignore')

    alue = 'Tampereen tk-alue'
    postinumero = '33100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Alajärven tk-alue'
    postinumero = '62900'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Lahden tk-alue'
    postinumero = '15110'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Helsingin tk-alue'
    postinumero = '00100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Turun tk-alue'
    postinumero = '20100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Maarianhaminan tk-alue'
    postinumero = '22100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Savonlinnan tk-alue'
    postinumero = '57100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Rauman tk-alue'
    postinumero = '26100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Oulun tk-alue'
    postinumero = '90100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Kotkan tk-alue'
    postinumero = '48100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Jyväskylän tk-alue'
    postinumero = '40100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Porin tk-alue'
    postinumero = '28100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Mikkelin tk-alue'
    postinumero = '50100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Kankaanpään tk-alue'
    postinumero = '38700'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Kajaanin tk-alue'
    postinumero = '87100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Iisalmen tk-alue'
    postinumero = '74100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Kouvolan tk-alue'
    postinumero = '45100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Seinäjoen tk-alue'
    postinumero = '60100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Joensuun tk-alue'
    postinumero = '80100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Lappeenrannan tk-alue'
    postinumero = '53100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Vaasan tk-alue'
    postinumero = '65100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Varkauden tk-alue'
    postinumero = '78200'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Jämsän tk-alue'
    postinumero = '42100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Kuopion tk-alue'
    postinumero = '70100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Kokkolan tk-alue'
    postinumero = '67100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Närpiön tk-alue'
    postinumero = '64200'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Kauhajoen tk-alue'
    postinumero = '61800'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Kemin tk-alue'
    postinumero = '94100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Uudenkaupungin tk-alue'
    postinumero = '23500'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Loimaan tk-alue'
    postinumero = '32200'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    
    alue = 'Raahen tk-alue'
    postinumero = '92100'
    tkalue = keskus_koordinaatit(tkalue, alue, postinumero)
    


    tkdata=stat['Postinumero'].apply(etaisyys)

    stat.loc[:,'etaisyys'] = tkdata[0]
    stat.loc[:,'tkalue'] = tkdata[1]

    return(stat)