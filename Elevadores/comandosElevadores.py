import uart
import time
import RPi.GPIO as GPIO
import pid
import i2c

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class PWM:
    def __init__(self, pino):
        self.pino = pino
        GPIO.setup(pino, GPIO.OUT)
        self.pwm = GPIO.PWM(pino, 100)
        self.pwm.start(0)

    def potenciaMotor(self, potencia):
        self.pwm.ChangeDutyCycle(potencia)
    
    def desligarMotor(self):
        self.pwm.stop()
        GPIO.cleanup()
class Elevador:
    
    def __init__(self, elevadorID, direcao1, direcao2, pwm, sensorTerreo, sensor1Andar, sensor2Andar, sensor3Andar):
        self.elevadorID = elevadorID
        self.direcao1 = direcao1
        self.direcao2 = direcao2
        self.pwm = pwm
        self.sensorTerreo = sensorTerreo
        self.sensor1Andar = sensor1Andar
        self.sensor2Andar = sensor2Andar
        self.sensor3Andar = sensor3Andar
        self.pid = pid.PID()
        self.movimento = "Parado"
        self.posEncoder = 0
        self.temperatura = 0
        self.posTerreo = 1560
        self.posAndar1 = 5257.5
        self.posAndar2 = 10320
        self.posAndar3 = 19700
        self.pwmAtual = 0
        self.andarAtual = 0
        self.filaDescida = [0,0,0,0]
        self.filaSubida = [0,0,0,0]
        self.fila=[]
        self.potencia=PWM(pwm)
        self.botoes = [0,0,0,0,0,0,0,0,0,0,0]
        
    def subir(self):
        GPIO.output(self.direcao1, GPIO.HIGH)
        GPIO.output(self.direcao2, GPIO.LOW)
        self.movimento = "Subindo"
    
    def descer(self):
        GPIO.output(self.direcao1, GPIO.LOW)
        GPIO.output(self.direcao2, GPIO.HIGH)
        self.movimento = "Descendo"
    
    def parar(self):
        self.potencia.potenciaMotor(0)
        self.pwmAtual = 0
        GPIO.output(self.direcao1, GPIO.HIGH)
        GPIO.output(self.direcao2, GPIO.HIGH)
        self.movimento = "Parado"
    
    def lerBotoes(self,botao0ID):
        self.botoes = uart.lerRegistradores(botao0ID)
        print("Botoes: ", self.botoes)
        return self.botoes

    def lerEncoder(self):
        encoder = int(uart.lerEncoder(self.elevadorID))
        return encoder

    def detectarAndar(self, andar):
        GPIO.wait_for_edge(andar, GPIO.RISING)
        subida = uart.lerEncoder(self.elevadorID)
        return subida

    def calibrarElevador(self):
        print("Calibrando Elevador: ", self.elevadorID+1) 
        i2c.telaCalibrando(self.elevadorID)
        encoder = uart.lerEncoder(self.elevadorID)
        time.sleep(0.1)
        while(encoder > 0):
            self.descer()
            self.potencia.potenciaMotor(50)
            self.pwmAtual = 50
            encoder = uart.lerEncoder(self.elevadorID)
            time.sleep(0.1)
        self.parar()
        self.subir()
        self.potencia.potenciaMotor(50)
        andar0 = self.detectarAndar(self.sensorTerreo)
        print("Andar 0 = ", andar0)
        andar1 = self.detectarAndar(self.sensor1Andar)
        print("Andar 1 = ", andar1)
        andar2 = self.detectarAndar(self.sensor2Andar)
        print("Andar 2 = ", andar2)
        andar3 = self.detectarAndar(self.sensor3Andar)
        print("Andar 3 = ", andar3)
        while encoder < 25000:
            print("Subindo ate limite")
            encoder = uart.lerEncoder(self.elevadorID)
            time.sleep(1)
        self.parar()
        self.descer()
        self.potencia.potenciaMotor(50)
        self.pwmAtual = 50
        
        andar3 = (self.detectarAndar(self.sensor3Andar)+andar3)/2
        print(" MEDIA ANDAR 3 = ", andar3)
        andar2 = (self.detectarAndar(self.sensor2Andar)+andar2)/2
        print(" MEDIA ANDAR 2 = ", andar2)
        andar1 = (self.detectarAndar(self.sensor1Andar)+andar1)/2
        print(" MEDIA ANDAR 1 = ", andar1)
        andar0 = (self.detectarAndar(self.sensorTerreo)+andar0)/2
        print(" MEDIA ANDAR 0 = ", andar0)
        self.posTerreo=andar0
        self.posAndar1=andar1
        self.posAndar2=andar2
        self.posAndar3=andar3
        print("Terreo: ", self.posTerreo)
        print("Andar 1: ", self.posAndar1)
        print("Andar 2: ", self.posAndar2)
        print("Andar 3: ", self.posAndar3)
        print("Calibracao finalizada")
        self.parar()

    def andarDestino(self, idbotao0,idbotao1, idbotao2, idbotao3, idbotao4, idbotao5,idbotao6,idbotao7,idbotao8,idbotao9,idbotao10):
      
        while True:
            if self.botoes[6] == 1:
                self.parar()
            else:
                if self.botoes[0] or self.botoes[7]:
                    if not self.posTerreo in self.fila:
                        self.fila.append(self.posTerreo)
                    if self.posEncoder >= (self.posTerreo - 500) and self.posEncoder <= (self.posTerreo + 500):
                        self.parar()
                        self.fila.remove(self.posTerreo)
                        uart.escreverRegistradores(idbotao0,0)
                        uart.escreverRegistradores(idbotao7,0)
                        time.sleep(5)

                    else:
                        if self.posEncoder < self.posTerreo:
                            self.subir()
                            self.potencia.potenciaMotor(40)
                            self.pwmAtual = 40
                        elif self.posEncoder > self.posTerreo:
                            self.descer()
                            self.potencia.potenciaMotor(40)
                            self.pwmAtual = 40

                if self.botoes[1] or self.botoes[2] or self.botoes[8]:
                    if not self.posAndar1 in self.fila:
                        self.fila.append(self.posAndar1)
                    if self.posEncoder >= (self.posAndar1 - 500) and self.posEncoder <= (self.posAndar1 + 500):
                        self.parar()
                        self.fila.remove(self.posAndar1)
                        uart.escreverRegistradores(idbotao1,0)
                        uart.escreverRegistradores(idbotao2,0)
                        uart.escreverRegistradores(idbotao8,0)
                        time.sleep(5)
                    
                    else:
                        if self.posEncoder < self.posAndar1:
                            self.subir()
                            self.potencia.potenciaMotor(40)
                            self.pwmAtual = 40
                        elif self.posEncoder > self.posAndar1:
                            self.descer()
                            self.potencia.potenciaMotor(40)
                            self.pwmAtual = 40

                if self.botoes[3]  or self.botoes[4]  or self.botoes[9]:
                    if not self.posAndar2 in self.fila:
                        self.fila.append(self.posAndar2)
                    if self.posEncoder >= (self.posAndar2 - 500) and self.posEncoder <= (self.posAndar2 + 500):
                        self.parar()
                        self.fila.remove(self.posAndar2)
                        uart.escreverRegistradores(idbotao3,0)
                        uart.escreverRegistradores(idbotao4,0)
                        uart.escreverRegistradores(idbotao9,0)
                        time.sleep(5)
                    
                    else:
                        if self.posEncoder < self.posAndar2:
                            self.subir()
                            self.potencia.potenciaMotor(40)
                            self.pwmAtual = 40
                        elif self.posEncoder > self.posAndar2:
                            self.descer()
                            self.potencia.potenciaMotor(40)
                            self.pwmAtual = 40

                if self.botoes[5] or self.botoes[10]:
                    if not self.posAndar3 in self.fila:
                        self.fila.append(self.posAndar3)
                    if self.posEncoder >= (self.posAndar3 - 500) and self.posEncoder <= (self.posAndar3 + 500):
                        self.parar()
                        self.fila.remove(self.posAndar3)
                        uart.escreverRegistradores(idbotao5,0)
                        uart.escreverRegistradores(idbotao6,0)
                        uart.escreverRegistradores(idbotao10,0)
                        time.sleep(5)
                    
                    else:
                        if self.posEncoder < self.posAndar3:
                            self.subir()
                            self.potencia.potenciaMotor(40)
                            self.pwmAtual = 40
                        elif self.posEncoder > self.posAndar3:
                            self.descer()
                            self.potencia.potenciaMotor(40)
                            self.pwmAtual = 40

                time.sleep(0.1)

    def andarElevador(self):
            fimTerreo = int((self.posTerreo+self.posAndar1)/2)
            fimAndar1 = int((self.posAndar1+self.posAndar2)/2)
            fimAndar2 = int((self.posAndar2+self.posAndar3)/2)
            if(self.posEncoder < fimTerreo):
                self.andarAtual = 0
            elif(self.posEncoder < fimAndar1 and self.posEncoder > fimTerreo):
                self.andarAtual = 1
            elif(self.posEncoder < fimAndar2 and self.posEncoder > fimAndar1):
                self.andarAtual = 2
            elif(self.posEncoder > fimAndar2):
                self.andarAtual = 3
    