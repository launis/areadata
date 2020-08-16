#these functions read and manage kiinteisto/adderess register either from local file
#or from given address


def kiinteisto(url):
    
    """reads kiinteisto data from Finnish registes
    
    args:
        url:  the latest kiinteisto URL
 
    Exsample of url = "https://www.avoindata.fi/data/dataset/cf9208dc-63a9-44a2-9312-bbd2c3952596/resource/ae13f168-e835-4412-8661-355ea6c4c468/download/suomi_osoitteet_2020-05-15.7z"
        
    the data is in sevenZipfile
    Python py7zr library supports 7zip archive management
    https://pypi.org/project/py7zr/
        
    Description of kiinteistodata
    https://www.avoindata.fi/data/dataset/cf9208dc-63a9-44a2-9312-bbd2c3952596/resource/ae13f168-e835-4412-8661-355ea6c4c468

    Returns:
         register of kiinteisto
    """
    import requests 
    import py7zr
    import io
    import pandas as pd
    from supportfunctions import add_zeros

    
    r = requests.get(url)

    path = "/tmp"
    archive = py7zr.SevenZipFile(io.BytesIO(r.content))
    archive.extractall(path=path)
    datafile=path+"/"+archive.getnames()[0]
    archive.close()
    kiinteisto=pd.read_csv(datafile,sep=";", header=None, encoding="ISO-8859-1", low_memory=False)
    kiinteisto.columns=['Rakennustunnus','Kuntanumero','Maakunta','Käyttötarkoitus',
              'Pohjoiskoordinaatti','Itäkoordinaatti','Osoitenumero','Kadunnimi suomeksi',
              'Kadunnimi ruotsiksi','Katunumero','Postinumero','Äänestysalue','Äänestysalueen nimi suomeksi',
              'Äänestysalueen nimi ruotsiksi','Sijaintikiinteistö','Tietojen poimintapäivä']

    df_obj = kiinteisto.select_dtypes(['object'])
    kiinteisto[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    kiinteisto['Postinumero'] = kiinteisto['Postinumero'].apply(add_zeros)
    #äänestysalue ja kuntanumero samaan alue dataan, käytetään myöhemmin
    kiinteisto.loc[(kiinteisto['Äänestysalue'].notna()) & (kiinteisto['Kuntanumero'].notna()), 'Alue'] = kiinteisto.loc[kiinteisto['Kuntanumero'].notna(), 'Kuntanumero'].astype(int).astype(str) + "-" + kiinteisto.loc[kiinteisto['Äänestysalue'].notna(), 'Äänestysalue']

    return(kiinteisto)




def read_kiinteisto(path, url_kiinteisto):
    
    """This function reads all needed data
       either from file or calls a function to fetch data
       via API calls directly from sources and then writes data to files

    Args:
        path: path, where the data is stored 
        url_kiinteisto: 
        https://www.avoindata.fi/data/dataset/cf9208dc-63a9-44a2-9312-bbd2c3952596/resource/ae13f168-e835-4412-8661-355ea6c4c468

    
    Returns:
        kiinteisto: dataframe of kiinteisto

    """

    import pandas as pd   
    import os
    import inspect
    from supportfunctions import add_zeros

    #read post and muncipalities
    filename_kiinteisto = 'kiinteisto.csv'

    filename_kiinteisto = os.path.join(path, filename_kiinteisto)

    if os.access(filename_kiinteisto, os.R_OK):
        #read it from files
        print(inspect.stack()[0][3],' read from file')
        kiinteisto_data = pd.read_csv(filename_kiinteisto, encoding="ISO-8859-1", low_memory=False)
        kiinteisto_data.loc[:,'Postinumero'] = kiinteisto_data['Postinumero'].apply(add_zeros)

    else:
        #read kiinteistodata
        print(inspect.stack()[0][3],' read from API')
        kiinteisto_data = kiinteisto(url_kiinteisto)
        kiinteisto_data.to_csv(filename_kiinteisto, index=False, encoding="ISO-8859-1")
    return(kiinteisto_data)

