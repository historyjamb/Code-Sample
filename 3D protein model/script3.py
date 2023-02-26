from modeller import *

env = Environ()
aln = Alignment(env)
mdl = Model(env, file='tseqW3_5z3b', model_segment=('FIRST:A','LAST:A'))
aln.append_model(mdl, align_codes='tseqW3_5z3b', atom_files='tseqW3_5z3b.pdb')
aln.append(file='qseq_PHKA2Wild.ali', align_codes='qseq_PHKA2Wild')
aln.align2d(max_gap_length=50)
aln.write(file='qseq_PHKA2Wild-tseqW3_5z3b.ali', alignment_format='PIR')
aln.write(file='qseq_PHKA2Wild-tseqW3_5z3b.pap', alignment_format='PAP')