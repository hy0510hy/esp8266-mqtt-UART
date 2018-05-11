# main.pyimport network
import webrepl
import network
from umqtt.simple import MQTTClient
from machine import Pin
from machine import UART
import ubinascii
import machine
import utime
import array
from machine import Timer

#LED = Pin(2,Pin.OUT, value=0)
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
CONFIG = {
    "broker": "192.168.31.85",
    "mqtt_user": "hass",
    "mqtt_password": "000510",
    "mqtt_topic_command": b"study/ac/temperature/set",
    "mqtt_topic_state": b"hachina/hardware/led01/state"
} 
SSID = "Xiaomi_58BC"
PASSWORD = "12345678"
uart = None
counter = 0
c=None
arrcheckinfo = array.array('B',[0x7e,0x01,0x01,0x05,0x07])
def control(code):
    if code == 1:#开机
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x06,0x01])
        arr.append(0x01+0x03+0x04+0x06+0x01);
        arr.append(0x0d)
    elif code == 2:#关机
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x06,0x00])
        arr.append(0x01+0x03+0x04+0x06+0x00);
        arr.append(0x0d)
    elif code == 3:#强风
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x0a,0x05])
        arr.append(0x01+0x03+0x04+0x0a+0x05);
        arr.append(0x0d)
    elif code == 4:#弱风
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x0a,0x01])
        arr.append(0x01+0x03+0x04+0x0a+0x01);
        arr.append(0x0d)  
    elif code == 5:#自动
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x08,0x03])
        arr.append(0x01+0x03+0x04+0x08+0x03);
        arr.append(0x0d)
    elif code == 6:#制冷
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x08,0x02])
        arr.append(0x01+0x03+0x04+0x08+0x02);
        arr.append(0x0d)  
    elif code == 7:#制热
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x08,0x01])
        arr.append(0x01+0x03+0x04+0x08+0x01);
        arr.append(0x0d) 
    elif code == 8:#除湿
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x08,0x07])
        arr.append(0x01+0x03+0x04+0x08+0x07);
        arr.append(0x0d)
    elif code == 9:#送风
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x08,0x00])
        arr.append(0x01+0x03+0x04+0x08+0x00);
        arr.append(0x0d)
    elif code == 9:#设温度
        arr = array.array('B',[0x7e,0x01,0x03,0x04,0x09,0x00])
        arr.append(0x01+0x03+0x04+0x08+0x00);
        arr.append(0x0d)   
    return arr     

def uartread(timer):
    global counter
    #print('timer on:',counter)
    if uart.any()>0:
        data = uart.read()
        print(len(data),data[0])
        counter = counter+1

def inituart(num):
    global uart
    uart = UART(num,9600)
    uart.init(9600, bits=8, parity=None, stop=1)
    #print('uart num is ',num)
    #while True:
    #    utime.sleep(2)
    #    uart.write('uart ok ')


def sub_cb(topic, msg):
    global c
    global uart
    #print((topic, msg))
    if msg == b'\xe5\x85\xb3\xe6\x9c\xba':#关机
        #LED.value(1)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"Off" )
            uart.write(control(2))
    elif msg == b'\xe5\xbc\x80\xe6\x9c\xba':#开机
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"On" )
            uart.write(control(1))
    elif msg == b'\xe5\x88\xb6\xe5\x86\xb7':#制冷
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"cool" )
            uart.write(control(6))
    elif msg == b'\xe5\x88\xb6\xe7\x83\xad':#制热
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"heat" )
            uart.write(control(7))
    elif msg == b'\xe8\x87\xaa\xe5\x8a\xa8':#自动
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"auto" )
            uart.write(control(5))
    elif msg == b'\xe9\x99\xa4\xe6\xb9\xbf':#除湿
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"wet" )
            uart.write(control(8))
    elif msg == b'\xe9\x80\x81\xe9\xa3\x8e':#送风
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"fan" )
            uart.write(control(9))
    elif msg == b'\xe9\x80\x81\xe9\xa3\x8e':#弱风
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"OFF" )
            uart.write(control(1))
    elif msg == b'\xe9\x80\x81\xe9\xa3\x8e':#强风
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            fc = c.publish( CONFIG["mqtt_topic_state"], b"OFF" )
            uart.write(control(1))
    elif len(msg) <6:#设置温度
        #LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            arr = array.array('B',[0x7e,0x01,0x03,0x04,0x09])
            stra = msg.decode().split('.')
            imsg = int(stra[0])
            arr.append(imsg)
            arr.append(0x01+0x03+0x04+0x09+imsg);
            arr.append(0x0d)  
            fc = c.publish( CONFIG["mqtt_topic_state"], b"temperature" )
            uart.write(arr)                                                          
def mqtt():
    global c
    # 创建MQTT的客户端对象
    c = MQTTClient(CLIENT_ID, CONFIG["broker"], user=CONFIG["mqtt_user"], password=CONFIG["mqtt_password"])
 
    # 设置当订阅的信息到达时的处理函数
    c.set_callback(sub_cb)
 
    # 连接MQTT代理服务器
    c.connect()
 
    # 订阅命令信息
    fc = c.subscribe(CONFIG["mqtt_topic_command"])
    #print("Connected to %s, subscribed to %s topic" % (CONFIG["broker"], CONFIG["mqtt_topic_command"]))
 
    try:
        while True:
            c.wait_msg()
    finally:
        c.disconnect()

def do_connect():

	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	if not wlan.isconnected():
		print('connecting to network...')
		wlan.connect(SSID, PASSWORD)

	start = utime.time()
	while not wlan.isconnected():
		utime.sleep(1)
		if utime.time()-start > 5:
			print("connect timeout!")
			break

	if wlan.isconnected():
		print('network config:', wlan.ifconfig())

do_connect()
inituart(0)
tim = Timer(-1)
tim.init(period=500, mode=Timer.PERIODIC, callback=uartread)
mqtt()
