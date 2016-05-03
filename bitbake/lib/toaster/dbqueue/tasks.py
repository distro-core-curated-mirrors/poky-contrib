from __future__ import absolute_import
from celery import shared_task
from orm.models import Project

@shared_task
def save_object(obj):
    """
    Call save() on the Django Model object obj

    data: a single Django Model instance in a list (it's in a list because we
    need this to serialise the model)
    """
    print 'DATABASE WRITER: save_object(); class: %s' % obj.__class__.__name__
    method_to_call = getattr(obj, 'save')
    return method_to_call()

@shared_task
def bulk_create(clazz, data):
    print 'DATABASE WRITER: bulk_create(); class: %s' % clazz.__name__
    return clazz.objects.bulk_create(data)

@shared_task
def get_or_create_default_project():
    print 'DATABASE WRITER: get_or_create_default_project()'
    return Project.objects.get_or_create_default_project()