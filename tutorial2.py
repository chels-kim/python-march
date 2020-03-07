import random
import numpy as np
import math

'''
Feb 4, 2020

< Goal >
Reproduce the first tutorial's contents, with different classes and objects

< Notes >
Good naming conventions/practices
- have CRUD (Create, Read, Update, and Delete) in mind, when writing your code.
- "get...", "set...", "is...", "remove..." are some common prefixes that helps with readability of the code, for yourself as well as others who will read your code.
- Remember that only classes, not variables, start with upper case.

< Next steps/Challenges >
- Serve to humans
- Track inventory
- Track number of sips per drink
- Track ingested drink in each human
'''

# Blood Alcohol Percentage; source https://www.healthline.com/health/how-much-does-it-take-to-get-drunk#intoxication-levels
# Modified some numbers for convenience

BAP_males = np.array([[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
	[0.04, 0.04, 0.025, 0.025, 0.02, 0.02, 0.02, 0.02, 0.02],
	[0.08, 0.08, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03],
	[0.11, 0.11, 0.09, 0.08, 0.07, 0.06, 0.06, 0.05, 0.05],
	[0.15, 0.15, 0.12, 0.11, 0.09, 0.08, 0.08, 0.07, 0.06],
	[0.19, 0.19, 0.16, 0.13, 0.12, 0.11, 0.09, 0.09, 0.08],
	[0.23, 0.23, 0.19, 0.16, 0.14, 0.13, 0.11, 0.10, 0.09],
	[0.26, 0.26, 0.22, 0.19, 0.16, 0.15, 0.13, 0.12, 0.11],
	[0.30, 0.30, 0.25, 0.21, 0.19, 0.17, 0.15, 0.14, 0.13],
	[0.34, 0.34, 0.27, 0.24, 0.21, 0.19, 0.17, 0.15, 0.14],
	[0.38, 0.38, 0.31, 0.28, 0.23, 0.21, 0.19, 0.17, 0.16]])
	# First column had to be added aritifically bc they had no male data for ~90lb

BAP_females = np.array([[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
	[0.05, 0.05, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02],
	[0.10, 0.092, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04],
	[0.15, 0.14, 0.11, 0.10, 0.092, 0.08, 0.07, 0.06, 0.06],
	[0.20, 0.18, 0.15, 0.13, 0.11, 0.10, 0.095, 0.08, 0.08],
	[0.25, 0.23, 0.19, 0.16, 0.14, 0.13, 0.11, 0.10, 0.095],
	[0.30, 0.27, 0.23, 0.19, 0.17, 0.15, 0.14, 0.12, 0.11],
	[0.35, 0.32, 0.27, 0.23, 0.20, 0.18, 0.16, 0.14, 0.13],
	[0.40, 0.36, 0.30, 0.26, 0.23, 0.20, 0.18, 0.17, 0.15],
	[0.45, 0.41, 0.34, 0.29, 0.26, 0.23, 0.20, 0.19, 0.17],
	[0.51, 0.45, 0.38, 0.32, 0.28, 0.25, 0.23, 0.21, 0.19]])


class Drink(object):


	def __init__(self, index): # stuff that goes in the parentheses here are the class's arguments. "self" is always always always there.
		self.number = index + 1 
		self.nameDrink = 'Drink'
		self.currentVolumeInMl = 175 # default drink volume


	def __repr__(self):
		return	self.nameDrink + ' #' + str(self.number)


	def getCurrentVolumeInMl(self):
		return str(self.currentVolumeInMl) + 'mL remaining'



class Wine(Drink):

	def __init__( self , index ):

		super().__init__( index ) # "super" function is used to refer back to its parent class, in this case "Drink". 
								  # This is useful when you want to preserve and add to the parent class's definitions.
		self.nameDrink = 'Wine'	  # Here we override the nameDrink variable inherited from "Drink" class into a variable named "Wine".



class Human(object):

	def __init__(self, name, weight):
		self.name = name
		self.age = 24
		self.sex = 'female'
		self.weight = weight

		self.drinksInPossession = []
		self.numDrinksBought = 0

		self.remainingDrinks = []
		self.finishedDrinks = []

		weightsIndices = np.append(90, np.linspace(100,240,8))
		temp = np.abs(weightsIndices - self.weight)
		self.weightIdx = np.where(temp == min(temp))[0][0]
		self.drinkIdx = 0
		self.totalVolumeIngested = 0
		self.BAP = 0
		self.thresholdBAP = []


	def __repr__(self):
		return	'Sexy ' + self.name


	def canGoToBar(self):
		if self.age < 18:
			print('Get the hell out of this bar!')
		else:
			print(self.name + " goes to the bar. Let's get lit!")


	def buyDrinks(self, nameBar, numDrinksBought):
		self.drinksInPossession += nameBar.serveDrink(numDrinksBought)	# += operator: add to the current value. e.g. a += b is equivalent to a = a+b
		self.numDrinksBought = len(self.drinksInPossession)
		self.remainingDrinks = [ i for i in self.drinksInPossession]
		
		if nameBar.getCurrentCustomers.count(self) == 0:
			nameBar.getCurrentCustomers.append(self)
		return


	def takeSips(self, numSips, drinkIndex = 0):
		# 1. choose the drink in the list. evaluate its current volume.
		# 2-1. if numSips gives volume (X) that is greater than or equal to that (Y) remaining in chosen drink,
			# add Y to total volume ingested and prompt to get rest of the sips from a different drink
			# set Y to equal zero
			# move that drink from the list of remaining to finished drinks
		# 2-2. if X < Y
			# add X to total volume ingested
			# set Y to equal Y - X

		drinkChosen = self.remainingDrinks[drinkIndex] # a "Drink" object

		sipVolume = Human.getSipVolume( numSips )
		if sipVolume >= drinkChosen.currentVolumeInMl:
			self.totalVolumeIngested += drinkChosen.currentVolumeInMl

			numSipsRemaining = numSips - math.ceil(drinkChosen.currentVolumeInMl/20)
			print("You have taken " + str(math.ceil(drinkChosen.currentVolumeInMl/20)) + ' sips from ' + drinkChosen.__repr__() + ".")
			print("Unsatisfied? Take the remaining " + str(numSipsRemaining) + " sips from a different drink.")
			
			drinkChosen.currentVolumeInMl = 0
			del self.remainingDrinks[drinkIndex]
			self.finishedDrinks.append(drinkChosen)
		else:
			self.totalVolumeIngested += sipVolume
			drinkChosen.currentVolumeInMl += -sipVolume
			print("You have taken " + str(numSips) + ' sips from ' + drinkChosen.__repr__() + ".")


	@staticmethod # this is a "decorator"; it modifies the method's behaviour without adding extra lines to the method
				  # This particular decorator allows us to ignore the need for "self" argument --- read more on this
	def getSipVolume( inNumSips ):
		return inNumSips * 20


	def isIntoxicated(self):

		self.drinkIdx = round(self.totalVolumeIngested / 175)
		
		intoxicationLevels = ['Safe driving limit','Impaired','Driving skills affected','Legally intoxicated','Possible death']

		if self.sex == 'female':
			self.thresholdBAP = [0.001, 0.04, 0.095, 0.30, 0.52]
			self.BAP = BAP_females[self.drinkIdx, self.weightIdx]
		else:
			self.thresholdBAP = [0.001, 0.03, 0.11, 0.28, 0.5]
			self.BAP = BAP_males[self.drinkIdx, self.weightIdx]

		tmp = self.thresholdBAP - self.BAP
		intoxicationIdx = np.where(tmp == min([n for n in tmp if n > 0]))[0][0]
		return 'Your blood alcohol percentage is approximately '+ str(self.BAP * 100) +' percent. ' + intoxicationLevels[intoxicationIdx] + '.'


	def howMuchMoreTillIntoxicated(self):
		if self.BAP > self.thresholdBAP[2]:
			return 'Already legally intoxicated.'
		else:
			if self.sex == 'female':
				thresholdVolumes = np.multiply([2, 3, 3, 3, 4, 4, 4, 5, 5],175)
			else:
				thresholdVolumes = np.multiply([2, 3, 3, 3, 4, 4, 4, 5, 5],175)
			return self.name + ' can drink approximately ' + str(thresholdVolumes[self.weightIdx] - self.totalVolumeIngested) + 'mL more alcohol before being intoxicated.'



class Bar(object):


	def __init__(self, nameOfBar, totalNumDrinks):
		self.nameOfBar = nameOfBar
		self.inventory = [ Wine(idx) for idx in range(totalNumDrinks) ] # This is called list comprehension
		self.totalNumDrinks = totalNumDrinks
		self.getCurrentCustomers = []


	def __repr__(self):
		return self.nameOfBar


	def getNumberOfCustomers(self):
		return len(self.getCurrentCustomers)


	def serveDrink(self,numDrinksBought):
		drinksServed = []
		if numDrinksBought > len(self.inventory):
			print("There are not enough drinks! Sorry, we'll just give you all that's left.")
			numDrinksBought = len(self.inventory)
		else:
			print(self.nameOfBar + ' is serving ' + str(numDrinksBought) + ' drinks...')
			
		for drink in range(numDrinksBought):
			drinksServed.append(self.inventory.pop()) # "pop" takes off and returns the last item/indexed item from the list
	
		self.totalNumDrinks = self.totalNumDrinks - numDrinksBought
		print(str(self.totalNumDrinks) + ' drinks remain at the bar:')
		print(self.inventory)
		return drinksServed



# Challenge

TresAmigos = Bar('Tres Amigos', 20)

print(TresAmigos)
print(TresAmigos.inventory)

print('\n')
TresAmigos.serveDrink(3)
#print(TresAmigos.inventory) # One less in the inventory


print('\n')
chelsea = Human('Chelsea', weight = 125)
print(chelsea)

print('\n')
chelsea.canGoToBar()


print('\n')
numDrinks = 2#random.randint(1,10)
chelsea.buyDrinks( TresAmigos, numDrinks ) # Number of drinks. Hint: you might neeed to pass the bar as an argument
chelsea.buyDrinks( TresAmigos, numDrinks ) # Number of drinks. Hint: you might neeed to pass the bar as an argument

print('\n')
print('Chelsea has bought the following '+ str(chelsea.numDrinksBought) + ' drinks:')
print(chelsea.drinksInPossession)
print("That's right y'all, Chelsea is gonna get lit with " + str(chelsea.numDrinksBought) + ' drinks tonight')

print('\n')
print(TresAmigos.inventory) # Has to show less drinks down by the number of drinks ingested


print('\n')
chelsea.takeSips(numSips = 20, drinkIndex = 1)
chelsea.takeSips(5, 2)
chelsea.takeSips(10, 0)
print(str(chelsea.totalVolumeIngested) + 'mL ingested in total')


print('\n')
print( "Chelsea has not yet finished the following drinks:")
for remainingDrink in chelsea.remainingDrinks:#( TresAmigos, numDrinksBought, numDrinksRemaining)
	print( remainingDrink )
	print( remainingDrink.getCurrentVolumeInMl() )

print('\n')
print( "Chelsea has finished the following drinks:")
for drink in chelsea.finishedDrinks:
	print( drink )
	print( drink.getCurrentVolumeInMl() )

print('\n')
print( chelsea.isIntoxicated() )

print('\n')
print( TresAmigos.getNumberOfCustomers() )
print( TresAmigos.getCurrentCustomers ) #Return chelsea obj


for customer in TresAmigos.getCurrentCustomers:
	print( customer.howMuchMoreTillIntoxicated() )

	for drink in customer.remainingDrinks:
		print(drink.getCurrentVolumeInMl())

