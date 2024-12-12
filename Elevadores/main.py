import RPi.GPIO as GPIO
import time
from functools import partial   
import comandosElevadores
import uart
import threading
import i2c

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

"""             |Elevador 1 | Elevador 2|
Direção 1       |    20     |    19     |
Direção 2       |    21     |    26     |
PWM             |    12     |    13     |
Sensor_Terreo   |    18     |    17     |
Sensor_1_andar  |    23     |    27     |
Sensor_2_andar  |    24     |    22     |
Sensor_3_andar  |    25     |     6     |
"""
#Pinos do elevador 1
direcao1E1 = 20
direcao2E1 = 21
pwmE1 = 12
sensorTerreoE1 = 18
sensor_1_andarE1 = 23
sensor_2_andarE1 = 24
sensor_3_andarE1 = 25
elevador01ID = 0x00

#Pinos do elevador 2
direcao1E2 = 19
direcao2E2 = 26
pwmE2 = 13
sensorTerreoE2 = 17
sensor_1_andarE2 = 27
sensor_2_andarE2 = 22
sensor_3_andarE2 = 6
elevador02ID = 0x01

pinosEntradas = [sensorTerreoE1, sensorTerreoE2, sensor_1_andarE1, sensor_1_andarE2, 
                 sensor_2_andarE1, sensor_2_andarE2, sensor_3_andarE1, sensor_3_andarE2]

pinosSaidas = [direcao1E1, direcao2E1, pwmE1, direcao1E2, direcao2E2, pwmE2]

GPIO.setup(pinosEntradas, GPIO.IN)
GPIO.setup(pinosSaidas, GPIO.OUT)

elevador01 = comandosElevadores.Elevador( elevador01ID,direcao1E1, direcao2E1, pwmE1, sensorTerreoE1, sensor_1_andarE1, sensor_2_andarE1, sensor_3_andarE1)
elevador02 = comandosElevadores.Elevador( elevador02ID,direcao1E2, direcao2E2, pwmE2, sensorTerreoE2, sensor_1_andarE2, sensor_2_andarE2, sensor_3_andarE2)

def attEncoderEAmigos():
    while True:
        elevador01.posEncoder = uart.lerEncoder(elevador01.elevadorID)
        elevador02.posEncoder = uart.lerEncoder(elevador02.elevadorID)  
        print("Posição do encoder E1: ", elevador01.posEncoder)
        print("Posição do encoder E2: ", elevador02.posEncoder)
        uart.enviarTemperatura(elevador01.elevadorID)
        uart.enviarTemperatura(elevador02.elevadorID)
        time.sleep(0.02)
        uart.enviarPWM(elevador01.elevadorID, elevador01.pwmAtual)
        uart.enviarPWM(elevador02.elevadorID, elevador02.pwmAtual)
        elevador01.posEncoder = uart.lerEncoder(elevador01.elevadorID)
        elevador02.posEncoder = uart.lerEncoder(elevador02.elevadorID)  
        elevador01.lerBotoes(0x00)
        time.sleep(0.03)
        elevador02.lerBotoes(0xA0)

def atualizarTela():
    while True:
        elevador01.temperatura = i2c.lerTemperatura(i2c.addElevador01)
        time.sleep(0.05)
        elevador02.temperatura = i2c.lerTemperatura(i2c.addElevador02)
        time.sleep(0.05)   
        i2c.telaPadrao(elevador01.andarAtual, elevador02.andarAtual, elevador01.movimento, elevador02.movimento, elevador01.temperatura, elevador02.temperatura)
        time.sleep(0.1)

def funcionarElevadores():    
    while True:
        elevador01.andarElevador()
        time.sleep(1)
        elevador02.andarElevador()
        time.sleep(1)
        
def umElevador():
    #while True:
    elevador01.andarDestino(0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A)
def doisElevador():
    #while True:
    elevador02.andarDestino(0xA0,0XA1,0XA2,0xA3,0xA4,0xA5,0xA6,0xA7,0xA8,0xA9,0xAA)

threadUART = threading.Thread(target = attEncoderEAmigos)
threadTela = threading.Thread(target = atualizarTela)
threadElevador = threading.Thread(target = funcionarElevadores)
threadElevador1 = threading.Thread(target = umElevador)
threadElevador2 = threading.Thread(target = doisElevador)

try:
    
    elevador01.calibrarElevador()
    elevador02.calibrarElevador()
    threadUART.start()
    threadTela.start()
    threadElevador.start()
    threadElevador1.start()
    threadElevador2.start()
    threadUART.join()
    threadTela.join()
    threadElevador.join()
    threadElevador1.join()
    threadElevador2.join()

    time.sleep(0.1)
except KeyboardInterrupt:
    print("Parou o programa")
    elevador01.parar()
    elevador02.parar()
    elevador01.potencia.desligarMotor()
    elevador02.potencia.desligarMotor()
    
    GPIO.cleanup()
    exit()



