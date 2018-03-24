import matplotlib.pyplot as plt
def readData(folder):
	for t in [5]:
		for bw in [10]:
			for sz in [i for i in range(2,50,3)]:
				try:
					filename = folder+'/'+"server_run_{0}ms_0_{1}_{2}".format(t,bw,sz)
					avg = 0.0
					with open(filename) as handle:
						lines = handle.readlines()
						lines = lines[0:-1]
						for l in lines:
							f = float(l[3:])
							avg+=f
						lat.append((t,bw,sz,avg/5.0))
				except FileNotFoundError:
					continue
lat = []
readData("tms")
x = [tp[2] for tp in lat]
y = [tp[3] for tp in lat]
plt.plot(x,y,label="TCP")
lat = []
readData("qms")
x = [tp[2] for tp in lat]
y = [tp[3] for tp in lat]
plt.plot(x,y,label="QUIC")
plt.xlabel("Sender number")
plt.ylabel("Total transmission time/(ms)")
plt.title("RTT 5ms,Bandwidth=10Mbps")
leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
plt.axis([0,50,200,1000])
plt.show()