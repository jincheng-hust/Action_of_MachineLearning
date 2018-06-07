from numpy import *
import operator

def creatDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    repeatMat = tile(inX, (dataSetSize, 1)) 
    #tile(A, B): repeat A, B times
    diffMat = repeatMat - dataSet
    sqDiffMat = diffMat**2
    sqDistences = sqDiffMat.sum(axis=1)
    distences = sqDistences**0.5
    sortedDistIndicies = distences.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1  
        # D.get(key[, default=None]): 
        #   return the value of key, 
        #   If the key is not in the dictionary, returns a specified value
    sortedClassCount = sorted(classCount.iteritems(),
                            key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        if listFromLine[-1] == 'didntLike':
			classLabelVector.append(1)
        elif listFromLine[-1] == 'smallDoses':
			classLabelVector.append(2)
        elif listFromLine[-1] == 'largeDoses':
			classLabelVector.append(3)
        index += 1
    return returnMat, classLabelVector

def visOfData(datingDataMat, datingLabels):
    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 1], datingDataMat[:, 0],
                15.0*array(datingLabels), 15.0*array(datingLabels))
                # x aixs, y aixs,
                # size of plot, color of plot
    plt.show()

def autoNorm(dataSet):
    minVals = dataSet.min(0) # 0: min of colums
    maxVals = dataSet.max(0) # 0: max of colums
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    # build a new array
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet / tile(ranges, (m,1))
    # Note: the use of 'tile'
    return normDataSet, ranges, minVals

def datingClassTest():
    testRatio = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * testRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:],
                                    datingLabels[numTestVecs:m], 4)
        print "The classifier came back with: %d, the real answer is: %d"\
                % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
    print "The total error rate is: %f" % (errorCount/float(numTestVecs))

def classifyPerson():
    resultLists = ['didntLike', 'smallDoses', 'largeDoses']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals)/ranges, normMat, datingLabels, 3)
    print "You will probably like this person: ", resultLists[classifierResult - 1]

if __name__ == "__main__":
    # group, labels = creatDataSet()
    # print classify0([0,0], group, labels, 3) 
    
    # datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    # visOfData(datingDataMat, datingLabels)
    
    #datingClassTest()
    
    classifyPerson()
