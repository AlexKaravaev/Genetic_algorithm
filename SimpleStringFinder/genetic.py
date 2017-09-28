import random



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
	index2 = random.randrange(0,len(parent))
	childGenes = list(parent)
	newGene1,newGene2,alternative1,alternative2  = random.sample(geneSet,4)
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




def generate_start_population(target,amount,geneset):
	population = []
	for i in range(0,amount):
		
		population.append(generate_parent(len(target),geneset))
	return population

def generate_new_population(couple,family):
	population = []
	

	for i in range(0,amount):
		prob = random.randint(0,10)
	
		population.append(mutate((crossover(couple[0],couple[1]))))

def generate_parent(length,geneSet):
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