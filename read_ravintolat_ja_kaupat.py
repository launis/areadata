#this section takes care of reading all needed alco licese data

def ravintolat_ja_kaupat(url, post):
    
    """Reads licensed bars and shops right to sell alco
    url: data from register
    post: data from postcodes
    
    Example url = "http://avoindata.valvira.fi/alkoholi/alkoholilupa_toimipaikkatiedot_ABC.csv"
    Format
    https://www.avoindata.fi/data/fi/dataset/alkoholielinkeinorekisteri
    
    Returns:
         register of postcodes with restaurants and bars
         The data includes all postcodes even where
         restaurants and bars are empty
    """

    import pandas as pd
    from supportfunctions import add_zeros

    ravintolat=pd.read_csv(url, sep=";", encoding="ISO-8859-1", low_memory=False)
    
    df_obj = ravintolat.select_dtypes(['object'])
    ravintolat[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    ravintolat['POSTINUMERO'] = ravintolat['POSTINUMERO'].apply(add_zeros)

    #decide if this is a bar or shop    
    ravintolat['baari'] = (ravintolat['LUPATYYPPI'].str.contains('ann', case = False)) | (ravintolat['LUPATYYPPI'].str.contains('A', case = True)) | (ravintolat['LUPATYYPPI'].str.contains('B', case = True))
    pnro_baari = ravintolat[ravintolat['baari']==False].reset_index().groupby(['POSTINUMERO'],as_index=False).count()[['POSTINUMERO','baari']].copy()
    pnro_myymala = ravintolat[ravintolat['baari']==True].reset_index().groupby(['POSTINUMERO'],as_index=False).count()[['POSTINUMERO','baari']].copy()
    pnro_palvelut = pd.merge(pnro_baari, pnro_myymala, how='outer', on='POSTINUMERO', copy=True, sort=True).copy()
    pnro_palvelut.rename(columns={'POSTINUMERO' : 'Postinumero','baari_x': 'Ravintolat', 'baari_y': 'Myymälät'}, inplace=True)
    pnro_palvelut =  pnro_palvelut[['Postinumero', 'Ravintolat', 'Myymälät' ]].copy()
    pnro_palvelut=pd.merge(post, pnro_palvelut, how='left', left_on = 'postcode',right_on= 'Postinumero',
         left_index=False, right_index=False,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None).copy()
    pnro_palvelut.drop(['Postinumero'], axis=1, inplace=True)
    pnro_palvelut.rename(columns={'postcode' : 'Postinumero'}, inplace=True)

    #postcodes without any services to 0-values
    pnro_palvelut['Ravintolat'].fillna(0, inplace=True)
    pnro_palvelut['Myymälät'].fillna(0, inplace=True)
    pnro_palvelut = pnro_palvelut[['Postinumero', 'Ravintolat', 'Myymälät']].copy()
    return(pnro_palvelut)



def read_ravintolat_ja_kaupat(path, post, url_ravintolat ):
    
    """This function reads all needed data
       either from file or calls a function to fetch data
       via API calls directly from sources and then writes data to files

    Args:
        path: path, where the data is stored 
        post: data of postcodes
        url_ravintolat : csv data file
    see:
    https://www.avoindata.fi/data/fi/dataset/alkoholielinkeinorekisteri
 
    
    Returns:
        ravintolat: dataframe of ravintolat and shops allowed sella lc

    """
    import os
    import pandas as pd   
    import inspect
    from supportfunctions import add_zeros

    #read post and muncipalities
    filename_ravintolat_ja_kaupat = 'ravintolat_ja_kaupat.csv'
    filename_ravintolat_ja_kaupat = os.path.join(path, filename_ravintolat_ja_kaupat)    

    if os.access(filename_ravintolat_ja_kaupat, os.R_OK):
        #read it from files

        print(inspect.stack()[0][3],' read from file')
        ravintolat= pd.read_csv(filename_ravintolat_ja_kaupat, encoding="ISO-8859-1")
        ravintolat.loc[:,'Postinumero'] = ravintolat['Postinumero'].apply(add_zeros)

    else:
        #read restaurant/shop data
        #https://www.avoindata.fi/data/fi/dataset/alkoholielinkeinorekisteri
        print(inspect.stack()[0][3],' read from API')
        ravintolat= ravintolat_ja_kaupat(url_ravintolat, post)

        if os.path.exists(path):

            ravintolat.to_csv(filename_ravintolat_ja_kaupat, index=False, encoding="ISO-8859-1")
    return(ravintolat)