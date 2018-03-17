package main

import (
	"flag"
	"fmt"
	"math/rand"
	"strings"
	"time"

	"github.com/surgemq/message"
	"github.com/surgemqTCPService/service"
)

func setConnMsg(version int, ID string, KeepAlive int) *message.ConnectMessage {
	msg := message.NewConnectMessage()
	msg.SetVersion(byte(version))
	msg.SetClientId([]byte(ID))
	msg.SetKeepAlive(uint16(KeepAlive))
	//msg.SetUsername([]byte("surgemq"))
	//msg.SetPassword([]byte("verysecret"))
	return msg
}

func setPubMsg(Id int, topic string, payload string, qos int) *message.PublishMessage {
	pubmsg := message.NewPublishMessage()
	pubmsg.SetPacketId(uint16(Id))
	pubmsg.SetTopic([]byte(topic))
	pubmsg.SetPayload([]byte(payload))
	pubmsg.SetQoS(byte(qos))
	return pubmsg
}

func main() {
	version := flag.Int("v", 3, "Version of MQTT Client")
	CliID := flag.String("id", "Pub", "Client Id, a string")
	KeepAlive := flag.Int("alive", 5, "Timeout time")
	targetHost := flag.String("h", "localhost:1883", "Broker host address")
	topic := flag.String("t", "test", "Topic")
	// message := flag.String("m", "Steal your heart!", "Message body")
	MsgQosLevel := flag.Int("q", 0, "QoS level")
	PayloadSize := flag.Int("size", 1, "Payload Size")
	flag.Parse()

	message := strings.Repeat("A", *PayloadSize*1024) // payload size in MB

	// Instantiates a new Client
	c := &service.Client{}

	// Creates a new MQTT CONNECT message and sets the proper parameters
	msg := setConnMsg(*version, *CliID, *KeepAlive)

	// Connects to the remote server at 127.0.0.1 port 1883
	c.Connect("tcp://"+*targetHost, msg)

	fmt.Println("connected")
	// Creates a new PUBLISH message with the appropriate contents for publishing
	pubmsg := setPubMsg(rand.Intn(65536), *topic, message, *MsgQosLevel)

	// Publishes to the server by sending the message
	c.Publish(pubmsg, nil)

	time.Sleep(1 * time.Second)
	// Disconnects from the server
	c.Disconnect()
}
