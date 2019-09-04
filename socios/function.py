from .models import *
from datetime import datetime

def traer_datos_socios(archivo):
    datos = []
    path = '/home/hb/Documentos/Diego Franco/%s' % archivo
    with open(path, 'r', encoding='utf-8-sig') as datos_archivo:
        for linea in datos_archivo:
            datos.append(linea.strip('/n').strip('\n').split(','))
    return datos


def importar_domicilios(datos):
    x = 0
    for campo in datos[1:]:
        x += 1
        try:
            new_socio, created = Socios.objects.get_or_create(nro_socio=campo[0])
            if not created:
                new_object = Domicilios()
                new_object.socio = new_socio #0 sexonro
                new_object.calle = campo[1] #1 direccion
                new_object.nro_socio = campo[2] #2 nro
                new_object.piso = campo[3] #3 pisoDpto
                new_object.partido = campo[4] #4 partido
                new_object.ciudad = campo[5] #5 localidad
                new_object.provincia = campo[6] #6 provincia
                new_object.codigo_postal = campo[7] #7 cpostal
                new_object.barrio = campo[9] #9 barrio
                new_object.chequeado = campo[12] #12 chequeado
                new_object.activo = campo[14] #14 activo
                new_object.save()
                if x%5000 == 0:
                    print(x)
        except:
            print(x)
            print(campo)

                #     print('---------------- Error ---------------')
        #     pass

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
    for campo in socios[1:-1]:

        try:
            print(x)
            print(campo)
            new_socio, created = Socios.objects.get_or_create(nro_socio=campo[0])
            if created:
                creados += 1
            else:
                actualizados +=1
            new_socio.apellidos =campo[1] #apenom
            new_socio.tipo_documento =campo[2] #tipodoc
            new_socio.numero_documento =campo[3] #nrodoc
            new_socio.estado_civil =campo[4] #ecivil
            campo[5] = '1900-01-01' if campo[5] == 'NULL' else datetime.strptime(campo[5][:-4], '%Y-%m-%d %H:%M:%S').date()
            campo[6] = '1900-01-01' if campo[6] == 'NULL' else datetime.strptime(campo[6][:-4], '%Y-%m-%d %H:%M:%S').date()
            campo[7] = '1900-01-01' if campo[7] == 'NULL' else datetime.strptime(campo[7][:-4], '%Y-%m-%d %H:%M:%S').date()
            new_socio.fecha_nacimiento = campo[5] #fnacimiento
            new_socio.fecha_ingreso =campo[6]#fechaingreso
            new_socio.fecha_baja = campo[7] #fechabaja
            new_socio.estado =campo[8] #estado
            new_socio.categoria =campo[9] #categoria
            new_socio.ucp =campo[10] #UCP
            new_socio.activo =campo[12] #activo
            new_socio.save()
        except:
            errores.append(campo[0])
        x += 1
    print('Creados %i' % creados)
    print('Actualizados %i' % actualizados)

