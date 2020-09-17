
def read_and_prepare_data(path, readapi=False):
    
    """This function calls functions to read all needed data
       and transforms it to ready made data
        
    Args:
        path: path, where the data is stored
    
    Returns:
        post: dataframe of post
        muncipalities: dataframe of muncipalities
        postcode_list: postcodes as lists
        muncipality_list: muncipalities as lists 


    """

    import pandas as pd
    import inspect
    import os
    from shapely import wkt
    import geopandas as gp

    from inpute_null import inpute_null
    from read_and_merge_all import read_and_merge_all 
    from create_new_values import create_new_values
    from create_share_of_values import create_share_of_values
    from delete_outliers import delete_outliers
    from manage_negatives import manage_negatives
    from supportfunctions import add_zeros
    
    filename_stat = 'stat_all.csv'
    filename_stat = os.path.join(path, filename_stat)

    filename_kunta_stat =  'kunta_stat_all.csv'
    filename_kunta_stat = os.path.join(path, filename_kunta_stat)
    
    filename_vaalidata =  'vaalidata_all.csv'
    filename_vaalidata = os.path.join(path, filename_vaalidata)

    filename_post =  'post_all.csv'
    filename_post = os.path.join(path, filename_post)
 
    if (os.access(filename_stat, os.R_OK)) & (os.access(filename_kunta_stat, os.R_OK)) & (os.access(filename_vaalidata, os.R_OK))& (os.access(filename_post, os.R_OK)) & (readapi == False):
        print(inspect.stack()[0][3],' read from file')
        stat = pd.read_csv(filename_stat, encoding="ISO-8859-1")
        stat.loc[:,'Postinumero'] = stat['Postinumero'].apply(add_zeros)
        kunta_stat = pd.read_csv(filename_kunta_stat, encoding="ISO-8859-1")
        vaalidata = pd.read_csv(filename_vaalidata, encoding="ISO-8859-1")
        post = pd.read_csv(filename_post, encoding="ISO-8859-1")
        post.loc[:,'postcode'] = post['postcode'].apply(add_zeros)
                
        stat.loc[:,'geometry'] = stat['geometry'].apply(wkt.loads)
        stat = gp.GeoDataFrame(stat, geometry='geometry')
                
        post.loc[:,'geometry'] = post['geometry'].apply(wkt.loads)
        post = gp.GeoDataFrame(post, geometry='geometry')
    else:
        print(inspect.stack()[0][3],' read from api')
        stat, post, kunta_stat, vaalidata = read_and_merge_all(path)
        #values not decimal
        kunta_stat.loc[:,'Ruotsinkielisten osuus väestöstä, %, 2019'] = kunta_stat['Ruotsinkielisten osuus väestöstä, %, 2019']/100
        kunta_stat.loc[:,'Taajama-aste, %, 2018'] = kunta_stat['Taajama-aste, %, 2018']/100
        kunta_stat.loc[:,'Ulkomaan kansalaisten osuus väestöstä, %, 2019'] = kunta_stat['Ulkomaan kansalaisten osuus väestöstä, %, 2019']/100




        col_list_sama_arvo = ['Talotyypit yhteensä 2019 Neliöhinta (EUR/m2)', 'Asumisväljyys, 2018 (TE)', 'Asukkaiden keski-ikä, 2018 (HE)', 
                                        'Asukkaiden keskitulot, 2017 (HR)', 'Talouksien keskitulot, 2017 (TR)',
                                        'Asuntojen keskipinta-ala, 2018 (RA)', 'Talouksien keskikoko, 2018 (TE)',
                                        'Talouksien mediaanitulot, 2017 (TR)', 'Ruotsinkielisten osuus väestöstä, %, 2019',
                                        'Taajama-aste, %, 2018','Ulkomaan kansalaisten osuus väestöstä, %, 2019']
        
        col_list_osuuus_asukkaat  = ['Miehet, 2018 (HE)', 'Naiset, 2018 (HE)', 'Taloudet yhteensä, 2018 (TE)', 
                                     'Työlliset, 2017 (PT)', 'Työttömät, 2017 (PT)', 
                                     'Asukkaiden ostovoimakertymä, 2017 (HR)', 'Kuntien välinen muuttovoitto/-tappio, henkilöä, 2019']
        col_list_osuuus_taloudet  = ['Aikuisten taloudet, 2018 (TE)', 'Eläkeläisten taloudet, 2018 (TE)', 'Talouksien ostovoimakertymä, 2017 (TR)']
        col_tot_asukkaat = 'Asukkaat yhteensä, 2018 (HE)'
        col_tot_taloudet = 'Taloudet yhteensä, 2018 (TE)'


    
        stat=inpute_null(stat, kunta_stat,
                col_list_sama_arvo, 
                col_list_osuuus_asukkaat,
                col_list_osuuus_taloudet,
                col_tot_taloudet,
                col_tot_asukkaat)
       

        stat = create_share_of_values(stat)
        stat = create_new_values(stat, vaalidata)
        
        col_list_negatives = ['Kuntien välinen muuttovoitto/-tappio, henkilöä, 2019 osuudesta asukkaat']
        stat=manage_negatives(stat, col_list_negatives)

        
        stat = delete_outliers(stat)
        stat = gp.GeoDataFrame(stat, geometry='geometry')
        post = gp.GeoDataFrame(post, geometry='geometry')

        if (os.path.exists(path)) & (readapi == False):
            print(inspect.stack()[0][3],' write to file')
            stat.to_csv(filename_stat, index=False, encoding="ISO-8859-1")
            kunta_stat.to_csv(filename_kunta_stat, index=False, encoding="ISO-8859-1")
            vaalidata.to_csv(filename_vaalidata, index=False, encoding="ISO-8859-1")
            post.to_csv(filename_post, index=False, encoding="ISO-8859-1")

    return(stat, post, kunta_stat, vaalidata)