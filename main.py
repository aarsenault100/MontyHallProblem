#The Monty Hall Problem Simulator
import random
import requests
import sys

#Will attempt to pull true random numbers from random.org using restful api
#else will create random numbers locally
class randomNumberRequest:

    def __init__(self,times):
        
        #The RESTFUL API used to create random numbers from random.org in a range of 0-2
        self.url = "https://www.random.org/integers/?num="+str(times)+"&min=0&max=2&col=1&base=10&format=plain&rnd=new"
        self.numberList = []

        #Attempts to make a get request.
        try:
            print("Fetching true random numbers from random.org\n")

            self.numberRequest = requests.get(self.url)
            
            #Parses text into Array
            self.numberList = self.numberRequest.text.splitlines()

            #Converts Chars into intigers
            for x in range(len(self.numberList)):
                self.numberList[x] = int(self.numberList[x])

            print('Fetch successful!\n')

        except:
            #If unable to retrieve from random.org, will generate locally  
            print("\nUnable to retrive numbers from random.org \nGenerating locally\n")

            for x in range(times):
                
                randomNum = random.randrange(0,3)

                self.numberList.append(randomNum)

    
    @property
    def get(self):
        return self.numberList



#Creates a single instance of the monty problem.
class MontyInstance:

    def __init__(self,moneyDoor,guess,switch):

        self.moneyDoor = moneyDoor
        self.guess = guess
        self.switch = switch
        self.openDoor = None
        self.hasWon = False

        #Creating doors
        self.doors = [0,0,0]
        #The 'Money' door is represented by a 1,The 'Goat' door is represented by 0
        
        #Setting the Money Door
        self.doors[moneyDoor] = 1

        #The host will reveal a door, The host will NEVER reveal the 'money', so will always reveal a 'goat'.
        for x in range(len(self.doors)):
            if x != self.guess and x != self.moneyDoor:
                self.openDoor = x
                break
        
        #The host will then ask if the contestant would like to switch his pick to the only option left.

        if switch:
            for x in range(len(self.doors)):
                if x != self.guess and x != self.openDoor:
                    self.guess = x
                    break
        
        #The host will then open the door that the contestant picked. If it is the money door, he wins.
        if self.guess == self.moneyDoor:
            self.hasWon = True

    @property
    def outCome(self):
        return self.hasWon




#Main Class
class Main:

    def __init__(self, times):

        times = int(times)

        #Random numbers are genorated ahead of time in bulk as to not spam the random.org server with requests
        self.moneyDoors = randomNumberRequest(times).get
        self.guesses = randomNumberRequest(times).get


        #Variable to store wins from when the contestant chose to switch.
        self.switchOutcomes = 0
        self.switchPer = 0.0

        #Variable to store wins from when the contestant chose not to switch.
        self.noSwitchOutcomes = 0
        self.noSwitchPer = 0.0

        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        for x in range(times):

            monty = MontyInstance(self.moneyDoors[x],self.guesses[x],True)
            if monty.outCome == True:
                self.switchOutcomes = self.switchOutcomes + 1

        print(f"Switching doors won {self.switchOutcomes} out of {times}")
            
        for x in range(times):

            monty = MontyInstance(self.moneyDoors[x],self.guesses[x],False)
            if monty.outCome == True:
                self.noSwitchOutcomes = self.noSwitchOutcomes + 1
        
        print(f"Not switching doors won {self.noSwitchOutcomes} out of {times}")


Main(sys.argv[1])