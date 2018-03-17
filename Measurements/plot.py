from matplotlib import pyplot as plt
data_tcp = {}
data_quic = {}

def readData(option):
	for delay in [50,100]:
		for loss in [2,5]:
			for bw in [2,5,10]:
				listOfPoints = []
				try:
					filename = "server_run_{0}ms_{1}_{2}".format(delay,loss,bw)
					if option == 'tcp':
						folder = 'tcp2/'
					else:
						folder = 'quic2/'
					
					with open(folder + filename) as handle:
						lines = handle.readlines()
						
						for l in lines:
							# f = float(l[3:])
							# avg+=f
							l = l.split(" ")
							size = int(l[0])
							time = float(l[1])
							listOfPoints.append((size, time))
						
					key = (delay, loss, bw)
					if option == 'tcp':
						data_tcp[key] = listOfPoints
					else:
						data_quic[key] = listOfPoints

				except IOError as e:
					continue

readData('tcp')
readData('quic')


key = (50,2,10)
	
x_tcp = [tp[0] for tp in data_tcp[key]]
y_tcp = [tp[1] for tp in data_tcp[key]]

x_quic = [tp[0] for tp in data_quic[key]]
y_quic = [tp[1] for tp in data_quic[key]]

plt.plot(x_tcp, y_tcp, label='tcp')
plt.plot(x_quic, y_quic, label='quic')
plt.legend()
# plt.xlabel("Bandwidth/(Mbps)")
# plt.ylabel("Latency/(ms)")
# plt.title("RTT 40ms")
# plt.axis([0,100,165,175])
plt.show()