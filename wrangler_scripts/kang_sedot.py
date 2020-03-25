import os
import json
import requests

from bs4 import BeautifulSoup
from pandas import DataFrame

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

    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'banten.json'), 'w', encoding='utf8') as outfile:
        json.dump(banten_arr, outfile)

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
    
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'jabar.json'), 'w', encoding='utf8') as outfile:
        json.dump(jabar_arr, outfile)

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

    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'jatim.json'), 'w', encoding='utf8') as outfile:
        json.dump(jatim_arr, outfile)

daftar_kang_sedot = [
    ('banten', sedot_banten), 
    ('jabar', sedot_jabar), 
    ('jatim', sedot_jatim)
]

for (prov, sedot_func) in daftar_kang_sedot:
    print('Menyedot data %s...' % prov)
    sedot_func()

print('Beres, bos')