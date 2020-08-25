Suomi on jakautunut erilaisiin alueisiin. Varsinaisia tuloksia ja näkemyksiä esttelen omilla kotisivuillani https://www.launis.net/blank.

Ohjelmistokokonaisuuteni toimii siten, että aina ennen analysointia notebookeissa, luen datat käsitellysti sisään. Luen datat eri lähteistä rajapintojen kautta suoraadataframeille. Koska tietojen lukeminen on  hidasta, oli pakko toteuttaa myös tiedostojen kautta tapahtuva käsittely. Tämä tarkoittaa sitä, että ensimmäiellä kerralla käytetään rajapintoja. Esimerkiksi Tilastokeskuksen datat luetaan POST-käskyillä, vastaanotettu JSON-data käsitellään ja muokataan yksitasoiseksi. Tämä on näppärä rajapinta. Kaikkia tilastokeskuksen datajo ei voi lukea tätä kautta. Esimerkiksi en onnistunut lukemaan toimipaikkarekisteriä. Otinkin siitä yhteyttä Tilastokeskuseen mutta he eivät ole kommentoineet minulle takaisin mitään. Jouduin splittaamaan isommat POST-lukuproseduurit useaan eri osaan.Järkevintä olisi tallentaa tiedostot eismerkiksi PostgreSQL -tietokantaan, mutta koneeseeni ei enää mahdu PostgreSQL.

Oletuksena on se, että datat ovat areadata nimisessä hakemistossa, mutta tämä on ohjelmoitavissa aina notebookien alussa. Tiedostoja kuten mallit tai dataa sisältävät tiedostot tallennetaan areadata/data -hakemistoon.

Ohjelmani read_and_prepare_data lukee valmiit tiedostot sisään tai read_and_merge_all ohjelman avulla luetaan datat sisään joko API-rajapintojen kautta tai seuraavan tason väliaikaistiedostojen avulla. Tämän tason väliaikaistiedostot ovat vähän turhia mutta tein ylätason ensimmäisenä, joten molemmissa tasoissa on nyt väliaikaistiedostojen käyttö mahdollista. Jos ensimmäistä kertaa käyttää ohjelmaa read_and_prepare_data, saattaa ajo kestää.

Kun tiedot on luettu sisään, ne käsitellään ja nolla-arvoille sekä NA arvoille haetaan uusia arvoja tai nämä rivit poistetaan kokonaan. Pienemmisä postinumeroissa on paljon nolla-arvoja. Osa niistä voi olla aivan aitoja nolla-arvoja ja osa taasen laitettu nolliksi yksityisyyen suojan takia.  Uudet arvot ovat arvoja suhteutettuna esimerkiksi talouksien kokoon tai asukasmääriin. Esimerkiksi 'Aikuisten taloudet' saatiiin suhteutettua jakamalla se kaikkien alueen talouksien määrällä. Osa dataoista suhteutettiin vertaamalla sitää kaikkeen dataan. Esimerkiksi asuntojen neliöhinnat muutettiin osuudeksi kaikista neliöhinnasta. Tällöi jotkut Helsinkiläiset alueet saattoivat saada arvoksi luvun lähellä kymmentä eli neliöhinta on 10 kertaa maan keskiarvoa isompi. Pienet alueet ovat ongelmallisia. Osaan arvoista voidaan vetää helposti kunta-tason luku mutta milloin nolla on oikea nolla jää epäselväksi. Voi olla että esimerkiksi alueella ei ole yhtään ylempään tuloluokkaan kuuluvaa taloutta tai sitten arvo on niin pieni, että se on yksityisyyssyistä suojattu ja laitettu nollaksi. Helpoimalla pääsisi jos ottaisi vaikka alle 50-100 henkeä postinumeroalueet kokonaan pois näytteestä. Ohjelmani, jotka suhteuttaa tai poistaa nolla arvoja ovat create_share_of_values, create_new_values ja delete_outliers. Käytän create_share_of_values, create_new_values ohjelmia myös silloin kun toteutin klusterista oman itsenäisen dataframen. Täten saan oikeat arvot datalle. Jos käyttäisin esimerkiksi vain suhteutettujen arvojen keskiarvoja, tulokset ovat vääriä. Esimerkiksi klusterista jossa on sekaisin asukasmäärältään pieniä tai isoja alueita, suhteuttaminen keskiarvolla tuottaa väärän tuloksen.

