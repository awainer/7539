from backend.models import *
from random import randint
from django.utils import timezone
from math import ceil
import random

MIN_CAPACIDAD = 15
MAX_CAPACIDAD = 100

MIN_CANALES_ATENCION = 4
MAX_CANALES_ATENCION = 8

MIN_PASO_SEGUNDOS = 25  # De 1 y 59
MAX_PASO_SEGUNDOS = 60

# En minutos:
MIN_TIEMPO_ATENCION = 15
MAX_TIEMPO_ATENCION = 30

TOTAL_DIAS = 30 

SEGUNDOS = 60

SE_ATIENDE = 95
SE_CAMBIA = 97
SE_VA = 100

ESPECIALIDADES = Specialty.objects.all()


def get_hospitales():
    return HealthCenter.objects.all()


def get_colas_de_atencion():
    return AtentionQueue.objects.all()


def eliminar_todas_las_colas_de_atencion():
    AtentionQueue.objects.all().delete()
    print("Se eliminaron las colas de atencion")


def eliminar_todos_los_pacientes():
    Patient.objects.all().delete()
    print("Se eliminaron los pacientes")


def eliminar_todos_los_registros_atencion():
    AttentionRecord.objects.all().delete()
    print("Se eliminaron los registros de atencion")


def limpiar_base_de_datos():
    print("Comenzando limpieza de la base...")
    eliminar_todos_los_registros_atencion()
    eliminar_todos_los_pacientes()
    eliminar_todas_las_colas_de_atencion()
    print("--- Finalizo la limpieza de la base --- ")


def get_prioridades():
    return TriageScaleLevel.objects.all()


def get_motivos_de_salida():
    return DeleteReason.objects.all()


def generar_nuevas_colas():
    hospitales = get_hospitales()
    generar_colas(hospitales, ESPECIALIDADES)
    print("Colas generadas!")


def generar_colas(hospitales, especialidades):
    for hospital in hospitales:
        for especialidad in especialidades:
            capacidad = randint(MIN_CAPACIDAD, MAX_CAPACIDAD)
            generar_cola(hospital, especialidad, capacidad)


def generar_cola(hospital, especialidad, capacidad):
    nombre = "{} - {} - Capacidad: {}"
    descripcion = nombre.format(hospital.name, especialidad.name, capacidad)

    cola = AtentionQueue()
    cola.health_center = hospital
    cola.specialty = especialidad
    cola.description = descripcion
    cola.max_capacity = capacidad
    cola.attention_channels = randint(MIN_CANALES_ATENCION, MAX_CANALES_ATENCION)

    cola.save()


def generar_fecha(dias, minutos):
    zona_horaria = timezone.pytz.timezone('America/Argentina/Buenos_Aires')
    fecha_inicial = timezone.datetime(2016, 11, 25, 0, 0, 0, 0, tzinfo=zona_horaria)
    fecha = fecha_inicial + timezone.timedelta(days=dias)
    fecha = fecha + timezone.timedelta(minutes=minutos)
    return fecha

from django.db import transaction
@transaction.atomic
def generar_pacientes(cola_hospital, colas_por_prioridad):
    msj = "Comienza la creación de pacientes para {}".format(cola_hospital.description)
    print(msj)

    for dias in range(TOTAL_DIAS):  # Por cada dia que se quiere simular
        l_minutos = list(filter(lambda x: x > 0 and x < 60*24 , [random.normalvariate(15*60,4*60) for _ in range(150)  ]))
        l_minutos.sort()
        for minutos in l_minutos:
            fecha = generar_fecha(dias, minutos)
            print(("Se crea un paciente el dia {}".format(fecha)))
            generar_paciente(cola_hospital, colas_por_prioridad, fecha)


def generar_paciente(cola_hospital, colas_por_prioridad, fecha):
    prioridades = get_prioridades()
    prioridad = randint(0, len(prioridades) - 1)

    paciente = Patient()
    paciente.triageScale = prioridades[prioridad]
    paciente.startTime = fecha
    paciente.queue = cola_hospital

    paciente.save()
    colas_por_prioridad[prioridad].append(paciente)


def todas_colas_vacias(colas):
    for cola in colas:
        if len(cola) > 0:
            return False
    return True


def get_proximo_paciente(colas_por_prioridad, hora_actual):
    for cola in colas_por_prioridad:
        if not cola:
            continue
        paciente = cola[0]
        if (paciente.startTime <= hora_actual):
            return quitar_primer_paciente(cola)

    return get_primer_paciente_mejor_prioridad(colas_por_prioridad)


def quitar_primer_paciente(cola):
    if not cola:
        return None

    paciente = cola[0]
    cola.pop(0)
    return paciente


