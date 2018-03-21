import matplotlib.pyplot as plt
lat = []
def readData():
	for t in [5]:
		for bw in [10]:
			for sz in [i for i in range(2,12)]:
				try:
					filename = "server_run_{0}ms_0_{1}_{2}".format(t,bw,sz)
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
readData()
print(lat)
x = [tp[2] for tp in lat]
y = [tp[3] for tp in lat]
plt.plot(x,y)
plt.xlabel("Network size")
plt.ylabel("Total transmission time/(ms)")
plt.title("RTT 5ms")
plt.axis([0,12,300,400])
plt.show()