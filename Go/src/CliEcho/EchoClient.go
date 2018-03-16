package main

import (
	"flag"
	// "crypto/rand"
	// "crypto/rsa"
	"crypto/tls"
	// "crypto/x509"
	// "encoding/pem"
	"fmt"
	// "io"
	// "log"
	// "reflect"
	// "math/big"

	quic "github.com/lucas-clemente/quic-go"
)

const message = "foobar"

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

	flag.Parse()

	session, err := quic.DialAddr(*targetHost, &tls.Config{InsecureSkipVerify: true}, nil)
	if err != nil {
		return err
	}

	stream, err := session.OpenStreamSync()
	if err != nil {
		return err
	}
	fmt.Printf("Client: Sending '%s'\n", message)
	_, err = stream.Write([]byte(message))
	if err != nil {
		return err
	}

	buf := make([]byte, len(message))
	_, err = stream.Read(buf)
	if err != nil {
		return err
	}
	fmt.Printf("Client: Got '%s'\n", buf)
	stream.Close()
	session.Close(nil)
	return nil
}