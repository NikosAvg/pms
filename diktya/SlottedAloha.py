import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams['figure.dpi'] = 150

class Node:
	poissonL = 0.35 #poisson rate for the system
	n = 100 #number of nodes
	qa = float(poissonL)/n # prob to become active and send (poisson l / number of nodes)
	qr = 0.06 #prob to send if backlogged 
	activeset = [] #nodes that will try to send backlogged and unbacklogged
	inactiveset = [] #nodes with no message
	succsent = 0 #number of messages send

#Initialize each node
	def __init__(self,b):
		if b == True:
			Node.activeset.append(self)
		else:
			Node.inactiveset.append(self)
		self.backlogged = b

#Return the number of backlogged nodes
	def backlogged():
		bg = 0
		for n in Node.activeset:
			if n.backlogged == True:
				bg += 1
		return bg

#Check if a new msg arrived
	def msgArrived():
		for n in Node.inactiveset:
			if np.random.poisson(Node.qa) >= 1:
				Node.inactiveset.remove(n)
				Node.activeset.append(n)
#Try To Transmit
	def tryTransmit():
		nodestried = []
		for n in Node.activeset:
			if n.backlogged == True:
				if np.random.uniform(0,1) < Node.qr:
					nodestried.append(n)
			else:
				nodestried.append(n)
		if len(nodestried) == 1:
			Node.succsent += 1
			Node.activeset.remove(nodestried[0])
			Node.inactiveset.append(nodestried[0])
		elif len(nodestried) > 1:
			for n in nodestried:
				if n.backlogged == False:
					n.backlogged = True
#Calculate throughput per slot
	def throughput(slot):
		return float(Node.succsent)/slot
#calculate G
	def G():
		active = len(Node.inactiveset)
		backlogged = Node.backlogged()
		return (active - backlogged)*Node.qa + backlogged*Node.qr
#Dynamic qr / G around 1
	def AdjustQr():
		active = len(Node.inactiveset)
		backlogged = Node.backlogged()
		Node.qr = (1.0 - (active - backlogged)*Node.qa)/float(backlogged)

#Initiale the network with a given number of backlogged nodes
def initNodes(numberOfBacklogged):
	for n in range(Node.n - numberOfBacklogged):
		Node(False)
	for n in range(numberOfBacklogged):
		Node(True)


def main():
	simTime = 10000
	backlogged_each_slot = []
	G_each_slot = []
	throughput = []

	initNodes(0)
	
	for slot in range(1,simTime+1):
#Dynamic qr try to keep G=1
		#if Node.backlogged() != 0:
		#	Node.AdjustQr()

		Node.msgArrived()
		Node.tryTransmit()
		backlogged_each_slot.append(Node.backlogged())
#Calculate every 10 slots the throughput
		if slot%10 == 0:
			throughput.append(Node.throughput(slot))
		G_each_slot.append(Node.G())
#Plot G per Slot

	#plt.plot(G_each_slot)
	#plt.ylabel('Attempted Transmission Rate G')
	#plt.xlabel('Slot')

#Plot throuput

	plt.plot(throughput)
	plt.ylabel('Throughput')
	plt.xlabel('Per 10 slots')

#Plot backlogged per slot
	#plt.plot(backlogged_each_slot)
	#plt.ylabel('Backlogged Nodes')
	#plt.xlabel('Slots')
	plt.show()
	


if __name__ == '__main__': main()
