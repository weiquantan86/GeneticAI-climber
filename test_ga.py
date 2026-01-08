import unittest 
import population
import simulation
import genome
import creature
import numpy as np


class TestGA(unittest.TestCase):

    def testBasicGA(self):
        #pop size can be changed too
        pop = population.Population(pop_size=200,
                                    gene_count=3)
         
        #number of threads = pool size, my mac has 8 cores so can go up to 8 
        sim = simulation.ThreadedSim(pool_size=8)
        #sim = simulation.Simulation()
        for iteration in range(10):
            #eval_population(pop,iterations), 2400 = 10 seconds, can change the parameters
            sim.eval_population(pop,4800)
            fits = [cr.get_distance_travelled() for cr in pop.creatures]
            links = [len(cr.get_expanded_links()) for cr in pop.creatures]
            print(iteration,"fittest:",np.round(np.max(fits),3), "mean",np.round(np.mean(fits),3),"mean links", np.round(np.mean(links)),"max links", np.round(np.max(links),3))
            fit_map = population.Population.get_fitness_map(fits)

            fmax = np.max(fits)
            for cr in pop.creatures:
                if cr.get_distance_travelled() == fmax:
                    elite = cr
                    break

            new_creatures=[]
            for i in range (len(pop.creatures)):
                p1_ind = population.Population.select_parent(fit_map)
                p2_ind = population.Population.select_parent(fit_map)
                p1 = pop.creatures[p1_ind]
                p2 = pop.creatures[p2_ind]
            
                #new
                dna = genome.Genome.crossover(p1.dna,p2.dna)
                dna = genome.Genome.point_mut(dna,rate=0.25,amount=0.25)
                dna = genome.Genome.shrink_mut(dna,rate=0.25)
                dna = genome.Genome.grow_mut(dna,rate=0.25)
                cr = creature.Creature(1)
                cr.update_dna(dna)
                new_creatures.append(cr)

            new_creatures[0] = elite
            #reset elite for the next run
            new_creatures[0].dist = 0
            new_creatures[0].start_position = None
            new_creatures[0].last_position = None
            csv_filename = str(iteration) + '_elite.csv'
            genome.Genome.to_csv(elite.dna, csv_filename)
                    
            
            pop.creatures = new_creatures

            self.assertIsNotNone(p1)
            self.assertIsNotNone(p2)
            


unittest.main()