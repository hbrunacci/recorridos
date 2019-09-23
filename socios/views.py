# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from django.utils.translation import ugettext_lazy as _
from cruds_adminlte.filter import FormFilter

from .models import Socios, Filtro, Comentarios, Domicilios, Emails, Telefonos

from django.views.generic.base import TemplateView
from django.db.models import Q
from django import forms
from .forms import ComentarioForm, SociosForm, FiltrosForm, DomiciliosForm

from django.http.response import HttpResponse
from cruds_adminlte.templatetags.crud_tags import crud_inline_url


class IndexView(TemplateView):
    template_name = 'index.html'


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
    paginate_by = 25
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'


class Direccion_AjaxCRUD(InlineAjaxCRUD):
    model = Domicilios
    base_model = Socios
    add_form = DomiciliosForm
    update_form = DomiciliosForm
    inline_field = 'socio'
    list_fields = ['calle', 'numero', 'piso', 'barrio', 'partido', 'provincia', 'codigo_postal']
    title = _("Domicilios")
    views_available = ['list', ]


class Emails_AjaxCRUD(InlineAjaxCRUD):
    model = Emails
    base_model = Socios
    inline_field = 'socio'
    list_fields = ['email', 'chequeado']
    title = _("Emails")
    views_available = ['list', ]


class Telefono_AjaxCRUD(InlineAjaxCRUD):
    model = Telefonos
    base_model = Socios
    inline_field = 'socio'
    list_fields = ['telefono', 'chequeado']
    title = _("Telefonos")
    views_available = ['list', ]


class Comentarios_AjaxCRUD(InlineAjaxCRUD):
    model = Comentarios
    base_model = Socios
    inline_field = 'socio'
    list_fields = ['comentario']
    title = _("Comentarios")
    add_form = ComentarioForm
    update_form = ComentarioForm

    def get_create_view(self):
            djCreateView = super(Comentarios_AjaxCRUD, self).get_create_view()

            class CreateView(djCreateView):

                def form_valid(self, form):
                    self.object = form.save(commit=False)
                    setattr(self.object, self.inline_field, self.model_id)
                    if hasattr(self.object, 'user'):
                        user_instance = User.objects.get(username=self.request.user.username)
                        setattr(self.object, 'user', user_instance)
                    self.object.save()
                    crud_inline_url(self.model_id,
                                    self.object, 'list', self.namespace)

                    return HttpResponse(""" """)
            return CreateView


class SociosFormFilter(forms.Form):
    Direccion = forms.ModelMultipleChoiceField(queryset=Domicilios.objects.all()[:10])


class filterSocios(FormFilter):
    form = SociosFormFilter


class SociosCRUD(CRUDView):
    model = Socios
    check_login = True
    check_perms = True
    #fields = ['nro_socio', 'categoria', 'fecha_ingreso', 'apellidos', 'nombres', 'tipo_documento', 'numero_documento',
    #          'fecha_nacimiento', 'domicilio_particular', 'telefono', 'telefono_aux', 'email', ]
    fields = '__all__'
    related_fields = ['domicilios']
    list_fields = ['apellidos', 'nombres', 'categoria', 'domicilios']
    display_fields = ['apellidos', 'nombres', 'categoria', 'domicilios']
    list_filter = ['categoria', 'fecha_ingreso', 'fecha_nacimiento', ]
    views_available = ['list', 'update', 'detail', ]
    search_fields = ['numero_documento', ]
    add_form = SociosForm
    update_form = SociosForm
    split_space_search = True
    paginate_by = 50
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = [Direccion_AjaxCRUD, Telefono_AjaxCRUD, Emails_AjaxCRUD, Comentarios_AjaxCRUD,]

    def get_list_view(self):
        TempListViewClass = super(SociosCRUD, self).get_list_view()

        class ListViewClass(TempListViewClass):
            def get_userfilter(self, queryset):
                queryset = queryset.filter(activo=True).exclude(apellidos__isnull=True).exclude(apellidos__exact='')
                user = self.request.user
                queryset = queryset.filter(built_userfilter(user))
                return queryset

            def get_queryset(self):
                queryset = super(ListViewClass, self).get_queryset()
                queryset = self.get_userfilter(queryset)
                queryset = self.search_queryset(queryset)
                queryset = self.get_listfilter_queryset(queryset)
                return queryset

        return ListViewClass


def built_userfilter(user):
    filtros = Filtro.objects.all().filter(usuario=user)

    querys = Q(activo=True)
    for filtro in filtros:
        query = Q()
        if filtro.categoria:
            query.add(Q(categoria__contains=filtro.categoria), Q.AND)
        if filtro.fecha_socio_desde:
            query.add(Q(fecha_ingreso__gte=filtro.fecha_socio_desde), Q.AND)
        if filtro.fecha_socio_hasta:
            query.add(Q(fecha_ingreso__lte=filtro.fecha_socio_hasta), Q.AND)
        if filtro.fecha_nacimiento_desde:
            query.add(Q(fecha_nacimiento__gte=filtro.fecha_nacimiento_desde), Q.AND)
        if filtro.fecha_nacimiento_hasta:
            query.add(Q(fecha_nacimiento__lte=filtro.fecha_nacimiento_hasta), Q.AND)
        if filtro.codigo_postal:
            query.add(Q(Domicilios__codigo_postal__contains=filtro.codigo_postal), Q.AND)
        if filtro.ciudad:
            query.add(Q(Domicilios__ciudad__contains=filtro.ciudad), Q.AND)
        if filtro.partido:
            query.add(Q(Domicilios__partido__contains=filtro.partido), Q.AND)
        if filtro.provincia:
            query.add(Q(Domicilios__provincia__contains=filtro.provincia), Q.AND)

        querys.add(query, Q.OR)

    return querys



