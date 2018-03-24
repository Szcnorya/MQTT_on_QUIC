import matplotlib.pyplot as plt
def readData(folder):
	lat = []
	for loss in [1,2]:
		for t in [5]:
			for bw in [10]:
				for sz in [i for i in range(2,50,3)]:
					try:
						filename = folder+'/'+"server_run_{0}ms_{1}_{2}_{3}".format(t,loss,bw,sz)
						avg = 0.0
						cnt = 0.0
						with open(filename) as handle:
							lines = handle.readlines()
							lines = lines[0:-1]
							for l in lines:
								f = float(l.split(':')[1])
								if(f>5000):
									continue
								avg+=f
								cnt+=1
						lat.append((t,loss,bw,sz,avg/cnt))
					except Exception as e:
						continue
	return lat
lat = readData("tms")
x = [tp[3] for tp in lat if tp[1]==2]
y = [tp[4] for tp in lat if tp[1]==2]
plt.plot(x,y,label="TCP")
lat = readData("qms")
x = [tp[3] for tp in lat if tp[1]==2]
y = [tp[4] for tp in lat if tp[1]==2]
plt.plot(x,y,label="QUIC")
plt.xlabel("Sender number")
plt.ylabel("Total transmission time/(ms)")
plt.title("RTT 20ms,Bandwidth=10Mbps,Loss=2%")
leg = plt.legend(loc='best', ncol=1, shadow=True, fancybox=True)
plt.axis([0,50,200,3000])
plt.show()