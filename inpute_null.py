
def inpute_null(stat, kunta_stat, col_list_sama_arvo, col_list_osuuus):
    """
    inpute null sets values for NA & 0 of postcodes based on the values
    of muncipalities

    args:
        stat : postocode level values
        kunta_stat : muncipality values
        col_list_sama_arvo: set same value as in muncipality level
        col_list_osuuus: set same share as in muncipality level

    Returns:
         kiintosuus
         
    """
    

    def anna_kunta_na_arvo_postinumerolle(col_list_sama_arvo, kunta_stat, stat):
    
        key = 'muncipality_code'
    
        def add_values(element):
        
            if len(kunta_stat[kunta_stat[key]==element[0]]) == 1:
                return(kunta_stat[kunta_stat[key]==element[0]][col].item())
            else:
                return(0)
        
        for col in col_list_sama_arvo:
            stat[col].fillna(stat[[key, col]].apply(add_values, axis=1), inplace=True)
            stat[col].fillna(0, inplace=True)
        return(stat)


    def anna_kunta_nolla_arvo_postinumerolle(col_list_osuuus, kunta_stat, stat, col_tot):
    
        def add_values(element):
            key = 'muncipality_code'
            if len(kunta_stat[kunta_stat[key]==element[0]]) == 1:
                kunta_arvot = kunta_stat[kunta_stat[key]==element[0]][col].item()
                kaikki_kunta = kunta_stat[kunta_stat[key]==element[0]][col_tot].item()
                osuus =  kunta_arvot / kaikki_kunta
                return(osuus * element[2])
            else:
                return(0)
        key = 'muncipality_code'    
        for col in col_list_osuuus:
            stat.loc[stat[col]==0,col] = stat[[key, col, col_tot]].apply(add_values, axis=1) 
            stat[col] = stat[col].astype(int)
                
        return(stat)

    #col_list_sama_arvo  = ['Talotyypit yhteensä 2019 Neliöhinta (EUR/m2)', 'Asumisväljyys, 2018 (TE)', 'Asuntojen keskipinta-ala, 2018 (RA)']

    stat=anna_kunta_na_arvo_postinumerolle(col_list_sama_arvo, kunta_stat, stat)

    #col_list_osuuus  = ['Miehet, 2018 (HE)', 'Naiset, 2018 (HE)', 'Taloudet yhteensä, 2018 (TE)']
    col_tot = 'Asukkaat yhteensä, 2018 (HE)'
    stat=anna_kunta_nolla_arvo_postinumerolle(col_list_osuuus, kunta_stat, stat, col_tot)

    return(stat)