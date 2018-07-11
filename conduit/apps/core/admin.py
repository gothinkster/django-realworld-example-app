from django.contrib import admin
from django.db.models.fields.related import ManyToManyField


def auto_register(model):
    """ Auto-register all models incl Django and 3rd party models (obviously not for production)

    Based on: http://technowhisp.com/2017/08/13/django/auto-registering-models-in-django-admin/
    """
    # Get all fields from model, but exclude autocreated reverse relations and ManyToManyField
    field_list = [f.name for f in model._meta.get_fields() if f.auto_created == False and not isinstance(f, ManyToManyField)]
    # Dynamically create ModelAdmin class and register it.
    my_admin = type('MyAdmin', (admin.ModelAdmin,),
                    {'list_display': field_list}
                    )
    try:
        admin.site.register(model, my_admin)
    except admin.sites.AlreadyRegistered:
        # This model is already registered
        pass


from django.apps import apps

for model in apps.get_models():
    auto_register(model)
