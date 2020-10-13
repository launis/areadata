#all stats from vero/tilastokeskus are managed due these functions


def read_json_stats(url, parameters, tunnus):
    
    """This functions reads json stat
       defined by parameters with POST comand

    Args:
        url: selected stat
        parameters:  parameter, how to read data
    
    Returns:
        dataframe

    this uses pyjstat module https://pypi.org/project/pyjstat/
    """
    

    import requests 
    from pyjstat import pyjstat
    from collections import OrderedDict
    import pandas as pd
    
    
    #query from JSON to be able to flatten data to one level
    col_list=[]
    for j in parameters["query"]:
        col_list.append(j['code'])
        
    
    col_list.remove(tunnus)

    response = requests.post(url, json=parameters)
    if response.status_code == 200:
        try:
            json_data = response.json(object_pairs_hook=OrderedDict)
        except:
            print('Json error !!!!')
            return
    else:
        print('Error: Status code: {}'.format(response.status_code))
        return
    
    results = pyjstat.from_json_stat(json_data)
    stat=pd.DataFrame(results[0])
    stat = pd.pivot_table(stat, values='value', index=[tunnus],columns=col_list)
    stat.fillna(0,inplace=True)
    stat.reset_index(level=[0], inplace=True)
    if len(col_list) > 1:
        stat.columns = stat.columns.map(' '.join)
    stat.columns = stat.columns.str.strip()
    return(stat)



def pnro_stats(stat, postinumero, stat_old):

    """This sets all postcoderelated data to one

    Args:
        stat: dataframe of managed by jsons stats
        postinumero:  id name of postcode
        stat_old: the dataframe to which the managed dataframe will be added
    
    Returns:
        new dataframe

    reading data from stat.fi, see:
        http://www.stat.fi/static/media/uploads/org/avoindata/pxweb_api-ohje.pdf
    """

    import pandas as pd
    
    stat[postinumero] = stat[postinumero].str[0:5]
    stat.rename(columns={postinumero: "Postinumero"}, inplace=True)
    stat.rename_axis(None, inplace=True, axis=1)
    if not stat_old.empty:
        stat = pd.merge(stat_old, stat, how='left', on = "Postinumero",
            left_index=False, right_index=False,
             suffixes=('_x', '_y'), copy=True, indicator=False,
             validate=None)
    return(stat)



def kunta_stats(stat, muncipalities, kuntatunnus, stat_old):
    """This merges all muncipalities data to one

    Args:
        stat: dataframe of managed by jsons stats
        muncipalities: dataframe of muncipalities
        kuntatunnus:  id name of muncipalities id
        stat_old: the dataframe to which the managed dataframe will be added
    
    Returns:
        new dataframe
    reading data from stat.fi, see:
        http://www.stat.fi/static/media/uploads/org/avoindata/pxweb_api-ohje.pdf

    """
    
    import pandas as pd
    
    #the stat does not have the muncipality number, so it needs to be found through municpality data
    stat = pd.merge(left=stat, right=muncipalities, left_on=kuntatunnus, right_on = 'muncipality_name')
    stat.drop(kuntatunnus, axis=1, inplace=True)
    stat.rename_axis(None, inplace=True, axis=1)

    
    if not stat_old.empty:
        stat = pd.merge(stat_old, stat, how='left', on = "muncipality_code",
            left_index=False, right_index=False,
             suffixes=('', '_y'), copy=True, indicator=False,
             validate=None)
        stat.drop('muncipality_name_y', axis=1, inplace=True)

    return(stat)

