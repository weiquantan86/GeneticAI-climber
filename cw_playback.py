import pybullet as p
import time
import numpy as np
import os

# Import your modules
import genome
import creature
import cw_envt

def playback(csv_file):
    # 1. Setup Visual Environment
    p.connect(p.GUI) # GUI mode so you can see it
    p.setPhysicsEngineParameter(enableFileCaching=0)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0) # Turn off sidebars
    p.setGravity(0, 0, -10)
    arena_size = 20
    cw_envt.make_arena(arena_size=arena_size)
    mountain_position = (0, 0, -1)  # Adjust as needed
    mountain_orientation = p.getQuaternionFromEuler((0, 0, 0))
            
    p.setAdditionalSearchPath('shapes/')
    mountain = p.loadURDF("gaussian_pyramid.urdf", mountain_position, mountain_orientation, useFixedBase=1)

    

    # 3. Load the Creature Genome
    print(f"Loading genome from: {csv_file}")
    if not os.path.exists(csv_file):
        print(f"ERROR: File {csv_file} not found! Did you run cw-envt.py?")
        return

    dna = genome.Genome.from_csv(csv_file)
    cr = creature.Creature(gene_count=1) # Gene count doesn't matter here, DNA overwrites it
    cr.update_dna(dna)
    
    # 4. Save & Load Creature URDF
    xml_filename = 'temp_playback.urdf'
    with open(xml_filename, 'w') as f:
        f.write(cr.to_xml())
    
    # Drop creature from a safe height (z=3) and away from the mountain
    rob1 = p.loadURDF(xml_filename, [-7, -7, 3]) 
    
    # 5. Simulation Loop
    while True:
        p.stepSimulation()
        time.sleep(1.0/240.0) # Slow down to real-time (240Hz)
        
        # Update Motors
        motors = cr.get_motors()
        for jid in range(p.getNumJoints(rob1)):
            m = motors[jid]
            p.setJointMotorControl2(rob1, jid, 
                                    controlMode=p.VELOCITY_CONTROL, 
                                    targetVelocity=m.get_output(), 
                                    force=500.0)
        
        # Camera Tracking (Optional - Follows the robot)
        pos, orn = p.getBasePositionAndOrientation(rob1)
        p.resetDebugVisualizerCamera(cameraDistance=10, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=pos)
        
        cr.update_position(pos)
        # Optional: Print distance
        print(f"Distance: {cr.get_distance_travelled()}")

if __name__ == "__main__":
    # CHANGE THIS to the generation you want to watch (e.g., 'elite_19.csv')
    csv_file_to_watch = 'best.csv' 
    
    playback(csv_file_to_watch)