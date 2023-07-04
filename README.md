
My workspace
 / 
Home Weather Station
Home Weather Station

Hanna Lindgren
hl223ki

This is a little tutorial for a project in the course Applied IoT at Linneaus University.
By using among other things a micro controller, temperature and humidity sensor and a WiFi connection I was able to create a little weather station. I can monitor the transmitted data through a cloud service.

Approximate time consumtion: 1-2h
Objective

I have chosen to make a weather station for easy and flexible readings of the air around my house. Wether I choose to place it on our balcony where my tomatoes might need more humidity or inside so that my parter doesn’t overheat! I might have to make another one so that everyone is happy.

My little weather station will be able to give me reliable info about the current temperature and humidity that I can follow in real time through my phone or PC browser, where ever I am.

This is a very good first project for a IoT newbie like I definately was. You will learn about connecting different devices both with code and physical components. It gives a good first look into what can be done in IoT with relatively simple measures and a small budget. I’ve also included a visualisation of the project through 2 LEDs in different colors indicating is the measurement went as it should. It gives a physical verification that the device still is running and measuring without having to check further.
Material

Fortunately the course is in collaboration with a company named Electrokit, who put together a small kit for students with the basic components and some sensors. I have mainly used products from this bundle.
Image 	Product 	Store 	Price
	Raspberry Pi Pico W 	Electrokit 	98 kr
	USB cable A-male to micro B-male 	Electrokit 	39 kr
	DHT11 - Digital temperature and humidity sensor 	Electrokit 	49 kr
	Breadboard 	Electrokit 	69 kr
	LED 5mm green diffuse 80mcd 	Electrokit 	5 kr
	LED 5mm red diffuse 1500mcd 	Electrokit 	5 kr
	Resistor carbon film 0.25W 330ohm (330R) 	Electrokit 	1 kr
	Resistor carbon film 0.25W 560ohm (560R) 	Electrokit 	1 kr
	Breadboard jumper cables 	Temu 	5 kr

Total amount: 272 kr
The prices are approximate as many of the products are bought as parts of kits.
Setup

Preparing the Pico
Before connecting the Pico device we need to download the neccesary software so that we can run micropython on the Pico.
Go to raspberry Pis’ official website and download the latest version of the SDK (Software Development Kit) to your computer.

While pressing down the BOOTSEL button on your Pico plug the usb cable into the PC. The Pico should appear as a drive. Place the SDK file on the Picos drive and wait until it automatically disconnects.

Computer setup

Install the following software according to your needs:

    Python
    Node.js
    VS Code and the plugin PyMakr
    Thonny can be an alternative to VS Code

    I chose to work mostly in VS Code, but before getting a hold on how it worked I used Thonny because of the simplicity. Thonny in my opinion is more of a plyg’n’play IDE and has an easier way of overlooking files, where VS Code can be a little confusing.

Putting everything together

Start by connecting the 3V3 output pin on the pico to the red line (+) on the breadboard. This will now give power to what ever is connected to it. Then connect a wire between GND and the blue line (-) on the breadboard. This will allow a current to flow through the components.
When looking at the DHT11 sensor from in front of it, connect the middle pin to the red line and the right pin to the blue line. We can now have a current. To be able to send data from the sensor, connect the left pin of the sensor to any GPIO pin of the pico (in my case GPIO pin 27).

The LEDs get power through the GPIO pin, and therefore only need to be connected to that pin and GND. We do need resistors depending on how bright we want the lights to be. I’ve chosen to connect the red led from GPIO 14, through a 560 ohm resistor to GND. The green LED is connected to GPIO pin 15, through a 330 ohm resistor and then to GND.
Platform

I chose to use adafruit.io as platform for my project. It’s a user friendly and free cloud service that felt like a good choice for me. I could pretty quickly start visualising the data being sent from the pico and customize the dashboard according to my taste.

As an MQTT broker Adafruit IO provides an easy setup for connections, data storage, different dashboard alternatives and a secure way of retrieving data due to SSL/TLS encryption. It is good for smaller projects, whereas a larger project or solution might need a more powerful message broker like RabbitMQ where more of the focus is on availability and scalability.

RabbitMQ for example supports sharding which is a more scalable way of distributing the data. A query gets sent to several nodes, who then can work paralell to each other. Each node is responsible for storing a specific set of data, and is later combined with the other nodes to form the result. As the project grows it’s easy to add more nodes to the project.

 Describe the different alternatives on going forward if you want to scale your idea.

Describe platform in terms of functionality

The code

Libraries:

import dht Used to communicate with the DHT11 sensor
import config as c Login/user details for WiFi and Adafruit connection
import utime A module for time-related functions
import network A module for using the built in WiFi on the Pico
from machine import Pin Used to make connections to and from the pins of the pico
from simple import MQTTClient import a class responsible for connection to the MQTT servers

I have chosen to use premade libraries and code inspiration from the applied-iot-lnu HackMD.
With a little help from ChatGPT 4 as a bug finder I have customized the code to fit my project needs.

Code snippet:

def sens_data():
    """Measure temperature and humidity from DHT11 sensor, publish to Adafruit IO."""
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

This function is responsible for measuring and publishing the data. The print statements are not neccesary but I found myself connecting the pico to my PC several times, and therefore left the code for debugging purposes. It uses the sleep function to wait 30 seconds until it does it again. I have chosen to physically visualise the error message with a red LED:

(A very short loop, it doesn’t blink this crazily, only once if an error occured in the code.)

The short, but sweet, main loop:

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

I found that the LEDs sometimes could get stuck in value(1) and kept shining outside of the normal span, so I chose to make sure they are turned off in the beggining of the main loop.
To make sure that the program keeps running i chose to place the connect_wifi and connect_mqqt functions in the main loop.
Transmitting data

I chose to use WiFi to connect the pico to the internet. The project would work fine and be more portable if using for example a LoRaWan, but due to the convenience of having a WiFi chip on the Pico I opted to go for that.

I’m using the MQTT broker Adafriut. I also tried using webhook and send the data through discord, but due to the lack of visualisation possibilities I gave up on that idea. The adafriut dashboard gave a better package with both smooth transportation and presentation.

Data from the DHT sensor is being sent every 30 seconds to get an accurate representation of the changes in temperature and humidity.
Presenting the data

Through Adafruit I have created a dashboard showing the temperature and humidity in two ways each. One kind with the current readings, and the other with a graph showing the results over a time span of 8 hours. The feed gets updated every 30 seconds.
I also have chosen to keep track of the success vs fail rate, and it’s visualized together with date and time.

Data is saved for 30 days on Adafruit, but you can decide yourself if you want it to be saved for that long or not.
Finalizing the design

The final product:

Over all it went fine for a first time IoT project. I bumped into some minor issues here and there but in the end it turned out ok but if I were to redo the project I would maybe go for a more complex build. Or maybe tried a portable way of powering the pico instead of an AC adapter. If for example I connected it through the LoRa network and powered it with batteries I could have used the pico in our basement, where I have seen some signs of possible water leaks. (Good thing we’re moving soon!)
Select a repo
