import random
import time

from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader


from getInputsForNeuralNetworks import *

def main():

	net =  NetworkReader.readFrom('savedNeuralNets/trainedNet.xml')
	dataModel = createTheDataModel([3,9,18])

	totalGamesPredicted = 0
	totalGames = 0
	incorrect = 0
	correct = 0
	for input, target in dataModel:

	    i = list(input)
	    if len(i) != 172:
	    	continue

	    totalGames += 1

	    result = net.activate(i)[0]
	    #print result, target[0]
	    #print result
	    if result > 2.1:
	    	result = 1
	    elif result < -3.2:
	    	result = 0
	    else:
	    	continue

	    totalGamesPredicted += 1


	    if result == target[0]:
	    	correct += 1
	    else:
	    	incorrect += 1


	print 'correct: ' + str(correct) + " (" + str(100.0 * correct/totalGamesPredicted)[0:6] + "%)"
	print 'incorrect: ' + str(incorrect) + " (" + str(100.0 * incorrect/totalGamesPredicted)[0:6] + "%)"
	print 'totalGames: ', totalGames
	print 'totalGamesPredicted: ', totalGamesPredicted



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