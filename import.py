from socios.models import Socios, Domicilios, Personas

def procesar():
    with open('padron_bkp.csv') as file:
        lines = file.readlines()
    total = 7923
    en_padron = 0
    for line in lines[total:]:
        print(total)
        line = line.replace('\n','')
        total += 1
        campos = line.split(';')
        nro_socio = campos[2]
        nro_documento = campos[5]
        nombre_completo = campos[4]
        parts_nombre = nombre_completo.split(' ')
        nombre = ''
        apellido = ''
        for part in parts_nombre:
            if part.isupper():
                apellido = f'{apellido} {part}'
            else:
                nombre =  f'{nombre} {part}'

        direccion_completa = campos[6].split(',')
        if len(direccion_completa) > 2:
            direccion = direccion_completa[0]
            localidad = direccion_completa[1]
            provincia = direccion_completa[2]
        else:
            direccion = direccion_completa[0]
            localidad = ''
            provincia = ''

        socio_padron = Socios.objects.filter(numero_documento__icontains=nro_documento).first()

        if socio_padron:
            en_padron += 1
            socio_padron.padron = True
            socio_padron.categoria = f'{socio_padron.categoria} ({campos[3]})'
            socio_padron.save()
        else:
            socio = Socios()
            socio.apellidos = apellido
            socio.nombres = nombre
            socio.ucp = campos[7]
            socio.categoria = campos[3]
            socio.numero_documento = nro_documento
            socio.fecha_nacimiento = '1900-01-01'
            socio.nro_socio = nro_socio
            socio.padron = True
            socio.save()
