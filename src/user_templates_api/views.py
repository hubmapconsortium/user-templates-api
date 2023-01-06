from django.shortcuts import render

from django.views import View
from django.http import HttpResponse
from django.conf import settings
import json


def index(request):
    return HttpResponse('Welcome to the User Templates API.')


class TemplateTypeView(View):
    def get(self, request):
        return HttpResponse(json.dumps(settings.CONFIG))


class TemplateView(View):
    def get(self, request, template_type, template_name=""):
        response = {}

        if not template_name:
            templates_dir = settings.BASE_DIR / 'user_templates_api' / 'templates'
            for template_type_dir in (templates_dir / template_type).iterdir():
                template_metadata = json.load(open(template_type_dir / 'metadata.json'))
                response[template_type_dir.name] = {
                    "template_title": template_metadata['title'],
                    "description": template_metadata['description']
                }
            response = json.dumps(response)
        else:
            response = render(request, f'{template_type}/{template_name}/template.txt')

        return HttpResponse(response)
