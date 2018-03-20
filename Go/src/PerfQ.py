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

RUN_TIME = 20

DELAYS = (10,)
BANDWIDTHS = (25,)
LOSSES = (0,)

class SimpleTopology(Topo):

    def build(self, size, **opts):
        s1 = self.addSwitch('s1')
        host = []
        for i in range(1,size+1):
            host.append(self.addHost('h'+str(i),ip="192.168.0.%d/24" % (i,)))
        for h in host:
            self.addLink(h, s1,**opts)

    @staticmethod
    def create_net(**opts):
        return Mininet(topo=SimpleTopology(**opts), link=TCLink)

def performance_test(srv_cmd, clt_cmd, run_index, repeat_times, size, **opts):
    print("Starting performance test run %s with parameters %s" % (run_index, opts))
    net = SimpleTopology.create_net(size,**opts)
    net.start()
    host = [net.get("h"+str(i)) for i in range(1,size+1)]
    print("Running server:\n%s" % srv_cmd)
    ofile = open('meas/server_run_%s_%s' % ('_'.join("%s" % val for (key,val) in opts.iteritems()),size), 'w')
    log = ""
    avg = 0.0
    for i in range(repeat_times):
        host[0].sendCmd(srv_cmd)
        time.sleep(1)
        start = time.time()
        for j in range(1,size):
            host[j].sendCmd(clt_cmd + " -h=192.168.0.1")
        cnt = 0
        while(cnt<size-1):
            for j in range(1,size):
                ret = host[j].monitor()
                if not host[j].waiting:
                    cnt += 1
        det = time.time()-start
        det *= 1000
        host[0].sendInt()
        while(host[0].waiting):
            host[0].monitor()
        log = log + "#{0}:{1}\n".format(i,det)
    ofile.write(log)
    ofile.write("#AVG:"+str(avg/repeat_times)+"ms\n")
    ofile.close()
    net.stop()
    print("Performance test finished")

def run_all_tests_sequentially():
    run_index = 0
    for delay in DELAYS:
        for bw in BANDWIDTHS:
            for loss in LOSSES:
                for sz in SIZES:
                    performance_test("./SevEcho","./CliEcho -sz=10 -cnt=10",run_index, RUN_TIME,size, delay=str(delay)+"ms", bw=bw, loss=loss)
                    run_index+=1
                    Cleanup.cleanup()
                
def run_cli():
    net = SimpleTopology.create_net()
    net.start()
    CLI(net)
    net.stop()

#run_cli()
run_all_tests_sequentially()
