import genome
import creature
import pybullet as p
import time
import random

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape,plane_shape)
p.setGravity(0,0,-10)
p.setRealTimeSimulation(1)

#generate random creature
cr = creature.Creature(gene_count=3)
cr.update_position([0,0,0])

with open ('test.urdf', 'w') as f:
    f.write(cr.to_xml())

rob1 = p.loadURDF('test.urdf')
#make sure that the floor does not push the robot up
p.resetBasePositionAndOrientation(rob1,[0,0,3], [0,0,0,1])
step = 0
while True:
    p.stepSimulation()
    step +=1
    if step % 120 == 0:
        motors = cr.get_motors()
        #motors should be one less than number of joints
        assert len(motors) == p.getNumJoints(rob1), "bad motors!"
        for jid in range (p.getNumJoints(rob1)):
            mode = p.VELOCITY_CONTROL
            vel = 5*(random.random() - 0.5)
            p.setJointMotorControl2(rob1,
                                    jid,
                                    controlMode = mode,
                                    targetVelocity = vel)
        pos,orn = p.getBasePositionAndOrientation(rob1)
        cr.update_position(pos)
        print(cr.get_distance_travelled())
    time.sleep(1.0/240)
