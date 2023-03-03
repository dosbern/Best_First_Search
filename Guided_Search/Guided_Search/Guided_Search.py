from queue import PriorityQueue
import math

#class template
class city:
    def __init__(self, xCord, yCord):
        self.xCord = xCord
        self.yCord = yCord
        self.adjacentCities = {}
        self.visited = False
        
    def setVisited(self):
        self.visited = True

    def setUnvisited(self):
        self.visited = False

    def getCords(self):
        return 

cityDict = {}
allCities = []

def calculateDistance(x1, y1, x2, y2):
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    dist = math.sqrt( (x2-x1)**2 + (y2-y1)**2 )
    return dist


#read data from file, create object for each city containing name, xCord, yCord
with open(r"coordinates.txt") as f:
    linesFromFile = []
    for line in f:
        #remove newline character and add line to list
        linesFromFile.append(line.rstrip('\n'))
        stringFromFile = ""
        #list of tokens to strings
        for element in linesFromFile:
            stringFromFile += element
        #split on spaces
        splitString = stringFromFile.split(' ')
        #also make a list of all cities
        allCities.append(splitString[0])
        #link the city name and its coordinates in cityDict
        cityDict[splitString[0]] = city(splitString[1], splitString[2])
        #clean up
        linesFromFile.clear()
        stringFromFile = None
        splitString.clear()
    f.close()

#read data from file, create object for each city containing name, xCord, yCord
with open(r"Adjacencies.txt") as f:
    linesFromFile = []
    for line in f:
        #remove newline character and add line to list
        linesFromFile.append(line.rstrip('\n'))
        stringFromFile = ""
        #list of tokens to strings
        for element in linesFromFile:
            stringFromFile += element
        #split on spaces
        splitString = stringFromFile.split(' ')
        #calculate and store distances between the adjacent cities
        for key,value in cityDict.items():
            if splitString[0] == key:
                for i in range(1, len(splitString)):
                    d = calculateDistance(cityDict[splitString[0]].xCord, cityDict[splitString[0]].yCord, cityDict[splitString[i]].xCord, cityDict[splitString[i]].yCord)
                    cityDict[key].adjacentCities[splitString[i]] = d
                    if splitString[0] not in cityDict[splitString[i]].adjacentCities:
                        d = calculateDistance(cityDict[splitString[i]].xCord, cityDict[splitString[i]].yCord, cityDict[splitString[0]].xCord, cityDict[splitString[0]].yCord)
                        cityDict[splitString[i]].adjacentCities[key] = d
        #clean up
        linesFromFile.clear()
        stringFromFile = None
        splitString.clear()
    f.close()

def bestFirstSearch(startCity, endCity, cityDict):
    #setup
    priorityQ = PriorityQueue()
    unvisitedList = []
    visitedList = []
    cityDict[startCity].setVisited()
    visitedList.append(startCity)
    currentCity = startCity
    #loop
    while currentCity != endCity:
        def populatePriorityQ(currentCity):
        #put the current city's adjacencies in unvisitedList
            for key in cityDict[currentCity].adjacentCities.keys():
                unvisitedList.append(key)
        #put each city in unvisited list into priorityQ to sort by distance
            for eachCity in unvisitedList:
                for cityDist in cityDict[eachCity].adjacentCities.values():
                    priorityQ.put((cityDist, eachCity))

        populatePriorityQ(currentCity)

        #check if nearest city has been visited
        def checkQForVisited(Q):
            #maybe if Q is not empty?
            if Q.qsize() > 0:
                cityToCheck = Q.queue[0]
                list(cityToCheck)
                cityToCheck = cityToCheck[1]
                if cityDict[cityToCheck].visited == True:
                    discardCity = priorityQ.get()
                    return checkQForVisited(Q)
                else:
                    pass
            else:
                pass

        checkQForVisited(priorityQ)
        if priorityQ.empty():
            del visitedList[-1]
            currentCity = visitedList[-1]
        else:
            #update currentCity to the nearest adjacent city
            currentCity = priorityQ.queue[0]
            list(currentCity)
            currentCity = currentCity[1]
            #set currentCity to visited, add it to visitedList
            cityDict[currentCity].setVisited()
            visitedList.append(currentCity)

        #clear priorityQ
        priorityQ.queue.clear()
        unvisitedList.clear()

    #print list of cities visited
    print("\nA route you could take would be:")
    print(*visitedList, sep = " ->\n")

    def clearVisitedStatus(listOfCities):
        for city in allCities:
            cityDict[city].setUnvisited()

    clearVisitedStatus(allCities)

#Begin
running = True
while(running):
    print("This program finds a route between two cities using best first search.")

    '''
    format_string = "{:<}{:<}{:<}"
    #print(format_string.format(*headers))
    for entry in allCities:
        print(format_string.format(*entry))
    '''

    while True:
        startCity = input('Enter starting city: ')
        if startCity in allCities:
            break
        else:
            print("Please enter a valid city.\n")
            continue

    while True:
        endCity = input('Enter ending city: ')
        if endCity in allCities:
            break
        else:
            print("Please enter a valid city.\n")
            continue

    bestFirstSearch(startCity, endCity, cityDict)

    choosing = True
    while(choosing):
        choice = input("\nWould you like to find another route?\n")
        if choice == "yes" or choice == "Yes" or choice == "YES" or choice == "Y" or choice == "y":
            choosing = False
        elif choice == "no" or choice == "No" or choice == "NO" or choice == "N" or choice == "n":
            running = False
            choosing = False
        else:
            print("\nPlease enter yes or no.")