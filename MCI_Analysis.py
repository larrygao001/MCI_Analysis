'''
Created on Feb 3, 2017

@author: langg
'''
import numpy as np
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot
import pylab

xAxis = []
accelerationX = []
accelerationY = []
accelerationZ= []
magnitude = []
rawActivities = []
time = []
FileName = raw_input("Please enter the file name:\n")
gravity = raw_input("Do you want to include gravity in the acceleration? (yes or no)\n")

def processData():
    global xAxis, accelerationX, accelerationY, accelerationZ, magnitude, rawActivities, time
    countLine = 0
    start = 0
    end = 0
    for line in open(FileName,"r"):
        line = line.split(",")

        accelerationX.append(float(line[5]))
        accelerationY.append(float(line[6]))
        accelerationZ.append(float(line[7]))
        time.append(line[0])
        rawActivities.append((line[9]))
        
        if (line[8] == "start task"):
            start = countLine
        if (line[8] =="quit"):
            end = countLine
        countLine += 1
    if gravity == "yes":
        accelerationZ = [(accelerationZ[i]-9.807) for i in range(len(accelerationZ))]
    #Trim the data based on the marker for start task and quit   
    accelerationX = [accelerationX[i] for i in range(start,end+1)]    
    accelerationY = [accelerationY[i] for i in range(start,end+1)] 
    accelerationZ = [accelerationZ[i] for i in range(start,end+1)]
    
    xAxis = [i for i in range(start, end+1)] 
    time = [time[i] for i in range(start,end+1)] 
    rawActivities = [rawActivities[i] for i in range(start,end+1)]        

    for i in range(len(time)):
        tempX = np.power(accelerationX[i],2)
        tempY = np.power(accelerationY[i],2)
        tempZ = np.power(accelerationZ[i],2)
        magnitude.append(np.sqrt((tempX + tempY + tempZ)/3))

      
#find all the activities, including each one's starting and ending time
def findActivities(): 
    activities = []
    count = 0
    rawActivities.append("")
    for i in range(len(rawActivities)-1):       
        j = i+1
        if rawActivities[j] == rawActivities[i]:
            j+=1
            count+=1
        else:        
            startIndex = j - count
            endIndex = j - 1
            startTime = time[startIndex]
            endTime = time[endIndex]
            
            if startTime!=endTime:
                activities.append([rawActivities[j-1],startIndex, endIndex, startTime, endTime])
            count = 0        
    return activities

#This function take the time strings as input and calculate the time duration in seconds
def calTime(time1, time2):    
    #Calculate minutes difference
    minutes = int(time2.split(":")[1]) - int(time1.split(":")[1])        
    #Calculate seconds
    seconds = minutes*60 + int(time2.split(":")[2]) - int(time1.split(":")[2])
    return seconds


#find peak positions for the acceleration in the x, y, and z direction
#thres (float between 0-1): Normalized threshold.  suggested: around 0.5
#min_dist (int): Minimum distance between each detected peak. suggested: around 10
def peakPosition(thres, min_dist):
    X = np.array(accelerationX)
    Y = np.array(accelerationY)
    Z = np.array(accelerationZ)
    Norm = np.array(magnitude)

    indexesX = peakutils.indexes(X, thres, min_dist)
    indexesX_negative = peakutils.indexes(-X,thres, min_dist)
    indexesX=np.unique(np.append(indexesX_negative, indexesX)) 
    
    indexesY = peakutils.indexes(Y, thres, min_dist) 
    indexesY_negative = peakutils.indexes(-Y,thres, min_dist)
    indexesY=np.unique(np.append(indexesY_negative, indexesY))     
    
    indexesZ = peakutils.indexes(Z, thres, min_dist) 
    indexesZ_negative = peakutils.indexes(-Z,thres, min_dist)
    indexesZ=np.unique(np.append(indexesZ_negative, indexesZ))     
     
    # Norm contains non-negative values no need to reverse
    indexesNorm = peakutils.indexes(Norm, thres, min_dist) 
     
    return indexesX, indexesY, indexesZ, indexesNorm

