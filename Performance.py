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

DELAYS = (10,)
BANDWIDTHS = (50,75,100)
LOSSES = (0,1,2)
PAYLOADS = (50,256,1024,2048)

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

def performance_test(srv_cmd, clt_cmd, brok_cmd, run_index, repeat_times, payload, **opts):
    print("Starting performance test run %s with parameters %s and payload %d" % (run_index, opts,payload))
    net = SimpleTopology.create_net(**opts)
    net.start()
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h3.sendCmd(brok_cmd)
    time.sleep(1)
    ofile = open('meas/server_run_%s_%s' % ('_'.join("%s" % val for (key,val) in opts.iteritems()),payload), 'w')
    print("Running server:\n%s" % srv_cmd)
    h1.sendCmd(srv_cmd)
    payload = "A"*payload
    time.sleep(1)
    log = ""
    avg = 0.0
    for i in range(repeat_times):
        start = time.time()
        h2.sendCmd(clt_cmd+payload)
        print("###"+str(i)+"###:\n")
        while(h1.waiting):
            ret = h1.monitor()
            det = time.time()-start
            det *= 1000
            print(ret)
            print(str(det)+"\n")
            if(ret=='\r\n'):
                log = log + "#{0}:{1}\n".format(i,det)
                avg += det
                break 
            elif det > (RUN_TIME * 2 * 1000):
                print("Started at %s and it's now %s, that's %s ms later" % (start, time.time(), det))
                break
        while(h2.waiting):
            _ = h2.monitor(timeoutms=RUN_TIME * 2 * 1000)
    for host in [h1,h2,h3]:
        host.sendInt()
        while(host.waiting):
            host.monitor()
    ofile.write(log)
    ofile.write("#AVG:"+str(avg/repeat_times)+"ms\n")
    ofile.close()
    net.stop()
    print("Performance test finished")

# def run_all_tests_parallel(run_index):
#     pool = Pool(POOL_SIZE)
#     for delay in DELAYS:
#         for bw in BANDWIDTHS:
#             for loss in LOSSES:
#                 r = pool.apply_async(performance_test,
#                                      ['./mosquitto-1.4.14/client/serv',
#                                       "./quic_perf_client -d=%s 192.168.0.1" % RUN_TIME,
#                                       run_index ],
#                                       dict(delay=delay, bw=bw, loss=loss)
#                                      )
#                 r = pool.apply_async(performance_test,
#                                      ['./tcp_perf_server',
#                                       "./tcp_perf_client -d=%s 192.168.0.1" % RUN_TIME,
#                                       run_index ],
#                                       dict(delay=delay, bw=bw, loss=loss)
#                                      )
#     pool.close()
#     pool.join()

def run_all_tests_sequentially():
    run_index = 0
    for delay in DELAYS:
        for bw in BANDWIDTHS:
            for loss in LOSSES:
                for pl in PAYLOADS:
                    performance_test('./mosquitto-1.4.14/client/mosquitto_sub -h 192.168.0.3 -q 1 -t test -C 30', "./mosquitto-1.4.14/client/mosquitto_pub -h 192.168.0.3 -q 1 -t test -m ","mosquitto", run_index, 30, pl, delay=str(delay)+"ms", bw=bw, loss=loss)
                    run_index+=1
                    Cleanup.cleanup()
                
def run_cli():
    net = SimpleTopology.create_net()
    net.start()
    CLI(net)
    net.stop()

#run_cli()
run_all_tests_sequentially()
