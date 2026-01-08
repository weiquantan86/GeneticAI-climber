import numpy as np
import copy
from xml.dom.minidom import getDOMImplementation
import random


class Genome():
    def __init__(self):
        pass

    @staticmethod
    def get_random_gene(length):
        gene = np.array([np.random.random() for i in range(length)])
        return gene
    
    @staticmethod
    #genome is a list of genes
    def get_random_genome(gene_length,gene_count):
        genome = [Genome.get_random_gene(gene_length) for i in range(gene_count)]
        return genome
    
    @staticmethod
    #convert the randomly generated genes
    #into the parameters of the specs
    #so each number have a meaning
    def get_gene_spec():
        gene_spec = {
            #all these can be changed as its parameters
            "link-shape":{"scale":1},
            "link-length":{"scale":1},
            "link-radius":{"scale":0.25},
            "link-recurrence":{"scale":1},
            "link-mass":{"scale":1},
            "joint-type":{"scale":1},
            "joint-parent":{"scale":1},
            "joint-axis-xyz":{"scale":1},
            #rpy is the rotation hence it is in radians
            "joint-origin-rpy-1":{"scale":0.5},
            "joint-origin-rpy-2":{"scale":0.5},
            "joint-origin-rpy-3":{"scale":np.pi},
            "joint-origin-xyz-1":{"scale":0.5},
            "joint-origin-xyz-2":{"scale":0.5},
            "joint-origin-xyz-3":{"scale":0.1},
            #this is for the motors
            "control-waveform":{"scale":1},
            "control-amp":{"scale":1.5},
            "control-freq":{"scale":1}   
        }
        #adding indexes to each specification
        #i assume is to make it into a readable
        #dictionary more easily
        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"] = ind
            ind = ind+1
        return gene_spec
    
    @staticmethod
    #convert the gene to gene dict
    def get_gene_dict(gene,spec):
        gene_dict = {}
        for key in spec:
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gene_dict[key] = gene[ind] * scale
                

        return gene_dict

    @staticmethod
    def get_genome_dict(genome, spec):
        #it is a list of genomes 
        #made out of gene dictionaries
        #naming is abit weird
        genome_dict=[]
        for gene in genome:
            genome_dict.append(Genome.get_gene_dict(gene,spec))
        return genome_dict
    
    @staticmethod
    def expandLinks(parent_link, uniq_parent_name, flat_links, exp_links):
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        sibling_ind = 1
        for c in children:
            for r in range (int(c.recur)):
                sibling_ind = sibling_ind + 1
                c_copy = copy.copy(c)
                c_copy.parent_name = uniq_parent_name
                uniq_name = c_copy.name + str(len(exp_links))
                c_copy.name = uniq_name
                c_copy.sibling_ind = sibling_ind
                exp_links.append(c_copy)
                Genome.expandLinks(c,uniq_name,flat_links,exp_links)

    @staticmethod
    def genome_to_links(gdicts):
        links = []
        link_ind = 0
        parent_names = [str(link_ind)]
        for gdict in gdicts:
            link_name = str(link_ind)
            #fixing index error
            raw_ind = int(gdict["joint-parent"] * len(parent_names))
            #use modulo to wrap index
            parent_ind = raw_ind % len(parent_names)
            parent_name = parent_names[int(parent_ind)]
            recur = gdict["link-recurrence"]
            link = URDFLink(name=link_name,
                            parent_name = parent_name,
                            recur = recur+1,
                            link_length=gdict["link-length"],
                            link_radius=gdict["link-radius"],
                            link_mass=gdict["link-mass"],
                            joint_type = gdict["joint-type"],
                            joint_parent = gdict["joint-parent"],
                            joint_axis_xyz = gdict["joint-axis-xyz"],
                            joint_origin_rpy_1 = gdict["joint-origin-rpy-1"],
                            joint_origin_rpy_2 = gdict["joint-origin-rpy-2"],
                            joint_origin_rpy_3 = gdict["joint-origin-rpy-3"],
                            joint_origin_xyz_1 = gdict["joint-origin-xyz-1"],
                            joint_origin_xyz_2 = gdict["joint-origin-xyz-2"],
                            joint_origin_xyz_3 = gdict["joint-origin-xyz-3"],
                            control_waveform = gdict["control-waveform"],
                            control_amp = gdict["control-amp"],
                            control_freq = gdict["control-freq"])
            
            links.append(link)
            if link_ind !=0:
                parent_names.append(link_name)
            link_ind = link_ind+1

        links[0].parent_name="None"
        return links

    #mutating the genes        
    @staticmethod
    def crossover(g1,g2):
        
        x1 = random.randint(0,len(g1)-1)
        x2 = random.randint(0,len(g2)-1)
        g3 = np.concatenate((g1[x1:],g2[x2:]))
        if len(g3) > len(g1):
            g3 = g3[0:len(g1)]
        return g3

    #point mutation
    @staticmethod
    def point_mut(genome, rate, amount):
        new_genome = copy.deepcopy(genome)
        for gene in new_genome:
            if np.random.rand() < rate:
                ind = np.random.randint(len(gene))
                r = (np.random.rand() - 0.5) * amount
                gene[ind] = gene[ind] + r
        return new_genome
    
    #shrink mutation
    @staticmethod
    def shrink_mut(genes, rate):
        if np.random.rand()<rate:
            #only remove if there is more than 1 gene
            if len(genes) > 1:
                ind = np.random.randint(len(genes))
                genes = np.delete(genes,ind,0)
        return genes

    #grow mutation
    @staticmethod
    def grow_mut(genes,rate):
        if np.random.rand() < rate :
            gene = Genome.get_random_gene(len(genes[0]))
            genes = np.append(genes, [gene], 0)
        return genes

    #convert to csv
    @staticmethod
    def to_csv(dna, csv_file):
        csv_str = ""
        for gene in dna:
            for val in gene:
                csv_str = csv_str + str(val) + ","
            csv_str = csv_str + '\n'
        with open (csv_file, 'w') as f:
            f.write(csv_str)

    #read back from the csv
    @staticmethod
    def from_csv(filename):
        csv_str = ''
        with open (filename) as f:
            csv_str = f.read()
        dna = []
        lines = csv_str.split('\n')
        for line in lines:
            vals = line.split(',')
            gene = [float(v) for v in vals if v!='']
            if len(gene) > 0:
                dna.append(gene)
        return dna



