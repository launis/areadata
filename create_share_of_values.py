def create_share_of_values(stat, pnroalue = True):
    """
    make share of valus both for  households
    and residents

    args:
        stat : postocode level values
  

    Returns:
         stat
         
    """
    import numpy as np
    from OrderedSet import OrderedSet
        

    #postinumeroalueen pinta-ala suhteessa alueeseen
    if pnroalue:
        group_column = 'area_code'
        col_list = ['Postinumeroalueen pinta-ala', 'etaisyys']
        compare = 'mean'
        
        for col in stat[col_list]:
            target_col = col + " osuus " + group_column
            stat[target_col] = stat[col] / stat.groupby(group_column)[col].transform(compare)
            stat[target_col].replace([np.inf, -np.inf], np.nan, inplace=True)
            stat[target_col].fillna(0, inplace=True)

    
    start = stat.columns.get_loc(stat.columns[1])          
    end = stat.columns.get_loc('1. Verotuspäätöksen saajien lukumäärä Yhteensä Saajien lukumäärä')
    col_list_stat = stat.iloc[:,start:end].columns.to_list()
    if pnroalue:
        col_list_others = ['Ravintolat','Myymälät', 'Kuntien välinen muuttovoitto/-tappio, henkilöä, 2019']
    else:
        col_list_others = ['Kuntien välinen muuttovoitto/-tappio, henkilöä, 2019']
    col_list_stat = col_list_stat + col_list_others

    matchers = ['taloudet', 'pinta-ala', 'koordinaatti', 'Asukkaat yhteensä', 'Taloudet yhteensä', 'tuloluokkaan','Talouksien keskikoko', 'keski-ikä', 'muncipality']
    not_matching = [s for s in col_list_stat if any(xs in s for xs in matchers)]
    col_list_stat_asukkaat = list(OrderedSet(col_list_stat) - OrderedSet(not_matching))

    matchers = ['taloudet']
    col_list_stat_talous = [s for s in col_list_stat if any(xs in s for xs in matchers)]

    start = stat.columns.get_loc('1. Verotuspäätöksen saajien lukumäärä Yhteensä Saajien lukumäärä')
    end = stat.columns.get_loc('Talotyypit yhteensä 2019 Neliöhinta (EUR/m2)')
    col_list_tax = stat.iloc[:,start:end].columns.to_list()
    matchers = ['Saajien lukumäärä']
    col_list_tax_persons = [s for s in col_list_tax if any(xs in s for xs in matchers)]

    matchers = ['Summa, euroa']
    col_list_tax_euros = [s for s in col_list_tax if any(xs in s for xs in matchers)]

    share_word = " osuudesta "

    sum_column = 'Asukkaat yhteensä, 2018 (HE)'
    for col in stat[col_list_stat_asukkaat]:
        target_col = col + share_word + 'asukkaat'
        stat[target_col] = 0
        stat.loc[stat[sum_column]>0, target_col] = stat[col] / stat[sum_column]
        stat[target_col].fillna(0, inplace=True)
    first_column = stat.columns[1] + share_word + 'asukkaat'

    sum_column = 'Taloudet yhteensä, 2018 (TE)'
    for col in stat[col_list_stat_talous]:
        target_col = col + share_word + 'taloudet'
        stat[target_col] = 0
        stat.loc[stat[sum_column]>0, target_col] = stat[col] / stat[sum_column]
        stat[target_col].fillna(0, inplace=True)

    sum_column = '1. Verotuspäätöksen saajien lukumäärä Yhteensä Saajien lukumäärä'
    for col in stat[col_list_tax_persons]:
        target_col = col + share_word + 'verotetut'
        stat[target_col] = 0
        stat.loc[stat[sum_column]>0, target_col] = stat[col] / stat[sum_column]
        stat[target_col].fillna(0, inplace=True)
    middle_column = sum_column+ share_word + 'verotetut'   
    
    start = stat.columns.get_loc(first_column)
    end = stat.columns.get_loc(stat.columns[-1])          
    col_list_share = stat.iloc[:,start:end+1].columns.to_list()
    group_column = 'total'

    col_list_add = ['Asuntojen keskipinta-ala, 2018 (RA)', 
                    'Talouksien keskikoko, 2018 (TE)',
                    'Asukkaiden keskitulot, 2017 (HR)',
                    'Asukkaiden mediaanitulot, 2017 (HR)',
                    'Asukkaiden ostovoimakertymä, 2017 (HR)',
                    'Talouksien keskitulot, 2017 (TR)',
                    'Talouksien mediaanitulot, 2017 (TR)',
                    'Talouksien ostovoimakertymä, 2017 (TR)',
                    'Talotyypit yhteensä 2019 Neliöhinta (EUR/m2)', 
                    'Asumisväljyys, 2018 (TE)',
                    'Asukkaiden keski-ikä, 2018 (HE)']    


    col_list_share = col_list_share  + col_list_add

    for col in stat[col_list_share]:
        
        if stat[col].dtype != object: #'Suurin puolue lisätään myöhemmin ja se on tekstiä, joten kun tätä käyteään muualla
            target_col = col + " osuus " + group_column
            stat[target_col] = stat[col] / stat[col].mean()
            stat[target_col].replace([np.inf, -np.inf], np.nan, inplace=True)
            stat[target_col].fillna(0, inplace=True)
            
    for col in stat[col_list_tax_euros]:
        if stat[col].dtype != object:
            target_col = col + " osuus " + group_column
            stat[target_col] = (stat[col] / stat['1. Verotuspäätöksen saajien lukumäärä Yhteensä Saajien lukumäärä']) / (stat[col].mean() / stat['1. Verotuspäätöksen saajien lukumäärä Yhteensä Saajien lukumäärä'].mean())
            stat[target_col].replace([np.inf, -np.inf], np.nan, inplace=True)
            stat[target_col].fillna(0, inplace=True)
    middle_column2=middle_column + " osuus " + group_column
    
    stat.drop(middle_column, axis=1, inplace=True)
    stat.drop(middle_column2, axis=1, inplace=True)
    if not pnroalue:
        matchers = ['Liikennekäytössä']
        matching = [s for s in stat.columns if any(xs in s for xs in matchers)]
        share_word = " osuudesta "
        sum_column = 'Asukkaat yhteensä, 2018 (HE)'
        for col in matching:
            target_col = col + share_word + 'asukkaat'
            stat[target_col] = 0
            stat.loc[stat[sum_column]>0, target_col] = stat[col] / stat[sum_column]
            stat[target_col].fillna(0, inplace=True)
    
    return(stat)