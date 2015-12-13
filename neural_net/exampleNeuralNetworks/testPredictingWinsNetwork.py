import random
import time

from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader

def main():

	for i in range(10):
		netName = 'savedNeuralNets/trainedNet'+str(i)+'.xml'
		runSaveNet(netName)

def runSaveNet(netName):
	net =  NetworkReader.readFrom(netName)

	print '0,0,0->', net.activate([0,0,0])
	print '0,0,1->', net.activate([0,0,1])
	print '0,1,0->', net.activate([0,1,0])
	print '0,1,1->', net.activate([0,1,1])
	print '1,0,0->', net.activate([1,0,0])
	print '1,0,1->', net.activate([1,0,1])
	print '1,1,0->', net.activate([1,1,0])
	print '1,1,1->', net.activate([1,1,1])

	print "-----------------------------------------------------"

	print 'Max position of 0,0,0->', getMaxPosition(net.activate([0,0,0])) + 1
	print 'Max position of 0,0,1->', getMaxPosition(net.activate([0,0,1])) + 1
	print 'Max position of 0,1,0->', getMaxPosition(net.activate([0,1,0])) + 1
	print 'Max position of 0,1,1->', getMaxPosition(net.activate([0,1,1])) + 1
	print 'Max position of 1,0,0->', getMaxPosition(net.activate([1,0,0])) + 1
	print 'Max position of 1,0,1->', getMaxPosition(net.activate([1,0,1])) + 1
	print 'Max position of 1,1,0->', getMaxPosition(net.activate([1,1,0])) + 1
	print 'Max position of 1,1,1->', getMaxPosition(net.activate([1,1,1])) + 1

	print 
	print


def getMaxPosition(output):

	theMax = -1000000
	counter = 0
	for i in output:
		if i > theMax:
			position = counter
			theMax = i
		counter += 1

	return position

main()