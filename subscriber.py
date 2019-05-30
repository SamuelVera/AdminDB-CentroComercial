import json
import psycopg2 as pg2
import sys
import datetime as dt
import paho.mqtt.client as mqtt


    #Tópicos de MQTT
canalCamarasAcceso = "camarasAcceso/0"
canalCamarasLocal = "camarasLocal/0"
canalBeaconAccesoEntrada = "beaconAccesoEntrada/0"
canalBeaconAccesoSalida = "beaconAccesoSalida/0"
canalBeaconLocalEntrada = "beaconLocalEntrada/0"
canalBeaconLocalSalida = "beaconLocalSalida/0"
canalMesa = "mesa/0"
canalMesaSensor = "mesaSensor/0"
canalFactura = "factura/0"
canalRegisterSmartphone = "registrarSmartphone/0"


def main():
    print('GUISO')

if __name__=='__main__':
    main()
    sys.exit(0)