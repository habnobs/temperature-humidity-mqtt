import dht
import config as c
import utime
import network
from machine import Pin
from simple import MQTTClient

# Sensor and LED setup
sensor = dht.DHT11(Pin(27, Pin.OUT, Pin.PULL_DOWN))  # DHT11 Sensor on Pin 27 of Pico W
red_led = Pin(14, Pin.OUT)
green_led = Pin(15, Pin.OUT)

# Wifi and Adafruit configuration
wifi_ssid = c.wifi_ssid
wifi_password = c.wifi_password

adafruit_io_url = c.adafruit_io_url
adafruit_username = c.adafruit_username
adafruit_io_key = c.adafruit_io_key

temperature_feed = f'{adafruit_username}/feeds/temperature'
humidity_feed = f'{adafruit_username}/feeds/humidity'

# Success and fail counters
success_count = 0
fail_count = 0

success_feed = f'{adafruit_username}/feeds/success_count'
fail_feed = f'{adafruit_username}/feeds/fail_count'


# MQTT client setup
client = MQTTClient('dht11_mqtt_client', adafruit_io_url,
                    user=adafruit_username, password=adafruit_io_key)


def connect_wifi():
    """Connect to the WiFi network"""
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    print('Connecting to WiFi...')
    wifi.connect(wifi_ssid, wifi_password)
    while not wifi.isconnected():
        utime.sleep(1)
    print('Connected to WiFi')


def sens_data():
    """Measure temperature and humidity data from the DHT11 sensor and publish it to Adafruit IO."""
    global success_count, fail_count
    
    try:
        sensor.measure
        temperature = sensor.temperature
        humidity = sensor.humidity
        print("Temperature:", temperature)
        print("Humidity:", humidity)

        client.publish(temperature_feed, str(temperature))
        client.publish(humidity_feed, str(humidity))
        success_count += 1
        led_blink('green')
        
    except Exception as e:
        print('Error in sens_data:', e)
        fail_count += 1
        led_blink('red')
        
    client.publish(success_feed, str(success_count))
    client.publish(fail_feed, str(fail_count))


def connect_mqtt():
    """Connect to the Adafruit IO MQTT broker."""
    try:
        client.connect()
        print('Connected to Adafruit IO MQTT')
    except Exception as e:
        print('Error connecting to Adafruit IO MQTT:', e)
        
        
def led_blink(color):
    """Blink an LED of the specified color ('red' or 'green')."""
    if color == 'red':
        led = red_led
    elif color == 'green':
        led = green_led
    else:
        print(f"Error: Invalid color {color}")
        return
    led.value(1)
    utime.sleep(0.75)
    led.value(0)
    

if __name__ == '__main__':
    red_led.value(0)
    green_led.value(0)
    connect_wifi()
    connect_mqtt()
    while True:
        try:
            sens_data()
        except Exception as e:
            print('Error:', e)
        utime.sleep(30)
