import importlib
import inspect
import json

from django.apps import apps
from django.conf import settings
from django.http import HttpResponse
from django.views import View


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
        templates_dir = settings.BASE_DIR / "user_templates_api" / "templates"

        if not template_name:
            # TODO: Add support for checking is_multi_dataset_template field.
            query_tags = request.GET.getlist("tags", [])

            for template_type_dir in (
                templates_dir / template_type / "templates"
            ).iterdir():
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
            template_metadata = json.load(
                open(
                    templates_dir
                    / template_type
                    / "templates"
                    / template_name
                    / "metadata.json"
                )
            )

            response[template_name] = {
                "template_title": template_metadata["title"],
                "description": template_metadata["description"],
            }

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

                data = {
                    "group_token": group_token,
                    "metadata": json.load(
                        open(
                            settings.BASE_DIR
                            / "user_templates_api"
                            / "templates"
                            / template_type
                            / "templates"
                            / template_name
                            / "metadata.json"
                        )
                    ),
                    "body": json.loads(request.body),
                }

                template_class_obj_inst = None
                for template_class_name, template_class_obj in inspect.getmembers(
                    template_module, inspect.isclass
                ):
                    if template_name in template_class_obj.__module__:
                        template_class_obj_inst = template_class_obj()
                        break

                rendered_template = template_class_obj_inst.render(data)

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


class TestTemplateView(View):
    def post(self, request, template_type, template_format):
        # Call utility functions for rendering that template. This is necessary as some templates
        # might have their own python scripts to actually generate the script.
        # Load the appropriate template module dynamically

        template_module = importlib.import_module(
            f"user_templates_api.templates.{template_type}.render",
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

            data = {
                "group_token": group_token,
                "metadata": {"template_format": template_format},
                "body": json.loads(request.body),
            }

            template_class_obj_inst = None
            for template_class_name, template_class_obj in inspect.getmembers(
                template_module, inspect.isclass
            ):
                if template_type in template_class_obj.__module__:
                    template_class_obj_inst = template_class_obj()
                    break

            rendered_template = template_class_obj_inst.render(data)

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
