def read_and_merge_all(path):
    """This function reads all needed data and stores them to datafraeme
       either from file or calls a function to fetch data
       via API calls directly from sources and then writes data to files

    Args:
        path: path, where the data is stored
    Returns:
        stat: statics by postcode
        kunta_stat:statistics by muncipality

    """


    import pandas as pd
    from read_post_muncipalities import read_post 
    from read_stats_postcode import kunta_stats, pnro_stats, read_json_stats    
    from read_ravintolat_ja_kaupat import ravintolat_ja_kaupat    
    from read_kiinteisto import kiinteisto
    from read_vaalit import kiinteisto_alueiksi, aaniosuudet
    
    from supportfunctions import add_zeros_muncipality
    import geopandas as gp

    #1 post & muncipalities
    
    #reads all needed direct postcode data either from file or calls a function to fetch data via API calls 
    #https://www.stat.fi/static/media/uploads/org/avoindata/kartta-aineistojen_lataus_url-osoitteen_kautta_ohje.pdf
    #http://www.posti.fi/liitteet-yrityksille/ehdot/postinumeropalvelut-palvelukuvaus-ja-kayttoehdot.pdf
    url_geometry = "http://geo.stat.fi/geoserver/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=postialue:pno_tilasto&outputFormat=SHAPE-ZIP"    
    post = read_post(url_geometry)
    #post = gp.GeoDataFrame(post, geometry='geometry')
    #create list of muncipalities from the reacent postcode data
    muncipalities = post.groupby(['muncipality_code', 'muncipality_name'],as_index=False ).mean()[['muncipality_code', 'muncipality_name']][['muncipality_code', 'muncipality_name']]
            
    #make postcodes to lists
    postcode_list = post['postcode'].tolist() 
    #make muncipalities to lists and add zeros to muncipality_code
    muncipality_list = muncipalities['muncipality_code'].apply(add_zeros_muncipality).to_list()


    #2 tilastokeskus, vero statistics
    #reads all needed postcode related statistical data either from file or calls a function to fetch data via API calls 

    #http://pxnet2.stat.fi/PXWeb/pxweb/fi/Postinumeroalueittainen_avoin_tieto/Postinumeroalueittainen_avoin_tieto__2020/paavo_pxt_12f7.px/
    #http://pxnet2.stat.fi/PXWeb/pxweb/fi/Postinumeroalueittainen_avoin_tieto/Postinumeroalueittainen_avoin_tieto__2020/paavo_pxt_12f8.px/
    #https://pxnet2.stat.fi/PXWeb/pxweb/fi/Kuntien_avainluvut/Kuntien_avainluvut__2020/kuntien_avainluvut_2020_viimeisin.px/?rxid=444223df-f91c-4479-891f-5dcd50b983d2
    #http://vero2.stat.fi/PXWeb/pxweb/fi/Vero/Vero__Henkiloasiakkaiden_tuloverot__lopulliset__postinum/postinum_104.px/
    #http://vero2.stat.fi/PXWeb/pxweb/fi/Vero/Vero__Henkiloasiakkaiden_tuloverot__lopulliset__postinum/postinum_101.px/
    #http://pxnet2.stat.fi/PXWeb/pxweb/fi/StatFin/StatFin__asu__ashi__vv/statfin_ashi_pxt_112q.px/
    #http://pxnet2.stat.fi/PXWeb/pxweb/fi/StatFin/StatFin__asu__ashi__vv/statfin_ashi_pxt_112v.px/

    stat_url = "http://pxnet2.stat.fi/PXWeb/api/v1/fi/Postinumeroalueittainen_avoin_tieto/2020/paavo_pxt_12f7.px"
    stat_url_kunta = "http://pxnet2.stat.fi/PXWeb/api/v1/fi/Postinumeroalueittainen_avoin_tieto/2020/paavo_pxt_12f8.px" 
  
    data_list_post1=["euref_x","euref_y", "pinta_ala","he_vakiy","he_miehet","he_naiset","he_kika",
                     "he_0_2","he_3_6","he_7_12","he_13_15","he_16_17","he_18_19","he_20_24","he_25_29",
                     "he_30_34","he_35_39","he_40_44","he_45_49","he_50_54","he_55_59","he_60_64","he_65_69",
                     "he_70_74","he_75_79","he_80_84","he_85_","ko_ika18y","ko_perus","ko_koul","ko_yliop",
                     "ko_ammat","ko_al_kork","ko_yl_kork"]

    data_list_post2=["hr_ktu","hr_mtu","hr_pi_tul","hr_ke_tul","hr_hy_tul","hr_ovy","te_taly","te_takk",
                     "te_as_valj","te_nuor","te_eil_np","te_laps","te_plap","te_aklap","te_klap","te_teini",
                     "te_aik","te_elak","te_omis_as","te_vuok_as","te_muu_as","tr_ktu","tr_mtu",
                     "tr_pi_tul","tr_ke_tul","tr_hy_tul","tr_ovy","ra_ke","ra_raky","ra_muut","ra_asrak",
                     "ra_asunn","ra_as_kpa","ra_pt_as","ra_kt_as"]

    data_list_post3=["tp_tyopy","tp_alku_a","tp_jalo_bf","tp_palv_gu","tp_a_maat","tp_b_kaiv","tp_c_teol",
                    "tp_d_ener","tp_e_vesi","tp_f_rake","tp_g_kaup","tp_h_kulj","tp_i_majo","tp_j_info",
                    "tp_k_raho","tp_l_kiin","tp_m_erik","tp_n_hall","tp_o_julk","tp_p_koul","tp_q_terv",
                    "tp_r_taid","tp_s_muup","tp_t_koti","tp_u_kans","tp_x_tunt","pt_vakiy","pt_tyoll",
                    "pt_tyott","pt_0_14","pt_opisk","pt_elakel","pt_muut"]
    

    data_list_posts=[data_list_post1, data_list_post2, data_list_post3]

    stat_url_kuntatiedot = 'https://pxnet2.stat.fi:443/PXWeb/api/v1/fi/Kuntien_avainluvut/2020/kuntien_avainluvut_2020_viimeisin.px'
    data_list_muncipality=["M408","M476","M404","M410","M297"]

    stat_url_vero = "http://vero2.stat.fi/PXWeb/api/v1/fi/Vero/Henkiloasiakkaiden_tuloverot/lopulliset/postinum/postinum_104.px"
    stat_url_vero_kunta = 'http://vero2.stat.fi/PXWeb/api/v1/fi/Vero/Henkiloasiakkaiden_tuloverot/lopulliset/alue/alue_104.px'
    data_list_vero = ["HVT_TULOT_10", "HVT_TULOT_50","HVT_TULOT_80","HVT_TULOT_220","HVT_TULOT_370","HVT_TULOT_410","HVT_TULOT_420","HVT_TULOT_430","HVT_TULOT_440","HVT_TULOT_450","HVT_TULOT_590","HVT_TULOT_630","HVT_TULOT_1330","HVT_TULOT_1080","HVT_VEROT_90","HVT_VAHENNYKSET_40","HVT_VAHENNYKSET_60","HVT_VAHENNYKSET_740","HVT_VAHENNYKSET_1080","HVT_VAHENNYKSET_1400","HVT_VEROT_20"]

    stat_url_asunnot = "http://pxnet2.stat.fi/PXWeb/api/v1/fi/StatFin/asu/ashi/vv/statfin_ashi_pxt_112q.px"
    stat_url_asunnot_kunta = 'http://pxnet2.stat.fi/PXWeb/api/v1/fi/StatFin/asu/ashi/vv/statfin_ashi_pxt_112v.px'

       
    postinumero = "Postinumeroalue"

    stat = pd.DataFrame()
    for values in data_list_posts:  
        parameters = {"query":[{"code":"Postinumeroalue","selection":
                               {"filter":"item","values":postcode_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":values}}],
                      "response":{"format":"json-stat"}}    
        
        stat_new=read_json_stats(stat_url, parameters, postinumero)
        stat=pnro_stats(stat_new, postinumero, stat)

        
    #kuntadata demands in this case ku to the front
    string = 'KU'
    kuntatunnus = "Alue"
    new_muncipality_list = [string + x for x in muncipality_list]
    kunta_stat = pd.DataFrame()
    for values in data_list_posts: 
        parameters = {"query":[{"code":"Alue","selection":{"filter":"item","values":new_muncipality_list}},
                               {"code":"Tiedot","selection":{"filter":"item","values":values}}],
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
    
    
    #3 alco data
    #reads all needed license data to sell alcohol in pubs and shops data either from file or calls a function to fetch data via API calls 

    #https://www.avoindata.fi/data/fi/dataset/alkoholielinkeinorekisteri
 
    url_ravintolat = "http://avoindata.valvira.fi/alkoholi/alkoholilupa_toimipaikkatiedot_ABC.csv"

    ravintolat= ravintolat_ja_kaupat(url_ravintolat, post)
    
    
    #4 address register
    #
    # NOTE the value of url_kiinteisto changes regurally, couple of times per year
    #
    #reads all needed addres register related statistical data either from file or calls a function to fetch data via API calls 
    #https://www.avoindata.fi/data/dataset/cf9208dc-63a9-44a2-9312-bbd2c3952596/resource/ae13f168-e835-4412-8661-355ea6c4c468

    url_kiinteisto = "https://www.avoindata.fi/data/dataset/cf9208dc-63a9-44a2-9312-bbd2c3952596/resource/ae13f168-e835-4412-8661-355ea6c4c468/download/suomi_osoitteet_2020-08-14.7z"
    kiinteisto = kiinteisto(url_kiinteisto)

    
    #5 voting data 
    #reads all needed voting data either from file or calls a function to fetch data via API calls

    #https://tulospalvelu.vaalit.fi/EKV-2019/fi/ladattavat_tiedostot.html
    #https://tulospalvelu.vaalit.fi/EKV-2019/ohje/Vaalien_tulostiedostojen_kuvaus_EKV-EPV-2019_FI.pdf​    ​

    url_puolueet = "https://tulospalvelu.vaalit.fi/EKV-2019/ekv-2019_puo_maa.csv.zip"
    url_alueet = 'https://tulospalvelu.vaalit.fi/EKV-2019/ekv-2019_alu_maa.csv.zip'
    kiint = kiinteisto_alueiksi(kiinteisto)
    osuudet, vaalidata = aaniosuudet(kiint, post, url_puolueet, url_alueet)

    
    #Next all data will be merged
    
    stat = pd.merge(stat, osuudet, how='inner', on='Postinumero',
         left_index=False, right_index=False,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

    stat = pd.merge(stat, post, how='inner', left_on = 'Postinumero',right_on='postcode',
         left_index=False, right_index=False,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

    stat = pd.merge(stat, ravintolat, how='left', on='Postinumero',
         left_index=False, right_index=False,
         suffixes=('_x', '_y'), copy=True, indicator=False,
         validate=None)

    areas=vaalidata.groupby(['Kuntanumero','Vaalipiirinumero'],as_index=False ).mean()[['Kuntanumero','Vaalipiirinumero']][['Kuntanumero','Vaalipiirinumero']]

    stat = pd.merge(left=stat, right=areas, left_on='muncipality_code', right_on = 'Kuntanumero')
    stat.drop(['Kuntanumero'], axis=1, inplace=True)

    post = pd.merge(left=post, right=areas, left_on='muncipality_code', right_on = 'Kuntanumero')
    post.drop(['Kuntanumero'], axis=1, inplace=True)
    stat.drop(['postcode'], axis=1, inplace=True)
    return(stat, post, kunta_stat, vaalidata)    
    
