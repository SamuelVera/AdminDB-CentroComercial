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

##Selección de la fecha de la simulación
dia=10
mes=5
a=2019
fecha=dt.datetime(a, mes, dia, 10)


################################ Variables
fake=Faker()
existingSmartphones=[]
assignedSmartphones=[]
beaconsAcceso=[]
beaconsLocal=[]
sensores=[]
clientesInCC=[]
clientesOutOfCC=[]
camarasAcceso=[]
camarasLocal=[]
puertas=[]
locales=[]
mesas=[]
mesasOcupadas=[]
clientesInMesas=[]
clientesInLocales=[]
salida=5

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
        self.mqtt_client=mqtt.Client()
    
    def connect_to_broker(self):
        self.mqtt_client.connect(host='127.0.0.1', port=1883)
        self.mqtt_client.on_connect=on_connect
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
    conn = pg2.connect(host='localhost', dbname="sambilproyecto", user="postgres", password="1234")
        #Cursor para operar
    global cur 
    cur = conn.cursor()

#Instanciar smartphones existentes
def instanciateSmartphones():
    cur.execute("SELECT id FROM smartphone;")
    aux = cur.fetchall()
    for x in aux:
        existingSmartphones.append(x[0])

#Instanciar cámaras y conectarlas al broker
def instanciateCamaras():
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
def instanciateSensores():
    cur.execute("SELECT id FROM sensormesa;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=ClienteMqtt(x[0])
        toInsert.connect_to_broker()
        sensores.append(toInsert)

#Instanciar beacons y conectarlos al broker
def instanciateBeacons():
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
def instanciatePuertas():
    cur.execute("SELECT numero FROM puerta;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=DataMaestra(x[0])
        puertas.append(toInsert)

#Instanciar locales
def instanciateLocales():
    cur.execute("SELECT id FROM local;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=DataMaestra(x[0])
        locales.append(toInsert)

#Instanciar mesas
def instanciateMesas():
    cur.execute("SELECT id FROM mesa;")
    aux = cur.fetchall()
    for x in aux:
        toInsert=DataMaestra(x[0])
        mesas.append(toInsert)

#Registro de un nuevo smartphone
def register_smartphone(smartphone):
    x={
        "id": (smartphone)
    }
    y=json.dumps(x)
    sensores[0].mqtt_client.publish(topic=canalRegistrarSmartphone,payload=y,qos=0)

#Publish al acceso por una puerta
def publish_access(camaraAcceso, cliente, puerta):
    minutes=r.randint(0,15)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "sexo": cliente.sexo,
        "edad": cliente.edad,
        "fechaacceso": str(fechaAcceso),
        "idpuerta": puerta.id,
    }
    y=json.dumps(x)
    camaraAcceso.mqtt_client.publish(topic=canalCamarasAcceso,payload=y,qos=0)

#Publicar salida por una puerta
def publish_salida_puerta(camaraAcceso, cliente, puerta):
    minutes=r.randint(16,50)
    fechaSalida=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "sexo": cliente.sexo,
        "edad": cliente.edad,
        "fechaAcceso": str(fechaSalida),
        "idpuerta": puerta.id,
    }
    y=json.dumps(x)
    camaraAcceso.mqtt_client.publish(topic=canalCamarasAcceso,payload=y,qos=0)

#Publish al comienzo de la estadia de alguien con smartphone
def publish_start_estadia(beaconEntrada, smartphone, puerta):
    minutes=r.randint(0,15)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "fechaentrada":str(fechaAcceso),
        "idpuertaentrada": puerta.id
    }
    y=json.dumps(x)
    beaconEntrada.mqtt_client.publish(topic=canalBeaconAccesoEntrada,payload=y,qos=0)

#Publish al salir un smartphone del centro comercial
def publish_finish_estadia(beaconSalida, smartphone, puerta):
    minutes=r.randint(16,50)
    fechaSalida=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "fechasalida": str(fechaSalida),
        "idpuertasalida": puerta.id
    }
    y=json.dumps(x)
    beaconSalida.mqtt_client.publish(topic=canalBeaconAccesoSalida,payload=y,qos=0)

