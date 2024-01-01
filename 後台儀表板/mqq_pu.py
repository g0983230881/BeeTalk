import paho.mqtt.publish as publish

host = "203.145.202.162"              # Broker's IP
topic = "NIU"           # Topic
var =1                          # Declare variable
while var ==1:                  # Infinite loop
	payload = input('Please enter your message：')  # content of the message
	publish.single(topic, payload, qos=1, hostname=host) #publish message
