from django import forms
from .models import Evento, Entrada, Tarifa, LimiteReserva, Pedido
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML

from django.utils.translation import ugettext_lazy as _
from cruds_adminlte import (DatePickerWidget,
                            TimePickerWidget,
                            DateTimePickerWidget,
                            ColorPickerWidget,
                            CKEditorWidget)


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha']

    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('nombre', wrapper_class="col-md-12"),
            Field('fecha', wrapper_class="col-md-12"),
        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Aceptar'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                                href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )


class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['evento', 'nombre', 'valor']

    def __init__(self, *args, **kwargs):
        super(TarifaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('evento', wrapper_class="col-md-12"),
            Field('nombre', wrapper_class="col-md-12"),
            Field('valor', wrapper_class="col-md-12"),
            )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Aceptar'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )


class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['evento','tarifa','nombre_destinatario','dni_destinatario','nro_socio_destinatario',]
    def __init__(self, *args, **kwargs):
        super(EntradaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('evento', wrapper_class="col-md-12"),
            Field('tarifa', wrapper_class="col-md-12"),
            Field('nombre_destinatario', wrapper_class="col-md-12"),
            Field('dni_destinatario', wrapper_class="col-md-12"),
            Field('nro_socio_destinatario', wrapper_class="col-md-12"),

        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Aceptar'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )


class LimiteReservaForm(forms.ModelForm):
    class Meta:
        model = LimiteReserva
        fields = ['evento', 'usuario', 'tarifa', 'cantidad']

    def __init__(self, *args, **kwargs):
        super(LimiteReservaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('evento', wrapper_class="col-md-12"),
            Field('usuario', wrapper_class="col-md-12"),
            Field('tarifa', wrapper_class="col-md-12"),
            Field('cantidad', wrapper_class="col-md-12"),

        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Aceptar'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )

class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['user', 'evento']

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('user', wrapper_class="col-md-12"),
            Field('evento', wrapper_class="col-md-12"),
        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Aceptar'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )
