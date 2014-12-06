import json
from django.http import HttpResponse


class JsonResponseMixin(object):
    def json_success_response(self, **context):
        context.update(status=True)
        return HttpResponse(json.dumps(context), 'json')

    def json_fail_response(self, **context):
        context.update(status=False)
        return HttpResponse(json.dumps(context), 'json')