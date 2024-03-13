import datetime

from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


class JSONResponseRenderer(JSONRenderer):
    # media_type = 'text/plain'
    # media_type = 'application/json'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].status_code < 400:
            if data and ('data' in data):  # 'data' in data
                response_dict = self.generate_dict_response(
                    data['data'], data['payload']['pagination']
                    if 'payload' in data else None,
                    renderer_context['response'].status_text,
                    renderer_context['response'].status_code,
                    str(datetime.datetime.now(timezone.timezone.utc))
                )
            else:
                response_dict = self.generate_dict_response(
                    data, None,
                    renderer_context['response'].status_text,
                    renderer_context['response'].status_code,
                    str(datetime.datetime.now(timezone.timezone.utc)))
        else:
            response_dict = self.generate_dict_response(
                None, None,
                renderer_context['response'].status_text,
                renderer_context['response'].status_code,
                str(datetime.datetime.now(timezone.timezone.utc)),
                data
            )
        return json.dumps(response_dict)

    @staticmethod
    def generate_dict_response(data, pagination, message,
                               status_code, timestamp, errors=None):
        response_dict = {
            'data': data,
            'payload': {
                'pagination': pagination,
                'errors': errors,
                'message': message,
                'status_code': status_code,
                'success': True if status_code < 400 else False,
                'timestamp': timestamp
            }
        }
        return response_dict


class JSONResponseRendererDetail(JSONRenderer):
    # media_type = 'text/plain'
    # media_type = 'application/json'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context['response'].status_code < 400:

            data = (data if renderer_context['response'].status_code < 400
                    else [value[0] for key, value in
                          renderer_context['response'].data.items()],)

            response_dict = self.generate_dict_response(
                data,
                None,
                renderer_context['response'].status_text,
                renderer_context['response'].status_code,
                str(datetime.datetime.now(timezone.timezone.utc))
            )

        else:
            response_dict = self.generate_dict_response(
                None,
                None,
                renderer_context['response'].status_text,
                renderer_context['response'].status_code,
                str(datetime.datetime.now(timezone.timezone.utc)),
                data
            )
        return json.dumps(response_dict)

    @staticmethod
    def generate_dict_response(data, pagination, message,
                               status_code, timestamp, errors=None):
        response_dict = {
            'data': data,
            'payload': {
                'pagination': pagination,
                'errors': errors,
                'message': message,
                'status_code': status_code,
                'success': True if status_code < 400 else False,
                'timestamp': timestamp
            }
        }
        return response_dict
