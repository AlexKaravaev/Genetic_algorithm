import random
import datetime
global geneSet,target,generations,startTime,startingpopulation
geneSet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!.?"
target = "Hello World"
generations = 50
startingpopulation = 6


def generate_start_population(length):
	population = []
	for i in range(0,startingpopulation):
		
		population.append(generate_parent(length))
	return population

def generate_new_population(couple,couple2):
	population = []
	prob = random.randint(0,2)
	for i in range(0,6):
		if(i<=2):
			if(prob == 1):
				population.append(mutate((crossover(couple[0],couple[1]))))
			else:
				population.append(crossover(couple[0],couple[1]))
		else:
			if(prob==1):
				population.append(mutate((crossover(couple2[0],couple2[1]))))
			else:
				population.append(crossover(couple2[0],couple2[1]))
	
	return population

def best_fitness(population):
	bestFitness = -1
	for i in range(0,len(population)):
		if (get_fitness(population[i]) > bestFitness):
			bestFitness = get_fitness(population)

	return bestFitness

def generate_parent(length):
	genes = []
	while len(genes) < length:
		sampleSize = min(length - len(genes),len(geneSet))
		genes.extend(random.sample(geneSet,sampleSize))
	return ''.join(genes)

def get_fitness(guess):
	sum = 0
	for expected,actual in zip(target,guess):
		if expected == actual:
			sum+=1
	return sum

def mutate(parent):
	index = random.randrange(0,len(parent))
	childGenes = list(parent)
	newGene,alternative  = random.sample(geneSet,2)
	if newGene == childGenes[index]:
		childGenes[index] = alternative
	else:
		childGenes[index] = newGene
	return ''.join(childGenes)

def crossover(mother,father):
	child = list()
	for i in range(0,len(father)):
		
		if(i < len(mother) - random.randint(0,len(father))):
			child.append(mother[i])
		else:
			child.append(father[i])
	


	return ''.join(child)





def display(guess):
	timeDiff = datetime.datetime.now() - startTime
	fitness = get_fitness(guess)
	print ("{0} \t {1} \t {2} ".format(guess,fitness,startTime))

def display_population(population):
	for i in range(0,len(population)):
		display(population[i])


def mating_pool(population):
	couple1 = [population[0],population[1]]
	couple2 = [population[len(population)-2],population[len(population)-1]]
	'''firstbestfitness = population[0]
	secondbestfitness = population[1]
	for i in range(2,len(population)):
		if (get_fitness(population[i]) > secondbestfitness):
			if(get_fitness(population[i]) > firstbestfitness):
				
				couple1[1] = couple1[0]
				secondbestfitness = get_fitness(couple1[1])
				
				couple1[0] = population[i]
				firstbestfitness = get_fitness(population[i])
				
			else:
				couple1[1] = population[i]
				secondbestfitness = get_fitness(population[i])

	firstbestfitness = population[len(population)-2]
	secondbestfitness = population[len(population)-1]

	for i in range(0,len(population)):
		if(population[i] not in couple1):
			if (get_fitness(population[i]) > secondbestfitness):
				if(get_fitness(population[i]) > firstbestfitness):
					
					couple2[1] = couple2[0]
					secondbestfitness = get_fitness(couple2[1])
					
					couple2[0] = population[i]
					firstbestfitness = get_fitness(population[i])
					
				else:
					couple2[1] = population[i]
	
				secondbestfitness = get_fitness(population[i])'''
	
	couple=[]
	number=0
	for i in range(0,4):
		bestFitness = -1
		for item in range(0,len(population)-i):
			if (get_fitness(population[item]) > bestFitness):
				couple.append(population[item])
				bestFitness = get_fitness(population[item])
				number = item
		population.pop(number)
				
				


	
	

	return couple



random.seed()
startTime = datetime.datetime.now()
population = generate_start_population(len(target))
bestParent = population[0]
bestFitness = get_fitness(population[0])
couple = mating_pool(population)
i = 0
new_population = []
display_population(population)
#print(population[0])

for generation in range(0,generations):
		
	couple1=[]
	couple2=[]
	couple = mating_pool(population)
	#print(couple[0])
	couple1.append(couple[0])
	couple1.append(couple[1])
	couple2.append(couple[2])
	couple2.append(couple[3])
	if(generation==0 or generation==generations-1):
			print(couple1)
			print(couple2)
			display_population(generate_new_population(couple1,couple2))
	new_population = generate_new_population(couple1,couple2)
	

	
	
	if (bestFitness == len(target)):
		print("I am in if state this is best_fitness{0}".format(bestFitness))
		break
	
	for i in range(len(population))[::-1]:
		del population[i]
	population = new_population
	
	bestFitness = best_fitness(new_population)
	#display_population(population)

print("it's generation!{0}\t".format(generation))
display_population(population)



