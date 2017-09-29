import random
import math
import datetime
import graphics as gs
import time

WINH = 500
WINW = 500
NumberOfCities = 15				#Number of cities you need to visit
generations = 500				#Number of generations
population = 30				#Number of 

global startTime,generations,population

class Window:

	def __init__(self):
		self.win = gs.GraphWin("My window",WINH,WINW)
		self.win.setBackground('black')

	def clear(self):
	    for item in self.win.items[:]:
	        item.undraw()
	    self.win.update()

	def DrawCities(self,cities,order,generation):
	
		


		for j in range(0,len(order)-1):
			self.pt1 = gs.Point(cities[order[j]][0],cities[order[j]][1])
			self.pt2 = gs.Point(cities[order[j+1]][0],cities[order[j+1]][1])
			self.cir = gs.Circle(self.pt1,5)
			self.cir.setFill('white')
			self.cir.draw(self.win)
			self.ln = gs.Line(self.pt1,self.pt2)
			self.ln.setOutline('white')
			self.ln.draw(self.win)

		
		self.pt2 = gs.Point(cities[order[j+1]][0],cities[order[j+1]][1])
		self.cir = gs.Circle(self.pt2,5)
		self.cir.setFill('white')
		self.cir.draw(self.win)

		self.message = gs.Text(gs.Point(self.win.getWidth()/2, 20), 'Generation number: {0}'.format(generation))
		self.message.setFill('white')
		self.message.draw(self.win)

		time.sleep(0.00005)
		if(generation == generations-1):
			self.win.getMouse()
		self.clear()

	def exit(self):
		self.win.getMouse()
		self.win.close()

class City:

	def __init__(self):
		self.x = random.randint(0,500)
		self.y = random.randint(0,500)

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y


class Country:
	def __init__(self,amount):
		self.amount = amount
		self.cities=[]

	def generate(self):
		for i in range(0,self.amount):
			self.city = City()
			self.cities.append([self.city.get_x(),self.city.get_y()])

	def getCities(self):
		return self.cities


class Solver:

	class Parent:
		def __init__(self,cities):
			self.cities =  cities
			self.order = []
			#self.fitness 
			for i in range(0,len(cities)):
				self.order.append(i)
			random.shuffle(self.order)

		def mutate(self):
			self.index1 = random.randint(0,len(self.cities)-1)
			self.index2 = random.randint(0,len(self.cities)-1)
			while self.index1 == self.index2:
				self.index2 = random.randint(0,len(self.cities)-1)
			self.temp = self.order[self.index1]
			self.order[self.index1] = self.order[self.index2]
			self.order[self.index2] = self.temp


		def display(self):
			self.fit = self.calc_fitness()
			print ("{0} \t {1} \t {2} \t ".format(self.cities,self.order,self.fit))

		def calc_fitness(self):
			self.fitness = 0
			self.vector = [0,0]
			for i in range(0,len(self.order)-1):
				self.vector[0] = self.cities[self.order[i+1]][0] - self.cities[self.order[i]][0]
				self.vector[1] = self.cities[self.order[i+1]][1] - self.cities[self.order[i]][1]
				self.fitness += (pow(self.vector[0],2) + pow(self.vector[1],2))
			return self.fitness



	class Population:

		def __init__(self,startpopulation,cities):
			self.popul_amt=startpopulation 
			self.cities = cities 
			

		def generate_start_population(self):
			self.population = []
			for i in range(0,self.popul_amt):
				self.population.append(Solver.Parent(self.cities))


		def display_population(self):
			print("LENGHT OF THE POPULATION IS {0} ".format(len(self.population)))
			for i in range(0,len(self.population)):
				Solver.Parent.display(self.population[i])

		def makelist(list,index,option):
			self.newlist=[]
			if(option == 1):
				for i in range(index,len(list)):
					self.newlist.append(list[i])
			if(option == 0):
				for i in range(0,index):
					self.newlist.append(list[i])
			return newlist

		def crossover(self,father,mother):
			self.order1 = father.order
			self.order2 = mother.order

			self.start = math.floor(random.randint(0,len(self.order1)))
			self.end = math.floor(random.randint(self.start+1,len(self.order1)+1))

			self.neworder = self.order1[self.start:self.end]

			self.leftover = len(self.order1) - len(self.neworder)

			self.count = 0
			self.i = 0
			while(self.count < self.leftover):
				self.city = self.order2[self.i]
				if(self.city not in self.neworder):
					self.neworder.append(self.city)
					self.count+=1
				self.i+=1
			self.child = Solver.Parent(self.cities)
			self.child.order = self.neworder
			return self.child
			

		def eval(self):

			self.parents = []
			self.number1,self.number2 = 0,1
			self.bestFitness = [math.inf,math.inf]

			for i in range(0,len(self.population)):
				self.guess = Solver.Parent.calc_fitness(self.population[i])
				if(self.guess < self.bestFitness[1]):
					if(self.guess < self.bestFitness[0]):
						self.bestFitness[1] = self.bestFitness[0]
						self.bestFitness[0] = self.guess
						self.number1 = i
					else:
						self.bestFitness[1] = self.guess
						self.number2 = i
			
			self.parents.append(self.population[self.number1])
			
			self.parents.append(self.population[self.number2])

			#print("\n")
			#print("--------------------------------")
			#print("NEW BEST PARENTS")

			#Solver.Parent.display(self.parents[0])
			#Solver.Parent.display(self.parents[1])
			#print("--------------------------------")
			#print("\n")
			return self.parents				
				#print(calc_fitness(self.population[i]))

		def generate_new_population(self):
			self.new_population = []
			for i in range(0,len(self.population)):
				self.prob = random.randint(0,100)
				self.offspring = Solver.Parent(self.cities)
				self.offspring = self.crossover(self.parents[0],self.parents[1])
				if(self.prob == 10):
					Solver.Parent.mutate(self.offspring)
				self.new_population.append(self.offspring)
			self.population = self.new_population




	def __init__(self,startpopulation,cities,maxgenerations):
		self.population = Solver.Population(startpopulation,cities)
		self.population.generate_start_population()
		self.maxgen = maxgenerations
		self.cities = cities
		
		


	def solve(self):
		
		print("\n")
		self.population.display_population()
		win = Window()
		for generation in range(0,self.maxgen):
			#print("--------------------------------------------------")
			#print("IT'S {0} GENERATION".format(generation))
			
			#self.population.display_population()
			#print("--------------------------------------------------")
			par=self.population.eval()

			Window.DrawCities(win,self.cities,par[0].order,generation)
			Solver.Population.generate_new_population(self.population)



def main():
	random.seed()
	startTime = datetime.datetime.now()
	

	Russia = Country(NumberOfCities)

	Russia.generate()
	sol = Solver(population,Russia.getCities(),generations)
	sol.solve()

main()