def show_election_result(data, y, target_col_start, vaalidata, list_of_parties):
    
    from sklearn.metrics import mean_squared_error
    from math import sqrt

    from create_target_columns import create_target_columns
    target = create_target_columns(list_of_parties, target_col_start)
    
    if target_col_start == 'Ääniosuus ':
        for t in target:
            data.loc[:,"Ennustettu "+ t] = y[t] * data['Äänet yhteensä lkm Äänet']

    if target_col_start == 'Äänet yhteensä lkm ':    
        for t in target:
            data.loc[:,"Ennustettu "+ t] = y[t]

    estimated_col_start = 'Ennustettu ' + target_col_start
    ennustettu = create_target_columns(list_of_parties, estimated_col_start)
    data.loc[:,'Ennustettu Suurin_puolue'] = data[ennustettu].idxmax(axis=1).str.split(' ', 3, expand=True)[2]
    data.loc[:,'Ennustettu Suurin_puolue numero'] = data['Ennustettu Suurin_puolue'].astype('category').cat.codes


    i = 0
    lask = []
    ait = []
    enn = []



    vaalidata=vaalidata[vaalidata['Kuntanumero'].isin(list(data['muncipality_code'].unique()))].copy()
    for t in list_of_parties:

        laskennallinen = data['Äänet yhteensä lkm ' + t].sum()
        ennuste = data['Ennustettu ' + target_col_start + t].sum()
        aitotulos = vaalidata[vaalidata['Puolueen nimilyhenne suomeksi']==t]['Äänet yhteensä lkm'].sum()
        lask.append(laskennallinen)
        enn.append(ennuste)
        ait.append(aitotulos)
        print(t, ' lasketut äänet: Aitotulos ', round(aitotulos), 'Laskennallinen ', round(laskennallinen), 'Ennuste ', round(ennuste))
        print('Laskennallisen virhe aitoon tulokseen', round(100*(aitotulos - laskennallinen)/aitotulos,3),'%')
        print('Ennusteen virhe aitoon tulokseen', round(100*(aitotulos - ennuste)/aitotulos,3),'%')
        print('Ennusteen virhe laskennalliseen tulokseen', round(100*(laskennallinen - ennuste)/laskennallinen,3),'%')
        print('Laskennallinen ääniosuus', round(100*ennuste/data['Äänet yhteensä lkm Äänet'].sum(),3),'%')
        print('Aito ääniosuus', round(100*vaalidata[vaalidata['Puolueen nimilyhenne suomeksi']==t]['Äänet yhteensä lkm'].sum()/vaalidata[vaalidata['Puolueen nimilyhenne suomeksi']=='Äänet']['Äänet yhteensä lkm'].sum(),3),'%')
        print()
        i = i+1
    rms_lask = sqrt(mean_squared_error(ait, lask))
    rms_enn = sqrt(mean_squared_error(lask, enn))
    print('Varianssi: Aito', round(rms_lask), 'Ennuste ', round(rms_enn))
    
    return(data)