import matplotlib.pyplot as plt
def readData(loss,bw):
	lat = []
	for t in [10]:
		for payload in [50,256,1024,2048]:
			try:
				filename = "server_run_{0}ms_{1}_{2}_{3}".format(t,loss,bw,payload)
				avg = 0.0
				with open(filename) as handle:
					lines = handle.readlines()
					lines = lines[1:-1]
					for l in lines:
						l = l.split(":")
						f = float(l[1])
						avg+=f
					lat.append((payload,avg/len(lines)))
			except FileNotFoundError:
				continue
	return lat
def ploting(lat,lbl,sym):
	x = [tp[0] for tp in lat]
	y = [tp[1] for tp in lat]
	plt.plot(x,y,sym,label = lbl)
for loss in [0,1,2]:
    for bw in [100]:
        ploting(readData(loss,bw),("Loss={0}%,bw={1}".format(loss,bw)),'o-')
plt.xlabel("Payload/(byte)")
plt.ylabel("Latency/(ms)")
plt.title("RTT 20ms")
leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
plt.axis([0,2048,100,500])
plt.show()