class URDFLink:
    def __init__(self,name,parent_name,recur,
                 link_length=0.1 ,
                 link_radius=0.1,
                 link_mass=0.1,
                 joint_type=0.1,
                 joint_parent=0.1,
                 joint_axis_xyz=0.1,
                 joint_origin_rpy_1=0.1,
                 joint_origin_rpy_2=0.1,
                 joint_origin_rpy_3=0.1,
                 joint_origin_xyz_1=0.1,
                 joint_origin_xyz_2=0.1,
                 joint_origin_xyz_3=0.1,
                 control_waveform=0.1,
                 control_amp=0.1,
                 control_freq=0.1
                 ):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur
        self.link_length = link_length
        self.link_radius = link_radius
        self.link_mass = link_mass
        self.joint_type = joint_type
        self.joint_parent = joint_parent
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3
        self.joint_origin_xyz_1 = joint_origin_xyz_1
        self.joint_origin_xyz_2 = joint_origin_xyz_2
        self.joint_origin_xyz_3 = joint_origin_xyz_3
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq

        self.sibling_ind = 1

    
    def to_link_element(self,adom):
        #refer to toXML video minute 15:
        #creating the objects
        link_tag = adom.createElement("link")
        link_tag.setAttribute("name",self.name)
        vis_tag = adom.createElement("visual")
        geom_tag = adom.createElement("geometry")
        cyl_tag = adom.createElement("cylinder")
        cyl_tag.setAttribute("length", str(self.link_length))
        cyl_tag.setAttribute("radius", str(self.link_radius))

        geom_tag.appendChild(cyl_tag)
        vis_tag.appendChild(geom_tag)

        #creating the collision for the objects
        coll_tag = adom.createElement("collision")
        c_geom_tag = adom.createElement("geometry")
        c_cyl_tag = adom.createElement("cylinder")
        c_cyl_tag.setAttribute("length",str(self.link_length))
        c_cyl_tag.setAttribute("radius",str(self.link_radius))

        c_geom_tag.appendChild(c_cyl_tag)
        coll_tag.appendChild(c_geom_tag)

        #creating the inertias
        inertial_tag = adom.createElement("inertial")
        mass_tag = adom.createElement("mass")
        mass = np.pi * (self.link_radius * self.link_radius) * self.link_length
        mass_tag.setAttribute("value",str(mass))
        inertia_tag = adom.createElement("inertia")
        inertia_tag.setAttribute("ixx","0.03")
        inertia_tag.setAttribute("iyy","0.03")
        inertia_tag.setAttribute("izz","0.03")
        inertia_tag.setAttribute("ixy","0")
        inertia_tag.setAttribute("ixz","0")
        inertia_tag.setAttribute("iyx","0")

        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)
        
        link_tag.appendChild(vis_tag)
        link_tag.appendChild(coll_tag)
        link_tag.appendChild(inertial_tag)
        
        return link_tag
    
    def to_joint_element(self,adom):
        joint_tag = adom.createElement("joint")
        joint_tag.setAttribute("name",self.name + "_to_" + self.parent_name)
        if self.joint_type >=0.5 :
            joint_tag.setAttribute("type","revolute")
        else:
            joint_tag.setAttribute("type","fixed")
        parent_tag = adom.createElement("parent")
        parent_tag.setAttribute("link",self.parent_name)
        child_tag = adom.createElement("child")
        child_tag.setAttribute("link",self.name)
        axis_tag = adom.createElement("axis")
        if self.joint_axis_xyz <= 0.33:
            axis_tag.setAttribute("xyz","1 0 0")
        if self.joint_axis_xyz > 0.33 and self.joint_axis_xyz <= 0.66:
            axis_tag.setAttribute("xyz", "0 1 0")
        if self.joint_axis_xyz > 0.66:
            axis_tag.setAttribute("xyz", "0 0 1")
        
        limit_tag = adom.createElement("limit")
        limit_tag.setAttribute("effort","1")
        limit_tag.setAttribute("upper","0")
        limit_tag.setAttribute("lower","1")
        limit_tag.setAttribute("velocity","1")

        orig_tag = adom.createElement("origin")

        rpy1 = self.joint_origin_rpy_1 * self.sibling_ind

        rpy = str(rpy1) + " " + str(self.joint_origin_rpy_2) + " " + str(self.joint_origin_rpy_3)
        orig_tag.setAttribute("rpy",rpy)
        xyz = str(self.joint_origin_xyz_1) + " " + str(self.joint_origin_xyz_2) + " " + str(self.joint_origin_xyz_3)
        orig_tag.setAttribute("xyz", xyz)

        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(orig_tag)
        return joint_tag