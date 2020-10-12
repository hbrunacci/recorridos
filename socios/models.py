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

        def __str__(self):
            return self.apellidos + ' ' + self.nombres

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

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:

            fname = f.name
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_' + fname + '_display'
            if hasattr(self, get_choice):
                value = getattr(self, get_choice)()
            else:
                try:
                    value = getattr(self, fname)
                except AttributeError:
                    value = None

            # only display fields with values and skip some fields entirely
            if f.editable and value and f.name not in ('id', 'status', 'workshop', 'user', 'complete'):
                fields.append(
                    {
                        'label': f.verbose_name,
                        'name': f.name,
                        'value': value,
                    }
                )
        return fields


class Emails(BaseModel):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, blank=True, related_name='emails')
    email = models.CharField(max_length=200)
    chequeado = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        ordering = ['chequeado']


    def __str__(self):
        return self.email


class Telefonos(BaseModel):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, blank=True, related_name='telefonos')
    telefono = models.CharField(max_length=20)
    chequeado = models.BooleanField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Telefono'
        verbose_name_plural = 'Telefonos'
        ordering = ['chequeado']

    def __str__(self):
        return self.telefono

class Domicilios(BaseModel):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, blank=True, related_name='domicilio')
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
        ordering = ['codigo_postal', '-calle']

    def __str__(self):
        return F'{self.calle} {self.numero} {self.piso} {self.departamento}'

    def __unicode__(self):
        return self.calle


class Comentarios(BaseModel):
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE, blank=True, related_name='comentarios')
    comentario = models.TextField(max_length=500,blank=True, null=True)
    nosocio = models.BooleanField(default=False, blank=True, null=True, verbose_name='No es mas socio')
    fallecido = models.BooleanField(default=False, blank=True, null=True, verbose_name='El socio fallecio')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='comentarios')

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['pk']

    def __str__(self):
        return self.comentario

    def save(self, *args, **kwargs):
        super(Comentarios, self).save(*args, **kwargs)


class Categorias(BaseModel):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion

class Filtro(BaseModel):
    nombre_filtro = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, blank=True, null=True)
    fecha_nacimiento_desde = models.DateField(null=True, blank=True)
    fecha_nacimiento_hasta = models.DateField(null=True, blank=True)
    fecha_socio_desde = models.DateField(null=True, blank=True)
    fecha_socio_hasta = models.DateField(null=True, blank=True)
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)
    ciudad = models.CharField(max_length=35, null=True,blank=True)
    partido = models.CharField(max_length=35, null=True,blank=True)
    provincia = models.CharField(max_length=35, null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Filtros'
        verbose_name = 'Filtro'
        ordering = ['-usuario']

    def __str__(self):
        return self.nombre_filtro
