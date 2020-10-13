def delete_outliers(selected):
    """
    

    Parameters
    ----------
    selected : dataframe

    Returns
    -------
    None.

    96320 Rovaniemi teollisuusalue
    70210 Kuopio sairala-alue
    06850 Neste Kulloo terminaali
    01720 Petikko suuri kauppa-alue
    00290 Meilahden sairaala-alue
    01530 Helsinki-Vantaa lentoasema
    99670 Kevitsan kaivos
    00880 Laajasalo teollisuusalue
    10350 Meltolan sairaala-alue
    88120 Talvivaara kaivosalue
    90620 Oulu teollisuusalue
    01740 Vantaa kauppa-alue
    33380 Pitkäniemi sairaala
    57120 Savonlinna keskussaairaala
    97145 Totonvaara palveluasumista
    96930 Napapiiri
    91670 Rokua harjoitusalue
    45750 Kuusankosken Sairaala-alue
    42720 Keuruun entisen varuskunnan alue
    08360 Kisakallio
    13530 Hämeenlinna sairaala-alue	
    80210 Sairaala-alue	Joensuu
    
    """
    
    #20 is the limit of people living
    selected=selected[selected['Asukkaat yhteensä, 2018 (HE)']>19].copy()

    postcode_list = ['96320','70210','10350', '06850','01720','00290','01530','99670', '80210', '00880','88120',
         '90620','01740','33380','57120','97145','96930','91670', '45750', '42720', '08360', '13530']

    selected = selected.loc[selected['Postinumero'].isin(postcode_list)==False]
    selected.reset_index(drop=True, inplace=True)
    
    return(selected)