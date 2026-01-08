import pybullet as p
import pybullet_data
import time
import numpy as np
import random
import creature
import math

import population
import simulation
import genome
import creature


# p.connect(p.GUI)
# p.setAdditionalSearchPath(pybullet_data.getDataPath())






def make_mountain(num_rocks=100, max_size=0.25, arena_size=10, mountain_height=5,physicsClientId=0):
    def gaussian(x, y, sigma=arena_size/4):
        """Return the height of the mountain at position (x, y) using a Gaussian function."""
        return mountain_height * math.exp(-((x**2 + y**2) / (2 * sigma**2)))

    for _ in range(num_rocks):
        x = random.uniform(-1 * arena_size/2, arena_size/2)
        y = random.uniform(-1 * arena_size/2, arena_size/2)
        z = gaussian(x, y)  # Height determined by the Gaussian function

        # Adjust the size of the rocks based on height. Higher rocks (closer to the peak) will be smaller.
        size_factor = 1 - (z / mountain_height)
        size = random.uniform(0.1, max_size) * size_factor

        orientation = p.getQuaternionFromEuler([random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)],physicsClientId=physicsClientId)
        rock_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size],physicsClientId=physicsClientId)
        rock_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[size, size, size], rgbaColor=[0.5, 0.5, 0.5, 1],physicsClientId=physicsClientId)
        rock_body = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=rock_shape, baseVisualShapeIndex=rock_visual, basePosition=[x, y, z], baseOrientation=orientation,physicsClientId=physicsClientId)
        p.changeDynamics(rock_body, -1, lateralFriction=4.0,physicsClientId = physicsClientId)



def make_rocks(num_rocks=100, max_size=0.25, arena_size=10,physicsClientId=0):
    for _ in range(num_rocks):
        x = random.uniform(-1 * arena_size/2, arena_size/2)
        y = random.uniform(-1 * arena_size/2, arena_size/2)
        z = 0.5  # Adjust based on your needs
        size = random.uniform(0.1,max_size)
        orientation = p.getQuaternionFromEuler([random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)],physicsClientId=physicsClientId)
        rock_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size])
        rock_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[size, size, size], rgbaColor=[0.5, 0.5, 0.5, 1],physicsClientId=physicsClientId)
        rock_body = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=rock_shape, baseVisualShapeIndex=rock_visual, basePosition=[x, y, z], baseOrientation=orientation,physicsClientId=physicsClientId)


def make_arena(arena_size=10, wall_height=1, physicsClientId=0):
    wall_thickness = 3.0
    floor_collision_shape = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[arena_size/2, arena_size/2, wall_thickness],physicsClientId=physicsClientId)
    floor_visual_shape = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[arena_size/2, arena_size/2, wall_thickness], rgbaColor=[1, 1, 0, 1],physicsClientId=physicsClientId)
    floor_body = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=floor_collision_shape, baseVisualShapeIndex=floor_visual_shape, basePosition=[0, 0, -wall_thickness],physicsClientId=physicsClientId)

    wall_collision_shape = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[arena_size/2, wall_thickness/2, wall_height/2],physicsClientId=physicsClientId)
    wall_visual_shape = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[arena_size/2, wall_thickness/2, wall_height/2], rgbaColor=[0.7, 0.7, 0.7, 1],physicsClientId=physicsClientId)  # Gray walls

    # Create four walls
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_collision_shape, baseVisualShapeIndex=wall_visual_shape, basePosition=[0, arena_size/2, wall_height/2],physicsClientId=physicsClientId)
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_collision_shape, baseVisualShapeIndex=wall_visual_shape, basePosition=[0, -arena_size/2, wall_height/2],physicsClientId=physicsClientId)

    wall_collision_shape = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[wall_thickness/2, arena_size/2, wall_height/2],physicsClientId=physicsClientId)
    wall_visual_shape = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[wall_thickness/2, arena_size/2, wall_height/2], rgbaColor=[0.7, 0.7, 0.7, 1],physicsClientId=physicsClientId)  # Gray walls

    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_collision_shape, baseVisualShapeIndex=wall_visual_shape, basePosition=[arena_size/2, 0, wall_height/2],physicsClientId=physicsClientId)
    p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_collision_shape, baseVisualShapeIndex=wall_visual_shape, basePosition=[-arena_size/2, 0, wall_height/2],physicsClientId=physicsClientId)

    return floor_body # return this for grounding logic


# p.setGravity(0, 0, -10)

# arena_size = 20
# make_arena(arena_size=arena_size)

# #make_rocks(arena_size=arena_size)

# mountain_position = (0, 0, -1)  # Adjust as needed
# mountain_orientation = p.getQuaternionFromEuler((0, 0, 0))
# p.setAdditionalSearchPath('shapes/')
# # mountain = p.loadURDF("mountain.urdf", mountain_position, mountain_orientation, useFixedBase=1)
# # mountain = p.loadURDF("mountain_with_cubes.urdf", mountain_position, mountain_orientation, useFixedBase=1)

# mountain = p.loadURDF("gaussian_pyramid.urdf", mountain_position, mountain_orientation, useFixedBase=1)

# # generate a random creature
# cr = creature.Creature(gene_count=3)
# # save it to XML
# with open('test.urdf', 'w') as f:
#     f.write(cr.to_xml())
# # load it into the sim
# rob1 = p.loadURDF('test.urdf', (0, 0, 10))


