import smbus2
import bme280
import Adafruit_SSD1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
port = 1
addElevador01 = 0x76
addElevador02 = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, addElevador01)
calibration_params02 = bme280.load_calibration_params(bus, addElevador02)

RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_bus=port)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
font = ImageFont.load_default()
x=0

def lerTemperatura(address):
    if(address == 0x00):
        data = bme280.sample(bus, addElevador01, calibration_params)
    else:
        data = bme280.sample(bus, addElevador02, calibration_params)
    return data.temperature

           
def telaPadrao(elevador01_andarAtual, elevador02_andarAtual, elevador01_movimento, elevador02_movimento, elevador01_temperatura, elevador02_temperatura):
                
    posElevador1 = elevador01_andarAtual
    posElevador2 = elevador02_andarAtual
    movElevador1 = elevador01_movimento
    movElevador2 = elevador02_movimento
    tempElevador2 = f" {elevador02_temperatura:.2f}°C"  
    tempElevador1 = f" {elevador01_temperatura:.2f}°C"  
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top),str("Elevador 1"),fill=255)
    draw.text((x, top+16),str(tempElevador1), font=font, fill=255)
    draw.text((x, top+32),str(posElevador1), font=font, fill=255)
    draw.text((x, top+48),str(movElevador1), font=font, fill=255)
    draw.line((width/2, 0, width/2, height), fill=255)
    draw.text((width/2+4, top),str("Elevador 2"), font=font, fill=255)
    draw.text((width/2+4, top+16),str(tempElevador2), font=font, fill=255)
    draw.text((width/2+4, top+32),str(posElevador2), font=font, fill=255)
    draw.text((width/2+4, top+48),str(movElevador2), font=font, fill=255)
    disp.image(image)
    disp.display()
    
    time.sleep(0.1)

def telaCalibrando(elevadorID):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top),str("Calibrando Elevador: "),fill=255)
    draw.text((x, top+16),str(elevadorID+1), font=font, fill=255)
    disp.image(image)
   
    disp.display()
    time.sleep(0.1)