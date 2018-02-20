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
RUN_TIME = 15
NUM_RUNS = 1

DELAYS = (15)
BANDWIDTHS = (5, 10)
LOSSES = (0)

class SimpleTopology(Topo):

    def build(self, **opts):
        h1 = self.addHost('h1', ip="192.168.0.1/24", mac="cc:cc:cc:cc:cc:01")
        h2 = self.addHost('h2', ip="192.168.0.2/24", mac="cc:cc:cc:cc:cc:02")
        h3 = self.addHost('h2', ip="192.168.0.3/24", mac="cc:cc:cc:cc:cc:03")
        self.addLink(h1, h2, **opts)
        self.addLink(h1, h3, **opts)
        self.addLink(h2, h3, **opts)

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
    ofile = open('server_run_%s_%s_%s' % (run_index, re.sub('[ /]', '_', srv_cmd), '_'.join("%s=%r" % (key,val) for (key,val) in opts.iteritems())), 'w')
    print("Running server:\n%s" % srv_cmd)
    h1.sendCmd(srv_cmd + " 2>>error_log")
    time.sleep(1)
    h2.sendCmd(clt_cmd)
    result = ''
    start = time.time()
    while h1.waiting:
        data = h1.monitor(timeoutms=RUN_TIME * 2 * 1000)
        if time.time() - start > (RUN_TIME * 2):
            print("Started at %s and it's now %s, that's %s seconds later" % (start, time.time(), time.time() - start))
            errfile = open('error_log', 'a')
            errfile.write("In run %s test with parameters %s did timeout\n" % (run_index, opts))
            errfile.close()
            break
        result += data
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
                performance_test('./mosquitto-1.4.14/client/mosquitto_sub -h h3 -t test -C 1', "./mosquitto-1.4.14/client/mosquitto_pub -h h3 -t test -m Aloha~","mosquitto", run_index, delay=delay, bw=bw, loss=loss)

def run_cli():
    net = SimpleTopology.create_net()
    net.start()
    CLI(net)
    net.stop()

for run_index in range(0,NUM_RUNS):
    run_all_tests_sequentially(run_index)