import graphene
from graphene_django.converter import convert_django_field
from djongo.models.fields import ObjectIdField


@convert_django_field.register(ObjectIdField)
def convert_objectid_to_string(field, registry=None):
    return graphene.String(description=str(field.help_text), required=not field.null)
