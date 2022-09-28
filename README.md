# modbusRTU_send
use serial port and RS485 Transmit modbus_RTU code

first, you need import modbusMaster.py into modbus_Send.py


quick start
functionCode ="01 05 00 00 00 00" # CRC will auto create
master1 = master.Master() 
master1.SetMaster(COM="COM3", baudrate=9600,timeout=0.5,writeTimeOut=0.5)
master1.SendModbusData(functionCode) 

#and you can read what slave transmit
