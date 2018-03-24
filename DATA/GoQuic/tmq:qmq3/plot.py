import matplotlib.pyplot as plt
import numpy as np
import math
def readData(folder):
	lat = []
	for loss in [0]:
		for t in [5]:
			for bw in [10]:
				for payload in [50,100,200]:
					try:
						filename = folder+'/'+"server_run_{0}ms_{1}_{2}_{3}".format(t,loss,bw,payload)
						avg = []
						with open(filename) as handle:
							lines = handle.readlines()
							lines = lines[0:-1]
							for l in lines:
								f = float(l)
								avg.append(f)
						avg.sort()
						avg = avg[1:-1]
						avg = sum(avg)/len(avg)
						lat.append((t,loss,bw,payload,avg))
					except Exception as e:
						print(e)
						continue
	return lat
lat = readData("tms")
x = [tp[3] for tp in lat]
y = [tp[4] for tp in lat]
plt.plot(x,y,label="TCP")
lat = readData("qms")
x = [tp[3] for tp in lat]
y = [tp[4] for tp in lat]
plt.plot(x,y,label="QUIC")
plt.xlabel("Payload(byte)")
plt.ylabel("Total transmission time/(ms)")
plt.title("RTT 30ms,Bandwidth=10Mbps,loss=0%")
leg = plt.legend(loc='best', ncol=1, shadow=True, fancybox=True)
plt.axis([0,220,150,500])
plt.show()
