
def read_and_prepare_data(path):
    
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

    import inspect
    from inpute_null import inpute_null
    from read_and_merge_all import read_and_merge_all 
    from create_new_values import create_new_values
    from create_share_of_values import create_share_of_values
    from delete_outliers import delete_outliers

    
    print(inspect.stack()[0][3],' read from start')

    stat, post, kunta_stat, vaalidata = read_and_merge_all(path)
    #stat=stat[stat['Asukkaat yhteensä, 2018 (HE)']!=0].copy()
        
    
    col_list_sama_arvo  = ['Talotyypit yhteensä 2019 Neliöhinta (EUR/m2)', 'Asumisväljyys, 2018 (TE)', 'Asuntojen keskipinta-ala, 2018 (RA)']
    col_list_osuuus  = ['Miehet, 2018 (HE)', 'Naiset, 2018 (HE)', 'Taloudet yhteensä, 2018 (TE)']
    stat=inpute_null(stat, kunta_stat, col_list_sama_arvo, col_list_osuuus)
    
    
    stat = create_share_of_values(stat)
    stat = create_new_values(stat, vaalidata)
    stat = delete_outliers(stat)


        

    return(stat, post, kunta_stat, vaalidata)