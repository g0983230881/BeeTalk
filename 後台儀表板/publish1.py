import paho.mqtt.publish as publish

host = "203.145.202.162"              # Broker's IP
topic = "NIU/a"           # Topic
var =1                          # Declare variable
while True:                  # Infinite loop
	payload = 1 # content of the message
	publish.single(topic, payload, qos=1, hostname=host) #publish message
