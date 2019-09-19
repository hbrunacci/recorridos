from .models import *
from datetime import datetime
from collections import defaultdict
from django.apps import apps



class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size
        self.actual = 0

    def _commit(self, model_class):
        try:

            model_key = model_class._meta.label
            model_class.objects.bulk_create(self._create_queues[model_key])
            self._create_queues[model_key] = []
            return True
        except:
            self._create_queues[model_key] = []
            return False

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            if not self._commit(model_class):
                print('Error entre %s -> %s' % (self.actual, self.actual + self.chunk_size))
            self.actual += self.chunk_size
            print(self.actual)


    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))

def traer_datos_socios(archivo):
    datos = []
    path = '/home/primeroriver/django/recorridos/%s' % archivo
    with open(path, 'r', encoding='utf-8-sig') as datos_archivo:
        for linea in datos_archivo:
            datos.append(linea.strip('/n').strip('\n').split(','))
    return datos



def importar_domicilios(datos):
    x = 0
    bulk_mgr = BulkCreateManager(chunk_size=20)
    for campo in datos[1:]:
        try:
            x += 1
            new_socio = Socios.objects.get(nro_socio=campo[0])
            bulk_mgr.add(Domicilios(
                socio=new_socio
                , calle=campo[1]
                , numero=campo[2]
                , piso=campo[3]
                , partido=campo[4]
                , ciudad=campo[5]
                , provincia=campo[6]
                , codigo_postal=campo[7]
                , barrio=campo[9]
                , activo=campo[14]))
        except:
            print('---------------- Error ---------------')

def importar_emails(datos):
    x = 0
    for campo in datos[1:]:
        x += 1
        try:
            print(x)
            print(campo)
            new_socio, created = Socios.objects.get_or_create(nro_socio=campo[0])
            new_socio.save()
            new_email = Emails()
            new_email.socio = new_socio
            new_email.email = campo[1]
            new_email.chequeado = campo[2]
            new_email.activo = campo[4]
            new_email.save()
        except:
            print('---------------- Error ---------------')
            pass

def importar_telefonos(datos):
    x = 0
    data = []
    for campo in datos[250000:]:
        x += 1
        new_socio, created = Socios.objects.get_or_create(nro_socio=campo[0])
        if created:
            print(new_socio)
            new_socio.save()
        data.append(Telefonos.create(socio=new_socio, telefono=campo[1], chequeado=campo[3], activo=campo[4]))
        if x%5 == 0:
            print(data)
            Socios.objects.bulk_create(data)

def importar_socios(socios):
    x = 0
    errores = []
    creados = 0
    actualizados = 0
    bulk_mgr = BulkCreateManager(chunk_size=20)
    for campo in socios[1:-1]:

        try:
            campo[5] = '1900-01-01' if campo[5] == 'NULL' else datetime.strptime(campo[5][:-4],
                                                                                 '%Y-%m-%d %H:%M:%S').date()
            campo[6] = '1900-01-01' if campo[6] == 'NULL' else datetime.strptime(campo[6][:-4],
                                                                                 '%Y-%m-%d %H:%M:%S').date()
            campo[7] = '1900-01-01' if campo[7] == 'NULL' else datetime.strptime(campo[7][:-4],
                                                                                 '%Y-%m-%d %H:%M:%S').date()

            bulk_mgr.add(Socios(
                nro_socio=campo[0]
                ,apellidos =campo[1] #apenom
                ,tipo_documento =campo[2] #tipodoc
                ,numero_documento =campo[3] #nrodoc
                ,estado_civil =campo[4] #ecivil
                ,fecha_nacimiento = campo[5] #fnacimiento
                ,fecha_ingreso =campo[6]#fechaingreso
                ,fecha_baja = campo[7] #fechabaja
                ,estado =campo[8][0:24] #estado
                ,categoria =campo[9] #categoria
                ,ucp =campo[10] #UCP
                ,activo =campo[12] #activo
                ))
        except:
            errores.append(campo[0])
        x += 1
    bulk_mgr.done()



