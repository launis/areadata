#these two function manage the reading of postcodes

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


def read_post_muncipalities(path, url_geometry):
    
    """This function reads all needed data
       either from file or calls a function to fetch data
       via API calls directly from sources and then writes data to files

        filename_post file is a shape-file read/written throgh geopandas
        
        Post Finland gives opporturnity to find automatically the latests
        files, we do not have toinput it
        
        Muncipalities dataframe is formed based on postcode list
        
    Args:
        path: path, where the data is stored
        url_geometry : recent geodata from stat.fi
        
        url_geometry see
        https://www.stat.fi/static/media/uploads/org/avoindata/kartta-aineistojen_lataus_url-osoitteen_kautta_ohje.pdf
    
    Returns:
        post: dataframe of post
        muncipalities: dataframe of muncipalities
        postcode_list: postcodes as lists
        muncipality_list: muncipalities as lists 


    """

    from supportfunctions import add_zeros_muncipality, add_zeros

    import pandas as pd   
    import os
    import inspect
    import geopandas as gp

    #read post and muncipalities
    filename_post = 'post.shp'
    filename_post = os.path.join(path, filename_post)
    
    filename_muncipalities =  'muncipalities.csv'
    filename_muncipalities = os.path.join(path, filename_muncipalities)
    

    if (os.access(filename_post, os.R_OK)) & (os.access(filename_muncipalities, os.R_OK)):
        #read it from files
        print(inspect.stack()[0][3],' read from file')
        
        post = gp.read_file(filename_post, encoding="ISO-8859-1")
        post = gp.GeoDataFrame(post, geometry='geometry')

        #geopandas shortens columnnames, so they need to be reset
        post.rename(columns={"postcode_n": "postcode_name", "muncipalit": "muncipality_code", "muncipal_1" : "muncipality_name", "language_c" : "language_code" }, inplace=True)

        post.loc[:,'postcode'] = post['postcode'].apply(add_zeros)
        muncipalities = pd.read_csv(filename_muncipalities, encoding="ISO-8859-1")
    else:
        #call functions to read data through API cals from post Finland
        print(inspect.stack()[0][3],' read from API')
        post= read_post(url_geometry)
        post = gp.GeoDataFrame(post, geometry='geometry')
        #create list of muncipalities from the reacent postcode data
        muncipalities = post.groupby(['muncipality_code', 'muncipality_name'],as_index=False ).mean()[['muncipality_code', 'muncipality_name']][['muncipality_code', 'muncipality_name']]
        if os.path.exists(path):
            post.to_file(filename_post, encoding="ISO-8859-1")
            muncipalities.to_csv(filename_muncipalities, index=False, encoding="ISO-8859-1")
        
            
    #make postcodes to lists
    postcode_list = post['postcode'].tolist()
 
    #make muncipalities to lists and add zeros to muncipality_code
    muncipality_list = muncipalities['muncipality_code'].apply(add_zeros_muncipality).to_list()
    return(post, muncipalities, postcode_list, muncipality_list)
