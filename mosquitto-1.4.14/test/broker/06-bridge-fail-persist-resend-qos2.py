#!/usr/bin/env python

# Test whether a bridge can cope with an unknown PUBACK

import socket
import subprocess
import time

import inspect, os, sys
# From http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import mosq_test

rc = 1
keepalive = 60
connect_packet = mosq_test.gen_connect("bridge-u-test", keepalive=keepalive)
connack_packet = mosq_test.gen_connack(rc=0)

mid = 180
mid_unknown = 2000

publish_packet = mosq_test.gen_publish("bridge/unknown/qos2", qos=1, payload="bridge-message", mid=mid)
puback_packet = mosq_test.gen_puback(mid)

pubrec_packet_unknown1 = mosq_test.gen_pubrec(mid_unknown+1)
pubrel_packet_unknown1 = mosq_test.gen_pubrel(mid_unknown+1)

pubrel_packet_unknown2 = mosq_test.gen_pubrel(mid_unknown+2)
pubcomp_packet_unknown2 = mosq_test.gen_pubcomp(mid_unknown+2)

pubcomp_packet_unknown3 = mosq_test.gen_pubcomp(mid_unknown+3)


unsubscribe_packet = mosq_test.gen_unsubscribe(1, "bridge/#")
unsuback_packet = mosq_test.gen_unsuback(1)


if os.environ.get('MOSQ_USE_VALGRIND') is not None:
    sleep_time = 5
else:
    sleep_time = 0.5


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(10)
sock.bind(('', 1888))
sock.listen(5)

broker = mosq_test.start_broker(filename=os.path.basename(__file__), port=1889)
time.sleep(sleep_time)

try:
    (conn, address) = sock.accept()
    conn.settimeout(20)

    if mosq_test.expect_packet(conn, "connect", connect_packet):
        conn.send(connack_packet)

        if mosq_test.expect_packet(conn, "unsubscribe", unsubscribe_packet):
            conn.send(unsuback_packet)

            # Send the unexpected pubrec packet
            conn.send(pubrec_packet_unknown1)
            if mosq_test.expect_packet(conn, "pubrel", pubrel_packet_unknown1):

                conn.send(pubrel_packet_unknown2)
                if mosq_test.expect_packet(conn, "pubcomp", pubcomp_packet_unknown2):

                    conn.send(pubcomp_packet_unknown3)

                    # Send a legitimate publish packet to verify everything is still ok
                    conn.send(publish_packet)
        
                    if mosq_test.expect_packet(conn, "puback", puback_packet):
                        rc = 0

finally:
    broker.terminate()
    broker.wait()
    if rc:
        (stdo, stde) = broker.communicate()
        print(stde)
    sock.close()

exit(rc)

