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
    99670 Petkula???
    00880 Laajasalo teollisuusalue
    88120 Talvivaara kaivosalue
    90620 Oulu teollisuusalue
    01740 Vantaa kauppa-alue
    33380 Pitkäniemi sairaala
    57120 Savonlinna keskussaairaala
    97145 Totonvaara palveluasumista
    96930 Napapiiri
    91670 Rokua harjoitusalue
    
    """
    selected=selected[selected['Asukkaat yhteensä, 2018 (HE)']!=0].copy()

    postcode_list = ['96320','70210','06850','01720','00290','01530','99670','00880','88120',
         '90620','01740','33380','57120','97145','96930','91670']

    selected = selected.loc[selected['Postinumero'].isin(postcode_list)==False]
    selected.reset_index(drop=True, inplace=True)
    
    return(selected)