def get_primer_paciente_mejor_prioridad(colas_por_prioridad):
    tiempos = []
    for cola in colas_por_prioridad:
        tiempo = None if not cola else cola[0].startTime
        tiempos.append(tiempo)

    min_i = 0
    for i in range(1, len(tiempos)):
        if (tiempos[i]):
            if (not tiempos[min_i] or (tiempos[i] < tiempos[min_i])):
                min_i = i

    return quitar_primer_paciente(colas_por_prioridad[min_i])


def get_tiempo_atencion():
    return randint(MIN_TIEMPO_ATENCION, MAX_TIEMPO_ATENCION)


def get_motivo_salida():
    motivos = get_motivos_de_salida()
    motivo = randint(0, 99)  # Probabilidad

    if motivo < SE_ATIENDE:
        return motivos[0]

    if motivo < SE_CAMBIA:
        return motivos[1]

    return motivos[2]  # se va


def generar_registro_atencion(cola, paciente, motivo_salida, tiempo):
    registro = AttentionRecord()
    registro.health_center = cola.health_center
    registro.queue = cola
    registro.patient = paciente
    registro.reason = motivo_salida
    registro.startTime = paciente.startTime
    registro.endTime = paciente.endTime
    registro.waitTime = tiempo
    registro.triageScale = paciente.triageScale
    registro.save()
    imprimir_registro(cola, paciente, motivo_salida, tiempo)


def imprimir_registro(cola, paciente, motivo_salida, tiempo):
    msj = "{} - {} - Espero {} minutos"
    msj = msj.format(paciente.startTime, paciente.endTime, tiempo)
    msj += "- Se retiro un paciente de {} con motivo {}"
    msj = msj.format(paciente.triageScale.description, motivo_salida)
    print(msj)


def actualizar_salida(paciente, minutos_espera):
    fechaFin = paciente.startTime + timezone.timedelta(minutes=minutos_espera)
    paciente.endTime = fechaFin
    paciente.save()


def calcular_minutos_espera(fecha_inicio, fecha_fin):
    diferencia = fecha_fin - fecha_inicio
    return ceil(diferencia.seconds / SEGUNDOS)


def atender_paciente(paciente, tiempo_actual):
    if (not paciente):
        return 0

    cola = paciente.queue
    paciente.queue = None
    minutos_espera = calcular_minutos_espera(paciente.startTime, tiempo_actual)
    motivo_salida = get_motivo_salida()
    actualizar_salida(paciente, minutos_espera)
    cola.atention_time_total += (minutos_espera * SEGUNDOS)
    cola.atention_count += 1
    cola.save()
    generar_registro_atencion(cola, paciente, motivo_salida, minutos_espera)
    return get_tiempo_atencion()


PACIENTE = 0
TIEMPO = 1


@transaction.atomic
def atender_pacientes(cola_hospital, colas_por_prioridad):
    pacientes_por_canal = []
    cant_canales = cola_hospital.attention_channels

    print(("Se simula la atencion de {} con {} canales".format(cola_hospital.description, cant_canales)))

    # Cada canal atiende a su primer paciente
    for i in range(cant_canales):
        paciente = get_primer_paciente_mejor_prioridad(colas_por_prioridad)
        tiempo_atencion = atender_paciente(paciente, paciente.startTime)
        pacientes_por_canal.append([paciente, tiempo_atencion])

    #Atender todos los pacientes_restantes
    while not todas_colas_vacias(colas_por_prioridad):
        for i in range(cant_canales):
            paciente_anterior = pacientes_por_canal[i][PACIENTE]
            if (not paciente_anterior):
                continue
            tiempo_anterior = pacientes_por_canal[i][TIEMPO]
            hora_actual = paciente_anterior.endTime + timezone.timedelta(minutes=tiempo_anterior)
            paciente = get_proximo_paciente(colas_por_prioridad, hora_actual)
            if (paciente and paciente.startTime > hora_actual):
                hora_actual = paciente.startTime
            tiempo_atencion = atender_paciente(paciente, hora_actual)
            pacientes_por_canal[i][PACIENTE] = paciente
            pacientes_por_canal[i][TIEMPO] = tiempo_atencion


def simular_atencion_pacientes(cola_hospital):
    colas_por_prioridad = [[], [], [], [], []]  # En 0 la mejor prioridad
    generar_pacientes(cola_hospital, colas_por_prioridad)
    atender_pacientes(cola_hospital, colas_por_prioridad)


def main():
    print(" ---- Iniciando script de poblacion de datos ---- ")

    limpiar_base_de_datos()

    generar_nuevas_colas()

    colas = get_colas_de_atencion()
    for cola in colas:
        simular_atencion_pacientes(cola)

    print("Terminado")


main()
