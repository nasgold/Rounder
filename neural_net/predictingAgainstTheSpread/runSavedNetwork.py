import sys
sys.path.append("..") # Adds higher directory to python modules path.
sys.path.append("../..") # Adds higher directory to python modules path.

import random
import time

from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader


from getInputsForNeuralNetworks import *

def main():

	for i in range(1,3):
		epochs = i *2
		print epochs

		savedNet = './savedNeuralNets/trainedNet1-epoch' + str(epochs) + '.xml'
		runNeuralNets(savedNet)

def runNeuralNets(savedNet):

	net =  NetworkReader.readFrom(savedNet)
	dataModel = createTheDataModel([2,5,9,15])

	totalGamesPredicted = 0
	totalGames = 0
	incorrect = 0
	correct = 0
	for input, target in dataModel:

	    i = list(input)
	    if len(i) != 228:
	    	continue


	    totalGames += 1
	    result = net.activate(i)[0]

	    if result > 0:
	    	result = 1
	    else:
	    	result = 0

	    # elif result < -3.2:
	    # 	result = 0
	    # else:
	    # 	continue

	    totalGamesPredicted += 1

	    if result == target[0]:
	    	correct += 1
	    else:
	    	incorrect += 1

	
	print 'correct: ' + str(correct) + " (" + str(100.0 * correct/totalGamesPredicted)[0:6] + "%)"
	print 'incorrect: ' + str(incorrect) + " (" + str(100.0 * incorrect/totalGamesPredicted)[0:6] + "%)"
	print 'totalGames: ', totalGames
	print 'totalGamesPredicted: ', totalGamesPredicted

	print

	return 


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