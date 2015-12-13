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

	dataModel = createTheDataModel([2,5,9,15])

	trainingSet = SupervisedDataSet(228, 1)
	for input, target in dataModel:
	    trainingSet.addSample(input, target)


	net = buildNetwork(228, 220, 1, bias=True)

	numberOfEpochsToTrainFor = 2
	for epochNumber in range(1, 3):
		trainer = BackpropTrainer(net, trainingSet)
		trainer.trainEpochs(2)

		NetworkWriter.writeToFile(net, 'savedNeuralNets/trainedNet1-epoch' + str(epochNumber * numberOfEpochsToTrainFor) + '.xml')


	seconds = str(int(time.time() - start_time))
	print("The Program took %s seconds to run" % (seconds))


main()