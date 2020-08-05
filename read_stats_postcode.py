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



def read_stats_postcode(path,
                        data_list_post1,
                        data_list_post2,
                        data_list_post3,
                        data_list_muncipality,
                        data_list_vero,
                        muncipalities,
                        post,
                        postcode_list,
                        muncipality_list,
                        stat_url,
                        stat_url_kunta,
                        stat_url_kuntatiedot,
                        stat_url_vero,
                        stat_url_vero_kunta,
                        stat_url_asunnot,
                        stat_url_asunnot_kunta):
    
    """This function reads all needed data
       either from file or calls a function to fetch data
       via API calls directly from sources and then writes data to files

    Args:
        path: path, where the data is stored
        data_list_post: guidance what data to read from postarea data
        data_list_muncipality: guidance what data to read from muncipality data
        data_list_vero: : guidance what data to read from vero data
        muncipalities: dataframe of muncipalities
        post: list of postcodes
        postcode_list: simple list of postcode numbers as string
        muncipality_list: simple list of  muncipality numbers as string
        stat_url : the addres of recent Paavo
            http://pxnet2.stat.fi/PXWeb/pxweb/fi/Postinumeroalueittainen_avoin_tieto/Postinumeroalueittainen_avoin_tieto__2020/paavo_pxt_12f7.px/
            use always all data
        stat_url_kunta: similar as postcode
            http://pxnet2.stat.fi/PXWeb/pxweb/fi/Postinumeroalueittainen_avoin_tieto/Postinumeroalueittainen_avoin_tieto__2020/paavo_pxt_12f8.px/
        stat_url_kuntatiedot: similar as postcode
            https://pxnet2.stat.fi/PXWeb/pxweb/fi/Kuntien_avainluvut/Kuntien_avainluvut__2020/kuntien_avainluvut_2020_viimeisin.px/?rxid=444223df-f91c-4479-891f-5dcd50b983d2
        stat_url_vero: similar as postcode
            http://vero2.stat.fi/PXWeb/pxweb/fi/Vero/Vero__Henkiloasiakkaiden_tuloverot__lopulliset__postinum/postinum_104.px/
        stat_url_vero_kunta
            http://vero2.stat.fi/PXWeb/pxweb/fi/Vero/Vero__Henkiloasiakkaiden_tuloverot__lopulliset__postinum/postinum_101.px/
        
        stat_url_asunnot: prices of houses by postcode
            http://pxnet2.stat.fi/PXWeb/pxweb/fi/StatFin/StatFin__asu__ashi__vv/statfin_ashi_pxt_112q.px/
        stat_url_asunnot_kunta
            http://pxnet2.stat.fi/PXWeb/pxweb/fi/StatFin/StatFin__asu__ashi__vv/statfin_ashi_pxt_112v.px/
    
    Returns:
        stat: statics by postcode
        kunta_stat:statistics by muncipality

    """
    import pandas as pd   
    import os
    import inspect
    from supportfunctions import add_zeros
    

    #read post and muncipalities
    filename_stat = 'stat.csv'
    filename_stat = os.path.join(path, filename_stat )

    filename_kunta_stat =  'kunta_stat.csv'
    filename_kunta_stat = os.path.join(path, filename_kunta_stat )
 
    if (os.access(filename_stat, os.R_OK)) & (os.access(filename_kunta_stat, os.R_OK)):
        #try to read data from files
        print(inspect.stack()[0][3],' read from file')
        stat = pd.read_csv(filename_stat, encoding="ISO-8859-1")
        stat.loc[:,'Postinumero'] = stat['Postinumero'].apply(add_zeros)
        kunta_stat = pd.read_csv(filename_kunta_stat, encoding="ISO-8859-1")
    else:
        #call functions to read data through API cals
        print(inspect.stack()[0][3],' read from API')
        postinumero = "Postinumeroalue"
        
        parameters = {"query":[{"code":"Postinumeroalue","selection":
                               {"filter":"item","values":postcode_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":data_list_post1}}],
                      "response":{"format":"json-stat"}}
        
        stat_new=read_json_stats(stat_url, parameters, postinumero)
        stat=pnro_stats(stat_new, postinumero, pd.DataFrame())

        parameters = {"query":[{"code":"Postinumeroalue","selection":
                               {"filter":"item","values":postcode_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":data_list_post2}}],
                      "response":{"format":"json-stat"}}
        
        stat_new=read_json_stats(stat_url, parameters, postinumero)
        stat=pnro_stats(stat_new, postinumero, stat)

        parameters = {"query":[{"code":"Postinumeroalue","selection":
                               {"filter":"item","values":postcode_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":data_list_post3}}],
                      "response":{"format":"json-stat"}}
        
        stat_new=read_json_stats(stat_url, parameters, postinumero)
        stat=pnro_stats(stat_new, postinumero, stat)

        
        #kuntadata demands in this case ku to the front
        string = 'KU'
        kuntatunnus = "Alue"
        new_muncipality_list = [string + x for x in muncipality_list] 
        parameters = {"query":[{"code":"Alue","selection":{"filter":"item","values":new_muncipality_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":data_list_post1}}],
                      "response":{"format":"json-stat"}}
        
        stat_new=read_json_stats(stat_url_kunta, parameters, kuntatunnus)
        kunta_stat = kunta_stats(stat_new, muncipalities, kuntatunnus, pd.DataFrame())

        parameters = {"query":[{"code":"Alue","selection":{"filter":"item","values":new_muncipality_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":data_list_post2}}],
                      "response":{"format":"json-stat"}}
        
        stat_new=read_json_stats(stat_url_kunta, parameters, kuntatunnus)
        kunta_stat = kunta_stats(stat_new, muncipalities, kuntatunnus, kunta_stat)

        parameters = {"query":[{"code":"Alue","selection":{"filter":"item","values":new_muncipality_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":data_list_post3}}],
                      "response":{"format":"json-stat"}}
        
        stat_new=read_json_stats(stat_url_kunta, parameters, kuntatunnus)
        kunta_stat = kunta_stats(stat_new, muncipalities, kuntatunnus, kunta_stat)

        kuntatunnus = "Alue 2020"
        parameters = {"query":[{"code":"Alue 2020","selection":{"filter":"item","values":muncipality_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":data_list_muncipality}}],
                      "response":{"format":"json-stat"}}

        stat_new=read_json_stats(stat_url_kuntatiedot, parameters, kuntatunnus)
        kunta_stat = kunta_stats(stat_new, muncipalities, kuntatunnus, kunta_stat)

        #tax postcode
        postcode_vero_list = (post['muncipality_code'].apply(lambda x: "{:03d}{}".format(x,"_")) + post['postcode']).to_list()
        
        parameters = {"query":[{"code":"Erä","selection":{"filter":"item","values":data_list_vero}},{"code":"Sukupuoli","selection":{"filter":"item","values":["S"]}},{"code":"Kuntapostinumero","selection":{"filter":"item","values":postcode_vero_list}},{"code":"Tunnusluvut","selection":{"filter":"item","values":["Sum","N"]}}],"response":{"format":"json-stat"}}
        postinumero = "Kuntapostinumero"

        stat_new=read_json_stats(stat_url_vero, parameters, postinumero)
        stat=pnro_stats(stat_new, postinumero, stat)

        
        #tax muncipalities
        parameters = {"query":[{"code":"Erä","selection":{"filter":"item","values":data_list_vero}},{"code":"Sukupuoli","selection":{"filter":"item","values":["S"]}},{"code":"Alue","selection":{"filter":"item","values":muncipality_list}},{"code":"Tunnusluvut","selection":{"filter":"item","values":["Sum","N"]}}],"response":{"format":"json-stat"}}
        kuntatunnus = "Alue"
        stat_new=read_json_stats(stat_url_vero_kunta, parameters, kuntatunnus)
        kunta_stat = kunta_stats(stat_new, muncipalities, kuntatunnus, kunta_stat)


        stat_url_asunnot = "http://pxnet2.stat.fi/PXWeb/api/v1/fi/StatFin/asu/ashi/vv/statfin_ashi_pxt_112q.px"
        parameters = {"query":[{"code":"Postinumero","selection":{"filter":"item","values":postcode_list}},{"code":"Talotyyppi","selection":{"filter":"item","values":["6"]}},{"code":"Rakennusvuosi","selection":{"filter":"item","values":["0"]}},{"code":"Vuosi","selection":{"filter":"item","values":["2019"]}},{"code":"Tiedot","selection":{"filter":"item","values":["keskihinta_ptno"]}}],"response":{"format":"json-stat"}}
        postinumero = "Postinumero"

        stat_new=read_json_stats(stat_url_asunnot, parameters, postinumero)
        stat=pnro_stats(stat_new, postinumero, stat)

        parameters = {"query":[{"code":"Talotyyppi","selection":{"filter":"item","values":["0"]}},{"code":"Kunta","selection":{"filter":"item","values":muncipality_list}},{"code":"Vuosi","selection":{"filter":"item","values":["2019"]}},{"code":"Tiedot","selection":{"filter":"item","values":["keskihinta"]}}],"response":{"format":"json-stat"}}
        stat_url_asunnot_kunta = 'http://pxnet2.stat.fi/PXWeb/api/v1/fi/StatFin/asu/ashi/vv/statfin_ashi_pxt_112v.px'
        kuntatunnus = "Kunta"
        stat_new=read_json_stats(stat_url_asunnot_kunta, parameters, kuntatunnus)
        kunta_stat = kunta_stats(stat_new, muncipalities, kuntatunnus, kunta_stat)

        #from some strange reason names are not equal in both
        stat.rename(columns={'Talotyypit yhteensä Rakennusvuodet yhteensä 2019 Neliöhinta (EUR/m2)': "Talotyypit yhteensä 2019 Neliöhinta (EUR/m2)"}, inplace=True)

        if os.path.exists(path) :
            # Change the current working Directory    
            
            stat.to_csv(filename_stat, index=False, encoding="ISO-8859-1")
            kunta_stat.to_csv(filename_kunta_stat, index=False, encoding="ISO-8859-1")
    return(stat, kunta_stat)
