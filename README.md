Suomi on jakautunut erilaisiin alueisiin.

Katso tulokset https://www.launis.net/blank

Teknisesti data-analyysi on toteutettu lukemalla rajapintojen kautta tietoja suoraan dataframeille. Tässä ei tallenneta erikseen CSV-tiedostoja, vaan kaikki datat luetaan suoraan lähteiden kautta. Koska tiedostojen lukeminen on aika hidasta, oli pakko toteuttaa tiedostojen väliaikaista kirjoittamista erillisiksi tiedostoiksi. Tämä kokonaisuus toimii myös ilman väliaikaistiedostoja. 
Kun tiedot on luettu sisään, ne käsitellään ja nolla-arvoille sekä NA arvoille haetaan uusia lukuja tai nämä rivit poistetaan kokonaan.  Klusterien hakemiseen tällä kertaa käytettiin yleistä k-means optimoitimenetelmää.  Siinä optimoidaan alkioiden keskipisteiden euklidisia etäisyyksiä.
Klusterien hyvyyttä on vaikea piirtää auki matriisiin, jos selittävä ominaisuusjoukko on yli kolmen. Kuvaaamista varten pääkomponentti analyysi helpottaa taasen tätä työtä. Tässä yhteydessä kokeiltiin myös erilaisten dimenssioiden vähentäviä työkaluja, kuten Principal feature analysis https://www.hindawi.com/journals/cmmm/2013/645921/ , SequentialFeatureSelector, http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/ . Samoin Minimum Redundancy Maximum Relevance feature selection toiminnallisuutta kokeiltiin. Useat näistä menetelmistä olivat laskennallisesti hyvin vaativia, joten oma tietokoneeni ei näihin riittänyt. Sinänsä mielestäni dimensioiden ja muuttujien määrän pienentäminen on oleellista ohjaamattomassa oppimisessa. On ehdottoman tärkeä pystyä vähentämää turhan paljon korreloivia muuttujia ja pyrkiä löytämää juuri oikeat muuttujat.
Varsinaisessa analyysissa toteutettiin samalle datalle Xboost ohjattu oppiminen eli ennustettiin näitä juuri saatuja klustereita puumallilla. Tämä tehtiin sen takia, että päästii käsiksi selittävään tekoälyyn. Koneoppimisessa haasteena on ollut ja on vieläkin se, että se on vain musta laatikko, joka antaa tiettyjä arvoja. Selittämisessä ei riitä varianssiin perustuvat menetelmät. Tämän johdosta on kehitetty erilaisia malleista riippumattomia selittäviä malleja. Shapely value on mielestäni näistä parhain. Sen kautta voidaan saada jopa yksittäisille riveille selityksiä. Shapley value toteuteaan peliteorioista tutuilla menetelmillä, missä annetaan arvoja muuttujien selittäyydelle.
Kaikista osista löytyy funktiot ja aliohjelmat.

Notebook create_clusters.ipynb kokoaa kaiken yhteen. 
