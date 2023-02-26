from modeller import *
from modeller.automodel import *
#from modeller import soap_protein_od

env = Environ()
a = AutoModel(env, alnfile='qseq_PHKA2Wild-tseqW3_5z3b.ali',
              knowns='tseqW3_5z3b', sequence='qseq_PHKA2Wild',
              assess_methods=(assess.DOPE,
                              #soap_protein_od.Scorer(),
                              assess.GA341))
a.starting_model = 1
a.ending_model = 5
a.make()