# mark the peak positions and plot the image
def showPeaks():
    indexesX = peakPosition(0.5, 10)[0]
    x = np.array(xAxis)
    y = np.array(accelerationX)
    pyplot.figure(figsize=(10,6))
    pplot(x, y, indexesX)
    pyplot.title('First estimate')
    pylab.show()


# compare peak value change/positive or negative
def changeDirection(thres, min_dist): 
    activities = findActivities()
    indicesX, indicesY, indicesZ, indicesNorm = peakPosition(thres, min_dist)    
    countX = 0
    countY = 0
    countZ = 0
    countSum = 0
    result = []
    #for each activity, find the number of direction changes
    for i in range(len(activities)): 
        k_x = 0
        k_y = 0
        k_z = 0       
        
        #Calculate direction changes in X direction
        while indicesX[k_x + 1] <= activities[i][1]:
            k_x += 1
        while indicesX[k_x + 1] > activities[i][1] and indicesX[k_x + 1] <= activities[i][2]:
            if accelerationX[indicesX[k_x]] * accelerationX[indicesX[k_x + 1]] < 0:
                countX += 1
            if k_x+ 1< len(indicesX) - 1:
                k_x += 1
            else:
                break
            
        #Calculate direction changes in Y direction         
        while indicesY[k_y + 1] <= activities[i][1]:
            k_y += 1
        while indicesY[k_y + 1] > activities[i][1] and indicesY[k_y + 1] <= activities[i][2]:
            if accelerationY[indicesY[k_y]] * accelerationY[indicesY[k_y + 1]] < 0:
                countY += 1
            if k_y+ 1< len(indicesY) - 1:
                k_y += 1  
            else:
                break               
          
        #Calculate direction changes in Z direction     
        while indicesZ[k_z + 1] <= activities[i][1]:
            k_z += 1
        while indicesZ[k_z + 1] > activities[i][1] and indicesZ[k_z + 1] <= activities[i][2]:
            if accelerationZ[indicesZ[k_z]] * accelerationZ[indicesZ[k_z + 1]] < 0:
                countZ += 1
            if k_z+ 1< len(indicesZ) - 1:
                k_z += 1                 
            else:
                break

        #The total number of direction changes in all three directions
        countSum = countX+countY+countZ
        
        #Calculate the average number of direction changes within time duration of a specific activity:
        duration = calTime(time[activities[i][1]], time[activities[i][2]])
        average = countSum/float(duration)
        
        result.append([activities[i][0], countX, countY, countZ, countSum, average, activities[i][3], activities[i][4]])
        
        countX = 0
        countY = 0
        countZ = 0
        countSum = 0
    
    return result    

#return an array with the number of pauses, and the total duration of all the pauses for each activity
def pause(mTreshold, tTreshold):
    pauses = []
    activities = findActivities()
    
    for i in range(len(activities)):
        duration = 0
        duration_average = 0
        pauseCount = 0
        j = activities[i][1]          
        while j < activities[i][2]:
            count = 0
            if magnitude[j] > mTreshold:
                j+=1
            t1 = time[j]
            while magnitude[j]< mTreshold and j < activities[i][2]:
                count+=1
                j+=1
            if count > tTreshold:
                t2 = time[j-1]
                duration += calTime(t1, t2)
                pauseCount+=1 
                duration_average = duration/float(pauseCount)  
        pauses.append([activities[i][0], pauseCount, duration, duration_average, activities[i][3], activities[i][4]])    
    return pauses

def main():
    processData()
    
    mTreshold = input("Enter a threshold for the pause magnitude(below which will be defined as in a pause phase):\n")
    tTreshold = input("Enter a threshold for the duration of a pause:(below which will not be counted as a pause):\n")
    
    thres = input ("Enter a magnitude threshold (between 0 and 1) for the direction changes:\n")
    min_dist = input("Enter a time threshold (suggested: around 10):\n")
    
    directionChanges = changeDirection(thres, min_dist)
    pauses = pause(mTreshold,tTreshold)
    
    print "\n","direction changes:\n"
    for i in directionChanges:
        print(i)
        
    print "\n","pauses:\n "
    for i in pauses:
        print(i)  
          
    showPeaks()
     
main()   

    
    
    
