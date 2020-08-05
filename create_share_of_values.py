def create_share_of_values(stat):
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
        
    start = stat.columns.get_loc(stat.columns[1])          
    end = stat.columns.get_loc('1. Verotuspäätöksen saajien lukumäärä Yhteensä Saajien lukumäärä')
    col_list_stat = stat.iloc[:,start:end].columns.to_list()

    col_list_rav = ['Ravintolat','Myymälät']
    col_list_stat = col_list_stat + col_list_rav

    matchers = ['taloudet', 'pinta-ala', 'koordinaatti', 'Asukkaat yhteensä', 'Taloudet yhteensä', 'tuloluokkaan','Talouksien keskikoko', 'keski-ikä']
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
                'Talotyypit yhteensä 2019 Neliöhinta (EUR/m2)', 
                'Asumisväljyys, 2018 (TE)', 'Asukkaiden keski-ikä, 2018 (HE)']    

    col_list_share = col_list_share  + col_list_add

    for col in stat[col_list_share]:
        target_col = col + " osuus " + group_column
        stat[target_col] = stat[col] / stat[col].mean()
        stat[target_col].replace([np.inf, -np.inf], np.nan, inplace=True)
        stat[target_col].fillna(0, inplace=True)

    for col in stat[col_list_tax_euros]:
        target_col = col + " osuus " + group_column
        stat[target_col] = (stat[col] / stat['1. Verotuspäätöksen saajien lukumäärä Yhteensä Saajien lukumäärä']) / (stat[col].mean() / stat['1. Verotuspäätöksen saajien lukumäärä Yhteensä Saajien lukumäärä'].mean())
        stat[target_col].replace([np.inf, -np.inf], np.nan, inplace=True)
        stat[target_col].fillna(0, inplace=True)
    middle_column2=middle_column + " osuus " + group_column
    
    stat.drop(middle_column, axis=1, inplace=True)
    stat.drop(middle_column2, axis=1, inplace=True)
    
    return(stat)