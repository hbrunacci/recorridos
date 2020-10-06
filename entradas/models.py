from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group


# Create your models here.


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_date =models.DateTimeField(editable=False,
                                        default=timezone.now)
    update_date = models.DateTimeField(editable=False,
                                       default=timezone.now)
    export_date = models.DateTimeField(editable=False,
                                       blank=True, null=True)

    class Meta:
        abstract = True


class Evento(BaseModel):
    nombre = models.CharField(max_length=100, null=False)
    fecha = models.DateField(null=False)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['fecha', ]

    def __str__(self):
        return self.nombre


class Tarifa(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=False, blank=True, related_name='tarifas')
    nombre = models.CharField(max_length=100, null=False)
    valor = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = 'Tarifas'
        verbose_name = 'Tarifa'

    def __str__(self):
        return '%s %s' % (self.nombre, self.valor, )


class Pedido(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='pedidos')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=False, blank=True, related_name='pedidos')
    cantidad_tickets = models.IntegerField('Cantidad de tickets', default=0)
    monto_total = models.FloatField('Monto Total', default=0)

    def __str__(self):
        return F'Reserva para "{self.evento}" de {self.user}'

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['evento__pk', ]

    def get_resumen(self):
        return F'Entradas permitidas {self.get_total_permitidos()}, reservadas: {self.cantidad_tickets}'

    def get_total_permitidos(self):
        limites = LimiteReserva.objects.filter(evento=self.evento).filter(usuario=self.user)
        suma = 0
        for limite in limites:
            suma += limite.cantidad
        return suma

    def get_tarifas_disponibles(self):
        detalle = []
        limites = LimiteReserva.objects.filter(evento=self.evento).filter(usuario=self.user)
        for limite in limites:
            utilizado = self.entradas.filter(pedido=self, evento=self.evento, tarifa=limite.tarifa).count()
            if (limite.cantidad - utilizado) > 0:
                detalle.append({'tarifa': limite.tarifa,
                                'disponible': limite.cantidad - utilizado,
                                })
        return detalle

    def get_detalle_permitidos(self):
        detalle = []
        limites = LimiteReserva.objects.filter(evento=self.evento).filter(usuario=self.user)
        for limite in limites:
            utilizado = self.entradas.filter(pedido=self, evento=self.evento, tarifa=limite.tarifa).count()
            detalle.append({'tarifa': limite.tarifa.nombre,
                            'disponible': limite.cantidad,
                            'utilizado': utilizado})
        return detalle

    def get_(self):
        detalle = []
        limites = LimiteReserva.objects.filter(evento=self.evento).filter(usuario=self.user)
        for limite in limites:
            utilizado = self.entradas.filter(pedido=self, evento=self.evento, tarifa=limite.tarifa).count()
            detalle.append({'tarifa': limite.tarifa.nombre,
                                      'disponible': limite.cantidad,
                                      'utilizado': utilizado})
        return detalle


    def update_quantities_amounts(self):
        tickets = self.entradas.all()
        cantidad_tickets = 0
        monto_total = 0
        for ticket in tickets:
            monto_total += ticket.tarifa.valor
            cantidad_tickets += 1
        self.monto_total = monto_total
        self.cantidad_tickets = cantidad_tickets
        self.save()
        return True


class Entrada(BaseModel):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=False, blank=False, related_name='entradas')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=False, blank=False, related_name='entradas')
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE, null=False, blank=False, related_name='entradas')
    nombre_destinatario = models.CharField(max_length=50, null=False, blank=False)
    dni_destinatario = models.CharField(max_length=8, null=False, blank=False)
    nro_socio_destinatario = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['pk', ]
        unique_together = ('pedido','evento','dni_destinatario',)


class LimiteReserva(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=False, blank=True, related_name='limites')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False,related_name='limites')
    tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE, null=False, blank=False, related_name='limites')
    cantidad = models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Limites de Reservas'
        verbose_name = 'Limite de Reserva'
        ordering = ['pk', ]

    def __str__(self):
        return '%s %s' % (self.tarifa, self.cantidad)





