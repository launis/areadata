def show_election_result(data, vaalidata, target_col_start, list_of_partiest):
    i = 0
    lask = 0
    err = 0
    enn = 0

    for t in list_of_partiest:

        laskennallinen = data[target_col_start + " " + t].sum()
        ennuste = data['Ennustettu ' + target_col_start + " " + t].sum()
        lask = lask + laskennallinen
        enn = enn + ennuste
        err = err + abs(lask-enn)
    
        aitotulos = vaalidata[vaalidata['Puolueen nimilyhenne suomeksi']==t].sum()[target_col_start]
        print(t, ' lasketut äänet: Aitotulos ', round(aitotulos), 'Laskennallinen ', round(laskennallinen), 'Ennuste ', round(ennuste))
        print('Laskennallisen virhe aitoon tulokseen', round(100*(aitotulos - laskennallinen)/aitotulos,3),'%')
        print('Ennusteen virhe aitoon tulokseen', round(100*(aitotulos - ennuste)/aitotulos,3),'%')
        print('Ennusteen virhe laskennalliseen tulokseen', round(100*(laskennallinen - ennuste)/laskennallinen,3),'%')
        print()
        i = i+1
    
    print('Lasketut äänet:Laskennallinen ', round(lask), 'Ennuste ', round(enn), 'Err ', round(err))