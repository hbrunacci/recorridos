from __future__ import unicode_literals


from cruds_adminlte.crud import CRUDView
from cruds_adminlte.inline_crud import InlineAjaxCRUD
from django.utils.translation import ugettext_lazy as _

from .models import Evento, Entrada, Tarifa, LimiteReserva, Pedido
import datetime

from django.views.generic.base import TemplateView

from .forms import EventoForm, EntradaForm, TarifaForm, LimiteReservaForm, PedidoForm

from django.http.response import HttpResponse


from django.template.loader import render_to_string
from weasyprint import HTML,CSS
import tempfile







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
    template_name_base = 'eventos'


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
    list_fields = ['evento', 'tarifa', 'nombre_destinatario', 'dni_destinatario', 'nro_socio_destinatario',]
    update_form = EntradaForm
    add_form = EntradaForm
    paginate_by = 20
    paginate_position = 'Bottom'  # Both | Bottom
    paginate_template = 'cruds/pagination/enumeration.html'
    inlines = []
    views_available =['create', 'list', 'update', 'delete' ]


class Detalle_Pedidos_PDF(TemplateView):
    template_name = 'reportes/detalle_pedidos_pdf.html'

    def get(self, request, *args, **kwargs):
        html_string = render_to_string(self.template_name, self.get_context_data())
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()

        response = HttpResponse(content_type='application/pdf;')
        filename = 'OT_apellido_paciente_nro.pdf'
        response['Content-Disposition'] = 'inline; filename=%s' % filename
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response

    def get_context_data(self, **kwargs):
        context = super(Detalle_Pedidos_PDF, self).get_context_data()
        _id = self.kwargs.get('pk')
        eventos = Evento.objects.all()
        if _id:
            eventos = eventos.filter(id=_id)
        context['eventos'] = eventos.order_by('fecha')

        return context