Vaalidata saatiin ja muunnettiin yksinkertaisella tavalla suoraan DVVltä haetun osoiterekisterin avulla postinumerotiedoiksi. Alueiden koot suhteutettiin asuinkiinteistöjen määrällä. Asukkaiden määrän voisi arvioida paremmin, jos tietäisi huoneistojen määrän. Tämä data on olemassa osoiterekisterin kaupallisessa versiossa. Kun tarkistin datan oikeellisuutta, virheet olivat mielestäni hyväksyttävissä jo tällä karkealla rakennusten määrään perustuvalla jakamisella. Huoneiston määrä on olemassa Oikotiellä ja se olisi luettavissa sieltä kiinteistötasoisesti esim BeautifulSoup:in avulla, kokeilin tätä read_prices -ohjelmalla. En kuitenkaan totettanut tätä, sillä se ei ehkä ole ihan oikein.

Klusterien hakemiseen tällä kertaa käytettiin yleistä k-means optimoitimenetelmää (create_clusters_kmeans) ja normaalijakaumiin perustuvaa gaussian algoritmiä (create_clusters_gaussian). Yllättäen Kmeans toimi mielestäni paremmin. Gaussian taasen otti liikaa huomioon nolla-arvoja.

Klusterien hyvyyttä on vaikea piirtää auki matriisiin, jos selittävä ominaisuusjoukko on yli kolmen. Kuvaaamista varten pääkomponenttianalyysi helpottaa. Tässä yhteydessä kokeilin  erilaisten dimenssioiden vähentäviä työkaluja, kuten Principal feature analysis https://www.hindawi.com/journals/cmmm/2013/645921/ , SequentialFeatureSelector, http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/ . Samoin testailin Minimum Redundancy Maximum Relevance feature selection toiminnallisuutta. Useat näistä menetelmistä olivat laskennallisesti vaativia, joten oma tietokoneeni tai kärsivällisyyteni ei riittänyt. Mielestäni dimensioiden ja muuttujien määrän pienentäminen on oleellista ohjaamattomassa oppimisessa. On ehdottoman tärkeätä kyetä vähentämään korreloivia muuttujia ja pyrkiä löytämää juuri oikeat muuttujat. Tämä näyttää vahvasti käsityöltä. 

Varsinaisessa analyysissa toteutettiin samalle datalle Xboost ohjattu oppiminen eli ennustettiin näitä juuri saatuja klustereita puumallilla (XGBOOST). Tämän toteutin siksi, että pääsin käsiksi selittävään tekoälyyn. Koneoppimisessa haasteena on ollut ja vieläkin on se, että mallit ovat mustia laatikoita. Selittämisessä ei riitä varianssiin perustuvat menetelmät. Tämän johdosta on kehitetty erilaisia malleista riippumattomia selittäviä malleja. Shapely value on mielestäni näistä parhain. Sen kautta voidaan saada jopa yksittäisille riveille selityksiä. LIME-malli on toinen vastaava mutta päädyin Shapp-malliin. Shapley value toteuteaan peliteorioista tutuilla menetelmillä, missä annetaan arvoja muuttujien selittäyydelle. Shap -puumalli ei osaa käyttää alkuperäistä XGBOOST mallia, joten toimin ohessa esitetyllä tavalla https://github.com/slundberg/shap/issues/1215.

XGBOOST malliin toteutin automaattisen hyperparametrien hakijan. Tiedostossa create_prediction on aliohjelma Hyperparameter grid, joka toteuttaa tämän tehtävän. Koin tämän paremmaksi tavaksi kuin aiemmin käyttämäni perinteiset Grid Search -mallit. Ja halusin vähän myös kokeilla. En ole ihan varma, saanko tällä tavalla parhaat mallit.

