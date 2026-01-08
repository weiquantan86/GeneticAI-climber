import unittest
import genome 
import numpy as np
from xml.dom.minidom import getDOMImplementation
import os


class GenomeTest(unittest.TestCase):
    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def testRandomGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def testRandomGeneHasValues(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])

    def testRandomGeneLength(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(len(gene),20)

    def testRandomGeneIsNumpyArrays(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(gene),np.ndarray)

    def testRandomGeneExists(self):
        #this means to have 5 genome with 20 genes in each
        data = genome.Genome.get_random_genome(2,5)
        self.assertIsNotNone(data)  

    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec["link-length"]["ind"]], 0) 

    def testGeneToGeneDict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene,spec)
        self.assertIn("link-recurrence",gene_dict)

    def testGenomeToDict(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec),3)
        genome_dicts = genome.Genome.get_genome_dict(dna,spec)
        self.assertEqual(len(genome_dicts),3)

    def testFlatLinks(self):
        links =[
            genome.URDFLink(name="A", parent_name = None, recur = 1),
            genome.URDFLink(name="B", parent_name = "A", recur = 1),
            genome.URDFLink(name="C", parent_name = "B", recur = 2),
            genome.URDFLink(name="D", parent_name = "C", recur = 1)
        ]
        self.assertIsNotNone(links)

    def testExpandLinks1(self):
        links =[
            genome.URDFLink(name="A", parent_name = None, recur = 1),
            genome.URDFLink(name="B", parent_name = "A", recur = 2),      
        ]
        exp_links = [links[0]] # start from A as it has no parents
        genome.Genome.expandLinks(links[0],links[0].name,links,exp_links)
        self.assertEqual(len(exp_links),3)

    def testExpandLinks2(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1),
        ]
        exp_links=[links[0]]
        genome.Genome.expandLinks(links[0],links[0].name,links,exp_links)
        names = [l.name + "-parent-is-" + l.parent_name for l in exp_links]
        #print(names)
        self.assertEqual(len(exp_links),6)

    def testGetLinks(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec),3) 
        gdicts = genome.Genome.get_genome_dict(dna,spec)
        links = genome.Genome.genome_to_links(gdicts)
        self.assertEqual(len(links),3)

    def testGetLinksUniqueNames(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec),3)
        gdicts = genome.Genome.get_genome_dict(dna,spec)
        links = genome.Genome.genome_to_links(gdicts)
        for l in links:
            names = [link.name for link in links
                    if link.name == l.name]
            self.assertEqual(len(names),1)

    # def testLinkToXML(self):
    #     link = genome.URDFLink(name="A", parent_name = None, recur = 1)
    #     domimpl = getDOMImplementation()
    #     adom = domimpl.createDocument(None,"robot",None)
    #     xml_str = link.to_link_element(link,adom)
    #     print(xml_str)
    #     self.assertIsNotNone(xml_str)

    def testCrossover(self):
        g1 = np.array([[1,2,3],[4,5,6]])
        g2 = np.array([[7,8,9],[10,11,12]])
        for i in range(10):
            g3 = genome.Genome.crossover(g1,g2)
            #print(g1,g2,g3)
            self.assertGreater(len(g3),0)

    def test_point(self):
        #this sometimes fails because the random number is > rate
        # hence no mutations occur, 100% pass rate when rate=1
        g1 = np.array([[1.0],[2.0],[3.0]])
        #print(g1)
        g2 = genome.Genome.point_mut(g1,rate=1.0,amount=0.25)
        #print(g2)
        self.assertFalse(np.array_equal(g1,g2))

    def test_shrink(self):
        g1 = np.array([[1.0],[2.0]])
        g2 = genome.Genome.shrink_mut(g1,rate=1.0)
        #print(g1,g2)
        self.assertEqual(len(g2),1)

    def test_shrink2(self):
        g1 = np.array([[1.0],[2.0]])
        g2 = genome.Genome.shrink_mut(g1,rate=0.0)
        self.assertEqual(len(g2),2)

    def test_shrink3(self):
        g1 = np.array([[1.0]])
        g2 = genome.Genome.shrink_mut(g1,rate=1.0)
        self.assertEqual(len(g2),1)

    def test_grow1(self):
        g1 = np.array([[1.0],[2.0]])
        g2 = genome.Genome.grow_mut(g1,rate=1)
        self.assertGreater(len(g2),len(g1))


    def test_grow2(self):
        g1 = np.array([[1.0],[2.0]])
        g2 = genome.Genome.grow_mut(g1,rate=0)
        self.assertEqual(len(g2),len(g1))

    def test_tocsv(self):
        g1=[[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        self.assertTrue(os.path.exists('test.csv'))

    def test_tocsv_content(self):
        g1= [[1,2,3]]
        genome.Genome.to_csv(g1,'test.csv')
        expect = "1,2,3,\n"
        with open("test.csv") as f:
            csv_str = f.read()
        self.assertEqual(csv_str,expect)

    def test_tocsv_content2(self):
        g1= [[1,2,3],[4,5,6]]
        genome.Genome.to_csv(g1,'test.csv')
        expect = "1,2,3,\n4,5,6,\n"
        with open("test.csv") as f:
            csv_str = f.read()
        self.assertEqual(csv_str,expect)

    def test_from_csv(self):
        g1 =[[1,2,3]]
        genome.Genome.to_csv(g1,'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        self.assertTrue(np.array_equal(g1,g2))

    def test_from_csv2(self):
        g1 =[[1,2,3],[4,5,6]]
        genome.Genome.to_csv(g1,'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        self.assertTrue(np.array_equal(g1,g2))

unittest.main()