#Persona ingresa a una tienda
def publish_acceso_tienda_entrada(cliente, local, camara):
    minutes=r.randint(15,30)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "sexo": cliente.sexo,
        "edad": cliente.edad,
        "fechaacceso": str(fechaAcceso),
        "idlocal": local.id
    }
    y=json.dumps(x)
    camara.mqtt_client.publish(topic=canalCamarasLocal, payload=y, qos=0)

#Persona sale de una tienda
def publish_acceso_tienda_salida(cliente, local, camara):
    minutes=r.randint(55,59)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "sexo": cliente.sexo,
        "edad": cliente.edad,
        "fechaacceso": str(fechaAcceso),
        "idlocal": local.id
    }
    y=json.dumps(x)
    camara.mqtt_client.publish(topic=canalCamarasLocal, payload=y, qos=0)

#Smartphone ingresa a una tienda
def publish_recorrido_start(smartphone, local, beaconAcceso):
    minutes=r.randint(15,30)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idlocal": local.id,
        "fechaentrada": str(fechaAcceso)
    }
    y=json.dumps(x)
    beaconAcceso.mqtt_client.publish(topic=canalBeaconLocalEntrada,payload=y,qos=0)

#Smartphone sale de una tienda
def publish_recorrido_finish(smartphone, local, beaconSalida):
    minutes=r.randint(55,59)
    fechaSalida=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idlocal": local.id,
        "fechasalida": str(fechaSalida)
    }
    y=json.dumps(x)
    beaconSalida.mqtt_client.publish(topic=canalBeaconLocalSalida,payload=y,qos=0)
    
#Publicar una factura
def publish_factura(cliente, local, registradora):
    minutes=r.randint(30,45)
    fechaAcceso=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    smartphone=None
    if cliente.id_smartphone>0:
        smartphone=cliente.id_smartphone
    x={
        "cicomprador": cliente.ci,
        "idlocal": local.id,
        "monto": r.randint(10,1000),
        "fechacompra": str(fechaAcceso),
        "idsmartphone": smartphone
    }
    y=json.dumps(x)
    registradora.mqtt_client.publish(topic=canalFactura,payload=y,qos=0)

#Publicar que se ocupa una mesa
def publish_ocupa_mesa(mesa, sensor):
    minutes=r.randint(0,15)
    fechaEstado=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idmesa": mesa.id,
        "fechaestado": str(fechaEstado),
        "ocupado": True
    }
    y=json.dumps(x)
    sensor.mqtt_client.publish(topic=canalMesa,payload=y,qos=0)

#Publicar que se libera una mesa
def publish_libera_mesa(mesa, sensor):
    minutes=r.randint(55,59)
    fechaEstado=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idmesa": mesa.id,
        "fechaestado": str(fechaEstado),
        "ocupado": False
    }
    y=json.dumps(x)
    sensor.mqtt_client.publish(topic=canalMesa,payload=y,qos=0)

#Publica una nueva ocupación de mesa por un smartphone
def publish_sensor_ocupa_mesa(mesa, smartphone, sensor):
    minutes=r.randint(0,15)
    fechaOcupado=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idmesa": mesa.id,
        "fechaocupado": str(fechaOcupado)
    }
    y=json.dumps(x)
    sensor.mqtt_client.publish(topic=canalMesaSensorOcupado,payload=y,qos=0)

#Publica que se descoupa la mesa
def publish_sensor_libera_mesa(mesa, smartphone, sensor):
    minutes=r.randint(30,59)
    fechaDesocupado=dt.datetime(fecha.year, fecha.month, fecha.day, fecha.hour, minutes)
    x={
        "idsmartphone": smartphone,
        "idmesa": mesa.id,
        "fechadesocupado": str(fechaDesocupado),
    }
    y=json.dumps(x)
    sensor.mqtt_client.publish(topic=canalMesaSensorDescupado,payload=y,qos=0)

