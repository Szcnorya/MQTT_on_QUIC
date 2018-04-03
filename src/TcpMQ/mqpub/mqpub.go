package main

import (
	"flag"
	"time"
	"math/rand"

	"github.com/surgemqTCPService/service"
   	"github.com/surgemq/message"
)

func setConnMsg(version int, ID string, KeepAlive int) *message.ConnectMessage{
	msg := message.NewConnectMessage()
	msg.SetVersion(byte(version))
	msg.SetClientId([]byte(ID))
	msg.SetKeepAlive(uint16(KeepAlive))
	//msg.SetUsername([]byte("surgemq"))
	//msg.SetPassword([]byte("verysecret"))
	return msg
}

func setPubMsg(Id int, topic string, payload int, qos int) *message.PublishMessage{
	pubmsg := message.NewPublishMessage()
	pubmsg.SetPacketId(uint16(Id))
	pubmsg.SetTopic([]byte(topic))
	pubmsg.SetPayload(make([]byte,payload*1024))
	pubmsg.SetQoS(byte(qos))
	return pubmsg
}

func main(){
	version := flag.Int("v",3,"Version of MQTT Client")
	CliID := flag.String("id","Pub","Client Id, a string")
	KeepAlive := flag.Int("alive",10, "Timeout time")
	targetHost := flag.String("h","localhost:1883","Broker host address")
	topic := flag.String("t","test","Topic")
	message := flag.Int("m",1,"Message body legnth")
	MsgQosLevel := flag.Int("q",0,"QoS level")

	flag.Parse()

	// Instantiates a new Client
	c := &service.Client{}

	// Creates a new MQTT CONNECT message and sets the proper parameters
	msg := setConnMsg(*version,*CliID,*KeepAlive)

	// Connects to the remote server at 127.0.0.1 port 1883
	c.Connect("tcp://"+ *targetHost, msg)

	// Creates a new PUBLISH message with the appropriate contents for publishing
	pubmsg := setPubMsg(rand.Intn(65536),*topic,*message,*MsgQosLevel) 

	// Publishes to the server by sending the message
	c.Publish(pubmsg, nil)

	time.Sleep(1*time.Second)
	// Disconnects from the server
	c.Disconnect()
}
