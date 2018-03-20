package main

import (
	"flag"
	"fmt"
	"time"

	"github.com/surge/glog"
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

func onPublishCallback(msg *message.PublishMessage) error {
	fmt.Println(msg)
	return nil
}

func main() {
	version := flag.Int("v", 3, "Version of MQTT Client")
	CliID := flag.String("id", "Sub", "Client Id, a string")
	KeepAlive := flag.Int("alive", 30, "Timeout time")
	targetHost := flag.String("h", "localhost:1883", "Broker host address")
	topic := flag.String("t", "test", "Topic")
	MaxQosLevel := flag.Int("q", 0, "Max QoS level")

	flag.Parse()

	// Instantiates a new Client
	c := &service.Client{}

	// Creates a new MQTT CONNECT message and sets the proper parameters
	msg := setConnMsg(*version, *CliID, *KeepAlive)

	// Connects to the remote server at 127.0.0.1 port 1883
	err := c.Connect("tcp://"+*targetHost, msg)
	if err == nil {
		fmt.Println("connect succesfully")
	}else{
		glog.Errorf("connect fail %v", err)
	}

	submsg := message.NewSubscribeMessage()
	submsg.AddTopic([]byte(*topic), byte(*MaxQosLevel))
	err = c.Subscribe(submsg, nil, onPublishCallback)
	if err == nil {
		fmt.Println("subscribed succesfully")
	}else{
		glog.Errorf("subscribe fail %v", err)
	}
	for {
		if c.isDone(){
			break
		}
		err = c.Ping(nil)
		if err != nil{
			glog.Errorf("%v", err)
			break
		}
		time.Sleep(10 * time.Second)	
	}
	// Disconnects from the server
	c.Disconnect()
}