#Simulación
def simulacion():

    while salida > 0:
        
            #Ingreso de personas al comenzar una hora
        ingreso_personas()
            #Recorrido de las personas que están dentro del CC
        recorrido_personas()
            #Desocupado de mesas
        desocupan_mesas()
            #Salen de locales
        salen_de_local()
            #Checkeo para la salida de personas
        check_salida()

#Crear cliente
def create_cliente(ci):
    sexo = int(np.random.exponential(1.1))
    if sexo < 2:
        sexo = np.random.binomial(1,0.54)
    else:
        sexo = 2
    has_smartphone=r.randint(0,3)
    edad=int(np.random.normal(40,15))
    name=fake.name()

    if has_smartphone == 0:
        cliente=Cliente(ci,sexo,edad,name,0)
        clientesInCC.append(cliente)
    else:
            #Smartphone existente
        if len(existingSmartphones) > 0:
            smartphone=existingSmartphones.pop(0)
            cliente=Cliente(ci,sexo,edad,name,smartphone)
            assignedSmartphones.append(smartphone)
            clientesInCC.append(cliente)
            #Nuevo smartphone registrado
        else:
            smartphone=len(assignedSmartphones)
            assignedSmartphones.append(smartphone)
            cliente=Cliente(ci,sexo,edad,name,smartphone)
            clientesInCC.append(cliente)
            register_smartphone(smartphone)
            t.sleep(0.3)

    camara=camarasAcceso[(r.randint(1,len(camarasAcceso))-1)]
    puerta=puertas[(r.randint(1,len(puertas))-1)]
    publish_access(camara, cliente, puerta)
    t.sleep(0.3)
    if cliente.id_smartphone > 0:
        beacon=beaconsAcceso[(r.randint(1,len(beaconsAcceso))-1)]
        publish_start_estadia(beacon, cliente.id_smartphone, puerta)
        t.sleep(0.3)

#Ingreso de personas sleep
def ingreso_personas():
    #Solo entran antes de las 7:00 pm
    if fecha.hour < 19:
        clientsToCreate = int(np.random.normal(7,1))
        print('Ingresan ',str(clientsToCreate))
        ci=10+len(clientesInCC)+len(clientesOutOfCC)
        while clientsToCreate > 0:
            create_cliente(ci)
            clientsToCreate=clientsToCreate-1
            ci+=1
                
        regresaGente = np.random.normal(0,1)
        #25% de las veces vuele a entrar un lote de gente
        if regresaGente < -0.67:
            usersToReturn = int(np.random.normal(6,1))
            if usersToReturn < len(clientesOutOfCC):
                auxo = int(usersToReturn/2)
                print('Vuelven a entrar ',str(auxo))
                while usersToReturn > auxo:
                    cliente=clientesOutOfCC.pop(r.randint(1,len(clientesOutOfCC))-1)
                    clientesInCC.append(cliente)
                    usersToReturn=usersToReturn-1
                    camara=camarasAcceso[(r.randint(1,len(camarasAcceso))-1)]
                    puerta=puertas[(r.randint(1,len(puertas))-1)]
                    publish_access(camara, cliente, puerta)
                    t.sleep(0.3)
                    
                    if cliente.id_smartphone>0:
                        print(cliente.ci,' Tiene smartphone')
                        beacon=beaconsAcceso[(r.randint(1,len(beaconsAcceso))-1)]
                        publish_start_estadia(beacon, cliente.id_smartphone, puerta)
                        t.sleep(0.3)

