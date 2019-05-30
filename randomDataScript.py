import paho.mqtt.client as mqtt
import numpy as np
import json
import psycopg2 as pg2
import sys
import time as t
import datetime as dt
import random as r
import json
from faker import Faker

    #Tópicos de MQTT
canalCamarasAcceso = "camarasAcceso/0"
canalCamarasLocal = "camarasLocal/0"
canalBeaconAccesoEntrada = "beaconAccesoEntrada/0"
canalBeaconAccesoSalida = "beaconAccesoSalida/0"
canalBeaconLocalEntrada = "beaconLocalEntrada/0"
canalBeaconLocalSalida = "beaconLocalSalida/0"
canalMesa = "mesa/0"
canalMesaSensorOcupado = "mesaSensorOcupado/0"
canalMesaSensorDescupado = "mesaSensorDesocupado/0"
canalFactura = "factura/0"
canalRegistrarSmartphone = "registrarSmartphone/0"

################
    #Clases auxiliares
class Cliente:
    def __init__(self, ci, sexo, edad, nombre, id_smartphone):
        self.ci=ci
        self.sexo=sexo
        self.edad=edad
        self.nombre=nombre
        self.id_smartphone=id_smartphone

class DataMaestra:
    def __init__(self, id):
        self.id=id

class ClienteMqtt:
    def __init__(self, id):
        self.id=id
        self.mqtt_client=mqtt.Client(client_id=str(id))
    
    def connect_to_broker(self):
        self.mqtt_client.connect(host='127.0.0.1', port=1883)
        self.mqtt_client.loop_start()

################
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Conexión exitosa")
    else:
        print("Error de conexión, código: "+rc)

def connect_to_db():
        #Conexión a la db
    global conn 
    conn = pg2.connect(dbname="sambilProyecto", user="postgres", password="1234")
        #Cursor para operar
    global cur 
    cur = conn.cursor()

#Instanciar smartphones existentes
def instanciateSmartphones(smartphonesQtty, existingSmartphones):
    cur.execute("SELECT id FROM smartphone;")
    aux = cur.fetchall()
    for x in aux:
        existingSmartphones.append(x[0])

    smartphonesQtty = len(existingSmartphones)

