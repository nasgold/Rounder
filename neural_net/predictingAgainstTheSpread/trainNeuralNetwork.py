import sys
sys.path.append("..") # Adds higher directory to python modules path.
sys.path.append("../..") # Adds higher directory to python modules path.


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

	ds = SupervisedDataSet(228, 1)

	dataModel = createTheDataModel([2,5,9,15])

	for input, target in dataModel:
	    ds.addSample(input, target)

	# create the data set
	trainingSet = SupervisedDataSet(228, 1);
	for row in dataModel:
		inputs = row[0]
		target = row[1]
		trainingSet.addSample(input, target)

	net = buildNetwork(228, 220, 1, bias=True)

	trainer = BackpropTrainer(net, ds, learningrate = 0.001)

	numberOfEpochsToTrainFor = 200
	for epochNumber in range(1, 11):

		trainer.trainUntilConvergence(verbose=True,
		                              trainingData=trainingSet,
		                              validationData=ds,
		                              maxEpochs=numberOfEpochsToTrainFor)

		NetworkWriter.writeToFile(net, 'savedNeuralNets/trainedNet1-epoch' + str(epochNumber * numberOfEpochsToTrainFor) + '.xml')


	seconds = str(int(time.time() - start_time))
	print("The Program took %s seconds to run" % (seconds))


main()