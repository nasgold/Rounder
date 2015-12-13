import random
import time

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader

from getInputsForNeuralNetworks import *


def main():

	start_time = time.time()

	ds = SupervisedDataSet(172, 1)

	dataModel = createTheDataModel([3,9,18]) 
	for input, target in dataModel:
	    ds.addSample(input, target)

	# create the data set
	trainingSet = SupervisedDataSet(172, 1);
	for row in dataModel:
		inputs = row[0]
		target = row[1]
		trainingSet.addSample(input, target)

	net = buildNetwork(172, 150, 1, bias=True)

	trainer = BackpropTrainer(net, ds, learningrate = 0.001)

	trainer.trainUntilConvergence(verbose=True,
	                              trainingData=trainingSet,
	                              validationData=ds,
	                              maxEpochs=1)

	NetworkWriter.writeToFile(net, 'savedNeuralNets/trainedNet7.xml')

	seconds = str(int(time.time() - start_time))
	print("The Program took %s seconds to run" % (seconds))


main()