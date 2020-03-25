import os

import json
import requests
import html.parser as parser
from bs4 import BeautifulSoup
from datetime import datetime, timezone

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