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

class Personas(BaseModel):
    apellidos = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=10)
    numero_documento = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', null=True)
    estado_civil = models.CharField(max_length=20, verbose_name='Estado Civil')

    class Meta:
        abstract = True
        unique_together = (('tipo_documento', 'numero_documento'),)


class Socios(Personas):
    nro_socio = models.CharField(max_length=10, verbose_name='Numero de Socio')
    categoria = models.CharField(max_length=20, verbose_name='Categoria')
    fecha_ingreso = models.DateField(verbose_name='Fecha de Ingreso', null=True)
    fecha_baja = models.DateField(verbose_name='Fecha de Baja', null=True)
    ucp = models.CharField(max_length=10, verbose_name='Ultima cuota paga', null=True)
    estado = models.CharField(max_length=20, verbose_name='Estado', default='')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        ordering = ['fecha_ingreso']

    def __str__(self):
        return self.nro_socio


class Emails(BaseModel):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, blank=True, related_name='Emails')
    email = models.CharField(max_length=200)
    chequeado = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

class Telefonos(BaseModel):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, blank=True, related_name='Telefonos')
    telefono = models.CharField(max_length=20)
    chequeado = models.BooleanField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Telefono'
        verbose_name_plural = 'Telefonos'

class Domicilios(BaseModel):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, blank=True, related_name='Domicilios')
    tipo = models.CharField(max_length=15, null=True, blank=False, choices=TIPO_DOMICILIO, default='PARTICULAR')
    calle = models.CharField(max_length=50)
    numero = models.CharField(max_length=6)
    piso = models.CharField(max_length=10, verbose_name='Piso')
    departamento = models.CharField(max_length=3, verbose_name='Dpto')
    otro = models.CharField(max_length=50, verbose_name='Datos Adicionales')
    barrio = models.CharField(max_length=50, verbose_name='Barrio')
    ciudad = models.CharField(max_length=50, verbose_name='Ciudad/localidad')
    partido = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Domicilio'
        verbose_name_plural = 'Domicilios'

class Comentarios(BaseModel):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, blank=True, related_name='Comentarios')
    comentario = models.TextField(max_length=500,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='Comentarios')

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return self.comentario


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
