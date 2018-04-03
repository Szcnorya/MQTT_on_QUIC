package main

import (
	"flag"
	"crypto/tls"
	"fmt"
	// "io"
	// "log"
	// "reflect"
	// "math/big"
)


// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.
func main() {
	err := clientMain()
	if err != nil {
		panic(err)
	}
}

func clientMain() error {
	targetHost := flag.String("h","localhost:1883","host address")
	messageSize := flag.Int("sz",10,"message size")
	messageCnt := flag.Int("cnt",1,"total sent message count")
	message := make([]byte, *messageSize)

	flag.Parse()

	conn, err := tls.Dial("tcp",*targetHost, &tls.Config{InsecureSkipVerify: true})
	if err != nil {
		return err
	}
	for i:=0; i<*messageCnt; i++{
		_, err = conn.Write([]byte(message))
		if err != nil {
			return err
		}

		buf := make([]byte, len(message))
		_, err = conn.Read(buf)
		if err != nil {
			return err
		}
	}
	fmt.Printf("Client: Everything\n")
	conn.Close()
	return nil
}