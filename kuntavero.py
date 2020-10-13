def kuntavero(url, kunta_stat):

    import pandas as pd
    
    kunta_vero=pd.read_excel(url, skiprows=3, sheet_name='Suomi')
    kunta_vero.columns = kunta_vero.columns.str.strip()
    kunta_vero=kunta_vero[['Kunta','Tuloveroprosentti']].copy()
    kunta_vero.loc[:,'Kunta'] = kunta_vero['Kunta'].str.strip()
    kunta_vero=kunta_vero[4:].copy()
    kunta_vero.reset_index(inplace=True, drop=True)
    kunta_stat = pd.merge(left=kunta_stat, right=kunta_vero, left_on='muncipality_name', right_on = 'Kunta', how='left')
    kunta_stat.drop('Kunta', axis=1, inplace=True)
    kunta_stat.loc[:,'Tuloveroprosentti'] = kunta_stat['Tuloveroprosentti']/100
    return(kunta_stat)