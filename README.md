Suomi on jakautunut erilaisiin alueisiin.

Katso tulokset https://www.launis.net/blank

Tavanomaisten (sklearn, tensorflow) modulien lisäksi ainakin seuraavia moduuleja pitää olla ladattuna

pyjstat https://pypi.org/project/pyjstat/
shap https://pypi.org/search/?q=shap


Erllisten moduulien vaatimuksia:
Jos haluaa käyttää create_mlxtend -moduulia, tarvitaan  http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/
Tai jos haluaa kokeilla automated_outlier_detection modulia, tarvitaan https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.knn
jos haluaa kokeilla mrmr moduulia, tarvitaan https://pypi.org/project/pymrmr/ (tämä moduuli ei näytä olevan kovin ylläpidetty)

Lataamalla kaikkin nämä tiedostot areadata hakemistoon ja käynnistämällä esimerkiksi create_clusters_kmeans tai create_political_xgboost notebookin, homma alkaa pyörimään. Notebookit tekevät tällä samalla datalla erityyppisiä päätelmiä. Toisaalta create_clusters_gaussian ja create_clusters_kmeans tarjoavat luokittelua samasta datasta mutta eri menetelmillä.

Teknisesti data-analyysi on toteutettu lukemalla rajapintojen kautta tietoja suoraan dataframeille. Tässä ei tallenneta erikseen CSV-tiedostoja, vaan kaikki datat luetaan suoraan lähteiden kautta.  Kokonaisuus lähtee liikkeelle ilman väliaikaistiedostoja, mutta tallentaa ne lukemisen myötä väliaikaisteidostoiksi. Koska tiedostojen lukeminen on aika hidasta, oli pakko toteuttaa tiedostojen tukemaa tekemistä. Nämä olisi tietty hyvä tallentaa SQL kantaan. Tallennan tiedostoihin myös mallit sekä Shap mallin tuottamat arvot. Eka ajo saattaa kestää todella pitkään.

Kun tiedot on luettu sisään, ne käsitellään ja nolla-arvoille sekä NA arvoille haetaan uusia lukuja tai nämä rivit poistetaan kokonaan. Pienemmisä postinumeroissa on paljon nolla-arvoja. Osa niistä voi olla aivan aitoja nolla-arvoja ja osa taasen laitettu nolliksi yksityisyyen suojan takia. Klusterien hakemiseen tällä kertaa käytettiin yleistä k-means optimoitimenetelmää ja normaalijakaumiin perustuvaa gaussian algoritmiä.

Klusterien hyvyyttä on vaikea piirtää auki matriisiin, jos selittävä ominaisuusjoukko on yli kolmen. Kuvaaamista varten pääkomponenttianalyysi helpottaa taasen tätä työtä. Tässä yhteydessä kokeiltiin myös erilaisten dimenssioiden vähentäviä työkaluja, kuten Principal feature analysis https://www.hindawi.com/journals/cmmm/2013/645921/ , SequentialFeatureSelector, http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/ . Samoin Minimum Redundancy Maximum Relevance feature selection toiminnallisuutta kokeiltiin. Useat näistä menetelmistä olivat laskennallisesti hyvin vaativia, joten oma tietokoneeni ei näihin riittänyt. Sinänsä mielestäni dimensioiden ja muuttujien määrän pienentäminen on oleellista ohjaamattomassa oppimisessa. On ehdottoman tärkeä pystyä vähentämää turhan paljon korreloivia muuttujia ja pyrkiä löytämää juuri oikeat muuttujat. Tämä näyttää vahvasti käsityöltä. 

Varsinaisessa analyysissa toteutettiin samalle datalle Xboost ohjattu oppiminen eli ennustettiin näitä juuri saatuja klustereita puumallilla. Tämä tehtiin sen takia, että päästii käsiksi selittävään tekoälyyn. Koneoppimisessa haasteena on ollut ja on vieläkin se, että se on vain musta laatikko, gijoka antaa tiettyjä arvoja. Selittämisessä ei riitä varianssiin perustuvat menetelmät. Tämän johdosta on kehitetty erilaisia malleista riippumattomia selittäviä malleja. Shapely value on mielestäni näistä parhain. Sen kautta voidaan saada jopa yksittäisille riveille selityksiä. Shapley value toteuteaan peliteorioista tutuilla menetelmillä, missä annetaan arvoja muuttujien selittäyydelle.
Kaikista osista löytyy funktiot ja aliohjelmat.

Ohjelmassa  read_and_merge_all oleva url_kiinteisto = "https://www.avoindata.fi/data/dataset/cf9208dc-63a9-44a2-9312-bbd2c3952596/resource/ae13f168-e835-4412-8661-355ea6c4c468/download/suomi_osoitteet_2020-08-14.7z" pitää vaihtaa aina tuoreimpaan sivustolta https://www.opendata.fi/data/fi/dataset/rakennusten-osoitetiedot-koko-suomi/resource/ae13f168-e835-4412-8661-355ea6c4c468


Blogissani on kommentteja sisällöstä:
https://www.launis.net/blank

Kirjani liiittyen yleisemmin kysyntämarkkinointiin on ostettavissa Amazonista
https://www.amazon.de/Kysynt%C3%A4markkinointi-nelj%C3%A4nness%C3%A4-teollisessa-vallankumouksessa-asiakassuhteisiin-ebook/dp/B088TKY21T/ref=sr_1_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=risto+launis&qid=1591631343&sr=8-1
