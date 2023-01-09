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
            # TODO: Add basic "tag" searching functionality. IE check if tag is in metadata file.
            # TODO: Add support for checking is_multi_dataset_template field.
            for template_type_dir in (templates_dir / template_type).iterdir():
                template_metadata = json.load(open(template_type_dir / 'metadata.json'))
                response[template_type_dir.name] = {
                    "template_title": template_metadata['title'],
                    "description": template_metadata['description']
                }
            response = json.dumps(response)
        else:
            # This is meant to return the raw template.
            response = render(request, f'{template_type}/{template_name}/template.txt')

        return HttpResponse(response)

    def post(self, request, template_type, template_name=""):
        if not template_name:
            return HttpResponse('Missing template_name', status=500)
        else:
            # TODO: Add functionality which takes dataset_uuid and grabs data from external services
            #       which will be used to populate template.
            # Call utility functions for rendering that template. This is necessary as some templates
            # might have their own python scripts to actually generate the script.
            response = render(request, f'{template_type}/{template_name}/template.txt', context={})
            return HttpResponse(response)

