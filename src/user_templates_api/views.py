from django.shortcuts import render

from django.views import View
from django.http import HttpResponse
from django.conf import settings
import json
import importlib


def index(request):
    return HttpResponse('Welcome to the User Templates API.')


class TemplateTypeView(View):
    def get(self, request):
        return HttpResponse(json.dumps(settings.CONFIG['template_types']))


class TemplateView(View):
    def get(self, request, template_type, template_name=""):
        response = {}

        if not template_name:
            templates_dir = settings.BASE_DIR / 'user_templates_api' / 'templates'
            # TODO: Add support for checking is_multi_dataset_template field.
            query_tags = request.GET.getlist("tags", [])

            for template_type_dir in (templates_dir / template_type).iterdir():
                if not template_type_dir.is_dir() or '__' in str(template_type_dir):
                    continue

                template_metadata = json.load(open(template_type_dir / 'metadata.json'))

                template_tags = template_metadata['tags']

                if query_tags and (set(template_tags) & set(query_tags)):
                    response[template_type_dir.name] = {
                        "template_title": template_metadata['title'],
                        "description": template_metadata['description']
                    }
            response = json.dumps(response)
        else:
            # This is meant to return an example template.
            response = render(request, f'{template_type}/{template_name}/template.txt')

        return HttpResponse(response)

    def post(self, request, template_type, template_name=""):
        if not template_name:
            return HttpResponse('Missing template_name', status=500)
        else:
            # Call utility functions for rendering that template. This is necessary as some templates
            # might have their own python scripts to actually generate the script.
            # Load the appropriate template module dynamically
            template_module = importlib.import_module(f'user_templates_api.templates.{template_type}.{template_name}.render', package=None)

            # Call the render function to actually get the template
            try:
                rendered_template = template_module.render(json.loads(request.body))
                return HttpResponse(json.dumps({'success': True, 'message': 'Successful template render', 'data': {'template': rendered_template}}))
            except Exception as e:
                print(repr(e))
                return HttpResponse(json.dumps({'success': False, 'message': 'Failure when attempting to render template.'}))