Toisessa analyysissä etsin datasta syitä äänestää jotakin puoluetta. Tämän tein kahdella eri tavalla. Käytin XGBOOST mallia regressioanalyysissä, kun 'ennustin' ääniä puolueille. Eli toteutin siis mallin, joka ennustaa puolueiden äänet. XGBOOST on vain yhden outputin malli, joten tein regressiomallin jokaiselle puolueelle erikseen. Tämän jälkeen tein kaikille shap analysoinnin ja hain shap-arvot. Tallensin saadut shap arvot sen jälkeen yhdeksi listaksi, joten minulla oli toimiva shap malli kaikista puolueista. Toteutin myös Tensorflow:n avulla regressioanalyyysin multioutput mallina. Tämä on optimointimielessä vähän vielä kesken. Yritän etsiä parhaita parametreja, optimi piilotettujen tasojen määrää, neuronien määrää sekä optimointi funktiota.

Tiedän, että peliteriassa muuttujat ovat kokonaisuus mutta halusin vaan kokeilla jttuja. Kun olin saanut tulokset shap -mallista, otin tärkeimmät muuttujat listalta. Kun sain Shap mallin tärkeimmät muuttujat esimerkiski yhdestä klusterista, hain erikseen klusterin omalle dataframelle. Tein tälle samat suhteuttamis ja uusien datojen luomistyöt kuin datojen alkuperäisessä käsiteelyssä. Sain siis oikeat suhtetut arvot enkä keskiarvoja suhteista. Sen jälkeen vertaisin näitä tärkeitä muuttujia kaikkien tietojen ja yhden klusterin välillä. Puoluekannatuksessa vertasin taasetn niitä alueita, missä puolueen kannatus oli tuplat normaaliin. Tämä tapa on itse asiassa mielestäni aika kiva tapa esittää Shap mallin tuloksia ylätasolla. Se ei kerro muuttujien välisistä suhteista.

Kokeilin myös yksittäisten rivien tasolla Shap mallia. Ilmeisesti tämä toimi, koska Westend näytti tietynlaisia arvoja punaisella.

-------------------------------
Teknisiä huomioita

Ohjelmassa  read_and_merge_all oleva url_kiinteisto = "https://www.avoindata.fi/data/dataset/cf9208dc-63a9-44a2-9312-bbd2c3952596/resource/ae13f168-e835-4412-8661-355ea6c4c468/download/suomi_osoitteet_2020-08-14.7z" pitää vaihtaa aina tuoreimpaan sivustolta https://www.opendata.fi/data/fi/dataset/rakennusten-osoitetiedot-koko-suomi/resource/ae13f168-e835-4412-8661-355ea6c4c468. Jos haluaisi hienostella, tämänkin saisi automaattiseksi. Postin postitoimipaikkojen luvussa read_post_muncipalities, tätä on toteutettu automaattisesti.

Tavanomaisten (sklearn, tensorflow) modulien lisäksi ainakin seuraavia moduuleja pitää olla ladattuna

pyjstat https://pypi.org/project/pyjstat/
shap https://pypi.org/search/?q=shap


Erllisten moduulien vaatimuksia:
Jos haluaa käyttää create_mlxtend -moduulia, tarvitaan  http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/
Tai jos haluaa kokeilla automated_outlier_detection modulia, tarvitaan https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.knn
jos haluaa kokeilla mrmr moduulia, tarvitaan https://pypi.org/project/pymrmr/ (tämä moduuli ei näytä olevan kovin ylläpidetty)

Lataamalla kaikkin nämä tiedostot areadata hakemistoon ja käynnistämällä esimerkiksi create_clusters_kmeans tai create_political_xgboost notebookin, homma alkaa pyörimään. Notebookit tekevät tällä samalla datalla erityyppisiä päätelmiä. Toisaalta create_clusters_gaussian ja create_clusters_kmeans tarjoavat luokittelua samasta datasta mutta eri menetelmillä.



Blogissani on kommentteja sisällöstä:
https://www.launis.net/blank

Kirjani liiittyen yleisemmin kysyntämarkkinointiin on ostettavissa Amazonista
https://www.amazon.de/Kysynt%C3%A4markkinointi-nelj%C3%A4nness%C3%A4-teollisessa-vallankumouksessa-asiakassuhteisiin-ebook/dp/B088TKY21T/ref=sr_1_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=risto+launis&qid=1591631343&sr=8-1
