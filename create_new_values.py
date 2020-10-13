def create_new_values(stat, vaalidata):
    """
    inpute null sets values for NA & 0 of postcodes based on the values
    of muncipalities

    args:
        stat : postocode level values
  

    Returns:
         stat
         
    """
        
    target = 'Keskitulot'
    summa  = '2. Tulot yhteensä Yhteensä Summa, euroa'
    maara = '2. Tulot yhteensä Yhteensä Saajien lukumäärä'
    stat[target] = 0
    stat.loc[stat[maara]>0, target] = stat[summa]/stat[maara]

    target = 'Keskiverot'
    summa  = '1.1 Tuloverot yhteensä Yhteensä Summa, euroa'
    maara = '1.1 Tuloverot yhteensä Yhteensä Saajien lukumäärä'
    stat[target] = 0
    stat.loc[stat[maara]>0, target] = stat[summa]/stat[maara]

    target = 'Verojen osuus'
    summa  = 'Keskiverot'
    maara = 'Keskitulot'
    stat[target] = 0
    stat.loc[stat[maara]>0, target] = stat[summa]/stat[maara]
    
    target = 'Vähenykset suhteessa tulot yhteensä'
    summa  = '4. Ansiotuloista tehtävät luonnolliset vähennykset eli tulonhankkimiskulut yhteensä Yhteensä Summa, euroa'
    maara = '2. Tulot yhteensä Yhteensä Summa, euroa'
    stat[target] = 0
    stat.loc[stat[maara]>0, target] = stat[summa]/stat[maara]

    target = 'Pääomatulojen osuus'
    summa  = '5. Pääomatulot yhteensä Yhteensä Summa, euroa'
    maara = '2. Tulot yhteensä Yhteensä Summa, euroa'
    stat[target] = 0
    stat.loc[stat[maara]>0, target] = stat[summa]/stat[maara]

    target = 'Verojen osuus'
    summa  = '1.1 Tuloverot yhteensä Yhteensä Summa, euroa'
    maara = '2. Tulot yhteensä Yhteensä Summa, euroa'
    stat[target] = 0
    stat.loc[stat[maara]>0, target] = stat[summa]/stat[maara]


    target = 'Asuntolainan korkomenot vs tulot yhteensä'
    summa  = '11.5.1.1 Asuntolainan korkomenot (TVL 58 § 2 mom.) Yhteensä Summa, euroa'
    maara = '2. Tulot yhteensä Yhteensä Summa, euroa'
    stat[target] = 0
    stat.loc[stat[maara]>0, target] = stat[summa]/stat[maara]


    target = 'Asumistiheys'
    summa  = 'Asukkaat yhteensä, 2018 (HE)'
    maara = 'Postinumeroalueen pinta-ala'
    stat[target] = 0
    stat.loc[stat[maara]>0, target] = 100000 * stat[summa]/stat[maara]

    
    for puolue in vaalidata['Puolueen nimilyhenne suomeksi'].unique():
        lkm = "Äänet yhteensä lkm " + puolue
        osuus = "Ääniosuus " + puolue
        stat.loc[:,osuus] = stat[lkm]/stat.groupby(['Postinumero'])['Äänet yhteensä lkm Äänet'].transform(sum)    

    for puolue in vaalidata['Puolueen nimilyhenne suomeksi'].unique():
        lkm = "Vaalipäivän äänet lkm " + puolue
        osuus = "Ääniosuus Vaalipäivän äänet " + puolue
        stat.loc[:,osuus] = stat[lkm]/stat.groupby(['Postinumero'])['Vaalipäivän äänet lkm Äänet'].transform(sum)    

    for puolue in vaalidata['Puolueen nimilyhenne suomeksi'].unique():
        lkm = "Ennakkoäänet lkm " + puolue
        osuus = "Ääniosuus Ennakkoäänet " + puolue
        stat.loc[:,osuus] = stat[lkm]/stat.groupby(['Postinumero'])['Ennakkoäänet lkm Äänet'].transform(sum)    

    #haetaan suurimman puolueen asema
    aaniosuudet = stat.columns[stat.columns.str.startswith('Ääniosuus')].to_list()
    for i in [s for s in aaniosuudet if s.startswith('Ääniosuus Ennakkoäänet')]:
        aaniosuudet.remove(i)
    for i in [s for s in aaniosuudet if s.startswith('Ääniosuus Vaalipäivän äänet')]:
        aaniosuudet.remove(i)
        
    aaniosuudet.remove('Ääniosuus Hyväksytyt')
    aaniosuudet.remove('Ääniosuus Mitättömät')
    aaniosuudet.remove('Ääniosuus Äänioikeutetut yhteensä')
    aaniosuudet.remove('Ääniosuus Äänet') 
    
    stat.loc[:,'Ääniosuus Äänioikeutetut yhteensä'] = 1/stat['Ääniosuus Äänioikeutetut yhteensä']
    
    aaniosuudet = ['Ääniosuus KD', 'Ääniosuus KESK', 'Ääniosuus KOK', 'Ääniosuus RKP', 'Ääniosuus SDP', 'Ääniosuus VAS', 'Ääniosuus PS', 'Ääniosuus VIHR']

    stat.loc[:,'Suurin_puolue'] = stat[aaniosuudet].idxmax(axis=1).str.split(' ', 1, expand=True)[1]
    stat.loc[:,'Suurin_puolue numero'] = stat['Suurin_puolue'].astype('category').cat.codes
    #ahvenanmaa RKP:lle
    if len(stat[stat['area_code']=='FI200']) > 0:
        stat.loc[stat['area_code']=='FI200','Suurin_puolue numero'] = stat[stat['Suurin_puolue']=='RKP']['Suurin_puolue numero'].unique()[0]
        stat.loc[stat['area_code']=='FI200','Suurin_puolue']='RKP'   
    stat['Äänestysosuus'] =stat['Äänet yhteensä lkm Äänet']/stat['Äänet yhteensä lkm Äänioikeutetut yhteensä']
    return(stat)
