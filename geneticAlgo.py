# Simple Genetic Algorithm 

import pylab as pl
import numpy as np
import genetic
class sga:

  def __init__(self, stringLength, popSize, nGens, pm, pc):
        # stringLength: int, popSize: int, nGens: int, 
        # prob. mutation pm: float; prob. crossover pc: float
        fid=open("results.txt","w")        # open, initialize output file
        self.fid = fid
        self.stringLength = stringLength   # number of bits in a chromosome
        if np.mod(popSize,2)==0:           # popSize must be even
        	self.popSize = popSize
        else:
        	self.popSize = popSize+1
        self.pm = pm                       # probability of mutation
        self.pc = pc                       # probability of crossover
        self.nGens = nGens                 # max number of generations
        self.pop = np.random.rand(self.popSize,self.stringLength)
        self.pop = np.where(self.pop<0.5,1,0)  # create initial pop
        fitness = self.fitFcn(self.pop)    # fitness values for initial population
        self.bestfit = fitness.max()       # fitness of (first) most fit chromosome
        self.bestloc = np.where(fitness == self.bestfit)[0][0]  # most fit chromosome locn
        self.bestchrome = self.pop[self.bestloc,:]              # most fit chromosome
        self.bestfitarray = np.zeros(self.nGens + 1)  # array of max fitness vals each generation
        self.bestfitarray[0] = self.bestfit           #  (+ 1 for init pop plus nGens)
        self.meanfitarray = np.zeros(self.nGens + 1)  # array of mean fitness vals each generation
        self.meanfitarray[0] = fitness.mean()
        fid.write("popSize: {}  nGens: {}  pm: {}  pc: {}\n".format(popSize,nGens,pm,pc))
        fid.write("initial population, fitnesses: (up to 1st 100 chromosomes)\n")
        for c in range(min(100,popSize)):   # for each of first 100 chromosomes 
           fid.write("  {}  {}\n".format(self.pop[c,:],fitness[c]))
        fid.write("Best initially:\n  {} at locn {}, fitness = {}\n".format(self.bestchrome,self.bestloc,self.bestfit))



