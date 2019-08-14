from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group

# Create your models here.

TIPO_DOCUMENTOS = [('DNI', 'DNI'),
                   ]


TIPO_DOMICILIO = [
    ('PARTICULAR', 'PARTICULAR'),
    ('FISCAL', 'FISCAL'),
    ('CASA MATRIZ', 'CASA MATRIZ'),
    ('COMERCIAL', 'COMERCIAL')
]

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(editable=False,
                                        default=timezone.now)
    update_date = models.DateTimeField(editable=False,
                                       default=timezone.now)
    export_date = models.DateTimeField(editable=False,
                                       blank=True, null=True)

    class Meta:
        abstract = True

class Domicilio(BaseModel):
    tipo = models.CharField(max_length=15, null=True, blank=False, choices=TIPO_DOMICILIO, default='FISCAL')
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=6)
    piso = models.CharField(max_length=3, verbose_name='Piso')
    departamento = models.CharField(max_length=3, verbose_name='Dpto')
    otro = models.CharField(max_length=50, verbose_name='Datos Adicionales')
    barrio = models.CharField(max_length=50, verbose_name='Barrio')
    ciudad = models.CharField(max_length=50, verbose_name='Ciudad/localidad')
    partido = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=50)


class Personas(BaseModel):
    apellidos = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=10)
    numero_documento = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    domicilio_particular = models.OneToOneField(Domicilio, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, verbose_name='Telefono Celular')
    telefono_aux = models.CharField(max_length=15, verbose_name='Telefono Alternativo')
    email = models.CharField(max_length=60, verbose_name='Email')

    class Meta:
        abstract = True
        unique_together = (('tipo_documento', 'numero_documento'),)


class Socios(Personas):
    nro_socio = models.CharField(max_length=10, verbose_name='Numero de Socio')
    categoria = models.CharField(max_length=20, verbose_name='Categoria')
    fecha_ingreso = models.DateField(verbose_name='Fecha de Ingreso')
    comentarios = models.TextField()

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'

class Categorias(BaseModel):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion

class Filtro(BaseModel):
    nombre_filtro = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, blank=True)
    fecha_nacimiento_desde = models.DateField(null=True, blank=True)
    fecha_nacimiento_hasta = models.DateField(null=True, blank=True)
    fecha_socio_desde = models.DateField(null=True, blank=True)
    fecha_socio_hasta = models.DateField(null=True, blank=True)
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Filtros'
        verbose_name = 'Filtro'
        ordering = ['-usuario']
