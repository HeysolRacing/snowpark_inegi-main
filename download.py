#Creación de archivo para descarga
import requests 
import json
import os
import zipfile 

def inegiDownloadFile(url:str) -> bool:
    try:
        zipfilename = url.split('/')[-1]
        if not os.path.isfile(zipfilename):
            r = requests.get(url,allow_redirects=True)
            if r.status_code == 200:
                print('Connection established!')
                open(zipfilename, 'wb').write(r.content)
                return True    
            else:
                print('Failed to connect to the API. Please check your internet connection and try again')
                return False
        else:
            return False        
    except requests.RequestException as err:
        print('Failed to connect to the API. Please check your internet connection and try again')
        print(err)
        return None

def unzipData(zipfilename:str):
    dirname = os.getcwd()
    if os.path.isfile(zipfilename):
        print('File in directory...OK')
        extractDir = os.path.join(dirname, 'CSV')
        if not os.path.exists(extractDir):
            os.mkdir(extractDir)
        else:
            zippath = dirname + '/' + zipfilename
        with zipfile.ZipFile(zippath, 'r') as zipa:
            zipa.extractall(extractDir)
        print('Unzipped')
    else:
        print('File must be downloaded before!')

def unzipLocalData(zipfilename:str):
    rootdirname = os.getcwd()
    dirname = os.path.join(rootdirname, 'local') 
    
    if os.path.isfile(os.path.join(dirname,zipfilename)):
        print('Local file in directory...OK')
        extractDir = os.path.join(rootdirname, 'CSV')
        if not os.path.exists(extractDir):
            os.mkdir(extractDir)
        else:
            zippath = dirname + '/' + zipfilename
        with zipfile.ZipFile(zippath, 'r') as zipa:
            zipa.extractall(extractDir)
        print('Unzipped')
    else:
        print('File must be downloaded before!')

def searchFile(filename:str):
    #conjunto_de_datos_iter_00CSV20.csv
    dinegi ={'folder':'CSV/iter_00_cpv2020/conjunto_de_datos/', 'file':filename}
    dirname = os.path.join(os.getcwd(), dinegi['folder'])
    for fileRoot in os.listdir(dirname):
        if os.path.isfile(os.path.join(dirname, dinegi['file'])):
            return os.path.join(dirname,fileRoot)
        else:
            print('No File available')

