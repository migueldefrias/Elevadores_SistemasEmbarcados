import serial
import struct
import time
import crc
import i2c

matricula = "9635"


def configure_serial():
    srl = serial.Serial(port='/dev/serial0', baudrate=115200, parity=serial.PARITY_NONE, 
                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
    return srl

def lerEncoder(motorID):
    srl = configure_serial()
    srl.flushInput()
    message = [0x01, 0x23, 0xC1, motorID] + [int(digit) for digit in matricula]
    calculoCrc = crc.calculaCRC(message) 
    message = message + list(calculoCrc)
    srl.write(bytes(message))
    #time.sleep(0.05)
    data = srl.read(10)
    dados = data[3:7]
    if(crc.verificaCRC(data)):
        valorEncoder =  int.from_bytes(dados,"little")
    else:
        time.sleep(0.01)
        valorEncoder = lerEncoder(motorID)
    
    return valorEncoder

def lerRegistradores(enderecoRegistradores):
    srl = configure_serial()
    srl.flushInput()
    message = [0x01, 0x03, enderecoRegistradores, 11] + [int(digit) for digit in matricula]
    calculoCrc = crc.calculaCRC(message)
    message = message + list(calculoCrc)
    srl.write(bytes(message))
    time.sleep(0.2)
    dados = srl.read(16)
    valorInteiro = [byte for byte in dados]
    botoes = valorInteiro[2:-2]

    if(crc.verificaCRC(dados)):
        return botoes

    else:
        lerRegistradores( enderecoRegistradores)

def enviarTemperatura(elevadorID):
    srl = configure_serial()
    srl.flushInput()
    if(elevadorID == 0x00):
        addElevador = i2c.addElevador01
    elif(elevadorID == 0x01):
        addElevador = i2c.addElevador02
    temperatura = i2c.lerTemperatura(addElevador)
    temperaturaInt = struct.pack('<f', temperatura)
    #print("Temperatura: ", temperaturaInt)
    message = [0x01, 0x16, 0xD1, elevadorID] + list(temperaturaInt) + [int(digit) for digit in matricula]
    calculoCrc = crc.calculaCRC(message)  # Calcula o CRC-16
    message = message + list(calculoCrc)
    srl.write(bytes(message))

def enviarPWM(motorID, pwm):
    srl = configure_serial()
    srl.flushInput()
    pwmInt = struct.pack('<i', pwm)
    message = [0x01, 0x16, 0xC2, motorID] + list(pwmInt) +[int(digit) for digit in matricula]
    calculoCrc = crc.calculaCRC(message) 
    message = message + list(calculoCrc)
    srl.write(bytes(message))

def escreverRegistradores(enderecoRegistradores, valores):
    srl = configure_serial()
    srl.flushInput()
    valor = [valores]
    message = [0x01, 0x06, enderecoRegistradores, 1] + valor + [int(digit) for digit in matricula]
    calculoCrc = crc.calculaCRC(message)
    message = message + list(calculoCrc)
    srl.write(bytes(message))
