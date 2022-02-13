import machine #to connect with the ESP32
import network #configure wifi and wifi router
import wifi_credentials # ssid and pswd
import urequests #simplify Restful API
import time 
import flood_monitoring #HCSR04

#Create Object:
led = machine.Pin(2, machine.Pin.OUT)
ultrasonic = flood_monitoring.HCSR04(
    trigger_pin=13,
    echo_pin=12,
    echo_timeout_us=1000000)

#Configure the ESP32 wifi as STAtion
sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    sta.connect(wifi_credentials.ssid, wifi_credentials.password)
    while not sta.isconnected():
        pass
    print('network config:', sta.ifconfig())
    
#Constant and variables
HTTP_HEADERS = {'Content-Type':'application/json'}
THINGSPEAK_WRITE_API_KEY = 'CFT68GPBVHZE0ESQ'
UPDATE_TIME_INTERVAL = 15000 # in ms
last_update = time.ticks_ms()

#Main loop
while True:
    if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
        d = ultrasonic.distance_cm()
        
        distance_readings = {'field1':d}
        request = urequests.post(
            'https://api.thingspeak.com/update?api_key=Z14B8LPQLEMCUQ23&field1=0' + str(d),
            json = distance_readings,
            headers = HTTP_HEADERS)
        request.close()
        print(distance_readings)
        
        led.value(not led.value())
        last_update = time.ticks_ms()
        