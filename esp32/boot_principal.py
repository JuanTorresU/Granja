# This is script that run when device boot up or wake from sleep
#notify
#Pines que no se pueden utilizar
#1-3 Son la comunicacion serial
#12, bootlea la flash
print('RUN: boot.py')
import micropython, gc
micropython.mem_info()
print('--------------------------------------------------------------------')

###Libraries
import time, sys
import network
import time
from umqtt.robust import MQTTClient
from machine      import Pin, Timer, ADC, RTC, PWM, I2C, reset
import dht
import ntptime
import TSL2561

###Constants
ubidotsToken = 'BBFF-JhLzbBIyRwFmEJoXfFxEb2RPGi6hID'
#ubidotsToken = 'BBFF-JhLzbBIyRwFmEJoXfFxEb2RPGi6hID'
clientID = 'esp32' 
var = 0
adc_obj = []
dht_obj = []
dht_v = []
state = [0,0,0]
output = [0,0,0]
TIME_TIMER = 15000
OP_SINGLE_HRES1 = 0x20
DELAY_HMODE = 180  # 180ms in H-mode
i2c_addr = 35

#input pins
adc_pins = [33,32,35,34,39,36,36,36,36]  #Use 25,26 pins to select the mux, 37-40 to ADC pin 39. Soil Moisture pins
mux_out_pins = [0,0,4,2,1,0,3,7,5]
mux_pins = [39,34,35]
dht_pins = [14,27,26]                 #Temperature and relative humidity pins
lum_pins = [21,22]


#outputs pins
out_pins = {
    'level_1':{
        'ventilator':13,    #Tiene PWM
        'heater':23,        #Tiene PWM
        'valve':2,          #Tiene PWM
        },
    'level_2':{
        'ventilator':19,    #Tiene PWM
        'heater':18,        #Tiene PWM
        'valve':5,          #Tiene PWM
        },
    'level_3':{
        'ventilator':17,    #Tiene PWM
        'heater':16,        #Tiene PWM
        'valve':4,          #Tiene PWM
        },
    'light':15
    }
  
#Reference values
in_ref = {                               
    'tem':{                           #Temperature reference
        'high':25,
        'medium':22,
        'low':14
        },
    'hum':{                           #Relative humidity reference
        'high':80,
        'medium':60,
        'low':40
        },
    'mos':{                           #Soil Moisture reference
        'high':85,
        'medium':60,
        'low':40
        },
    'lum':{                           #Luminosity reference
        'high':25,
        'medium':18,
        'low':12
        }
    } 

out_ref = {
    'ventilator':{
        0:0,
        1:98,
        2:100,
        },
    'heater':{
        0:0,
        1:70,
        2:100,
        },
    'valve':{
        'value':{
            0:0,
            1:1,
            2:1,
            },
        'time':{
            0:0,
            1:50000,
            2:60000,
            },
        
        },
    'light':{
        0:0,
        1:70,
        2:100,
        },
    }
inputs = {
    12211:1,
    12202:1,
    12201:1,
    12111:1,
    00211:1,
    00202:1,
    00201:1,
    00111:1,
    11211:2,
    11202:2,
    11201:2,
    11111:2,
    10211:3,
    10202:3,
    10201:3,
    10111:3,
    12102:4,
    12101:4,
    12011:4,
    00102:4,
    00101:4,
    00011:4,
    11102:5,
    11101:5,
    11011:5,
    10102:6,
    10101:6,
    10011:6,
    12002:7,
    12001:7,
    00002:7,
    00001:7,
    11002:8,
    11001:8,
    10002:9,
    10001:9,
    12110:10,
    00110:10,
    11110:11,
    10110:12,
    12010:13,
    00010:13,
    11010:14,
    10010:15,
    12200:16,
    00200:16,
    11200:17,
    10200:18,
    12100:19,
    12020:19,
    00100:19,
    00020:19,
    11100:20,
    11020:20,
    10100:21,
    10020:21,
    12000:22,
    00000:22,
    11000:23,
    10000:24,
    12210:25,
    00210:25,
    11210:26,
    10210:27,
    12220:28,
    12120:28,
    00220:28,
    00120:28,
    11220:29,
    11120:29,
    10220:30,
    10120:30,
    12222:31,
    12221:31,
    12212:31,
    12122:31,
    12121:31,
    12112:31,
    00222:31,
    00221:31,
    00212:31,
    00122:31,
    00121:31,
    00112:31,
    11222:32,
    11221:32,
    11212:32,
    11122:32,
    11121:32,
    11112:32,
    10222:33,
    10221:33,
    10212:33,
    10122:33,
    10121:33,
    10112:33,
    12022:34,
    12021:34,
    12012:34,
    00022:34,
    00021:34,
    00012:34,
    11022:35,
    11021:35,
    11012:35,
    10022:36,
    10021:36,
    10012:36,
    00000:37,
    22222:38
    }
