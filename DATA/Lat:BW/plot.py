import matplotlib.pyplot as plt
lat = []
def readData():
	for t in [20]:
		for bw in [5,10,25,50,100]:
			try:
				filename = "server_run_{0}ms_0_{1}".format(t,bw)
				avg = 0.0
				with open(filename) as handle:
					lines = handle.readlines()
					lines = lines[1:-1]
					for l in lines:
						f = float(l[3:])
						avg+=f
					lat.append((t,bw,avg/9.0))
			except FileNotFoundError:
				continue
readData()
print(lat)
x = [tp[1] for tp in lat]
y = [tp[2] for tp in lat]
plt.plot(x,y)
plt.xlabel("Bandwidth/(Mbps)")
plt.ylabel("Latency/(ms)")
plt.title("RTT 40ms")
plt.axis([0,100,165,175])
plt.show()