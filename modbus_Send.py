import modbusMaster as master
import time 
functionCode ="01 05 00 00 00 00"
functionCode1 = "01 05 00 00 FF 00"
if __name__ == '__main__':
        master1 = master.Master()
        master1.SetMaster(COM="COM3", baudrate=9600,timeout=0.5,writeTimeOut=0.5)
        while True :
                master1.SendModbusData(functionCode) 
                time.sleep(0.5)
                master1.SendModbusData(functionCode1)
        # if no parameters means you need input by yourself
        # master1.SendModbusData(functionCode) # if here have string parameter means this is your functionCode
        
         