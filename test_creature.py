import unittest
import creature
import pybullet as p

class TestCreature(unittest.TestCase):
    def testCreatureExists(self):
        self.assertIsNotNone(creature.Creature)

    def testCreatureGetFlatLinks(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        self.assertEqual(len(links),4)

    def testExpLinks(self):
        c = creature.Creature(gene_count=25)
        links = c.get_flat_links()
        exp_links = c.get_expanded_links()
        print(len(exp_links))
        print(len(links))
        self.assertGreaterEqual(len(exp_links),len(links))

    def testLoadXML(self):
        c = creature.Creature(gene_count=2)
        links = c.get_flat_links()
        expanded = c.get_expanded_links()
        
        xml_str = c.to_xml()
        
        with open ('test.urdf','w') as f:
            f.write(xml_str)
        p.connect(p.DIRECT)
        cid = p.loadURDF('test.urdf')
        self.assertIsNotNone(cid)


    def testMotor(self):
        m = creature.Motor(0.1,0.5,0.5)
        self.assertIsNotNone(m)

    def testMotorVal(self):
        m = creature.Motor(0.1,0.5,0.5)
        self.assertEqual(m.get_output(),1)

    def testMotorVal2(self):
        m = creature.Motor(0.6,0.5,0.5)
        m.get_output()
        m.get_output()
        self.assertGreater(m.get_output(),0)

unittest.main()