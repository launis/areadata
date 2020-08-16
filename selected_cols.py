def selected_cols(largeset = False, parties=True):

    if largeset==True:
        numeric_features =  ['Miehet, 2018 (HE) osuudesta asukkaat',
                             'Naiset, 2018 (HE) osuudesta asukkaat',
                             'Asuntojen keskipinta-ala, 2018 (RA) osuus total',
                             'Talotyypit yhteensä 2019 Neliöhinta (EUR/m2) osuus total',
                             'Asumisväljyys, 2018 (TE) osuus total',
                             'Asukkaiden keski-ikä, 2018 (HE) osuus total',
                             'Postinumeroalueen pinta-ala osuus area_code',
                             'Perusasteen suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Ammatillisen tutkinnon suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Ylioppilastutkinnon suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Alemman korkeakoulututkinnon suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Ylemmän korkeakoulututkinnon suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Asukkaiden mediaanitulot, 2017 (HR) osuudesta asukkaat',
                             'Asukkaiden ostovoimakertymä, 2017 (HR) osuudesta asukkaat',
                             'Kerrostaloasunnot, 2018 (RA) osuudesta asukkaat',
                             'Kesämökit yhteensä, 2018 (RA) osuudesta asukkaat',
                             'Pientaloasunnot, 2018 (RA) osuudesta asukkaat',
                             'Työlliset, 2017 (PT) osuudesta asukkaat',
                             'Työttömät, 2017 (PT) osuudesta asukkaat',
                             'Opiskelijat, 2017 (PT) osuudesta asukkaat',
                             'A Maatalous, metsätalous ja kalatalous, 2017 (TP) osuudesta asukkaat',
                             'B Kaivostoiminta ja louhinta, 2017 (TP) osuudesta asukkaat',
                             'C Teollisuus, 2017 (TP) osuudesta asukkaat',
                             'D Sähkö-, kaasu- ja lämpöhuolto, jäähdytysliiketoiminta, 2017 (TP) osuudesta asukkaat',
                             'E Vesihuolto, viemäri- ja jätevesihuolto ja muu ympäristön puhtaanapito, 2017 (TP) osuudesta asukkaat',
                             'F Rakentaminen, 2017 (TP) osuudesta asukkaat',
                             'G Tukku- ja vähittäiskauppa; moottoriajoneuvojen ja moottoripyörien korjaus, 2017 (TP) osuudesta asukkaat',
                             'H Kuljetus ja varastointi, 2017 (TP) osuudesta asukkaat',
                             'I Majoitus- ja ravitsemistoiminta, 2017 (TP) osuudesta asukkaat',
                             'J Informaatio ja viestintä, 2017 (TP) osuudesta asukkaat',
                             'K Rahoitus- ja vakuutustoiminta, 2017 (TP) osuudesta asukkaat',
                             'L Kiinteistöalan toiminta, 2017 (TP) osuudesta asukkaat',
                             'M Ammatillinen, tieteellinen ja tekninen toiminta, 2017 (TP) osuudesta asukkaat',
                             'N Hallinto- ja tukipalvelutoiminta, 2017 (TP) osuudesta asukkaat',
                             'O Julkinen hallinto ja maanpuolustus; pakollinen sosiaalivakuutus, 2017 (TP) osuudesta asukkaat',
                             'P Koulutus, 2017 (TP) osuudesta asukkaat',
                             'Q Terveys- ja sosiaalipalvelut, 2017 (TP) osuudesta asukkaat',
                             'R Taiteet, viihde ja virkistys, 2017 (TP) osuudesta asukkaat',
                             'S Muu palvelutoiminta, 2017 (TP) osuudesta asukkaat',
                             'T Kotitalouksien toiminta työnantajina; kotitalouksien eriyttämätön toiminta tavaroiden ja palveluiden tuottamiseksi omaan käyttöön, 2017 (TP) osuudesta asukkaat',
                             'U Kansainvälisten organisaatioiden ja toimielinten toiminta, 2017 (TP) osuudesta asukkaat',
                             'Ravintolat osuudesta asukkaat',
                             'Myymälät osuudesta asukkaat',
                             'Nuorten yksinasuvien taloudet, 2018 (TE) osuudesta taloudet',
                             'Lapsettomat nuorten parien taloudet, 2018 (TE) osuudesta taloudet',
                             'Lapsitaloudet, 2018 (TE) osuudesta taloudet',
                             'Teini-ikäisten lasten taloudet, 2018 (TE) osuudesta taloudet',
                             'Aikuisten taloudet, 2018 (TE) osuudesta taloudet',
                             'Eläkeläisten taloudet, 2018 (TE) osuudesta taloudet',
                             'Omistusasunnoissa asuvat taloudet, 2018 (TE) osuudesta taloudet',
                             'Vuokra-asunnoissa asuvat taloudet, 2018 (TE) osuudesta taloudet',
                             'Alimpaan tuloluokkaan kuuluvat taloudet, 2017 (TR) osuudesta taloudet',
                             'Keskimmäiseen tuloluokkaan kuuluvat taloudet, 2017 (TR) osuudesta taloudet',
                             'Ylimpään tuloluokkaan kuuluvat taloudet, 2017 (TR) osuudesta taloudet',
                             '1.1.3 Kirkollisvero Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '11. Yrittäjätulot yhteensä Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.10 Muut veronalaiset sosiaalietuudet Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.6 Tapaturma- ym. muut päivärahat Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.7 Päivä- ja äitiyspäivärahat Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.8 Lapsen kotihoidon tuki Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.9 Kuntoutusraha ja -avustus Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '5.1.3 Vuokratulo Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '11.5.1.1 Asuntolainan korkomenot (TVL 58 § 2 mom.) Yhteensä Summa, euroa osuus total',
                             '14.12 Opintolainavähennys Yhteensä Summa, euroa osuus total',
                             '14.7 Kotitalousvähennys Yhteensä Summa, euroa osuus total',
                             '2. Tulot yhteensä Yhteensä Summa, euroa osuus total',
                             '1.1 Tuloverot yhteensä Yhteensä Summa, euroa osuus total',
                             '4.1.C Autoetu Yhteensä Summa, euroa osuus total',
                             '4.2 Työmatkakulujen perusteella palkkatulosta vähennettävä määrä (TVL 93 §) Yhteensä Summa, euroa osuus total',
                             '5. Pääomatulot yhteensä Yhteensä Summa, euroa osuus total']

    else:
        numeric_features = ['Miehet, 2018 (HE) osuudesta asukkaat',
                             'Naiset, 2018 (HE) osuudesta asukkaat',
                             'Asuntojen keskipinta-ala, 2018 (RA) osuus total',
                             'Talotyypit yhteensä 2019 Neliöhinta (EUR/m2) osuus total',
                             'Asumisväljyys, 2018 (TE) osuus total',
                             'Asukkaiden keski-ikä, 2018 (HE) osuus total',
                             'Postinumeroalueen pinta-ala osuus area_code',
                             'Perusasteen suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Ammatillisen tutkinnon suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Ylioppilastutkinnon suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Alemman korkeakoulututkinnon suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Ylemmän korkeakoulututkinnon suorittaneet, 2018 (KO) osuudesta asukkaat',
                             'Asukkaiden ostovoimakertymä, 2017 (HR) osuudesta asukkaat osuus total',
                             'Asunnot, 2018 (RA) osuudesta asukkaat',
                             'Kerrostaloasunnot, 2018 (RA) osuudesta asukkaat',
                             'Kesämökit yhteensä, 2018 (RA) osuudesta asukkaat',
                             'Pientaloasunnot, 2018 (RA) osuudesta asukkaat',
                             'Työlliset, 2017 (PT) osuudesta asukkaat',
                             'Työttömät, 2017 (PT) osuudesta asukkaat',
                             'Opiskelijat, 2017 (PT) osuudesta asukkaat',
                             'A Maatalous, metsätalous ja kalatalous, 2017 (TP) osuudesta asukkaat',
                             'J Informaatio ja viestintä, 2017 (TP) osuudesta asukkaat',
                             'K Rahoitus- ja vakuutustoiminta, 2017 (TP) osuudesta asukkaat',
                             'O Julkinen hallinto ja maanpuolustus; pakollinen sosiaalivakuutus, 2017 (TP) osuudesta asukkaat',
                             'P Koulutus, 2017 (TP) osuudesta asukkaat',
                             'Q Terveys- ja sosiaalipalvelut, 2017 (TP) osuudesta asukkaat',
                             'R Taiteet, viihde ja virkistys, 2017 (TP) osuudesta asukkaat',
                             'Ravintolat osuudesta asukkaat',
                             'Myymälät osuudesta asukkaat',
                             'Nuorten yksinasuvien taloudet, 2018 (TE) osuudesta taloudet',
                             'Lapsettomat nuorten parien taloudet, 2018 (TE) osuudesta taloudet',
                             'Lapsitaloudet, 2018 (TE) osuudesta taloudet',
                             'Teini-ikäisten lasten taloudet, 2018 (TE) osuudesta taloudet',
                             'Aikuisten taloudet, 2018 (TE) osuudesta taloudet',
                             'Eläkeläisten taloudet, 2018 (TE) osuudesta taloudet',
                             'Omistusasunnoissa asuvat taloudet, 2018 (TE) osuudesta taloudet',
                             'Vuokra-asunnoissa asuvat taloudet, 2018 (TE) osuudesta taloudet',
                             'Alimpaan tuloluokkaan kuuluvat taloudet, 2017 (TR) osuudesta taloudet',
                             'Keskimmäiseen tuloluokkaan kuuluvat taloudet, 2017 (TR) osuudesta taloudet',
                             'Ylimpään tuloluokkaan kuuluvat taloudet, 2017 (TR) osuudesta taloudet',
                             '1.1.3 Kirkollisvero Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '11. Yrittäjätulot yhteensä Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.6 Tapaturma- ym. muut päivärahat Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.7 Päivä- ja äitiyspäivärahat Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.8 Lapsen kotihoidon tuki Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '4.2.9 Kuntoutusraha ja -avustus Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '5.1.3 Vuokratulo Yhteensä Saajien lukumäärä osuudesta verotetut',
                             '11.5.1.1 Asuntolainan korkomenot (TVL 58 § 2 mom.) Yhteensä Summa, euroa osuus total',
                             '14.12 Opintolainavähennys Yhteensä Summa, euroa osuus total',
                             '14.7 Kotitalousvähennys Yhteensä Summa, euroa osuus total',
                             '1.1 Tuloverot yhteensä Yhteensä Summa, euroa osuus total',
                             '4.1.C Autoetu Yhteensä Summa, euroa osuus total',
                             '4.2 Työmatkakulujen perusteella palkkatulosta vähennettävä määrä (TVL 93 §) Yhteensä Summa, euroa osuus total',
                             '5. Pääomatulot yhteensä Yhteensä Summa, euroa osuus total']

    col_puolueet = ['Ääniosuus KD',
                    'Ääniosuus KESK',
                    'Ääniosuus KOK',
                    'Ääniosuus PS',
                    'Ääniosuus RKP',
                    'Ääniosuus SDP',
                    'Ääniosuus VAS',
                    'Ääniosuus VIHR',
                    'Äänestysosuus']
    
    
    categorical_features=['language_code']

    if parties:
        numeric_features = numeric_features + col_puolueet
    
    return(numeric_features, categorical_features)