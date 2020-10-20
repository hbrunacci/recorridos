# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from cruds_adminlte.crud import CRUDView,get_filters
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from django.utils.translation import ugettext_lazy as _
from cruds_adminlte.filter import FormFilter

from .models import Categorias, Socios, Filtro, Comentarios, Domicilios, Emails, Telefonos

from django.views.generic.base import TemplateView
from django.db.models import Q
from django import forms
from .forms import ComentarioForm, SociosForm, FiltrosForm, DomiciliosForm, FiltrosWebForm

from django.http.response import HttpResponse
from cruds_adminlte.templatetags.crud_tags import crud_inline_url
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
import tempfile

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

#nombre, localidad, nro_socio_categoria_Codigo_postal


# Categoria, Filtros prellenados


class Comentarios_AjaxCRUD(InlineAjaxCRUD):
    model = Comentarios
    base_model = Socios
    inline_field = 'socio'
    list_fields = ['comentario', 'fallecido']
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
    queryset = Categorias.objects.all().values('descripcion')
    socio__categoria = forms.ModelMultipleChoiceField(queryset=queryset)
    fecha_nacimiento_desde = forms.DateField()
    fecha_nacimiento_hasta= forms.DateField()
    fecha_ingreso_desde = forms.DateField()
    fecha_ingreso_hasta = forms.DateField()


class filterSocios(FormFilter):
    form = FiltrosWebForm


class DomiciliosCRUD(CRUDView):
    model = Domicilios
    related_fields = ['socio']
    list_fields = ['calle', 'ciudad', 'partido', 'codigo_postal', 'socio__apellidos', 'socio__categoria', 'socio__nro_socio']
    update_form = DomiciliosForm
    add_form = DomiciliosForm
    paginate_by = 50
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = [Comentarios_AjaxCRUD, Telefono_AjaxCRUD,]
    views_available = ['list', 'update', 'detail', ]
    split_space_search = False
    list_filter = ['calle', filterSocios]
    search_fields = ['socio__numero_documento', 'calle', 'ciudad','codigo_postal','socio__categoria']
    template_name_base = 'domicilio_crud'


    def get_list_view(self):
        TempListViewClass = super(DomiciliosCRUD, self).get_list_view()

        class ListViewClass(TempListViewClass):
            text_fields = ['calle', 'socio__categoria']

            def get_listfilter_queryset(self, queryset):
                if self.list_filter:
                    filters = get_filters(
                        self.model, self.list_filter, self.request)
                    for filter in filters:
                        filter_q = get_custom_filter(filter)
                        queryset = queryset.filter(filter_q)
                return queryset

            def search_queryset(self, query):
                if self.split_space_search is True:
                    self.split_space_search = ' '

                if self.search_fields and 'q' in self.request.GET:
                    q = self.request.GET.get('q')
                    if self.split_space_search:
                        q = q.split(self.split_space_search)
                    elif q:
                        q = [q]
                    sfilter = None
                    for field in self.search_fields:
                        for qsearch in q:
                            if field not in self.context_rel:
                                field = '%s__icontains' % field if field in self.text_fields else field
                                if sfilter is None:
                                    sfilter = Q(**{field: qsearch})
                                else:
                                    sfilter |= Q(**{field: qsearch})
                    if sfilter is not None:
                        query = query.filter(sfilter)

                if self.related_fields:
                    query = query.filter(**self.context_rel)
                return query

            def get_queryset(self):
                queryset = super(ListViewClass, self).get_queryset()
                queryset = get_user_queryset(self.request.user, queryset)
                queryset = self.search_queryset(queryset)
                queryset = self.get_listfilter_queryset(queryset)
                queryset = queryset.order_by('codigo_postal', 'ciudad', 'calle')
                return queryset

        return ListViewClass


class SociosCRUD(CRUDView):
    model = Socios
    check_login = True
    check_perms = True
    #fields = ['nro_socio', 'categoria', 'fecha_ingreso', 'apellidos', 'nombres', 'tipo_documento', 'numero_documento',
    #          'fecha_nacimiento', 'domicilio_particular', 'telefono', 'telefono_aux', 'email', ]
    fields = '__all__'
    related_fields = ['codigo_postal']
    list_fields = ['apellidos', 'nombres', 'categoria', 'domicilio__codigo_postal']
    display_fields = ['apellidos', 'nombres', 'categoria', 'domicilio']
    list_filter = ['categoria', 'fecha_ingreso', 'fecha_nacimiento', ]
    views_available = ['list', 'update', 'detail', ]
    search_fields = ['numero_documento', ]
    split_space_search = True
    add_form = SociosForm
    update_form = SociosForm
    paginate_by = 50
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = [Telefono_AjaxCRUD, Comentarios_AjaxCRUD, ]


