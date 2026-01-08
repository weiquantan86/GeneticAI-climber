import creature
import numpy as np

class Population():
    def __init__(self, pop_size, gene_count):
        self.creatures  = [creature.Creature(gene_count=gene_count) for i in range(pop_size)]
    
    @staticmethod
    def get_fitness_map(fit_vals):
        fitmap = []
        total=0
        for f in fit_vals:
            total = total + f
            fitmap.append(total)
        return fitmap     
        
    #from the fitmap, select the parent
    @staticmethod
    def select_parent(fitmap):
        r = np.random.rand() #0-1
        #generate a random number and scale it to
        #the map.
        r = r*fitmap[-1]
        for i in range (len(fitmap)):
            # if the generated number is smaller than
            # the i index in the fitmap, return the index
            #this way, the one with highest fitness function 
            # will be chosen more often
            if r<= fitmap[i]:
                return i
        
