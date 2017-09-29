import random
import datetime
from genetic import *


global geneSet,target,generations,startTime,startingpopulation

geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.?"

target ="YO SOBAKI YA HARUTO UZUMAKI DA I KSTATI YA BUDUSHI HOKAGE"
generations = 2000
startingpopulation = 100
startTime = datetime.datetime.now()




def best_fitness(population):
	bestFitness = -1
	number =-1
	for i in range(0,len(population)):
		if (get_fitness(population[i]) > bestFitness):
			number = i
			bestFitness = get_fitness(population[i])

	return bestFitness



def get_fitness(guess):
	sum = 0
	for expected,actual in zip(target,guess):
		if expected == actual:
			sum += 1
	return sum

def mutate(parent):
	index1 = random.randrange(0,len(parent))
	
	childGenes = list(parent)
	newGene1,alternative1  = random.sample(geneSet,2)
	if newGene1 == childGenes[index1]:
		childGenes[index1] = alternative1
	else:
		childGenes[index1] = newGene1
	return ''.join(childGenes)

def crossover(mother,father):
	child = []
	randnum = random.randint(0,len(father))
	for i in range(0,len(father)):
		
		if(i < (len(mother) - randnum)):
			child.append(mother[i])
		else:
			child.append(father[i])
	


	return ''.join(child)




def generate_start_population(target):
	population = []
	for i in range(0,startingpopulation):
		
		population.append(generate_parent(len(target)))
	return population

def generate_new_population(couple,family):
	population = []
	

	for i in range(0,startingpopulation):
		prob = random.randint(0,1)
		if(prob == 1):
			population.append(mutate((crossover(couple[0],couple[1]))))
		else:
			population.append((crossover(couple[0],couple[1])))

	return population

def generate_parent(length):
	genes = []
	while len(genes) < length:
		sampleSize = min(length - len(genes),len(geneSet))
		genes.extend(random.sample(geneSet,sampleSize))
	return ''.join(genes)

def mating_pool(population):
	couple=[]
	temp = population
	for i in range(0,4):
		bestFitness = -1
		number=-1
		bestValue=''
		#print(temp)
		#print("!couple here!")
		for item in range(0,len(temp)):

			if (get_fitness(temp[item]) >= bestFitness):
				#if(temp[item] not in couple):
				bestValue = temp[item]
				#print(temp[item])
				bestFitness = get_fitness(temp[item])
				number = item
		
		if(number!=-1):
			couple.append(bestValue)
			temp.pop(number)
				


	
	
	temp.extend(couple)
	return couple




def display(guess):
	timeDiff = datetime.datetime.now() - startTime
	fitness = get_fitness(guess)
	print ("{0} \t {1} \t {2} ".format(guess,fitness,timeDiff))

def display_population(population):
	for i in range(0,len(population)):
		display(population[i])


def main():
	random.seed()
	population = generate_start_population(target)
	bestParent = population[0]
	bestFitness = get_fitness(population[0])
	i = 0
	new_population = []
	print("start_population")
	display_population(population)
	print("\t")
	success = 0

	for generation in range(0,generations):

		couples = mating_pool(population)
		display_population(population)
		new_population = generate_new_population(couples,population)

		if (len(target) <= best_fitness(new_population)):
			print("I am in {1} generation state this is best_fitness {0}".format(best_fitness(new_population),generation))
			population = new_population
			success = 1

			print("------------SUCCESS!-----------")
			break

		for i in range(len(population))[::-1]:
			del population[i]
		population = new_population
		bestFitness = best_fitness(new_population)


	if(success == 0):
		print("---------FAILURE--------")

if __name__ == "__main__":
	main()


