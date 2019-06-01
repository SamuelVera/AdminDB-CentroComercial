import psycopg2 as pg2
import datetime as dt

global conn 
conn = pg2.connect(host='localhost', dbname="sambilproyecto", user="postgres", password="1234")

with conn, conn.cursor() as cur:
    queryaux='''
        SELECT id FROM sensormesa
        WHERE idmesa=%s;
    '''
    cur.execute(queryaux,("2"))
    sensor=cur.fetchone()
    print(sensor[0])
    query='''
        INSERT INTO estadomesa(idsensor, idmesa, fechaestado, ocupado)
        VALUES(%s,%s,%s,%s);
    '''
    cur.execute(query,(sensor[0],2,dt.datetime(2019,10,2),False))
    query='''
        INSERT INTO monitoreomesa(idsmartphone, idmesa, fechaocupado)
        VALUES(%s,%s,%s);
    '''
    cur.execute(query,(2,2,str(dt.datetime(2019,10,10))))