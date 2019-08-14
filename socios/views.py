# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD

from .models import Domicilio, Socios, Filtro

from django.views.generic.base import TemplateView
from django import forms
from cruds_adminlte.filter import FormFilter

from .forms import DomicilioForm, SociosForm, FiltrosForm


class IndexView(TemplateView):
    template_name = 'index.html'


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
    list_filter = ['categoria', 'fecha_ingreso',
                   'fecha_nacimiento', filterSocios]
    #  views_available = ['create', 'list',  'detail'] # original actions
    views_available = ['create', 'list', 'update', 'detail', 'delete']
    search_fields = ['numero_documento']
    add_form = SociosForm
    update_form = SociosForm
    split_space_search = True
    paginate_by = 1
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'


class FiltroCRUD(CRUDView):
    model = Filtro
    check_login = True
    check_perms = True
    fields = ['usuario', 'nombre_filtro']
    list_fields = ['usuario', 'nombre_filtro']
    display_fields = ['usuario', 'nombre_filtro']
    views_available = ['create', 'list', 'update', 'detail', 'delete']
    search_fields = ['usuario', 'nombre_filtro']
    add_form = FiltrosForm
    update_form = FiltrosForm
    split_space_search = True
    paginate_by = 1
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'


