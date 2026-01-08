import pybullet as p
import time
p.connect(p.GUI)

p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape,plane_shape)
p.setGravity(0,0,-10)
