import xml.etree.ElementTree as ET
from urllib.request import urlopen
from pprint import pprint
import re

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

def parseGeoRss(f):
  """
  >>> pprint(parseGeoRss('test.xml'))
  [{'lat': 46.6686111111111,
    'long': 13.0002777777778,
    'station': 'Mauthen - Gail'}]
  """
  ns = {'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#'}
  feed = ET.parse(f)
  r = list()
  for item in feed.findall('channel/item'):
    r.append({
      'station': item.findtext('title').strip(),
      'lat': float(item.findtext('geo:Point/geo:lat', namespaces=ns)),
      'long': float(item.findtext('geo:Point/geo:long', namespaces=ns)),
    })
  return r

#feed = ET.parse(urlopen('https://info.ktn.gv.at/asp/hydro/hydro_stationen_abfluss_rss.asp'))