outputs = {
    1:[0,0,0,0],    #State 1
    2:[0,0,0,1],    #State 2
    3:[0,0,0,2],    #State 3
    4:[0,0,1,0],    #State 4
    5:[0,0,1,1],    #State 5
    6:[0,0,1,2],    #State 6
    7:[0,0,2,0],    #State 7
    8:[0,0,2,1],    #State 8
    9:[0,0,2,2],    #State 9
    10:[0,1,0,0],    #State 10
    11:[0,1,0,1],    #State 11
    12:[0,1,0,2],    #State 12
    13:[0,1,1,0],    #State 13
    14:[0,1,1,1],    #State 14
    15:[0,1,1,2],    #State 15
    16:[0,2,0,0],    #State 16
    17:[0,2,0,1],    #State 17
    18:[0,2,0,2],    #State 18
    19:[0,2,1,0],    #State 19
    20:[0,2,1,1],    #State 20
    21:[0,2,1,2],    #State 21
    22:[0,2,2,0],    #State 22
    23:[0,2,2,1],    #State 23
    24:[0,2,2,2],    #State 24
    25:[1,0,0,0],    #State 25
    26:[1,0,0,1],    #State 26
    27:[1,2,0,2],    #State 27
    28:[1,2,0,0],    #State 28
    29:[1,2,0,1],    #State 29
    30:[1,2,0,2],    #State 30
    31:[2,0,0,0],    #State 31
    32:[2,0,0,1],    #State 32
    33:[2,0,0,2],    #State 33
    34:[2,0,1,0],    #State 34
    35:[2,0,1,1],    #State 35
    36:[2,0,1,2],     #State 36
    37:[0,0,0,0],
    38:[1,1,1,1],
    39:[0,2,0,2]
    }

##Objects
sta_if = network.WLAN(network.STA_IF); 
client = MQTTClient("clientID", "industrial.api.ubidots.com", 1883, user = ubidotsToken, password = ubidotsToken)
tim0 = Timer(0)
tim1 = Timer(1)
tim2 = Timer(2)
tim3 = Timer(3)

A=Pin(12,Pin.OUT)
B=Pin(25,Pin.OUT)
#i2c para comunicarse con el sensor de luz
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=40000)
#Se usa una libreria externa del sensor de luz TSL2561
try:
    tsl = TSL2561.TSL2561(i2c)
except:
    print("No se puede leer el sensor de luz")
#Reloj en tiempo real
rtc = RTC()
#Delcaración de los ADCs para los sensores de humedad del suelo
for i in range(len(adc_pins)):
    adc = ADC(Pin(adc_pins[i]))  #Crea un ocjeto ADC en el Pin adc_pins[i]
    adc.atten(ADC.ATTN_11DB)     #Cambia la referencia de 1v a 3,3v
    adc.width(ADC.WIDTH_9BIT)    #Define una precisión de 9bits
    adc_obj.append(adc)          #Agrega el objeto al array de objetos
#Declara los objetos de los sensores de Temperatura y humedad
for i in range(len(dht_pins)):
    d = dht.DHT22(Pin(dht_pins[i])) #Se utiliza una libreria interna
    dht_obj.append(d)               #Agrega el objeto al array de objetos
 



