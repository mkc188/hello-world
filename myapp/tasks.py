from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
import time
import os

@shared_task
def task_shortest(data):
  try:
    if len(data) < 2:
      return {'error': 'WrongBodyFormat' }
    lat, lng = data[0]
    if not str(lat).replace('.','',1).isdigit() or not str(lng).replace('.','',1).isdigit():
      return {'error': 'WrongNumber' }
    key = os.environ['GOOGLE_API_KEY']
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    url += 'origins=' + str(lat) + ',' + str(lng)
    latlngs = []
    for lat, lng in data[1:]:
      if not str(lat).replace('.','',1).isdigit() or not str(lng).replace('.','',1).isdigit():
        return {'error': 'WrongNumber' }
      latlngs.append(str(lat) + ',' + str(lng))
    url += '&destinations='  + '|'.join(latlngs)
    url += '&departure_time=now'
    url += '&key=' + key
    r = requests.get(url, timeout=2).json()

    totalDistance = totalDuration = 0
    if r['status'] == 'OK':
      for i in range(len(r['rows'][0]['elements'])):
        if r['rows'][0]['elements'][i]['status'] == 'OK':
          distance = r['rows'][0]['elements'][i]['distance']['value']
          if 'duration_in_traffic' in r['rows'][0]['elements'][i]:
            duration = r['rows'][0]['elements'][i]['duration_in_traffic']['value']
          else:
            duration = r['rows'][0]['elements'][i]['duration']['value']
          totalDistance += distance
          totalDuration += duration
        else:
          return {'error': r['status'] }
      return {'status': 'success', 'path': data, 'total_distance': totalDistance, 'total_time': totalDuration}
    else:
      return {'error': r['status'] }
  except Exception as e:
    return {'error': e.__class__.__name__ }