#Instanciar cámaras y conectarlas al broker
def instanciateCamaras(camarasAcceso, camarasLocal):
    cur.execute("SELECT id FROM camara;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=ClienteMqtt(x[0])
        toInsert.connect_to_broker()
        if(toInsert.id <= 3 ):
            camarasAcceso.append(toInsert)
        else:
            camarasLocal.append(toInsert)

#Instanciar cámaras y conectarlos al broker
def instanciateSensores(sensores):
    cur.execute("SELECT id FROM sensormesa;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=ClienteMqtt(x[0])
        toInsert.connect_to_broker()
        sensores.append(toInsert)

#Instanciar beacons y conectarlos al broker
def instanciateBeacons(beaconsAcceso, beaconsLocal):
    cur.execute("SELECT id FROM beacon;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=ClienteMqtt(x[0])
        toInsert.connect_to_broker()
        if(x[0] <= 3):
            beaconsAcceso.append(toInsert)
        else:
            beaconsLocal.append(toInsert)

#Instanciar puertas
def instanciatePuertas(puertas):
    cur.execute("SELECT numero FROM puerta;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=DataMaestra(x[0])
        puertas.append(toInsert)

#Instanciar locales
def instanciateLocales(locales):
    cur.execute("SELECT id FROM local;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=DataMaestra(x[0])
        locales.append(toInsert)

#Instanciar mesas
def instanciateMesas(mesas):
    cur.execute("SELECT id FROM mesa;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=DataMaestra(x[0])
        mesas.append(toInsert)

#Registro de un nuevo smartphone
def register_smartphone(smartphone):
    x={
        "id": (smartphone+100)
    }
    y=json.dumps(x)
    sensores[0].mqtt_client.publish(canalRegistrarSmartphone,y)
    t.sleep(1)

#Publish al acceso por una puerta
def publish_access(camaraAcceso, cliente, puerta, fecha):
    minutes=r.randint(0,15)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "sexo": cliente.sexo,
        "edad": cliente.edad,
        "fechaAcceso": str(fechaAcceso),
        "idpuerta": puerta.id,
        "idcamara": camaraAcceso.id
    }
    y=json.dumps(x)
    camaraAcceso.mqtt_client.publish(canalCamarasAcceso,y)

#Publicar salida por una puerta
def publish_salida_puerta(camaraAcceso, cliente, puerta, fecha):
    minutes=r.randint(30,59)
    fechaSalida=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "sexo": cliente.sexo,
        "edad": cliente.edad,
        "fechaAcceso": str(fechaSalida),
        "idpuerta": puerta.id,
        "idcamara": camaraAcceso.id
    }
    y=json.dumps(x)
    camaraAcceso.mqtt_client.publish(canalCamarasAcceso,y)

#Publish al comienzo de la estadia de alguien con smartphone
def publish_start_estadia(beaconEntrada, smartphone, puerta, fecha):
    minutes=r.randint(0,15)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idbeaconetrada": beaconEntrada.id,
        "idbeaconsalida": None,
        "fechaentrada":str(fechaAcceso),
        "fechasalida": None,
        "idpuertaentrada": puerta.id,
        "idpuertasalida": None
    }
    y=json.dumps(x)
    beaconEntrada.mqtt_client.publish(canalBeaconLocalEntrada,y)

#Publish al salir un smartphone del centro comercial
def publish_finish_estadia(beaconSalida, smartphone, puerta, fecha):
    minutes=r.randint(30,59)
    fechaSalida=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idbeaconsalida": beaconSalida.id,
        "fechasalida": str(fechaSalida),
        "idpuertasalida": puerta.id
    }
    y=json.dumps(x)
    beaconSalida.mqtt_client.publish(canalBeaconLocalEntrada,y)

#Persona ingresa a una tienda
def publish_acceso_tienda_entrada(cliente, local, camara, fecha):
    minutes=r.randint(15,30)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "sexo": cliente.sexo,
        "edad": cliente.edad,
        "fechaacceso": str(fechaAcceso),
        "idcamara": camara.id,
        "idlocal": local.id
    }
    y=json.dumps(x)
    camara.mqtt_client.publish(canalCamarasLocal, y)

#Persona sale de una tienda
def publish_acceso_tienda_salida(cliente, local, camara, fecha):
    minutes=r.randint(55,59)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "sexo": cliente.sexo,
        "edad": cliente.edad,
        "fechaacceso": str(fechaAcceso),
        "idcamara": camara.id,
        "idlocal": local.id
    }
    y=json.dumps(x)
    camara.mqtt_client.publish(canalCamarasLocal, y)

#Smartphone ingresa a una tienda
def publish_recorrido_start(smartphone, local, beaconAcceso, fecha):
    minutes=r.randint(15,30)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idlocal": local.id,
        "idbeacon": beaconAcceso.id,
        "fechaentrada": str(fechaAcceso),
        "fechasalida": None
    }
    y=json.dumps(x)
    beaconAcceso.mqtt_client.publish(canalBeaconLocalEntrada,y)

#Smartphone sale de una tienda
def publish_recorrido_finish(smartphone, local, beaconSalida, fecha):
    minutes=r.randint(55,59)
    fechaSalida=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idlocal": local.id,
        "idbeacon": beaconSalida.id,
        "fechasalida": str(fechaSalida)
    }
    y=json.dumps(x)
    beaconSalida.mqtt_client.publish(canalBeaconLocalSalida,y)
    
#Publicar una factura
def publish_factura(cliente, local, registradora, fecha):
    minutes=r.randint(30,45)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    smartphone=None
    if cliente.id_smartphone>0:
        smartphone=cliente.id_smartphone
    x={
        "cicomprador": cliente.ci,
        "idlocal": local.id,
        "monto": np.random.normal(100,10),
        "fechacompra": str(fechaAcceso),
        "idsmartphone": smartphone
    }
    y=json.dumps(x)
    registradora.mqtt_client.publish(canalFactura,y)

#Publicar que se ocupa una mesa
def publish_ocupa_mesa(mesa, fecha, sensor):
    minutes=r.randint(0,15)
    fechaEstado=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idmesa": mesa.id,
        "fechaestado": str(fechaEstado),
        "ocupado": True
    }
    y=json.dumps(x)
    sensor.mqtt_client.publish(canalMesa,y)

#Publicar que se libera una mesa
def publish_libera_mesa(mesa, fecha, sensor):
    minutes=r.randint(55,59)
    fechaEstado=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idmesa": mesa.id,
        "fechaestado": str(fechaEstado),
        "ocupado": False
    }
    y=json.dumps(x)
    sensor.mqtt_client.publish(canalMesa,y)

