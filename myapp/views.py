# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_celery_results.models import TaskResult
from myapp.tasks import task_shortest
import ujson
import traceback

@csrf_exempt
def submit_location(request):
  if request.method == 'POST':
    try:
      json_data = ujson.loads(request.body)
      return JsonResponse({'token': task_shortest.delay(json_data).task_id })
    except Exception as e:
      return JsonResponse({'error': e.__class__.__name__ })
  else:
    return HttpResponseNotAllowed('')

def get_driving_route(request, token):
  if request.method == 'GET':
    try:
      taskResults = TaskResult.objects.filter(task_id=token)
      if taskResults:
        taskResult = taskResults[0]
        if taskResult.status == 'SUCCESS':
          return JsonResponse(ujson.loads(taskResult.result))
        elif taskResult.status == 'FAILURE':
          return JsonResponse({'status': 'failure', 'error': ujson.loads(taskResult.result)['exc_type']})
        else:
          return JsonResponse({'status': 'in progress'})
      else:
        return JsonResponse({'status': 'in progress'})
    except Exception as e:
      return JsonResponse({'error': e.__class__.__name__ })
  else:
    return HttpResponseNotAllowed('')
