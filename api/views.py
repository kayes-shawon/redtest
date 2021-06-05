import json
import redis
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


class ItemViews(APIView):
    def get(self, request: Request, **kwargs) -> Response:
        items = {}
        count = 0
        for key in redis_instance.keys("*"):
            items[key.decode("utf-8")] = redis_instance.get(key)
            count += 1
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)


class CreateItemViews(APIView):
    def post(self, request: Request) -> Response:
        request_data = request.data
        key = list(request_data.keys())[0]
        value = list(request_data.values())[0]

        redis_instance.set(key, value)

        response = {
            'key': key,
            'value': value,
            'msg': 'Successfully item set'
        }

        return Response(response, status=201)


class UpdateItemViews(APIView):
    def put(self, request: Request, **kwargs) -> Response:
        request_data = request.data
        key = list(request_data.keys())[0]
        new_value = list(request_data.values())[0]

        value = redis_instance.get(key)

        if value:
            redis_instance.set(key, new_value)
            response = {
                'key': key,
                'value': value,
                'msg': f'Successfully updated {key}'
            }
            status = 201
        else:
            response = {
                'msg': 'Value not found'
            }
            status = 400
        return Response(response, status=status)

class DeleteAPIViews(APIView):
    def delete(self, request: Request, key) -> Response:
        value = redis_instance.get(key)

        if value:
            redis_instance.delete(key)
            response = {
                'msg':  f'Deleted item {key}'
            }
        else:
            response = {
                'msg': 'Value not found'
            }
        return Response(response, status=201)

