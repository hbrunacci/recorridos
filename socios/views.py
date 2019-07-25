# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD

from .models import Domicilio, Socios

from django.views.generic.base import TemplateView
from django import forms
from cruds_adminlte.filter import FormFilter

from .forms import DomicilioForm, SociosForm

class IndexView(TemplateView):
    template_name = 'index.html'


class Domicilio_AjaxCRUD(InlineAjaxCRUD):
    model = Domicilio
    base_model = Socios
    inline_field = 'Socio'
    add_form = DomicilioForm
    update_form = DomicilioForm
    fields = ['address', 'city']
    title = _("Direcciones")


class SociosFormFilter(forms.Form):
    Direccion = forms.ModelMultipleChoiceField(queryset=Domicilio.objects.all())

class filterSocios(FormFilter):
    form = SociosFormFilter

class SociosCRUD(CRUDView):
    model = Socios
    check_login = True
    check_perms = True
    fields = ['nro_socio', 'categoria', 'fecha_ingreso', 'apellidos', \
    'nombres', 'tipo_documento', 'numero_documento', 'fecha_nacimiento', \
    'domicilio_particular', 'telefono', 'telefono_aux', 'email',]
    list_fields = ['apellidos','nombres']
    display_fields = ['apellidos','nombres']
    inlines = [Domicilio_AjaxCRUD]
    list_filter = ['categoria', 'fecha_ingreso',
                   'fecha_nacimiento', filterSocios]
    #  views_available = ['create', 'list',  'detail'] # original actions
    views_available = ['create', 'list', 'update', 'detail', 'delete']
    search_fields = ['numero_documento']
    split_space_search = True
    paginate_by = 1
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'