#Publica una nueva ocupación de mesa por un smartphone
def publish_sensor_ocupa_mesa(mesa, smartphone, sensor, fecha):
    minutes=r.randint(0,15)
    fechaOcupado=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idmesa": mesa.id,
        "fechaocupado": str(fechaOcupado),
        "fechadesocupado": None,
    }
    y=json.dumps(x)
    sensor.mqtt_client.publish(canalMesaSensorOcupado,y)

#Publica que se descoupa la mesa
def publish_sensor_libera_mesa(mesa, smartphone, sensor, fecha):
    minutes=r.randint(55,59)
    fechaDesocupado=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idmesa": mesa.id,
        "fechadesocupado": str(fechaDesocupado),
    }
    y=json.dumps(x)
    sensor.mqtt_client.publish(canalMesaSensorDescupado,y)

#Ingreso de personas sleep
def ingreso_personas(ci, existingSmartphones, smartphonesQtty, beaconsAcceso, beaconsLocal, camarasAcceso, camarasLocal, puertas, clientesInCC, clientesOutOfCC, fecha):
    fake=Faker()
    #Solo entran antes de las 7:00 pm
    if fecha.hour < 19:
        usersToCreate = int(np.random.normal(20,5))
        print('Ingresan ',str(usersToCreate))
        while usersToCreate > 5:
            sexo=int(np.random.normal(2,1))
            ci=ci+1
            id_smartphone=int(np.random.normal(3,1.2))
            edad=int(np.random.normal(50,35))
            name=fake.name()
            if id_smartphone == 0:
                cliente=Cliente(ci,sexo,edad,name,0)
                clientesInCC.append(cliente)
            else:
                    #Smartphone existente
                if len(existingSmartphones) > 0:
                    cliente=Cliente(ci,sexo,edad,name,existingSmartphones.pop(0))
                    clientesInCC.append(cliente)
                    #Nuevo smartphone registrado
                else:
                    cliente=Cliente(ci,sexo,edad,name,smartphonesQtty)
                    clientesInCC.append(cliente)
                    smartphonesQtty=smartphonesQtty+1
                    register_smartphone(smartphonesQtty)
                
            usersToCreate=usersToCreate-1

            camara=camarasAcceso[(r.randint(1,len(camarasAcceso))-1)]
            puerta=puertas[(r.randint(1,len(puertas))-1)]
            publish_access(camara, cliente, puerta, fecha)
            if cliente.id_smartphone > 0:
                beacon=beaconsAcceso[(r.randint(1,len(beaconsAcceso))-1)]
                publish_start_estadia(beacon, cliente.id_smartphone, puerta, fecha)
                
        usersToReturn = int(np.random.normal(10,5))
        print('Vuelven ',str(usersToReturn))
        if usersToReturn > 10:
            auxo = int(usersToReturn/2)
            if usersToReturn < len(clientesOutOfCC):
                while usersToReturn > auxo:
                    cliente=clientesOutOfCC.pop(0)
                    clientesInCC.append(cliente)
                    usersToReturn=usersToReturn-1
                    camara=camarasAcceso[(r.randint(1,len(camarasAcceso))-1)]
                    puerta=puertas[(r.randint(1,len(puertas))-1)]
                    publish_access(camara, cliente, puerta, fecha)
                    if cliente.id_smartphone != 0:
                        beacon=beaconsAcceso[(r.randint(1,len(beaconsAcceso))-1)]
                        publish_start_estadia(beacon, cliente.id_smartphone, puerta, fecha)

