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

#setLogLevel("info")

POOL_SIZE = 8
RUN_TIME = 10
NUM_RUNS = 1

DELAYS = (50,)
BANDWIDTHS = (100,)
LOSSES = (0,)

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

def performance_test(srv_cmd, clt_cmd, brok_cmd, run_index, **opts):
    print("Starting performance test run %s with parameters %s" % (run_index, opts))
    net = SimpleTopology.create_net(**opts)
    net.start()
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h3.sendCmd(brok_cmd)
    time.sleep(1)
    ofile = open('server_run_%s_%s' % (run_index,  '_'.join("%s" % val for (key,val) in opts.iteritems())), 'w')
    print("Running server:\n%s" % srv_cmd)
    h1.sendCmd(srv_cmd + " 2>error_log")
    time.sleep(1)
    result = ''
    for i in range(20):
        start = time.time()
        h2.sendCmd(clt_cmd)
        data = h1.monitor(timeoutms=RUN_TIME * 2 * 1000)
        _ = h2.monitor()
        result += str(time.time()-start)+"\n"
	if time.time() - start > (RUN_TIME * 2):
            print("Started at %s and it's now %s, that's %s seconds later" % (start, time.time(), time.time() - start))
            errfile = open('error_log', 'a')
            errfile.write("In run %s test with parameters %s did timeout\n" % (run_index, opts))
            errfile.close()
            break
    h1.terminate()
    h2.terminate()
    h3.terminate()
    ofile.write(result)
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

def run_all_tests_sequentially(run_index):
    for delay in DELAYS:
        for bw in BANDWIDTHS:
            for loss in LOSSES:
                performance_test('./mosquitto-1.4.14/client/mosquitto_sub -h 192.168.0.3 -t test -C 20', "./mosquitto-1.4.14/client/mosquitto_pub -h 192.168.0.3 -t test -m Aloha","mosquitto &", run_index, delay=str(delay)+"ms", bw=bw, loss=loss)

def run_cli():
    net = SimpleTopology.create_net()
    net.start()
    CLI(net)
    net.stop()
#run_cli()
for run_index in range(0,NUM_RUNS):
    run_all_tests_sequentially(run_index)
