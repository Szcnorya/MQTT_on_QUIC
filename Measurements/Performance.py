#!/usr/bin/env python2

import time
import re
from multiprocessing import Pool
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.clean import Cleanup
#setLogLevel("info")

RUN_TIME = 30

DELAYS = (50,)
BANDWIDTHS = (2,)
LOSSES = (2,)


class SimpleTopology(Topo):

    def build(self, **opts):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip="192.168.0.1/24") 
        h2 = self.addHost('h2', ip="192.168.0.2/24")
        h3 = self.addHost('h3', ip="192.168.0.3/24")
        self.addLink(h1, s1,**opts)
        self.addLink(h2, s1,**opts)
        self.addLink(h3, s1,**opts)

    @staticmethod
    def create_net(**opts):
        return Mininet(topo=SimpleTopology(**opts), link=TCLink)

def performance_test(sub_cmd, pub_cmd, brok_cmd, protocol, **opts):
    print("Starting performance test run with parameters %s" % opts)
    #create topology
    net = SimpleTopology.create_net(**opts)
    net.start()

    #get handlers to all the nodes
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')

    # start broker on h3 and give it some time to settle
    h3.sendCmd(brok_cmd)
    time.sleep(1)
    print("Running server:%s\n" % brok_cmd)
    
    # open the file to write the output
    if protocol == 'tcp':
        ofile = open('meas_tcp/server_run_%s' % ('_'.join("%s" % val for (key,val) in opts.iteritems())), 'w')
    else:
        ofile = open('meas_quic/server_run_%s' % ('_'.join("%s" % val for (key,val) in opts.iteritems())), 'w')
    logfile = open('logfile', 'w')
    

    #start the measurements for different payload sizes
    log = ""
    for payloadSize in range(1,250,10):

        print("running payload size %s" % payloadSize)
        avg = 0.0
        for count in range(15):
            print('count='+str(count))
            #start subscriber on h1
            h1.sendCmd(sub_cmd)
            time.sleep(1)

            start = time.time() # get start time

            # start publisher on h2 with different payloadsizes to publish
            h2.sendCmd(pub_cmd+' -size='+str(payloadSize))
            
            #wait until subsriber finishes -- it would end as soon as it gets first message
            while(h1.waiting):
                print("here")
                ret = h1.monitor()
                print ret

            end = time.time() # get end time
            avg += end - start

        timeTaken = avg/15
        toWrite = str(payloadSize) + " " + str(timeTaken) + "\n"
        #write the output to file
        ofile.write(toWrite)
        logfile.write(log+'\n\n\n')
        

        # for stopping every program running on all the hosts
        # for host in [h1,h2,h3]:
        #     host.sendInt()
        #     while(host.waiting):
        #         host.monitor()
    
    # stop broker which is running in background before closing net
    h3.sendInt()
    while(h3.waiting):
        h3.monitor()

    ofile.close()
    logfile.close()
    net.stop()
    print("Performance test finished")

def run_all_tests_sequentially():
    
    for delay in DELAYS:
        for bw in BANDWIDTHS:
            for loss in LOSSES:
                performance_test('mqsubtcp -h=192.168.0.3:1883 -t=test -alive=1000', 'mqpubtcp -h=192.168.0.3:1883', 'surgemqtcp', 'tcp', delay=str(delay)+"ms", bw=bw, loss=loss)
                
                Cleanup.cleanup()

    for delay in DELAYS:
        for bw in BANDWIDTHS:
            for loss in LOSSES:
                performance_test('mqsubquic -h=192.168.0.3:1883 -t=test -alive=1000', 'mqpubquic -h=192.168.0.3:1883', 'surgemqquic', 'quic', delay=str(delay)+"ms", bw=bw, loss=loss)
                
                Cleanup.cleanup()
                
def run_cli():
    net = SimpleTopology.create_net()
    net.start()
    CLI(net)
    net.stop()

#run_cli()
run_all_tests_sequentially()
