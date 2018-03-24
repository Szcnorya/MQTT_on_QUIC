import matplotlib.pyplot as plt
def readData(folder):
	lat = []
	for loss in [0,1,2]:
		for t in [5]:
			for bw in [50,75,100]:
				for payload in [25,50,100,200]:
					try:
						filename = folder+'/'+"server_run_{0}ms_{1}_{2}_{3}".format(t,loss,bw,payload)
						avg = 0.0
						cnt = 0.0
						with open(filename) as handle:
							lines = handle.readlines()
							lines = lines[0:-1]
							for l in lines:
								f = float(l)
								if(f>5000):
									continue
								avg+=f
								cnt+=1
						lat.append((t,loss,bw,payload,avg/cnt))
					except Exception as e:
						print(e)
						continue
	return lat
lat = readData("tms")
x = [tp[3] for tp in lat if tp[1]==0 and tp[2]==100]
y = [tp[4] for tp in lat if tp[1]==0 and tp[2]==100]
plt.plot(x,y,label="TCP")
lat = readData("qms")
x = [tp[3] for tp in lat if tp[1]==0 and tp[2]==100]
y = [tp[4] for tp in lat if tp[1]==0 and tp[2]==100]
plt.plot(x,y,label="QUIC")
plt.xlabel("Payload(KB)")
plt.ylabel("Total transmission time/(ms)")
plt.title("RTT 20ms,Bandwidth=100Mbps,Loss=0%")
leg = plt.legend(loc='best', ncol=1, shadow=True, fancybox=True)
plt.axis([0,200,50,500])
plt.show()
