# layerindex-web - view definitions
#
# Copyright (C) 2013 Intel Corporation
#
# Licensed under the MIT license, see COPYING.MIT for details

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from layerindex.models import LayerItem, LayerMaintainer, LayerDependency, Recipe
from datetime import datetime
from django.views.generic import DetailView, ListView
from layerindex.forms import SubmitLayerForm, LayerMaintainerFormSet
from django.db import transaction
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
import simplesearch
import settings


def submit_layer(request):
    if request.method == 'POST':
        layeritem = LayerItem()
        form = SubmitLayerForm(request.POST, instance=layeritem)
        maintainerformset = LayerMaintainerFormSet(request.POST, instance=layeritem)
        if form.is_valid() and maintainerformset.is_valid():
            with transaction.commit_on_success():
                layeritem.created_date = datetime.now()
                form.save()
                maintainerformset.save()
                # Save dependencies
                for dep in form.cleaned_data['deps']:
                    deprec = LayerDependency()
                    deprec.layer = layeritem
                    deprec.dependency = dep
                    deprec.save()
                # Send email
                plaintext = get_template('layerindex/submitemail.txt')
                perm = Permission.objects.get(codename='publish_layer')
                users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm) ).distinct()
                for user in users:
                    d = Context({
                        'user_name': user.get_full_name(),
                        'layer_name': layeritem.name,
                        'layer_url': request.build_absolute_uri(reverse('layer_item', args=(layeritem.name,))),
                    })
                    subject = '%s - %s' % (settings.SUBMIT_EMAIL_SUBJECT, layeritem.name)
                    from_email = settings.SUBMIT_EMAIL_FROM
                    to_email = user.email
                    text_content = plaintext.render(d)
                    msg = EmailMessage(subject, text_content, from_email, [to_email])
                    msg.send()
                return HttpResponseRedirect(reverse('submit_layer_thanks'))
    else:
        form = SubmitLayerForm()
        maintainerformset = LayerMaintainerFormSet()

    return render(request, 'layerindex/submitlayer.html', {
        'form': form,
        'maintainerformset': maintainerformset,
    })

def submit_layer_thanks(request):
    return render(request, 'layerindex/submitthanks.html')

def about(request):
    return render(request, 'layerindex/about.html')

def publish(request, name):
    if not (request.user.is_authenticated() and request.user.has_perm('layerindex.publish_layer')):
        raise PermissionDenied
    return _statuschange(request, name, 'P')

def _statuschange(request, name, newstatus):
    w = get_object_or_404(LayerItem, name=name)
    if w.status != newstatus:
        w.change_status(newstatus, request.user.username)
        w.save()
    return HttpResponseRedirect(reverse('layer_item', args=(name,)))

class LayerListView(ListView):
    context_object_name = 'layer_list'

    def get_queryset(self):
        return LayerItem.objects.filter(status__in=self.request.session.get('status_filter', 'P')).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(LayerListView, self).get_context_data(**kwargs)
        context['layer_type_choices'] = LayerItem.LAYER_TYPE_CHOICES
        return context

class RecipeSearchView(ListView):
    context_object_name = 'recipe_list'
    paginate_by = 50

    def get_queryset(self):
        query_string = self.request.GET.get('q', '')
        if query_string.strip():
            entry_query = simplesearch.get_query(query_string, ['pn', 'summary', 'description', 'filename'])
            return Recipe.objects.filter(entry_query).order_by('pn', 'layer')
        else:
            return Recipe.objects.all().order_by('pn', 'layer')

    def get_context_data(self, **kwargs):
        context = super(RecipeSearchView, self).get_context_data(**kwargs)
        context['search_keyword'] = self.request.GET.get('q', '')
        return context


class PlainTextListView(ListView):
    def render_to_response(self, context):
        "Returns a plain text response rendering of the template"
        template = get_template(self.template_name)
        return HttpResponse(template.render(Context(context)),
                                 content_type='text/plain')