def get_user_queryset(user, queryset):
    queryset = queryset.filter(socio__activo=True) \
        .exclude(socio__apellidos__isnull=True) \
        .exclude(socio__apellidos__exact='')
    queryset = queryset.filter(built_userfilter(user))
    return queryset


def built_userfilter(user):
    filtros = Filtro.objects.all().filter(usuario=user)
    querys = Q()
    for filtro in filtros:
        query = Q()
        if filtro.categoria:
            query.add(Q(socio__categoria__icontains=filtro.categoria), Q.AND)
        if filtro.fecha_socio_desde:
            query.add(Q(socio__fecha_ingreso__gte=filtro.fecha_socio_desde), Q.AND)
        if filtro.fecha_socio_hasta:
            query.add(Q(socio__fecha_ingreso__lte=filtro.fecha_socio_hasta), Q.AND)
        if filtro.fecha_nacimiento_desde:
            query.add(Q(socio__fecha_nacimiento__gte=filtro.fecha_nacimiento_desde), Q.AND)
        if filtro.fecha_nacimiento_hasta:
            query.add(Q(socio__fecha_nacimiento__lte=filtro.fecha_nacimiento_hasta), Q.AND)
        if filtro.codigo_postal:
            query.add(Q(codigo_postal__icontains=filtro.codigo_postal), Q.AND)
        if filtro.ciudad:
            query.add(Q(ciudad__icontains=filtro.ciudad), Q.AND)
        if filtro.partido:
            query.add(Q(partido__icontains=filtro.partido), Q.AND)
        if filtro.provincia:
            query.add(Q(provincia__icontains=filtro.provincia), Q.AND)

        querys.add(query, Q.OR)

    querys.add(Q(activo=True), Q.AND)
    return querys

def get_custom_filter(filters):
    query = Q()
    for field, value in filters.form_instance.data.items():
        if not value == '':
            print(field)
            print(value)
            if field == 'calle':
                query.add(Q(socio__categoria__icontains=value), Q.AND)
            if field == 'categoria':
                query.add(Q(socio__categoria__icontains=Categorias.objects.filter(pk=value).first()), Q.AND)
            if field == 'fecha_socio_desde':
                query.add(Q(socio__fecha_ingreso__gte=value), Q.AND)
            if field == 'fecha_socio_hasta':
                query.add(Q(socio__fecha_ingreso__lte=value), Q.AND)
            if field == 'fecha_nacimiento_desde':
                query.add(Q(socio__fecha_nacimiento__gte=value), Q.AND)
            if field == 'fecha_nacimiento_hasta':
                query.add(Q(socio__fecha_nacimiento__lte=value), Q.AND)
            if field == 'codigo_postal':
                query.add(Q(codigo_postal__icontains=value), Q.AND)
            if field == 'ciudad':
                query.add(Q(ciudad__icontains=value), Q.AND)
            if field == 'partido':
                query.add(Q(partido__icontains=value), Q.AND)
            if field == 'provincia':
                query.add(Q(provincia__icontains=value), Q.AND)
    query.add(Q(activo=True), Q.AND)
    return query



class Listado_Socios_PDF(TemplateView):
    template_name = 'reportes/listado_socios_pdf.html'

    def get(self, request, *args, **kwargs):
        html_string = render_to_string(self.template_name, self.get_context_data())
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()

        response = HttpResponse(content_type='application/pdf;')
        filename = 'Listado_Socios.pdf'
        response['Content-Disposition'] = 'inline; filename=%s' % filename
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
        return response

    def get_context_data(self, **kwargs):
        context = super(Listado_Socios_PDF, self).get_context_data()
        _id = self.kwargs.get('pk')
        queryset = get_user_queryset(self.request.user, Domicilios.objects)
        queryset = queryset.order_by('codigo_postal', 'ciudad', 'calle')
        context['Direcciones'] = queryset
        return context




