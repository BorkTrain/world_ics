# world_ics

# ics_env

# USE
This environment was built for testing and training purposes. The HMI is 
designed to write values to the registry of the PLCs which exist on 6 
seperate VMs. The 'World' is designed to be a visual representation of 
the environment. The World communicates to the PLCs on a seperate 
network and only reads the values set in the register of the PLCs and 
displays a jpg depending on the sum of the values in regster 1-11 on 
each PLC. <br/>

# Setup 
#Location <br/>
/home/USER/DIR contains env, www(world/hmi), and plc_server<br/>
#FOR PLC<br/>
use plc_server.py store /home/USER/app/app.py <br/>
#Dependencies<br/>
virtualenv <br/>
pymodbus <br/>
# www
flask <br/>


# Launching Servers
cd /home/USER/dir
. env/bin/activate
{install dependencies in env}
./app.py

# TESTING Registry
#SETUP<br/>
from pymodbus.client.sync import ModbusTcpClient as ModbusClient<br/>
modbusClient = ModbusClient('**IP**', port=5020)<br/>
modbusClient.read_holding_registers(1,16)<br/>
#WRITE<br/>
print(modbusClient.write_register(REG_LOC,VALUE))<br/>
#READ<br/>
print(modbusClient.read_holding_registers(START_VAL,END_VALUE).registers<br/>

# Network
world-www - 10.10.1.150/24 <br/>
hmi-www - 192.168.26.150/24 <br/>
#PLCs IPSettings for World and HMI <br/>
#world <br/>
'FUEL':'10.10.1.120','WATERPUMP':'10.10.1.121','BOILER':'10.10.1.122','TURBINE':'10.10.1.123','GENERATOR':'10.10.1.124','PYLON':'10.10.1.125'<br/>
#hmi<br/>
'FUEL':'192.168.26.120','WATERPUMP':'192.168.26.121','BOILER':'192.168.26.122','TURBINE':'192.168.26.123','GENERATOR':'192.168.26.124','PYLON':'192.168.26.125'<br/>


