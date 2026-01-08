import unittest
import simulation
import creature
import os
import population

class TestSim(unittest.TestCase):

    def testSimExists(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim)

    def testSimId(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim.physicsClientId)

    def testRun(self):
        sim = simulation.Simulation()
        #cr = creature.Creature(gene_count=3)
        self.assertIsNotNone(sim.run_creature)

    def testRunXML(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count=3)
        sim.run_creature(cr)
        self.assertTrue(os.path.exists('temp.urdf'))
        
    def testPositionChanged(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count=3)
        sim.run_creature(cr)

        #print(cr.start_position)
        #print(cr.last_position)
        self.assertNotEqual(cr.start_position, cr.last_position)

    def testDist(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count=3)
        sim.run_creature(cr)
        dist = cr.get_distance_travelled()
        #print(dist)
        self.assertGreater(dist,0)
        
    def testPop(self):
        pop = population.Population(pop_size=10,gene_count=3)
        sim = simulation.Simulation()

        for cr in pop.creatures:
            sim.run_creature(cr)
        dists = [cr.get_distance_travelled() for cr in pop.creatures]
        
        #print(dists)
        self.assertIsNotNone(dists)

    #testing the multithread
    #it is now running correctly after creating a new venv with python3.7
    def testProc(self):
        pop = population.Population(pop_size=20,gene_count=3)
        tsim = simulation.ThreadedSim(pool_size=8)
        tsim.eval_population(pop,2400)
        dists = [cr.get_distance_travelled() for cr in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)


    
         
unittest.main()