##make this run the dino game, outputting the fitness of each chromosome

  def fitFcn(self,pop):          # compute population fitness values   
     fitness = np.zeros(self.popSize) # initialize fitness values (1D array)
     index = 0
     for ind, chromosome in enumerate(pop):  
         print('++++++++++++++++++++++++++')
         print('Population: '+ str(ind))
         print('++++++++++++++++++++++++++')                                  
         t = map(str, chromosome.tolist())
         fitness[index] = genetic.run_game(''.join(t)) ################Run game here
         index = index + 1
     return fitness
  

 ##Given some variables like distance, height
 #testComment
  def rulematch(self,rules,close,obstacle):  
      ruleIndex = 0 #index of what rule we're on
      ruleFineIndex = 0 ##index of exactly what point in the chromosome we're on

      while(ruleIndex < 5):
          match = True
          ruleFineIndex = 4 * ruleIndex

          #matching the first bit
          if obstacle == 'high':
              if rules[ruleFineIndex] == 1: match = False #if its a high obstacle but rule is for low
          else:
              if rules[ruleFineIndex] == 0: match = False #opposite

          #matching second bit
          if close:
              if rules[ruleFineIndex + 1] == 1: match = False #if its for close situations but rule is for far
          else:
              if rules[ruleFineIndex + 1] == 0: match = False #opposite

          if match:
              return self.decode(rules[ruleFineIndex:(ruleFineIndex + 4)])

      return 'nothing'           # no rules match (return empty array)
 

 ##Given a matching rule tell it to jump, duck or do nothing
  def decode(self,bits):           
      if bits[2] == 1: #if it thinks smart
         if bits[0] == 0: #if its a high obstacle
            return 'jump'
         else: #if its a low obstacle
             return 'duck'
      else: # if its not smart
          if bits[3] == 1: #it wants to jump
              return 'jump'
          else: #it wants to duck
              return 'duck'
 
 # conduct tournaments to select two offspring
  def tournament(self,pop,fitness,popsize):  # fitness array, pop size
     # select first parent par1
     cand1 = np.random.randint(popsize)      # candidate 1, 1st tourn., int
     cand2 = cand1                           # candidate 2, 1st tourn., int
     while cand2 == cand1:                   # until cand2 differs
        cand2 = np.random.randint(popsize)   #   identify a second candidate
     if fitness[cand1] > fitness[cand2]:     # if cand1 more fit than cand2 
        par1 = cand1                         #   then first parent is cand1
     else:                                   #   else first parent is cand2
        par1 = cand2
     # select second parent par2
     cand1 = np.random.randint(popsize)      # candidate 1, 2nd tourn., int
     cand2 = cand1                           # candidate 2, 2nd tourn., int
     while cand2 == cand1:                   # until cand2 differs
        cand2 = np.random.randint(popsize)   #   identify a second candidate
     if fitness[cand1] > fitness[cand2]:     # if cand1 more fit than cand2 
        par2 = cand1                         #   then 2nd parent par2 is cand1
     else:                                   #   else 2nd parent par2 is cand2
        par2 = cand2
     return par1,par2

  def xover(self,child1,child2):    # single point crossover
        # cut locn to right of position (hence subtract 1)
        locn = np.random.randint(0,self.stringLength - 1)
        tmp = np.copy(child1)       # save child1 copy, then do crossover
        child1[locn+1:self.stringLength] = child2[locn+1:self.stringLength]
        child2[locn+1:self.stringLength] = tmp[locn+1:self.stringLength]
        return child1,child2

  def mutate(self,pop):            # bitwise point mutations
        whereMutate = np.random.rand(np.shape(pop)[0],np.shape(pop)[1])
        whereMutate = np.where(whereMutate < self.pm)
        pop[whereMutate] = 1 - pop[whereMutate]
        return pop

  def runGA(self):     # run simple genetic algorithme
        fid=self.fid   # output file         
        for gen in range(self.nGens): # for each generation gen
           print('++++++++++++++++++++++++++')
           print('Generation: '+ str(gen))
           print('++++++++++++++++++++++++++')
           # Compute fitness of the pop         
           fitness = self.fitFcn(self.pop)  # measure fitness 
           # initialize new population
           newPop = np.zeros((self.popSize,self.stringLength),dtype = 'int64')
           # create new population newPop via selection and crossovers with prob pc
           for pair in range(0,self.popSize,2):  # create popSize/2 pairs of offspring
               # tournament selection of two parent indices
               p1, p2 = self.tournament(self.pop,fitness,self.popSize)  # p1, p2 integers
               child1 = np.copy(self.pop[p1,:])       # child1 for newPop
               child2 = np.copy(self.pop[p2,:])       # child2 for newPop
               if np.random.rand() < self.pc:                 # with prob self.pc 
                  child1, child2 = self.xover(child1,child2)  #   do crossover
               newPop[pair,:] = child1                # add offspring to newPop
               newPop[pair + 1,:] = child2
           # mutations to population with probability pm
           newPop = self.mutate(newPop)
           self.pop = newPop 
           fitness = self.fitFcn(self.pop)    # fitness values for population
           self.bestfit = fitness.max()       # fitness of (first) most fit chromosome
           self.bestfitarray[gen + 1] = self.bestfit        # save best fitness for plotting
           self.meanfitarray[gen + 1] = fitness.mean()      # save mean fitness for plotting
           self.bestloc = np.where(fitness == self.bestfit)[0][0]  # most fit chromosome locn
           self.bestchrome = self.pop[self.bestloc,:]              # most fit chromosome
           if (np.mod(gen,10)==0):            # print epoch, max fitness
                print("generation: ",gen+1,"max fitness: ",self.bestfit) 
        fid.write("\nfinal population, fitnesses: (up to 1st 100 chromosomes)\n")
        fitness = self.fitFcn(self.pop)         # compute population fitnesses
        self.bestfit = fitness.max()            # fitness of (first) most fit chromosome
        self.bestloc = np.where(fitness == self.bestfit)[0][0]  # most fit chromosome locn
        self.bestchrome = self.pop[self.bestloc,:]              # most fit chromosome
        for c in range(min(100,self.popSize)):  # for each of first 100 chromosomes
           fid.write("  {}  {}\n".format(self.pop[c,:],fitness[c])) 
        fid.write("Best:\n  {} at locn {}, fitness: {}\n\n".format(self.bestchrome,self.bestloc,self.bestfit))
        pl.ion()      # activate interactive plotting
        pl.xlabel("Generation")
        pl.ylabel("Fitness of Best, Mean Chromosome")
        pl.plot(self.bestfitarray,'kx-',self.meanfitarray,'kx--')
        pl.show()
        pl.pause(0)
        fid.close()
