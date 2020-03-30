from __future__ import unicode_literals

from django.contrib.auth.models import User

from cruds_adminlte.crud import CRUDView, get_filters
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from django.utils.translation import ugettext_lazy as _
from cruds_adminlte.filter import FormFilter

from .models import Evento, Entrada, Tarifa, LimiteReserva, Pedido
import datetime

from django.views.generic.base import TemplateView
from django.db.models import Q
from django import forms

from .forms import EventoForm, EntradaForm, TarifaForm, LimiteReservaForm, PedidoForm

from django.http.response import HttpResponse
from cruds_adminlte.templatetags.crud_tags import crud_inline_url



class Tarifas_Ajax(InlineAjaxCRUD):
    model = Tarifa
    base_model = Evento
    add_form = TarifaForm
    update_form = TarifaForm
    inline_field = 'evento'
    title = _("Tarifas Disponibles ")


class Limites_Reserva_Ajax(InlineAjaxCRUD):
    model = LimiteReserva
    base_model = Evento
    add_form = LimiteReservaForm
    update_form = LimiteReservaForm
    inline_field = 'evento'
    title = _("Limites de Reservas")

class EventoCRUD(CRUDView):
    model = Evento
    list_fields = ['nombre', 'fecha']
    update_form = EventoForm
    add_form = EventoForm
    paginate_by = 20
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = [Tarifas_Ajax, Limites_Reserva_Ajax]
    views_available = ['create', 'list', 'update', 'delete']


class TarifaCRUD(CRUDView):
    model = Tarifa
    related_fields = []
    list_fields = ['evento', 'nombre', 'valor']
    update_form = TarifaForm
    add_form = TarifaForm
    paginate_by = 20
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = []
    views_available =['create','list', 'update','delete' ]


class LimiteReservaCRUD(CRUDView):
    model = LimiteReserva
    related_fields = []
    list_fields = ['evento', 'usuario', 'tarifa', 'cantidad']
    update_form = LimiteReservaForm
    add_form = LimiteReservaForm
    paginate_by = 20
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = []
    views_available =['create', 'list', 'update', 'delete' ]


class Entradas_Ajax(InlineAjaxCRUD):
    model = Entrada
    base_model = Pedido
    add_form = EntradaForm
    update_form = EntradaForm
    list_fields = ['evento', 'tarifa', 'nombre_destinatario', 'dni_destinatario', 'nro_socio_destinatario', ]
    inline_field = 'pedido'
    title = _("Entradas pedidas")


class PedidoCRUD(CRUDView):
    model = Pedido
    related_fields = []
    list_fields = ['evento', 'user', 'cantidad_tickets', 'monto_total']
    update_form = PedidoForm
    add_form = PedidoForm
    paginate_by = 20
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = [Entradas_Ajax]
    views_available = ['create', 'list', 'update', 'delete' ]
    list_filter = ['evento']

    def get_create_view(self):
        TempCreateViewClass = super(PedidoCRUD, self).get_create_view()

        class CreateViewClass(TempCreateViewClass):

            def get_context_data(self):
                context = super(CreateViewClass, self).get_context_data()
                user = self.request.user
                context['form'].fields['user'].queryset =  context['form'].fields['user'].queryset.filter(id=user.id)
                context['form'].fields['user'].initial = context['form'].fields['user'].queryset[0]
                context['form'].fields['evento'].queryset = context['form'].fields['evento']\
                    .queryset.filter(fecha__gt=datetime.date.today())
                context['form'].fields['evento'].initial = context['form'].fields['evento'].queryset[0]

                return context

        return CreateViewClass

    def get_list_view(self):
        TempListViewClass = super(PedidoCRUD, self).get_list_view()

        class ListViewClass(TempListViewClass):
            text_fields = ['calle', 'socio__categoria']


            def get_queryset(self):
                usuario = self.request.user
                queryset = super(ListViewClass, self).get_queryset()
                if not (usuario.is_staff or usuario.groups.filter(name__in=['Admin Reservas']).exists()):
                    queryset = queryset.filter(user_id=usuario.id)
                for item in queryset:
                    result = item.update_quantities_amounts()

                return queryset

        return ListViewClass




class EntradaCRUD(CRUDView):
    model = Entrada
    related_fields = []
    list_fields = ['evento','tarifa','nombre_destinatario','dni_destinatario','nro_socio_destinatario',]
    update_form = EntradaForm
    add_form = EntradaForm
    paginate_by = 20
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = []
    views_available =['create','list', 'update','delete' ]

class ReportePedidosPDF(TemplateView):
    template_name = 'reportes/'