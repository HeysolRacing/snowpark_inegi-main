import download as d
import transform as t
import os

def urlDownload(tipo:str):
    print('Connecting to API...')   

    if tipo == 'remote':    
        url_download = 'https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip'
        if d.inegiDownloadFile(url_download):
            print('Downloaded!')
        else:
            print('Downloaded successfully!')   
        d.unzipData('iter_00_cpv2020_csv.zip')

    elif tipo == 'local':
        d.unzipLocalData('iter_00_cpv2020_csv.zip')
    else:
        return None
    
    csvPath = d.searchFile('conjunto_de_datos_iter_00CSV20.csv')
    newInegi = t.openCSV(csvPath)
    t.createCSV(newInegi)
    newInegi.clear()
    #Reading to create JSON file
    getCsvInfo = t.getData4Json('inegi.csv')
    t.splitJson(getCsvInfo,7)
    getCsvInfo.clear()
    print('Local ready!')