#Recorrido de las personas en el CC
def recorrido_personas(clientesInCC, clientesOutOfCC, sensores, mesas, beaconsLocal, camarasLocal, locales):
    for index, cliente in enumerate(clientesInCC):
        
        decision=r.randint(0,5)

            #Decide entrar a una tienda
        if decision > 3:
            print('Entra a una tienda')
            local=locales[(r.randint(1,len(locales)))-1]
            camara=camarasLocal[(r.randint(1,len(camarasLocal)))-1]
            publish_acceso_tienda_entrada(cliente, local, camara, fecha)
            beacon=beaconsLocal[(r.randint(1,len(beaconsLocal))-1)]
                #Beacon detecta que entra un smartphone
            if cliente.id_smartphone > 0:
                publish_recorrido_start(cliente.id_smartphone, local, beacon, fecha)
            
                #Decision de compra
            decisionCompra=r.randint(0,1)
                #Hace una compra
            if decisionCompra == 0:
                publish_factura(cliente, local, camara, fecha)
                
                #Sale de la tienda
            publish_acceso_tienda_salida(cliente, local, camara, fecha)
                #Si tiene smartphone registra la salida
            if cliente.id_smartphone > 0:
                publish_recorrido_finish(cliente.id_smartphone, local, beacon, fecha)
            #Decide sentarse en una mesa
        if decision > 1:
            print('Ocupa una mesa')
                #Se ocupa una mesa
            mesa=mesas[((r.randint(1,len(mesas)))-1)]
            sensor=sensores[((r.randint(1,len(sensores)))-1)]
            publish_ocupa_mesa(mesa, fecha, sensor)

            if cliente.id_smartphone > 0:
                publish_sensor_ocupa_mesa(mesa, cliente.id_smartphone, sensor, fecha)

                #Se libera una mesa
            publish_libera_mesa(mesa, fecha, sensor)
            if cliente.id_smartphone > 0:
                publish_sensor_libera_mesa(mesa, cliente.id_smartphone, sensor, fecha)

            #Decisión de salirse
        if decision == 0:
            print('Se sale')
            for idx in enumerate(clientesInCC):
                if index == idx:
                    clientesInCC.pop(idx)

            clientesOutOfCC.append(cliente)

            camara=camarasLocal[(r.randint(1,len(camarasLocal)))-1]
            puerta=puertas[(r.randint(1,len(puertas)))-1]
            publish_salida_puerta(camara, cliente, puerta, fecha)

            if cliente.id_smartphone>0:
                beacon=beaconsAcceso[(r.randint(1,len(beaconsAcceso))-1)]
                publish_finish_estadia(beacon, cliente.id_smartphone, puerta, fecha)

        #Decisión de no hacer nada

#Salida del día
def check_salida(salida, clientesInCC, clientesOutOfCC, fecha):

    fecha.replace(hour=fecha.hour + 1)
    if fecha.hour > 21:
        salida=salida-1
        for cliente in enumerate(clientesInCC):
            clientesInCC.pop(0)
            clientesOutOfCC.append(cliente)

#Simulación
def simulacion(smartphonesQtty, existingSmartphones, clientesInCC,clientesOutOfCC, beaconsAcceso, beaconsLocal, sensores, camarasAcceso, camarasLocal, puertas, locales, mesas):
        #Ciclo de horas
    global salida
    salida=5
    ci=9
    global fecha
    ##Selección de la fecha de la simulación
    dia=r.randint(1,20)
    mes=r.randint(1,12)
    a=2019
    fecha=dt.datetime(a, mes, dia, 10)

    while salida > 0:
        
            #Ingreso de personas al comenzar una hora
        ingreso_personas(ci, existingSmartphones, smartphonesQtty, beaconsAcceso, beaconsLocal, camarasAcceso, camarasLocal, puertas, clientesInCC, clientesOutOfCC, fecha)
            #Recorrido de las personas que están dentro del CC
        recorrido_personas(clientesInCC, clientesOutOfCC, sensores, mesas, beaconsLocal, camarasLocal, locales)
            #Checkeo para la salida de personas
        check_salida(salida, clientesInCC, clientesOutOfCC, fecha)
            
def main():
    connect_to_db()
    global smartphonesQtty, existingSmartphones, clientesInCC,clientesOutOfCC, beaconsAcceso, beaconsLocal, sensores, camarasAcceso, camarasLocal, puertas, locales, mesas
    existingSmartphones = []
    beaconsAcceso = []
    beaconsLocal = []
    sensores = []
    clientesInCC = []
    clientesOutOfCC = []
    camarasAcceso = []
    camarasLocal = []
    puertas = []
    locales = []
    mesas = []
    smartphonesQtty = 0
    ##Instanciación de la data maestra para la simulación
    instanciateSmartphones(smartphonesQtty, existingSmartphones)
    instanciateCamaras(camarasAcceso, camarasLocal)
    instanciateBeacons(beaconsAcceso, beaconsLocal)
    instanciateSensores(sensores)
    instanciateLocales(locales)
    instanciatePuertas(puertas)
    instanciateMesas(mesas)
    #Comienzo de la simulación
    simulacion(smartphonesQtty, existingSmartphones, clientesInCC,clientesOutOfCC, beaconsAcceso, beaconsLocal, sensores, camarasAcceso, camarasLocal, puertas, locales, mesas)

if __name__=='__main__':
    main()
    sys.exit(0)