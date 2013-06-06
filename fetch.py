import xml.etree.ElementTree as ET
from urllib.request import urlopen
from pprint import pprint
import re
from datetime import datetime

"""
A Python 3.3 script to fetch hydrography Open Government Data from
http://www.kagis.ktn.gv.at/279012_DE-OGD-Kaernten_%28beta%29-Ablussmessstationen
and store it in a SQLite 3 database.

Data is licensed CC-BY 3.0 ("Land Kärnten - data.ktn.gv.at").
This script/file is licensed GNU General Public License 3.
"""

def parseFloat(s, prefix=''):
  """
  >>> parseFloat('17')
  17.0
  >>> parseFloat('0.123')
  0.123
  >>> parseFloat('0,456')
  0.456
  """
  m = re.compile(prefix + '(\d+([,.]\d*)?)').search(s)
  if m:
    return float(m.group(1).replace(',', '.'))
  else:
    None

def parseDateTime(s, prefix=''):
  """
  >>> parseDateTime('06.06.2013 19:07:35')
  datetime.datetime(2013, 6, 6, 19, 7, 35)
  >>> parseDateTime('06.06.2013 19:07:00')
  datetime.datetime(2013, 6, 6, 19, 7)
  >>> parseDateTime('05.06.2013')
  datetime.datetime(2013, 6, 5, 0, 0)
  """
  m = re.compile(prefix + '(\d\d\.\d\d\.\d\d\d\d \d\d:\d\d:\d\d)').search(s)
  mD = re.compile(prefix + '(\d\d\.\d\d\.\d\d\d\d)').search(s)
  if m:
    return datetime.strptime(m.group(1), '%d.%m.%Y %H:%M:%S')
  elif mD:
    return datetime.strptime(mD.group(1), '%d.%m.%Y')
  else:
    return None


def parseGeoRss(f):
  """
  >>> pprint(parseGeoRss('test.xml'))
  [{'dt': datetime.datetime(2013, 6, 6, 18, 45, 5),
    'lat': 46.6686111111111,
    'long': 13.0002777777778,
    'q': 17.2,
    'river': 'Gail',
    'station': 'Mauthen',
    'w': 83.0}]
  """
  ns = {'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#'}
  feed = ET.parse(f)
  r = list()
  for item in feed.findall('channel/item'):
    title = item.findtext('title').strip().split(' - ')
    desc = item.findtext('description')
    r.append({
      'station': title[0],
      'river': title[1],
      'lat': float(item.findtext('geo:Point/geo:lat', namespaces=ns)),
      'long': float(item.findtext('geo:Point/geo:long', namespaces=ns)),
      'w': parseFloat(desc, 'Wasserstand\(cm\)\s*:\s*'),
      'q': parseFloat(desc, 'Abfluss\(m.*?\)\s*:\s*'),
      'dt': parseDateTime(desc, 'Datum/Uhrzeit der Messung\s*:\s*'),
    })
  return r

def fetchToSqlite():
  import sqlite3
  db = sqlite3.connect('data.db')
  db.execute('create table if not exists stationdata ('
      'station text,'
      'river text,'
      'lat real,'
      'long real,'
      'w real,'
      'q real,'
      'dt text,'
      'primary key (station, dt)'
      ')')
  cursor = db.cursor()
  for i in parseGeoRss(urlopen('https://info.ktn.gv.at/asp/hydro/hydro_stationen_abfluss_rss.asp')):
    pprint(i)
    cursor.execute(
        'replace into stationdata (station, river, lat, long, w, q, dt) values (?,?,?,?,?,?,?)',
        [i['station'], i['river'], i['lat'], i['long'], i['w'], i['q'], i['dt'].isoformat()])
  db.commit()
  cursor.close()

if __name__ == '__main__':
  fetchToSqlite()
