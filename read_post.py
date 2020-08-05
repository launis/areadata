def read_post(url_geometry):
    
    """read latest information of finnish postcodes
       all data is fround accoring to guidelines
       also the polygons are read from tilastokeskus
       
       http://www.posti.fi/liitteet-yrityksille/ehdot/postinumeropalvelut-palvelukuvaus-ja-kayttoehdot.pdf
    
       https://www.stat.fi/org/avoindata/paikkatietoaineistot.html
       https://www.stat.fi/static/media/uploads/org/avoindata/kartta-aineistojen_lataus_url-osoitteen_kautta_ohje.pdf
       
       Exsample of url_geometry = "http://geo.stat.fi/geoserver/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=postialue:pno_tilasto&outputFormat=SHAPE-ZIP"
    Returns:
         list of postcodes and related polygons
         
    """

    
    import pandas as pd
    import geopandas as gp
    from urllib.request import urlopen
    import requests 
    import re
    import zipfile
    import os
    import io
    import numpy as np
    
    from supportfunctions import add_zeros

    # http://www.posti.fi/liitteet-yrityksille/ehdot/postinumeropalvelut-palvelukuvaus-ja-kayttoehdot.pdf

    index = urlopen("http://www.posti.fi/webpcode/unzip/").read().decode('utf-8')

    # Find the DAT file (latest)
    postcodes_filename = re.findall(r'http://www.posti.fi/webpcode/unzip/PCF_[0-9]*?\.dat', index)[0]

    # Example of the name
    #postcodes_filename = ('https://www.posti.fi/webpcode/unzip/PCF_20200325.dat')

    # Manage data
    headings = ['postcode', 'postcode_name', 'postcode_sv_name', 'type', 'area_code', 'area_name', 'muncipality_code', 'muncipality_name', 'muncipality_sv_name', 'language_code']
    colspecs = [(13, 18), (18, 48), (48, 78), (110, 111), (111,116), (116,146), (176, 179), (179, 199), (199, 219), (219, 220)]


    # Retrieving the file
    data = pd.read_fwf(postcodes_filename, names=headings, header=None, colspecs=colspecs, encoding='latin1')

    #only real postcode types     
    data=data[data['type']==1]
    
    #postcode back to normal as a string
    data['postcode'] = data['postcode'].apply(add_zeros)


    #if Swedish speaking (language code = 4) then use it as a postcode_name and muncipality_name
    
    data['postcode_name']=np.where(data['language_code']==4, data['postcode_sv_name'], data['postcode_name'])
    data['muncipality_name']=np.where(data['language_code']==4, data['muncipality_sv_name'], data['muncipality_name'])


    #drop no more needed columns
    data=data.drop(columns=['postcode_sv_name', 'type', 'type', 'muncipality_sv_name'])
    
    #shorten the content in the names
    data['postcode_name']=data['postcode_name'].str.strip()
    data['muncipality_name']=data['muncipality_name'].str.strip()
    data['muncipality_code']=pd.to_numeric(data['muncipality_code'], errors='ignore')
    data['area_name']=data['area_name'].str.strip()
    data['area_code']=data['area_code'].str.strip()
    
    #step2 read ploygons from Tilastokeskus
    
    
    local_path = 'tmp/'
    
    #shapefile shoud be= "pno_tilasto.shp"
    r = requests.get(url_geometry)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path=local_path) # extract to folder
    filenames = [y for y in sorted(z.namelist()) for ending in ['cst', 'dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)] 
    cst, dbf, prj, shp, shx = [filename for filename in filenames]
    pno_map = gp.read_file(local_path + shp)
    #empty tmp files
    for y in filenames:
        os.remove(local_path + y)
    os.remove(local_path + 'wfsrequest.txt')
    pno_map = pno_map[['postinumer', 'geometry']]
    
    #combine data
    post_all = pd.merge(data, pno_map, how='inner', left_on='postcode', right_on='postinumer',copy=True, sort=True)
    post_all.drop(columns=['postinumer'], inplace=True)
    #post_all = gp.GeoDataFrame(post_all, geometry='geometry')

    return(post_all)