# p.setRealTimeSimulation(1)

# while True:
#     p.stepSimulation()
#     time.sleep(1.0/240)



class MountainSimulation(simulation.Simulation):
    """
    sublcass of Simulation to load mountain environment
    """
    def __init__(self, sim_id = 0):
        self.physicsClientId = p.connect(p.DIRECT)
        self.sim_id = sim_id

    def run_creature(self, cr, iterations=2400):
        try:
            pid = self.physicsClientId
            p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId = pid)
            p.resetSimulation(physicsClientId = pid)
            p.setGravity(0,0,-10,physicsClientId = pid)

            arena_size = 20
            floor_id = make_arena(arena_size=arena_size,physicsClientId = pid) #capture ID

            #make_rocks(arena_size=arena_size)

            mountain_position = (0, 0, -1)  # Adjust as needed
            mountain_orientation = p.getQuaternionFromEuler((0, 0, 0))
            p.setAdditionalSearchPath('shapes/')
            # mountain = p.loadURDF("mountain.urdf", mountain_position, mountain_orientation, useFixedBase=1)
            # mountain = p.loadURDF("mountain_with_cubes.urdf", mountain_position, mountain_orientation, useFixedBase=1)
            
            mountain_id = p.loadURDF("gaussian_pyramid.urdf", mountain_position, mountain_orientation, useFixedBase=1,physicsClientId = pid) #capture ID



            xml_file = 'temp' + str(self.sim_id) + '.urdf'
            xml_str = cr.to_xml()
            with open(xml_file, 'w') as f:
                f.write(xml_str)

            cid = p.loadURDF(xml_file, physicsClientId = pid)
            #starting position of the creature, change the height of its starting pos
            p.resetBasePositionAndOrientation(cid,[-7,-7,3], [0,0,0,1],physicsClientId = pid)

            #allow time for it to drop and settle
            for _ in range(240): # give it 1 second to fall
                p.stepSimulation(physicsClientId = pid)
             
            #erases the z=3 memory to force the creature to climb again
            start_pos, _ = p.getBasePositionAndOrientation(cid, physicsClientId = pid)
            current_z = start_pos[2]
            cr.max_z = current_z

            for step in range(iterations):
                p.stepSimulation(physicsClientId = pid)
                if step % 24 == 0 :
                    self.update_motors(cid = cid , cr = cr)

                pos,orn = p.getBasePositionAndOrientation(cid, physicsClientId = pid)
                lin_velocity, _ = p.getBaseVelocity(cid, physicsClientId = pid)
            

                #grounding logic
                c_floor = p.getContactPoints(bodyA = cid, bodyB = floor_id, physicsClientId = pid)
                c_mount = p.getContactPoints(bodyA = cid, bodyB = mountain_id, physicsClientId = pid)

                is_grounded = (len(c_floor)>0 or len(c_mount)> 0) # only true when the creature is touching the floor/mountain
                   
                cr.update_position(pos, is_grounded, lin_velocity)
        except Exception as e:
            print(f"Simulation failed:{e}")

class ThreadedMountainSim(simulation.ThreadedSim):
    def __init__(self,pool_size):
        self.sims = [MountainSimulation(i) for i in range (pool_size)]


def run_ga():
    pop_size = 100
    gene_count = 3
    generations = 120
    pool_size = 6

    print(f"Initializing population of {pop_size} creatures")
    pop = population.Population(pop_size=pop_size, gene_count=gene_count)

    sim = ThreadedMountainSim(pool_size=pool_size)

    for iteration in range(generations):
        start_time = time.time()

        sim.eval_population(pop,12000)# 50 seconds


        fits = [cr.get_distance_travelled() for cr in pop.creatures]
        # make the fits positive
        min_fit = min(fits)
        if min_fit<0 : 
            positive_fits = [(f- min_fit) + 0.1 for f in fits]
        else:
            positive_fits = fits
        links = [len(cr.get_expanded_links()) for cr in pop.creatures]
        max_fit = np.max(fits)
        avg_fit = np.mean(fits)

        print(f"Gen {iteration}: Max Fit: {max_fit:.3f}, Avg Fit: {avg_fit:.3f}, Time :{time.time() - start_time:.2f}s")

        elite = None
        for cr in pop.creatures:
            if cr.get_distance_travelled() == max_fit:
                elite = cr
                break


        fit_map = population.Population.get_fitness_map(positive_fits)
        new_creatures=[]

        if elite:
            elite.dist = 0
            elite.start_position = None
            elite.last_position = None
            new_creatures.append(elite)

        while len(new_creatures) < pop_size:
            p1 = pop.creatures[population.Population.select_parent(fit_map)]
            p2 = pop.creatures[population.Population.select_parent(fit_map)]

            dna = genome.Genome.crossover(p1.dna,p2.dna)
            dna = genome.Genome.point_mut(dna, rate=0.25, amount= 0.5)
            dna = genome.Genome.shrink_mut(dna, rate=0.25)
            dna = genome.Genome.grow_mut(dna, rate=0.25)

            cr = creature.Creature(1)
            cr.update_dna(dna)
            new_creatures.append(cr)

        pop.creatures = new_creatures
    if elite:
        genome.Genome.to_csv(elite.dna, 'elite.csv')
        print("Final elite saved to elite.csv")

if __name__ == "__main__":
    run_ga()