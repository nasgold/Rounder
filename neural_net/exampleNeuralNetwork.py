import random
import time

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader


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
	for ri in range(0,2000):
	    input,target = dataModel[random.getrandbits(3)];
	    trainingSet.addSample(input, target)

	net = buildNetwork(3, 8, 8, bias=True)

	trainer = BackpropTrainer(net, ds, learningrate = 0.001)

	trainer.trainUntilConvergence(verbose=True,
	                              trainingData=trainingSet,
	                              validationData=ds,
	                              maxEpochs=20)

	NetworkWriter.writeToFile(net, 'savedNeuralNets/trainedNet.xml')

	print("The Program took %s seconds to run" % (time.time() - start_time))

main()