#Recorrido de las personas en el CC
def recorrido_personas():
    print(len(clientesInCC))
    i=0
    while i<len(clientesInCC):
        
        decision=np.random.normal(0,1)

        #Decide ocupar mesa 19% de las veces
        if decision > 0.9:
            print('Ocupa una mesa')
                #Se ocupa una mesa si hay mesas disponibles
            if len(mesas) > 0:

                mesa=mesas.pop((r.randint(1,len(mesas)))-1)
                
                sensor=sensores[((r.randint(1,len(sensores)))-1)]

                publish_ocupa_mesa(mesa, sensor)
                t.sleep(0.3)

                cliente=clientesInCC.pop(i)
                clientesInMesas.append([cliente,mesa])

                if cliente.id_smartphone>0:
                    publish_sensor_ocupa_mesa(mesa, cliente.id_smartphone, sensor)
                    t.sleep(0.3)

            else: #No hay mesas disponibles
                i+=1
            
        #Decisión de salirse del centro comercial 28% de las veces
        elif decision < -0.6:
            print('Se sale')

            cliente=clientesInCC.pop(i)
            clientesOutOfCC.append(cliente)

            camara=camarasLocal[(r.randint(1,len(camarasLocal)))-1]
            puerta=puertas[(r.randint(1,len(puertas)))-1]
            publish_salida_puerta(camara, cliente, puerta)
            t.sleep(0.3)

            if cliente.id_smartphone>0:
                beacon=beaconsAcceso[(r.randint(1,len(beaconsAcceso))-1)]
                publish_finish_estadia(beacon, cliente.id_smartphone, puerta)
                t.sleep(0.3)

        #Decide entrar a una tienda o no hacer nada 53% de las veces
        else:
            decision2=np.random.normal(0,1)
                #En este caso 76% de las veces entra a una tienda 
            if decision2 < 0.7:

                print('Entra a una tienda')
                local=locales[(r.randint(1,len(locales)))-1]
                camara=camarasLocal[(r.randint(1,len(camarasLocal)))-1]
                
                cliente=clientesInCC.pop(i)
                clientesInLocales.append([cliente, local])

                publish_acceso_tienda_entrada(cliente, local, camara)
                t.sleep(0.3)
                
                #Beacon detecta que entra un smartphone
                if cliente.id_smartphone != 0:
                    beacon=beaconsLocal[(r.randint(1,len(beaconsLocal))-1)]
                    publish_recorrido_start(cliente.id_smartphone, local, beacon)
                    t.sleep(0.3)
                
                #Decision de compra
                decisionCompra=r.randint(0,1)
                #Hace una compra
                if decisionCompra == 0:
                    publish_factura(cliente, local, camara)
                    t.sleep(0.3)
                
            #24% de las veces no hace nada
            else:
                i+=1

#Personas que están en mesas y deciden pararse
def desocupan_mesas():
    i=0
    while i<len(clientesInMesas):

        decideLiberar=np.random.normal(0,1)
        #Libera la mesa 70% de las veces
        if decideLiberar<0.53:
            
                #Desocupa la mesa
            tupla=clientesInMesas.pop(i)
            cliente=tupla[0]
            clientesInCC.append(cliente)
            mesa=tupla[1]
            print(cliente.ci,' Desocupa la mesa ',mesa.id)
            sensor=sensores[((r.randint(1,len(sensores)))-1)]

            if cliente.id_smartphone != 0:
                print('TIENE SMARTPHONE')
                publish_sensor_libera_mesa(mesa, cliente.id_smartphone, sensor)
                t.sleep(0.3)

            #Se libera una mesa
            publish_libera_mesa(mesa, sensor)
            t.sleep(0.3)
            mesas.append(mesa)

        #No se para de la mesa 30% de las veces
        else:
            tupla=clientesInMesas[i]
            cliente=tupla[0]
            mesa=tupla[1]
            print(cliente.ci,' No desocupa la mesa ',mesa.id)
            i+=1

