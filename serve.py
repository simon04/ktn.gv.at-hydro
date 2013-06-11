from bottle import route, run, response, hook
import sqlite3
import datetime

db = sqlite3.connect('data.db')
db.row_factory = sqlite3.Row

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@route('/stations')
def stations():
  c = db.cursor()
  c.execute('select * from stationdata d1 where d1.dt = (select max(dt) from stationdata d2 where d1.station = d2.station)')
  r = [dict(zip(row.keys(), row)) for row in c.fetchall()]
  c.close()
  return {'stations': r}

@route('/stations/<sta>')
def station(sta):
  def meta_data():
    c = db.cursor()
    c.execute('select station,river,lat,long from stationdata where station = ? order by dt limit 1', [sta])
    return [dict(zip(row.keys(), row)) for row in c.fetchall()][0]
  def measurement_data(begin):
    c = db.cursor()
    c.execute('select dt,w,q from stationdata where station = ? and dt > ? order by dt', [sta, begin.isoformat()])
    return [dict(zip(row.keys(), row)) for row in c.fetchall()]
  r = dict(meta_data())
  r['data'] = measurement_data(datetime.datetime.now() - datetime.timedelta(days=3))
  return r

run(host='localhost', port=8281)
