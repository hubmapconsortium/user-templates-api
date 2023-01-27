import importlib
import json

from django.apps import apps
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from user_templates_api.utils.client import get_client


def index(request):
    return HttpResponse("Welcome to the User Templates API.")


class TemplateTypeView(View):
    def get(self, request):
        return HttpResponse(
            json.dumps(
                {
                    "success": True,
                    "message": "Success",
                    "data": settings.CONFIG["template_types"],
                }
            )
        )


class TemplateView(View):
    def get(self, request, template_type, template_name=""):
        response = {}

        if not template_name:
            templates_dir = settings.BASE_DIR / "user_templates_api" / "templates"
            # TODO: Add support for checking is_multi_dataset_template field.
            query_tags = request.GET.getlist("tags", [])

            for template_type_dir in (templates_dir / 'templates' / template_type).iterdir():
                if not template_type_dir.is_dir() or "__" in str(template_type_dir):
                    continue

                template_metadata = json.load(open(template_type_dir / "metadata.json"))

                template_tags = template_metadata["tags"]

                if query_tags and (set(template_tags) & set(query_tags)):
                    response[template_type_dir.name] = {
                        "template_title": template_metadata["title"],
                        "description": template_metadata["description"],
                    }
        else:
            # This is meant to return an example template.
            response = render(request, f"{template_type}/{template_name}/template.txt")

        return HttpResponse(
            json.dumps({"success": True, "message": "Success", "data": response})
        )

    def post(self, request, template_type, template_name=""):
        if not template_name:
            return HttpResponse("Missing template_name", status=500)
        else:
            # Call utility functions for rendering that template. This is necessary as some templates
            # might have their own python scripts to actually generate the script.
            # Load the appropriate template module dynamically

            # TODO: We need to instantiate the object and then call the render function from that object
            template_module = importlib.import_module(
                f"user_templates_api.templates.{template_type}.templates.{template_name}.render",
                package=None,
            )

            # Call the render function to actually get the template
            try:
                auth_helper = apps.get_app_config("user_templates_api").auth_helper

                group_token = auth_helper.getAuthorizationTokens(request.headers)

                if type(group_token) != str:
                    response = HttpResponse("Invalid token")
                    response.status_code = 401
                    return response

                util_client = get_client(group_token)

                # TODO: Instantiate the object and call the render function rather than just calling the render function
                rendered_template = template_module.render(
                    json.loads(request.body), util_client
                )
                return HttpResponse(
                    json.dumps(
                        {
                            "success": True,
                            "message": "Successful template render",
                            "data": {"template": rendered_template},
                        }
                    )
                )
            except Exception as e:
                print(repr(e))
                return HttpResponse(
                    json.dumps(
                        {
                            "success": False,
                            "message": "Failure when attempting to render template.",
                        }
                    )
                )