#Objeto tipo PWM para controlar el ventilador del nivel 1
out_ventilator_lvl1 = PWM(Pin(out_pins['level_1']['ventilator']), freq=20000, duty=0)
#Objeto tipo PWM para controlar el calefactor del nivel 1
out_heater_lvl1 = PWM(Pin(out_pins['level_1']['heater']), freq=20000, duty=0)
#Objeto tipo Pin (Salida) para controlar las valvulas del nivel 1
out_valve_lvl1 = Pin(out_pins['level_1']['valve'],Pin.OUT)

#Objetos del nivel 2
out_ventilator_lvl2 = PWM(Pin(out_pins['level_2']['ventilator']), freq=20000, duty=0)
out_heater_lvl2 = PWM(Pin(out_pins['level_2']['heater']), freq=20000, duty=0)
out_valve_lvl2 = Pin(out_pins['level_2']['valve'],Pin.OUT)

#Objetos del nivel 3
out_ventilator_lvl3 = PWM(Pin(out_pins['level_3']['ventilator']), freq=20000, duty=0)
out_heater_lvl3 = PWM(Pin(out_pins['level_3']['heater']), freq=20000, duty=0)
out_valve_lvl3 = Pin(out_pins['level_3']['valve'],Pin.OUT)

#Objeto tipo PWM para controlar las luces LED de todos los niveles
out_led = PWM(Pin(out_pins['light']), freq=20000, duty=0)



##FUNCTIONS
     
def checkwifi():
    while not sta_if.isconnected():
        time.sleep_ms(500)
        print(".")
    sta_if.connect()
    
def wifi_connect():
    sta_if.active(True)
    sta_if.scan() # Scan for available access points
    
    if sta_if.isconnected()!=True:
        print('connecting to network...')
        sta_if.connect("AUCOL.1", "AUCOLS22020") # Connect to an AP
        while not sta_if.isconnected():
            print('1')
            time.sleep_ms(500)
            pass
        print('network config:', sta_if.ifconfig())
        print('2')
    print('Sucess conection')

def publish(moisture, hum_temp, lum, out,state):
    checkwifi()
    msg = b'{"hum_suelo_nivel3_rec1":%s,"hum_suelo_nivel3_rec2":%s,"hum_suelo_nivel3_rec3":%s,' % (int(moisture[0][0]),int(moisture[0][1]),int(moisture[0][2]))
    msg = msg + b'"ventilator_lvl3":%s,"calefactor_lvl3":%s,"valve_lvl3":%s,"LEDS":%s,' % (int(out[2][0]),int(out[2][1]),int(out[0][2]),int(out[2][3]))
    msg = msg + b'"hum_rel_nivel3":%s,"temp_nivel3":%s,"luminescence":%s,"state":%s}' % (hum_temp[2][1],hum_temp[2][0],lum,state[2]) 
    print('Mensaje 1 que se envía:')
    print(msg,'\n') 
    
    client.publish("/v1.6/devices/esp32", msg)
    time.sleep_ms(10000)



