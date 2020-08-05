def reset_party_number(data):
    """
    reset party number depending on the largest party
    party numbers change during the use of models
    there can be lesser parties so the partynumbers do not 
    stay correct

    args:
        data : database

    returns:
        data: data with new correct values and colors
        class_names: party names used in this time
    """

    party=data.groupby('Suurin_puolue',as_index=False ).mean()[['Suurin_puolue', 'Suurin_puolue numero','Suurin_puolue numero uusi numero']]
    party.loc[:,'Suurin_puolue numero uusi numero'] = party['Suurin_puolue numero uusi numero'].astype(int) 
    party.sort_values('Suurin_puolue numero uusi numero').reset_index(drop=True, inplace=True)
    class_names = party['Suurin_puolue'].to_list()

    def get_puolue_nimi(data):
        val = party[party['Suurin_puolue numero uusi numero']==data]['Suurin_puolue'].unique().item()
        return (val)

    def get_puolue_numero(data):
        val = party[party['Suurin_puolue numero uusi numero']==data]['Suurin_puolue numero'].unique().item()
        return (val)

    data.loc[:, 'Ennustettu_Suurin_puolue nimi']= data['Ennustettu_Suurin_puolue numero uusi numero'].apply(get_puolue_nimi)
    data.loc[:, 'Ennustettu_Suurin_puolue numero']= data['Ennustettu_Suurin_puolue numero uusi numero'].apply(get_puolue_numero)
    puoluevari =  {'KD' : 'deepskyblue', 'KESK': 'darkgreen', 'KOK': 'blue', 'PS' : 'gold', 'RKP' : 'yellow', 'SDP' : 'pink', 'VAS' : 'red', 'VIHR': 'green'}
    data['Ennustettu_puoluevari'] =  data['Ennustettu_Suurin_puolue nimi'].map(puoluevari)
    return(data, class_names)