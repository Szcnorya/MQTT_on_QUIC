#!/usr/bin/env python2

import time
import signal
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

DELAYS = (100,50)
BANDWIDTHS = (2,5)
LOSSES = (1,2)


class SimpleTopology(Topo):

    def build(self, **opts):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip="10.0.0.1/24") 
        h2 = self.addHost('h2', ip="10.0.0.2/24")
        h3 = self.addHost('h3', ip="10.0.0.3/24")
        self.addLink(h1, s1,**opts)
        self.addLink(h2, s1,**opts)
        self.addLink(h3, s1,**opts)

    @staticmethod
    def create_net(**opts):
        return Mininet(topo=SimpleTopology(**opts), link=TCLink)

def kill(host):
    """ 
    Description: this method kills all the processes which are running on the host
    Args:
        host: the handler to the host on which all the process are to be killed
    Returns:
        none
    """
    didnt_kill = False
    host.sendInt()
    signal.signal(signal.SIGALRM, alarm_handler_kill)
    signal.alarm(20)
    while(host.waiting):
        try:
            host.monitor()
        except OSError, e:
            signal.alarm(0)
            didnt_kill = True
            break
    if didnt_kill:
        kill(host)
    
    

def alarm_handler(signum, frame):
    print "Timed-out"
def alarm_handler_kill(signum, frame):
    print "Timed out in kill process"

def performance_test(protocol, **opts):
    print("Starting performance test run with parameters %s" % opts)
    logfile.write("starting performance test for "+ protocol + "with parameters"+str(opts))

    brok_cmd = 'surgemq'+protocol
    sub_cmd = 'sub ' + protocol
    
    #create topology
    net = SimpleTopology.create_net(**opts)
    net.start()

    #get handlers to all the nodes
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')

    # start broker on h3 and give it some time to settle
    
    print("Running server:%s\n" % brok_cmd)
    
    # open the file to write the output
    if protocol == 'tcp':
        ofile = open('meas_tcp/server_run_%s' % ('_'.join("%s" % val for (key,val) in opts.iteritems())), 'w')
    else:
        ofile = open('meas_quic/server_run_%s' % ('_'.join("%s" % val for (key,val) in opts.iteritems())), 'w')
    
    payload_size = 5
    while payload_size < 16:

        h3.sendCmd(brok_cmd)
        time.sleep(1)
        
        pub_cmd = 'pub ' + protocol + ' ' + str(payload_size)

        log = ""
        dont_count = False

        h2.sendCmd(sub_cmd)
        time.sleep(1)

        h1.sendCmd(pub_cmd)
        
        # --------- ----------- ----------- --------------- ------------ ----------- ---------- ---------
        # things to be measured in here
        start = time.time()
        #wait until subsriber finishes -- it would end as soon as it gets 100 messages

        while(h2.waiting):
            signal.signal(signal.SIGALRM, alarm_handler) # to break the monitor call if it does not return
            signal.alarm(15)

            try:
                ret = h2.monitor()
            except OSError,e:
                dont_count = True
                # print "here in except"
                signal.alarm(0)
                break
            # print ret
            log += ret
        
        end = time.time()
        # --------- ----------- ----------- --------------- ------------ ----------- ---------- ---------

        # kill everyone
        kill(h1)
        kill(h2)
        kill(h3)
        time.sleep(2)

        # check if the thing succeeded otherwise retry
        if dont_count == False: # it worked     
            toWrite = str(payload_size * 256)+ ' ' +str(end - start) + '\n'
            ofile.write(toWrite)
        else:
            print("failed try again")
            logfile.write(log)
            continue

        payload_size += 1
        logfile.write(log)

    ofile.close()
    net.stop()
    print("Performance test finished")

def run_all_tests_sequentially():

    for delay in DELAYS:
        for bw in BANDWIDTHS:
            for loss in LOSSES:
                
                performance_test('quic', delay=str(delay)+"ms", bw=bw, loss=loss)
            
                Cleanup.cleanup()

    for delay in DELAYS:
        for bw in BANDWIDTHS:
            for loss in LOSSES:
                
                performance_test('tcp', delay=str(delay)+"ms", bw=bw, loss=loss)
            
                Cleanup.cleanup()

    
                
def run_cli():
    net = SimpleTopology.create_net()
    net.start()
    CLI(net)
    net.stop()

#run_cli()
logfile = open('logfile', 'w')
run_all_tests_sequentially()
logfile.close()
