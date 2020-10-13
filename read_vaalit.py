

#in these functions election data is prepared with the help of kiinteisto data

def kiinteisto_alueiksi(kiinteisto):
    
    """
    kiinteist:  kiinteisto/property register
    
    An artificial property / constituency division will be made for the regionalization of postal codes.
    A brute-force distribution is used, where the relative number of residential properties in the constituency is divided into postcodes. 
    Generally, constituencies are smaller than postcode areas.

    The paid property data (kiinteistorekisteri) also includes the number of apartments in the property data. In this way, the division would be more accurate.
    In various inspections, the division seemed competent.

    This returns the estimate of shares

    Returns:
         kiintosuus
         
    """
    import pandas as pd
    
    #new kiint and kiintpnrot -dataframes, with muncipality, constituency area and postcode
    kiint=kiinteisto[kiinteisto['Käyttötarkoitus']==1].reset_index().groupby(['Kuntanumero','Alue','Postinumero'],as_index=False ).count()
    kiint=kiint[['Alue','Postinumero','index']]
    
    kiintpnrot=kiint.reset_index().groupby(['Postinumero', 'Alue'],as_index=False ).sum()[['Alue','Postinumero','index']]
    kiintalueet=kiint.reset_index().groupby(['Alue'],as_index=False).sum()[['Alue','index']]
    
    
    #join them by constituency area
    kiintosuus= pd.merge(kiintpnrot, kiintalueet, how='inner', on='Alue',
         left_index=False, right_index=False,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

    #brute-force calculation of share of areas based on the amount of properties
    kiintosuus['Osuus']=kiintosuus['index_x']/kiintosuus['index_y']
    kiintosuus=kiintosuus[['Alue','Postinumero','Osuus']]
    return(kiintosuus)





def aaniosuudet(kiint, post, url_puolueet, url_alueet):
    """read election results and share the votest
       to postcodes
       https://tulospalvelu.vaalit.fi/EKV-2019/

       
       args:
           kiint: data of postcode shares of votes
           post: postcode data
           url_puolueet: data from election results of parties
           url_alueet: data from area based results
 
        Exsample of url = 
            url_puolueet = "https://tulospalvelu.vaalit.fi/EKV-2019/ekv-2019_puo_maa.csv.zip"
            url_alueet = 'https://tulospalvelu.vaalit.fi/EKV-2019/ekv-2019_alu_maa.csv.zip'
            
       returns:
           osuudet: shares of results by postcode
           vaalidata: actual vaalidata
    """
    import requests 
    import io
    import zipfile
    import numpy as np
    import pandas as pd
    
    #party based results
    r = requests.get(url_puolueet)
    zf = zipfile.ZipFile(io.BytesIO(r.content))

    zip_names = zf.namelist()

    # find the first matching csv file in the zip:
    match = [s for s in zip_names if ".csv" in s][0]
    vaalidata=pd.read_csv(zf.open(match), header=None, sep=";",na_values =['**','***','****'] ,error_bad_lines=False, low_memory=False, encoding="ISO-8859-1")

    vaalidata = vaalidata[vaalidata.columns[np.concatenate([range(0,23),range(38,45)])]]
                      
    vaalidata.columns=['Vaalilaji', 'Vaalipiirinumero', 'Kuntanumero', 'Alueen tyyppi','Äänestysalue', 
                   'Vaalipiirin lyhenne suomeksi','Vaalipiirin lyhenne ruotsiksi','Pysyvä puoluetunniste',
                   'Vakiopuoluenumero','Listajärjestysnumero', 'Puolueen nimilyhenne suomeksi',
                   'Puolueen nimilyhenne ruotsiksi', 'Puolueen nimilyhenne englanniksi',
                   'Alueen nimi suomeksi', 'Alueen nimi ruotsiksi', 'Puolueen nimi suomeksi',
                   'Puolueen nimi ruotsiksi', 'Puolueen nimi englanniksi','Pienin ehdokasnumero',
                   'Suurin ehdokasnumero','Vaaliliittonumero','Vaaliliiton nimi suomeksi', 'Vaaliliiton nimi ruotsiksi',
                   'Ennakkoäänet lkm', 'Vaalipäivän äänet lkm', 'Äänet yhteensä lkm', 'Osuus ennakkoäänistä (%)',
                   'Osuus vaalipäivän äänistä (%)', 'Osuus kaikista äänistä (%)', 'Paikat']

    #area based results    
    r = requests.get(url_alueet)
    zf = zipfile.ZipFile(io.BytesIO(r.content))

    zip_names = zf.namelist()

    # find the first matching csv file in the zip:
    match = [s for s in zip_names if ".csv" in s][0]
    vd=pd.read_csv(zf.open(match), header=None, sep=";",na_values =['**','***','****'] ,error_bad_lines=False, low_memory=False, encoding="ISO-8859-1")
    vd = vd[vd.columns[np.concatenate([range(0,5), range(13,14), range(36,37), range(38,39), range(40,41), range(63,69)])]]
   
    
    vd.columns=['Vaalilaji', 'Vaalipiirinumero', 'Kuntanumero', 'Alueen tyyppi','Äänestysalue', 'Äänioikeutetut yhteensä',
                'Ennakkoon äänestäneet', 'Vaalipäivänä äänestäneet', 'Äänestäneet yhteensä',
                'Hyväksytyt ennakkoäänet', 'Hyväksytyt vaalipäivän äänet', 'Hyväksytyt äänet yht.',
                'Mitättömät ennakkoäänet','Mitättömät vaalipäivän äänet ','Mitättömät äänet yht.']

    #calcultate  all votes pre-votes and date of election votes separately
    yht=pd.melt(vd, id_vars=vd.columns[:5], value_vars=vd.columns[np.concatenate([range(5,6), range(8,9), range(11,12), range(14,15)])], var_name = 'Puolueen nimilyhenne suomeksi', value_name ='Äänet yhteensä lkm')
    ennakko=pd.melt(vd, id_vars=vd.columns[:5], value_vars=vd.columns[np.concatenate([range(6,7), range(9,10), range(12,13)])], var_name = 'Puolueen nimilyhenne suomeksi', value_name ='Ennakkoäänet lkm')
    kaikki=pd.concat([yht, ennakko], axis=0)
    vaalipaiva=pd.melt(vd, id_vars=vd.columns[:5], value_vars=vd.columns[np.concatenate([range(7,8), range(10,11), range(13,14)])], var_name = 'Puolueen nimilyhenne suomeksi', value_name ='Vaalipäivän äänet lkm')
    kaikki=pd.concat([kaikki, vaalipaiva], axis=0)

    kaikki.loc[kaikki['Puolueen nimilyhenne suomeksi'].isin(['Äänestäneet yhteensä',
       'Ennakkoon äänestäneet', 'Vaalipäivänä äänestäneet']), 'Puolueen nimilyhenne suomeksi'] ='Äänet'
    kaikki.loc[kaikki['Puolueen nimilyhenne suomeksi'].isin(['Hyväksytyt äänet yht.', 'Hyväksytyt ennakkoäänet',
       'Hyväksytyt vaalipäivän äänet']), 'Puolueen nimilyhenne suomeksi'] ='Hyväksytyt'
    kaikki.loc[kaikki['Puolueen nimilyhenne suomeksi'].isin(['Mitättömät äänet yht.',
       'Mitättömät ennakkoäänet', 'Mitättömät vaalipäivän äänet ']), 'Puolueen nimilyhenne suomeksi'] = 'Mitättömät'
    kaikki = kaikki.reset_index().groupby(['Vaalilaji', 'Vaalipiirinumero', 'Kuntanumero', 'Alueen tyyppi','Äänestysalue', 'Puolueen nimilyhenne suomeksi'], as_index=False)[['Äänet yhteensä lkm', 'Ennakkoäänet lkm', 'Vaalipäivän äänet lkm']].sum()

    #combine both datas
    vaalidata = vaalidata.append(kaikki, sort=False)
    vaalidata=vaalidata[['Vaalilaji', 'Vaalipiirinumero', 'Kuntanumero', 'Alueen tyyppi','Äänestysalue', 'Puolueen nimilyhenne suomeksi', 'Äänet yhteensä lkm', 'Ennakkoäänet lkm', 'Vaalipäivän äänet lkm']]
    vaalidata.reset_index(inplace=True)

    
    areas=post.groupby(['muncipality_code','area_code'],as_index=False ).mean()[['muncipality_code', 'area_code']][['muncipality_code', 'area_code']]
    vaalidata = pd.merge(left=vaalidata, right=areas, left_on = 'Kuntanumero', right_on='muncipality_code')
    vaalidata.drop(['muncipality_code'], axis=1, inplace=True)

    df_obj = vaalidata.select_dtypes(['object'])
    vaalidata[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    #create id
    vaalidata.loc[(vaalidata['Äänestysalue'].notna()) & (vaalidata['Kuntanumero'].notna()), 'Alue'] = vaalidata.loc[vaalidata['Kuntanumero'].notna(), 'Kuntanumero'].astype(int).astype(str) + "-" + vaalidata.loc[vaalidata['Äänestysalue'].notna(), 'Äänestysalue']
    
    #combining postal code shares based on the number of properties obtained through the 
    #address register and the election results of the polling station
    postinumeroosuus = pd.merge(kiint, vaalidata, how='inner', on='Alue',
         left_index=False, right_index=False,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)[['Alue','Postinumero','Osuus', 'Puolueen nimilyhenne suomeksi','Äänet yhteensä lkm', 'Ennakkoäänet lkm', 'Vaalipäivän äänet lkm']]
  
    postinumeroosuus['Äänet yhteensä lkm'] = postinumeroosuus['Äänet yhteensä lkm'] * postinumeroosuus['Osuus'] 
    postinumeroosuus['Ennakkoäänet lkm'] = postinumeroosuus['Ennakkoäänet lkm'] * postinumeroosuus['Osuus'] 
    postinumeroosuus['Vaalipäivän äänet lkm'] = postinumeroosuus['Vaalipäivän äänet lkm'] * postinumeroosuus['Osuus'] 
    

    #partyvotes
    pnropuolue=postinumeroosuus.reset_index().groupby(['Postinumero', 'Puolueen nimilyhenne suomeksi'],as_index=False ).sum()[['Postinumero', 'Puolueen nimilyhenne suomeksi','Äänet yhteensä lkm', 'Ennakkoäänet lkm', 'Vaalipäivän äänet lkm']]

    #zeros to zeros
    pnropuolue['Äänet yhteensä lkm']=pnropuolue['Äänet yhteensä lkm'].astype(int)
    pnropuolue.loc[pnropuolue['Äänet yhteensä lkm']==0,'Ääniosuus']=0

    pnropuolue['Ennakkoäänet lkm']=pnropuolue['Ennakkoäänet lkm'].astype(int)
    pnropuolue.loc[pnropuolue['Ennakkoäänet lkm']==0,'Ääniosuus Ennakkoäänet']=0

    pnropuolue['Vaalipäivän äänet lkm']=pnropuolue['Vaalipäivän äänet lkm'].astype(int)
    pnropuolue.loc[pnropuolue['Vaalipäivän äänet lkm']==0,'Ääniosuus Vaalipäivän äänet']=0
    
    #pivot to otherway
    osuudet=pnropuolue.pivot(index='Postinumero', columns='Puolueen nimilyhenne suomeksi', values=['Äänet yhteensä lkm', 'Ääniosuus', 'Ennakkoäänet lkm', 'Ääniosuus Ennakkoäänet', 'Vaalipäivän äänet lkm', 'Ääniosuus Vaalipäivän äänet'])
    osuudet.fillna(0,inplace=True)
    osuudet.reset_index(level=[0], inplace=True)
    osuudet.columns = osuudet.columns.map(' '.join)
    osuudet.columns = osuudet.columns.str.strip()

    vaalidata = vaalidata[vaalidata['Äänestysalue'].notna()].copy()
    vaalidata.loc[:,['Vaalipiirinumero', 'Kuntanumero',  'Äänet yhteensä lkm', 'Ennakkoäänet lkm', 'Vaalipäivän äänet lkm']] = vaalidata[['Vaalipiirinumero', 'Kuntanumero',  'Äänet yhteensä lkm', 'Ennakkoäänet lkm', 'Vaalipäivän äänet lkm']].astype(int)

    return(osuudet, vaalidata)


def read_vaalit(path, post, kiinteisto, url_puolueet, url_alueet):
    
    """This function reads all needed data
       either from file or calls a function to fetch data
       via API calls directly from sources and then writes data to files

    Args:
        path: path, where the data is stored  
        post: dataframe of postcodes
        kiinteisto: dataframe of kiinteisto
        url_puolueet: data of party votes
        url_alueet: data of area votes
    
     https://tulospalvelu.vaalit.fi/EKV-2019/
     https://tulospalvelu.vaalit.fi/EKV-2019/ohje/Vaalien_tulostiedostojen_kuvaus_EKV-EPV-2019_FI.pdf
    
    Returns:
        osuudet: shares of vaalit
        vaalidata : pure vaalidata

    """

    import pandas as pd   
    import os
    import inspect
    from supportfunctions import add_zeros


    filename_vaalidata = 'vaalit.csv'
    filename_osuudet = 'osuudet.csv'

    filename_vaalidata = os.path.join(path, filename_vaalidata)

    filename_osuudet= os.path.join(path, filename_osuudet)


    if (os.access(filename_vaalidata, os.R_OK)) & (os.access(filename_osuudet, os.R_OK)):
        print(inspect.stack()[0][3],' read from file')
        osuudet = pd.read_csv(filename_osuudet, encoding="ISO-8859-1")        
        osuudet.loc[:,'Postinumero'] = osuudet['Postinumero'].apply(add_zeros)
        vaalidata = pd.read_csv(filename_vaalidata, encoding="ISO-8859-1")
    else:
        print(inspect.stack()[0][3],' read from API')
        kiint = kiinteisto_alueiksi(kiinteisto)
        osuudet, vaalidata = aaniosuudet(kiint, post, url_puolueet, url_alueet)
        if os.path.exists(path):
            osuudet.to_csv(filename_osuudet, index=False, encoding="ISO-8859-1")
            vaalidata.to_csv(filename_vaalidata, index=False, encoding="ISO-8859-1")
 
    return(osuudet, vaalidata)    