def values_scale(adc_values, dht_value,lum_values):    #Escala los valores de humedad relativa, del suelo y temperatura en tres niveles
    
    #adc_values=[10,10,10]

    #Convierte los valores de la humedad del suelo a 0, 1 o 2
    for i in range(len(adc_values)):                    
        if adc_values[i] >= in_ref['mos']['high']:
            adc_values[i] = 2
        elif adc_values[i]<= in_ref['mos']['low']:
            adc_values[i] = 0
        else:
            adc_values[i] = 1
    
    
    print('Valores del sensor de humedad del suelo maximos nivel 1, nivel 2, nivel 3')
    print(adc_values,'\n')
    print('Valores del sensor de [Temperatura Humedad] nivel 1, nivel 2, nivel 3')
    print(dht_value,'\n')
    #dht_values = [[10,10],[10,10],[10,10]]
    for i in range(len(dht_value)):
        for j in range(2):
            if j == 0:
                
                if dht_value[i][j] >= in_ref['tem']['high']:
                    dht_value[i][j] = 2
                elif dht_value[i][j] <= in_ref['tem']['low']:
                    dht_value[i][j] = 0
                else:
                    dht_value[i][j] = 1
            else:
                if dht_value[i][j] >= in_ref['hum']['high']:
                    dht_value[i][j] = 2
                elif dht_value[i][j] <= in_ref['hum']['low']:
                    dht_value[i][j] = 0
                else:
                    dht_value[i][j] = 1
                    
    print('valores normalizados del adc nivel 1, nivel 2, nivel 3')
    print(adc_values ,'\n')
    print('valores normalizados [Temperatura humedad] nivel 1, nivel 2, nivel 3')
    print(dht_value,'\n')
    
    return  (str(lum_values)+str(adc_values[0])+str(dht_value[0][1])+ str(dht_value[0][0]),
             str(lum_values)+str(adc_values[1])+str(dht_value[1][1])+ str(dht_value[1][0]),
             str(lum_values)+str(adc_values[2])+str(dht_value[2][1])+ str(dht_value[2][0]))




 


def measure_soil_moisture():
    adc_values = []
    adc_xlevel = [0,0,0]
    n = 0
    mux = 0
    
    for i in range(len(adc_obj)):
        '''
        if adc_pins[i] == 36:
            if mux == 0:
                A.value(0)
                B.value(1)
            elif mux == 0:
                A.value(1)
                B.value(0)
            elif mux == 0:
                A.value(0)
                B.value(0)
            elif mux == 0:
                A.value(1)
                B.value(1)
                
            mux = mux + 1
            '''
        adc_values.append((1-(adc_obj[i].read()-130)/312)*100)
             
        if adc_values[i] > 100:
            adc_values[i]= 100
        if adc_values[i] < 0:
            adc_values[i] = 0
        
        if not(i+1)%3:            
            adc_xlevel[n]=max(adc_values[i-2:i+1])
            n=n+1
        #time.sleep(1)
    print(adc_values)
    print ("-----------------------------")
    
    return adc_values, adc_xlevel

def measure_humidity_temperature():
    dht_values = []
    dht_v = []
    for i in range(len(dht_obj)):
        try:
            dht_obj[i].measure()
            time.sleep_ms(500)
            dht_values.append([dht_obj[i].temperature(),dht_obj[i].humidity()])
            dht_v.append([dht_obj[i].temperature(),dht_obj[i].humidity()])
        except:
            dht_values.append([0,0])
            dht_v.append([0,0])
    return dht_values,dht_v

def measure_lum():
    
    #adc = ADC(Pin(36))             # create ADC object on ADC pin
    #adc.atten(ADC.ATTN_11DB)
    #adc.width(ADC.WIDTH_9BIT)
    #result = adc.read()
    try:
        result = tsl.read()*17
    except:
        result = 10000
    print(result)

    print('Luminosidad')
    print(result,'\n')


    if rtc.datetime()[4] > 6 and rtc.datetime()[4] < 22:
        dia_noche = 1
    else:
        dia_noche = 0
    
    if result < 60:
        lum = 2
    elif result < 120:
        lum = 1
    else:
        lum = 0
    
    return int(str(dia_noche)+str(lum)),result







def output_ventilator(out_vent):
    out_ventilator_lvl1.duty(int(out_ref['ventilator'][out_vent[0]]*10.23))
    out_ventilator_lvl2.duty(int(out_ref['ventilator'][out_vent[1]]*10.23))
    out_ventilator_lvl3.duty(int(out_ref['ventilator'][out_vent[2]]*10.23))
    print('Valores pwm ventilador nivel 1, nivel 2, nivel 3')
    print(out_ventilator_lvl1.duty(),out_ventilator_lvl2.duty(),out_ventilator_lvl3.duty(),'\n')
    
