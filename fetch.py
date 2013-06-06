import xml.etree.ElementTree as ET
from urllib.request import urlopen

def parseGeoRss(f):
  """
  >>> parseGeoRss('test.xml')
  [{'station': 'Mauthen - Gail'}]
  """
  feed = ET.parse(f)
  r = list()
  for item in feed.findall('channel/item'):
    r.append({
      'station': item.findtext('title').strip()
    })
  return r

#feed = ET.parse(urlopen('https://info.ktn.gv.at/asp/hydro/hydro_stationen_abfluss_rss.asp'))
