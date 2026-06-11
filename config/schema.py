from django.conf import settings
from drf_spectacular.openapi import AutoSchema


class AppLabelTaggedSchema(AutoSchema):
    def get_tags(self):
        # Check for user-related endpoints from Djoser
        path = self.path
        if '/users/' in path or '/jwt/' in path:
            return ['Accounts']
        
        # Check for local apps in module
        if hasattr(self.view, '__module__'):
            module_parts = self.view.__module__.split('.')
            local_apps = settings.LOCAL_APPS
            for app_label in local_apps:
                if app_label in module_parts:
                    return [app_label.capitalize()]
        
        # Fallback to default
        return super().get_tags()