def output_heater(out_heater):
    out_heater_lvl1.duty(int(out_ref['heater'][out_heater[0]]*10.23))
    out_heater_lvl2.duty(int(out_ref['heater'][out_heater[1]]*10.23))
    out_heater_lvl3.duty(int(out_ref['heater'][out_heater[2]]*10.23))
    print('Valores pwm calefactor nivel 1, nivel 2, nivel 3')
    print(out_heater_lvl1.duty(),out_heater_lvl2.duty(),out_heater_lvl3.duty(),'\n')
    
def output_led(out_light):
    out_led.duty(int(out_ref['light'][out_light]*10.23))
    print('Valores pwm leds')
    print(out_led.duty(),'\n')

    
def output_valve(out_valve):
    tim1.deinit()
    tim2.deinit()
    tim3.deinit()
    out_valve_lvl1.value(out_ref['valve']['value'][out_valve[0]])
    out_valve_lvl2.value(out_ref['valve']['value'][out_valve[1]])
    out_valve_lvl3.value(out_ref['valve']['value'][out_valve[2]])
    
    if out_ref['valve']['value'][out_valve[0]]:
        print('valvula nivel 1 encendida por ',out_ref['valve']['time'][out_valve[0]]/1000,' segundos' ,'\n')
        tim1.init(period=out_ref['valve']['time'][out_valve[0]],mode=Timer.ONE_SHOT, callback=lambda t: (out_valve_lvl1.off(), print('Valvula nivel 1 apagada','\n')))
    if out_ref['valve']['value'][out_valve[1]]:
        print('valvula nivel 2 encendida por ',out_ref['valve']['time'][out_valve[1]]/1000,' segundos' ,'\n')
        tim2.init(period=out_ref['valve']['time'][out_valve[1]],mode=Timer.ONE_SHOT, callback=lambda t: (out_valve_lvl2.off(), print('Valvula nivel 2 apagada','\n')))
    if out_ref['valve']['value'][out_valve[2]]:
        print('valvula nivel 3 encendida por ',out_ref['valve']['time'][out_valve[2]]/1000,' segundos' ,'\n')
        tim3.init(period=out_ref['valve']['time'][out_valve[2]],mode=Timer.ONE_SHOT, callback=lambda t: (out_valve_lvl3.off(), print('Valvula nivel 3 apagada','\n')))



 





def main():
    print('---------------------------------')
    global var
    if var == 10:
        reset()
    var = var +1
    print(var)
    
    adc_values = measure_soil_moisture()
    dht_values,dht_v = measure_humidity_temperature()    
    lum_values,result = measure_lum()
    input_val = values_scale(adc_values[1],dht_values,lum_values)
    
      
    
    print('Valores de entrada [Dia/noche Lum HS HR Temp]')
    print(input_val,'\n')
    
    for i in range(3):
        state[i] = inputs[int(input_val[i])]
        output[i] = outputs[state[i]]
        
    print('Estado nivel 1, nivel 2, nivel 3')
    print(state,'\n')
    
    print('Valores de salida [Vent Calef Riego Luces]')
    print(output,'\n')
    
    
    #Salidas (Nivel 1, Nivel 2, Nivel 3)
    
    output_ventilator([output[0][0],output[1][0],output[2][0]])
    output_heater([output[0][1],output[1][1],output[2][1]])
    output_valve([output[0][2],output[1][2],output[2][2]])
    output_led(output[0][3])




    publish(adc_values,dht_v,result,output,state)
    


##Function calls 
wifi_connect()
client.connect()
# synchronize with ntp, need to be connected to wifi
try:
    ntptime.settime() # set the rtc datetime from the remote server
    rtc.datetime((rtc.datetime()[0],rtc.datetime()[1],rtc.datetime()[2],rtc.datetime()[3],rtc.datetime()[4]-5,rtc.datetime()[5],rtc.datetime()[6],rtc.datetime()[7]))
except:
    print('No es posible obtener la hora')
    rtc.datetime((2020, 10, 21, 2, 10, 0, 0, 0))
    
main()

tim0.init(period=TIME_TIMER,mode=Timer.PERIODIC, callback=lambda t: main())
 



