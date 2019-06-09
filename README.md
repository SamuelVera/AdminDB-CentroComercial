# AdminDB-CentroComercial
Proyecto de Administración de Bases de Datos

# Módulos a instalar

1. matplotlib. `python -m pip install -U pip`
2. pandas. `pip install pandas`
3. psycopg2. `pip install psycopg2`
4. numpy. `python -m pip install numpy`
5. paho. `pip install paho-mqtt`
6. Los demás módulos vienen por defecto con la instalación de python 3.

# Siga las siguientes instrucciones para ejecutar el proyecto:
1. Abra PgAdmin, cree una nueva Base de Datos, haga click derecho en "restore" y seleccione el archivo sambilproyecto-backup.tar.
 
2. Inicie jupyther notebook utilizando el comando `jupyter notebook` en la carpeta del repositorio.
 
3. Haga click en el archivo Notebook Jupyther.ipynb y cambie las credenciales de conexión a la base de datos de la celda 2 de código por las correspondientes.
 
4. Además cambie las credenciales de la base de datos en los scripts de python. En el script randomDataScript.py en la linea 82 y en la linea 31 del script subscriber.py.

4. Ejecute el script de subscripción subscriber.py ubicandose en la carpeta del proyecto. Espere a que por consola se le indique un mensaje que diga "Conexión exitosa".

5. Ejecute el script de simulación de data random "randomDataScript.py" y siga las instrucciones que se le dan en la consola.

# NOTA:
1. El día de simulación en la ejecución dura aproximadamente entre 3 minutos y medio y 4 minutos. Se pueden elegir hasta un máximo de 10 días de ejecucion.

2. El archivo de jupyter notebook tiene una gráfica a tiempo real y correspondiente a la Vista Extra 6, si se ejecuta el código mientras corren los scripts de "suscriptor" y "generador de data" se puede apreciar mejor el funcionamiento de dicha gráfica.

3. Las vistas correspondientes al último mes traen datos del mes de mayo de 2019.

4. El Backup de la DB tiene datos para enero de 2019 hasta mayo de 2019.
