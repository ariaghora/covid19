import os
import json
import requests

from pandas import DataFrame

jabar_raw = requests.get('https://covid19-public.digitalservice.id/analytics/longlat/').text
jabar_arr = json.loads(jabar_raw)['data']

nama_kabkot = set(map(lambda x: x['kabkot_str'], jabar_arr)) - {''}
nama_status = set(map(lambda x: x['status'], jabar_arr)) | {'meninggal', 'sembuh'} #  - {''}
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
df.columns = ['jml_odp', 'jml_sembuh', 'jml_meninggal', 'jml_pdp', 'jml_kasus']
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