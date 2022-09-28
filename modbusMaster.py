import serial, time
import logging   

class Master():
    ser = serial.Serial()
    
    def SetMaster(self,COM = "COM3",baudrate = "9600", timeout = 0.5, writeTimeOut = 0.5):
        self.ser.port = COM
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout          #non-block read 0.5s
        self.ser.writeTimeout = writeTimeOut     #timeout for write 0.5s        

        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        self.ser.xonxoff = False    #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control    

    def calc_crc16(self,string):
        try :
            '''here will crate a list to crc'''
            data = bytearray.fromhex(string)
            logging.info(type(data))
            crc = 0xFFFF
            for pos in data:
                    crc ^= pos
                    for i in range(8):
                            if((crc & 1) != 0):
                                    crc >>= 1
                                    crc ^= 0xA001
                            else:
                                    crc >>= 1

            result = str(hex(((crc & 0xff) << 8) + (crc >> 8)))
            return int(result[2:4],16),int(result[4:6],16)
        except Exception as ex :
            print("here have some error:", str(ex) ,"line: ", str(ex.__traceback__.tb_lineno))

    def change_data_to_modbus(self,data) :
        '''it can let string be modbus type'''
        try :
            rtu_list = data.split()
            rtu = []
            for i in range(len(rtu_list)) :
                rtu.append(int(rtu_list[i],16))
            print(rtu)
            crc = self.calc_crc16(data)
            rtu += crc
            return rtu  
        except Exception as ex :
            print("here have some error:", str(ex) ,"line: ", str(ex.__traceback__.tb_lineno))
                        
    def ByteToHex(self,data) :
        try :
            result = ['0x{:02X}'.format(x) for x in list(data)] 
            return result
        except Exception as ex :
            print("here have some error:", str(ex) ,"line: ", str(ex.__traceback__.tb_lineno))
            
    def ReadModbusData(self) :
        try :
            response1 = self.ser.read(3)
            #cheak third byte and cheak how long we need to read
            byteCount = self.ByteToHex(response1)[2]
            response2 = self.ser.read(int(byteCount,16))
            response3 = self.ser.read(2)
            return response1, response2, response3
        except Exception as ex :
            print("here have some error:", str(ex) ,"line: ", str(ex.__traceback__.tb_lineno))

    def SendModbusData(self,functionCode) :
        try :
            self.ser.open()
        except Exception as ex :
            print("open serial port error " + str(ex),"line: ",str(ex.__traceback__.tb_lineno))
        
        if self.ser.isOpen() :
                self.ser.flushInput() #flush input buffer
                self.ser.flushOutput() #flush output buffer
        
                #write 8 byte data
                try :
                    if len(functionCode) == 0 :
                        data = input("please input rtu:\n")
                    else :
                        data = functionCode 
                    if data == "0" :
                        print("no Data available")    
                    rtu = self.change_data_to_modbus(data)
                    #change data to modbus can read
                    
                    self.ser.write(rtu)
                    time.sleep(0.5)  #wait 0.5s
            
                    result = self.ReadModbusData() 
                    print( "inital information :", self.ByteToHex(result[0]) )
                    print( "Data :", self.ByteToHex(result[1]) )
                    print( "CRC code :", self.ByteToHex(result[2]) )
                    self.ser.close()
                except Exception as ex :
                    print("here have some error:", str(ex) ,"line: ", str(ex.__traceback__.tb_lineno))
                    self.ser.close()        

if __name__ == "__main__":
    master = Master()
    master.SetMaster(COM = "COM3",baudrate = 9600)
    master.SendModbusData()
        