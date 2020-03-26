import os
import json
import requests

from bs4 import BeautifulSoup
from pandas import DataFrame

def sedot_pusat():
    pusat_raw = requests.get('https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?f=json&where=(Kasus_Posi%20%3C%3E%200)%20AND%20(Provinsi%20%3C%3E%20%27Indonesia%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Kasus_Posi%20desc&outSR=102100&resultOffset=0&resultRecordCount=34&cacheHint=true').text
    pusat_json_arr = json.loads(pusat_raw)['features']
    pusat_arr = []

    n_positif, n_sembuh, n_meninggal = 0, 0, 0
    for i, o in enumerate(pusat_json_arr):
        pusat_arr.append({
            'no': i+1,
            'nama': o['attributes']['Provinsi'],
            'jml_kasus': int(o['attributes']['Kasus_Posi']),
            'jml_sembuh': int(o['attributes']['Kasus_Semb']),
            'jml_meninggal': int(o['attributes']['Kasus_Meni']),
            'jml_odp': '-',
            'jml_pdp': '-',
        })
        n_positif += int(o['attributes']['Kasus_Posi'])
        n_sembuh += int(o['attributes']['Kasus_Semb'])
        n_meninggal += int(o['attributes']['Kasus_Meni'])
    out = {
        'ringkasan': {
            'jml_kasus': n_positif,
            'jml_sembuh': n_sembuh,
            'jml_meninggal': n_meninggal,
            'jml_odp': '-',
            'jml_pdp': '-',
        },
        'data': pusat_arr
    }
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'pusat.json'), 'w', encoding='utf8') as outfile:
        json.dump(out, outfile)

def sedot_banten():
    banten_raw = requests.get('https://infocorona.bantenprov.go.id/kasus-terkonfirmasi').text
    banten_arr = []
    cnt = 1
    for row in BeautifulSoup(banten_raw, features='lxml').body.find('table').find('tbody').findAll('tr'):
        if cnt < 9:
            o = {
                'no': cnt,
                'nama': row.findAll('th')[0].text.title(),
                'jml_kasus': int(row.findAll('td')[3].text),
                'jml_sembuh': int(row.findAll('td')[0].text),
                'jml_meninggal': int(row.findAll('td')[2].text),
                'jml_odp': '-',
                'jml_pdp': '-',
            }
            cnt += 1
            banten_arr.append(o)
    
    out = {
        'ringkasan': {
            'jml_kasus': '-',
            'jml_sembuh': '-',
            'jml_meninggal': '-',
            'jml_odp': '-',
            'jml_pdp': '-',
        },
        'data': banten_arr
    }

    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'banten.json'), 'w', encoding='utf8') as outfile:
        json.dump(out, outfile)

def sedot_jabar():
    jabar_raw = requests.get('https://covid19-public.digitalservice.id/analytics/longlat/').text
    jabar_arr = json.loads(jabar_raw)['data']

    nama_kabkot = set(map(lambda x: x['kabkot_str'], jabar_arr)) - {''}
    nama_status = sorted(list(set(map(lambda x: x['status'], jabar_arr)) | {'meninggal', 'sembuh'}))
    nama_stage  =  set(map(lambda x: x['stage'], jabar_arr)) 

    df = DataFrame(columns=nama_status, index=nama_kabkot).fillna(0)
    for kasus in jabar_arr:
        try:
            df[kasus['status']][kasus['kabkot_str']] += 1
            if kasus['stage'] == 'Meninggal':
                df['meninggal'][kasus['kabkot_str']] += 1
            if kasus['stage'] == 'Sembuh':
                df['sembuh'][kasus['kabkot_str']] += 1
        except:
            pass
    
    #  Rename the columns
    df.columns = ['jml_odp', 'jml_pdp', 'jml_kasus', 'jml_meninggal', 'jml_sembuh']
    df = df.sort_index()

    jabar_arr = []
    for kabkot in df.index:
        kabkot_str = kabkot
        if kabkot == None:
            kabkot_str = '<strong>UNKNOWN</strong>'
                
        o = {
                'nama': kabkot_str
        }
        for prop in df.columns:
            o[prop] = int(df[prop][kabkot])
        jabar_arr.append(o)
    
    out = {
        'ringkasan': {
            'jml_kasus': '-',
            'jml_sembuh': '-',
            'jml_meninggal': '-',
            'jml_odp': '-',
            'jml_pdp': '-',
        },
        'data': jabar_arr
    }
    
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'jabar.json'), 'w', encoding='utf8') as outfile:
        json.dump(out, outfile)

def sedot_jatim():
    jatim_raw = requests.get('http://covid19dev.jatimprov.go.id/xweb/draxi').text
    jatim_arr = []
    cnt = 1
    for row in BeautifulSoup(jatim_raw, features='lxml').body.find('table').find('tbody').findAll('tr'):
        o = {
            'no': cnt,
            'nama': row.findAll()[0].text.title(),
            'jml_kasus': int(row.findAll()[3].text),
            'jml_sembuh': '-',
            'jml_meninggal': '-',
            'jml_odp': int(row.findAll()[1].text),
            'jml_pdp': int(row.findAll()[2].text),
        }
        cnt += 1
        jatim_arr.append(o)

    out = {
        'ringkasan': {
            'jml_kasus': '-',
            'jml_sembuh': '-',
            'jml_meninggal': '-',
            'jml_odp': '-',
            'jml_pdp': '-',
        },
        'data': jatim_arr
    }

    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'jatim.json'), 'w', encoding='utf8') as outfile:
        json.dump(out, outfile)

daftar_kang_sedot = [
    ('pusat', sedot_pusat),
    ('banten', sedot_banten), 
    ('jabar', sedot_jabar), 
    ('jatim', sedot_jatim)
]

for (prov, sedot_func) in daftar_kang_sedot:
    print('Menyedot data %s...' % prov)
    sedot_func()

print('Beres, bos')