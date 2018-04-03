package main

import (
        "crypto/rand"
        "crypto/rsa"
        "crypto/tls"
        "crypto/x509"
        "encoding/pem"
        // "fmt"
        "net"
        "io"
        // "time"
        "math/big"

)

const addr = "0.0.0.0:1883"
// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.
func main() {
        echoServer()
}

// Start a server that echos all data on the first stream opened by the client
func echoServer() error {
        listener, err := tls.Listen("tcp",addr, generateTLSConfig())
        if err != nil {
                return err
        }
        for{
                conn, err := listener.Accept()
                if err != nil {
                        continue
                }
                go echoSession(conn)
        }
        return nil
}

func echoSession(stream net.Conn) error{
        // Echo through 
        _, err := io.Copy(stream, stream)
        if err!= nil{
                return err
        }
        return nil
}

// Setup a bare-bones TLS config for the server
func generateTLSConfig() *tls.Config {
        key, err := rsa.GenerateKey(rand.Reader, 1024)
        if err != nil {
                panic(err)
        }
        template := x509.Certificate{SerialNumber: big.NewInt(1)}
        certDER, err := x509.CreateCertificate(rand.Reader, &template, &template, &key.PublicKey, key)
        if err != nil {
                panic(err)
        }
        keyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(key)})
        certPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certDER})

        tlsCert, err := tls.X509KeyPair(certPEM, keyPEM)
        if err != nil {
                panic(err)
        }
        return &tls.Config{Certificates: []tls.Certificate{tlsCert}}
}