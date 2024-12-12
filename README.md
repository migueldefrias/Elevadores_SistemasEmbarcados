# **Trabalho 2 - 2024.1 - NOTA 8.0**

## **Autores**
**Nome:** Miguel Matos Costa de Frias Barbosa &emsp; **Matrícula:** 211039635 <br>
**Nome:** Yan Luca Viana de Araújo Fontenele  &emsp; **Matrícula:**  211031889


## **Objetivo**
&emsp;&emsp;O trabalho envolve o desenvolvimento do software que efetua o controle completo de um sistema de elevadores prediais incluindo o controle de movimentação, acionamento dos botões internos e externos e monitoramento de temperatura. O movimento dos elevadores é controlado à partir de motores elétricos e a posição é sinalizada à partir de sensores de posição e encoders.

## **Apresentação**

&emsp;&emsp;link do video da apresentação: <<https://youtu.be/ciU1KzBzVnc>>

## **Pré-requisitos**

&emsp;&emsp;Dependendo da placa talvez seja necessário instalar as seguintes bibliotecas:


- instalar biblioteca RPI.GPIO
```bash 
pip install RPi.GPIO
```
- instalar biblioteca smbus2
```bash 
pip install smbus2
```
- instalar biblioteca pyserial
```bash 
pip install pyserial
```
- instalar biblioteca smbus2
```bash 
pip install Adafruit_SSD1306
```
- instalar biblioteca PIL
```bash 
pip install pillow
```

## **Execução**
 
&emsp;&emsp;Observação: Preferência pelas placas 42 e 45, onde o projeto não apresentou problemas referentes a biblioteca.

#### Entre no ssh da placa
```bash 
$ ssh seu-usuario@ip_da_placa -p 13508
```

#### Envie o diretório Elevadores

```bash 
$ scp -P 13508 -r ./Elevadores seu-usuario@ip_da_placa:~/
```

#### Entre no diretório do projeto
```bash 
$ cd ./Elevadores
```

#### Execute os arquivos do

```bash 
$ python3 main.py
```
- obs: Cancelar a execução com ctrl+c


## **Gráficos**

<div align = "center"><img src="/Images/grafico1.jpg">
<p>Imagem 1<br> Teste nos 2 elevadores</p></div>

<div align = "center"><img src="/Images/grafico2.png">
<p>Imagem 2<br> Teste no elevador 2</p></div>

<div align = "center"><img src="/Images/grafico3.png">
<p>Imagem 3<br> Teste do botão de emergência</p></div>

<div align = "center"><img src="/Images/image.png">
<p>Imagem 4<br> Funcionamento da tela com temperatura, posição e movimento</p></div>
