# Data Capture of a Smart Shopping Center (Simulation)

# Collaboratos

1. Sabrina García (https://github.com/SabrinaGar).
2. Juan Montenegro (https://github.com/ZetM).
3. Samuel Vera (Owner of this repo).

# Pip packages used:

1. matplotlib.
2. pandas.
3. psycopg2.
4. numpy.
5. paho.

# Instructions to run the project

1. Clone the repository with `git clone https://github.com/SamuelVera/Data-Capture-Smart-Shopping-Center-Simulation.git`
2. Restore the database with PostgreSQL and the file "sambilproyecto-backup.tar".
3. Open Jupyter Notebook in the cloned repo folder with the cmd command `Jupyter Notebook`.
4. Open the jupyter file "Notebook Jupyther.ipynb" in the Jupyter UI and change the database credentials in the second cell code to the ones in your postgreSQL server.
5. Change the database credentials from the line 31 of the script "subcriber.py" and the line 82 of the script "randomDataScript.py" to the ones used in your postgreSQL server.
6. Run the "subscriber.py" script and wait for the console message "Conexión exitosa".
7. Run the "randomDataScript.py" script y follow the console instructions.

# NOTE:

1. A day of simulation lasts between 3 and 4 minutes. You can choose a maximum of 10 days of simulation.
2. The jupyter notebook has a real time graphic. This can be appreciated if the cell code corresponding to "Vista Extra 3" is executed while the "subcriber.py" and "randomDataScript.py" scripts are runnning.
3. The views corresponding to the last month get data from May 2019.
4. The backup file has data from January 2019 to May 2019.

# Simulación de Captura de Datos de un Centro Comercial Inteligente

# Integrantes

1. Sabrina García (https://github.com/SabrinaGar).
2. Juan Montenegro (https://github.com/ZetM).
3. Samuel Vera (Dueño de este repo).

# Módulos a instalar:

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
5. Ejecute el script de subscripción subscriber.py ubicandose en la carpeta del proyecto. Espere a que por consola se le indique un mensaje que diga "Conexión exitosa".
6. Ejecute el script de simulación de data random "randomDataScript.py" y siga las instrucciones que se le dan en la consola.

# NOTA:

1. El día de simulación en la ejecución dura aproximadamente entre 3 minutos y medio y 4 minutos. Se pueden elegir hasta un máximo de 10 días de ejecucion.
2. El archivo de jupyter notebook tiene una gráfica a tiempo real y correspondiente a la Vista Extra 3, si se ejecuta el código mientras corren los scripts de "suscriptor" y "generador de data" se puede apreciar mejor el funcionamiento de dicha gráfica.
3. Las vistas correspondientes al último mes traen datos del mes de mayo de 2019.
4. El Backup de la DB tiene datos para enero de 2019 hasta mayo de 2019.
