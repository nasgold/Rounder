import random
import time

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

def main():

	start_time = time.time()

	dataModel = [
	    [(0,0,0), (1,0,0,0,0,0,0,0)],
	    [(0,0,1), (0,1,0,0,0,0,0,0)],
	    [(0,1,0), (0,0,1,0,0,0,0,0)],
	    [(0,1,1), (0,0,0,1,0,0,0,0)],
	    [(1,0,0), (0,0,0,0,1,0,0,0)],
	    [(1,0,1), (0,0,0,0,0,1,0,0)],
	    [(1,1,0), (0,0,0,0,0,0,1,0)],
	    [(1,1,1), (0,0,0,0,0,0,0,1)],
	]

	ds = SupervisedDataSet(3, 8)
	 
	for input, target in dataModel:
	    ds.addSample(input, target)

	# create a large random data set
	random.seed()
	trainingSet = SupervisedDataSet(3, 8);
	for ri in range(0,1000):
	    input,target = dataModel[random.getrandbits(3)];
	    trainingSet.addSample(input, target)

	net = buildNetwork(3, 8, 8, bias=True)

	trainer = BackpropTrainer(net, ds, learningrate = 0.001)

	trainer.trainUntilConvergence(verbose=True,
	                              trainingData=trainingSet,
	                              validationData=ds,
	                              maxEpochs=15)

	"""
	print '0,0,0->', net.activate([0,0,0])
	print '0,0,1->', net.activate([0,0,1])
	print '0,1,0->', net.activate([0,1,0])
	print '0,1,1->', net.activate([0,1,1])
	print '1,0,0->', net.activate([1,0,0])
	print '1,0,1->', net.activate([1,0,1])
	print '1,1,0->', net.activate([1,1,0])
	print '1,1,1->', net.activate([1,1,1])

	print "-----------------------------------------------------"
	"""

	print 'Max position of 0,0,0->', getMaxPosition(net.activate([0,0,0])) + 1
	print 'Max position of 0,0,1->', getMaxPosition(net.activate([0,0,1])) + 1
	print 'Max position of 0,1,0->', getMaxPosition(net.activate([0,1,0])) + 1
	print 'Max position of 0,1,1->', getMaxPosition(net.activate([0,1,1])) + 1
	print 'Max position of 1,0,0->', getMaxPosition(net.activate([1,0,0])) + 1
	print 'Max position of 1,0,1->', getMaxPosition(net.activate([1,0,1])) + 1
	print 'Max position of 1,1,0->', getMaxPosition(net.activate([1,1,0])) + 1
	print 'Max position of 1,1,1->', getMaxPosition(net.activate([1,1,1])) + 1

	print("The Program took %s seconds to run" % (time.time() - start_time))


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