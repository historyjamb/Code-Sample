from modeller import *

env = Environ()
aln = Alignment(env)
for (pdb, chain) in (('tseqW1_5z3d', 'A'), ('tseqW2_7c25', 'A'), ('tseqW3_5z3b', 'A'),
                     ('tseqW4_5z3e', 'A'), ('tseqW5_5z3a', 'A')):
    m = Model(env, file=pdb, model_segment=('FIRST:'+chain, 'LAST:'+chain))
    aln.append_model(m, atom_files=pdb, align_codes=pdb+chain)
aln.malign()
aln.malign3d()
aln.compare_structures()
aln.id_table(matrix_file='family.mat')
env.dendrogram(matrix_file='family.mat', cluster_cut=-1.0)