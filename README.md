# MQTT_on_QUIC
It's a ongoing project right now.
The ultimate goal is to migrate MQTT from TCP to QUIC and evaluate its performance.

## Milestones
- [x] Implement SurgeMQ test Clients
- [x] Get QuicGo server/client work(learn the interface)
- [x] Evaluate SurgeMQ(plain) test Client in Mininet
- [x] Migrate SurgeMQ to QUIC
- [x] Evaluate SurgeMQ(QUIC) test Client in Mininet

## Method for migration:
We map the TCP connection to QUIC stream in MQTT implementation. However, it is also possible to map topics as seperate QUIC streams to avoid Head of Line Blocking(May be done in future).

## What we Found
- QUIC stream perform better than TCP connection in lossy condition but not in perfect network

- MQTT with QUIC perform better than MQTT with TCP in perfect network but not in lossy network

## Working Environment Dependency
1. QUIC-go: https://github.com/lucas-clemente/quic-go
2. SurgeMQ: https://github.com/surgemq/surgemq(Clear implementation but with lots of bugs)
3. Golang 1.9
4. Mininet 2.2 on Ubuntu 14.04LTS 64bit(https://github.com/mininet/mininet/wiki/Mininet-VM-Images)

## Usage Instruction:
1. Set environment variable $GOPATH to proper path.

## Reference:
1. Taking a Long Look at QUIC(https://conferences.sigcomm.org/imc/2017/papers/imc17-final39.pdf)
2. draft-ietf-quic-transport-10(https://datatracker.ietf.org/doc/draft-ietf-quic-transport/)
3. MQTT Specification(http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)

