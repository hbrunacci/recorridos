from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML
from django import forms
from django.utils.translation import ugettext_lazy as _
from image_cropping import ImageCropWidget

from cruds_adminlte import (DatePickerWidget,
                            TimePickerWidget,
                            DateTimePickerWidget,
                            ColorPickerWidget,
                            CKEditorWidget)

from .models import Domicilio,Socios


class DomicilioForm(forms.ModelForm):

    class Meta:
        model = Domicilio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DomicilioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('tipo', wrapper_class="col-md-4"),
            Field('calle ', wrapper_class="col-md-4"),
            Field('numero', wrapper_class="col-md-4"),
            Field('piso', wrapper_class="col-md-4"),
            Field('departamento', wrapper_class="col-md-4"),
            Field('otro', wrapper_class="col-md-4"),
            Field('barrio', wrapper_class="col-md-4"),
            Field('ciudad', wrapper_class="col-md-4"),
            Field('partido', wrapper_class="col-md-4"),
            Field('provincia', wrapper_class="col-md-4"),
            Field('codigo_postal', wrapper_class="col-md-4"),

        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Submit'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )


class SociosForm(forms.ModelForm):

    class Meta:
        model = Socios
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SociosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field('nro_socio', wrapper_class="col-md-4"),
            Field('apellidos', wrapper_class="col-md-4"),
            Field('nombres ', wrapper_class="col-md-4"),
            Field('tipo_documento ', wrapper_class="col-md-4"),
            Field('numero_documento ', wrapper_class="col-md-4"),
            Field('categoria', wrapper_class="col-md-4"),
            Field('fecha_nacimiento ', wrapper_class="col-md-4"),
            Field('fecha_ingreso', wrapper_class="col-md-4"),
            Field('domicilio_particular ', wrapper_class="col-md-4"),
            Field('telefono ', wrapper_class="col-md-4"),
            Field('telefono_aux ', wrapper_class="col-md-4"),
            Field('email', wrapper_class="col-md-4"),
        )

        self.helper.layout.append(
            FormActions(
                Submit('submit', _('Submit'), css_class='btn btn-primary'),
                HTML("""{% load i18n %}<a class="btn btn-danger"
                        href="{{ url_delete }}">{% trans 'Delete' %}</a>"""),
            )
        )