#Personas que están en locales y deciden salir
def salen_de_local():
    i=0
    while i<len(clientesInLocales):
        decisionSalirLocal=np.random.normal(0,1)
        #Decise salir del local 70% de las veces
        if decisionSalirLocal<0.53:
            
            tupla=clientesInLocales.pop(i)
            cliente=tupla[0]
            clientesInCC.append(cliente)
            local=tupla[1]
            print(cliente.ci,' Sale del local ',local.id)
            camara=camarasLocal[(r.randint(1,len(camarasLocal)))-1]
            
            #Sale de la tienda
            publish_acceso_tienda_salida(cliente, local, camara)
            t.sleep(0.3)
                #Si tiene smartphone registra la salida
            if cliente.id_smartphone != 0:
                beacon=beaconsLocal[(r.randint(1,len(beaconsLocal))-1)]
                print('Tiene smartphone')
                publish_recorrido_finish(cliente.id_smartphone, local, beacon)
                t.sleep(0.3)
            
        else:
            tupla=clientesInLocales[i]
            cliente=tupla[0]
            local=tupla[1]
            print(cliente.ci,' Se mantiene en el local ',local.id)
            i+=1

#Salida del día
def check_salida():
    global fecha
    fecha=dt.datetime(year=fecha.year,month=fecha.month,day=fecha.day,hour=(fecha.hour+1))
    print(fecha)
    t.sleep(1)
    if fecha.hour > 21:
        global salida
        salida=salida-1
        fecha=dt.datetime(year=fecha.year,month=fecha.month,day=(fecha.day+1),hour=10)
        print('Se acabó el día')
        print('Quedan ',salida,' días de simulación')

        print('Quedan ', len(clientesInLocales),' en los locales, van a salir')
        while len(clientesInLocales)>0:
            tupla=clientesInLocales.pop(0)
            cliente=tupla[0]
            clientesInCC.append(cliente)
            local=tupla[1]
            print(cliente.ci,' Sale del local ',local.id)
            camara=camarasLocal[(r.randint(1,len(camarasLocal)))-1]        
            #Sale de la tienda
            publish_acceso_tienda_salida(cliente, local, camara)
            t.sleep(0.3)
                #Si tiene smartphone registra la salida
            if cliente.id_smartphone != 0:
                beacon=beaconsLocal[(r.randint(1,len(beaconsLocal))-1)]
                print('Tiene smartphone')
                publish_recorrido_finish(cliente.id_smartphone, local, beacon)
                t.sleep(0.3)

        print('Quedan ', len(clientesInMesas),' en las locales, van a desocuparlas')
        while len(clientesInMesas)>0:
                #Desocupa la mesa
            tupla=clientesInMesas.pop(0)
            cliente=tupla[0]
            clientesInCC.append(cliente)
            mesa=tupla[1]
            print(cliente.ci,' Desocupa la mesa ',mesa.id)
            sensor=sensores[((r.randint(1,len(sensores)))-1)]

            if cliente.id_smartphone != 0:
                print('TIENE SMARTPHONE')
                publish_sensor_libera_mesa(mesa, cliente.id_smartphone, sensor)
                t.sleep(0.3)

            #Se libera una mesa
            publish_libera_mesa(mesa, sensor)
            t.sleep(0.3)
            mesas.append(mesa)
        
        print('Aún hay ', len(clientesInCC),' personas en el CC, ahora saldrán')
        while len(clientesInCC)>0:
            cliente=clientesInCC.pop(0)
            camara=camarasAcceso[(r.randint(1,len(camarasAcceso))-1)]
            puerta=puertas[(r.randint(1,len(puertas))-1)]
            publish_salida_puerta(camara, cliente, puerta)
            print('Sale ',cliente.ci)
            t.sleep(0.3)
            if cliente.id_smartphone != 0:
                print('Tiene smartphone')
                beacon=beaconsAcceso[(r.randint(1,len(beaconsAcceso))-1)]
                publish_finish_estadia(beacon, cliente.id_smartphone, puerta)
                t.sleep(0.3)
            clientesOutOfCC.append(cliente)
        
        t.sleep(3)
            
def main():
    connect_to_db()
    ##Instanciación de la data maestra para la simulación
    instanciateSmartphones()
    global smartphonesQtty
    smartphonesQtty=len(existingSmartphones)
    instanciateCamaras()
    instanciateBeacons()
    instanciateSensores()
    instanciateLocales()
    instanciatePuertas()
    instanciateMesas()
    #Comienzo de la simulación
    simulacion()

if __name__=='__main__':
    main()
    sys.exit(0)