from todloop import TODLoop
from todloop.routines import DataLoader
from todloop.tod import TODLoader
from todloop.cuts import CompileCuts, CleanTOD

# initialize TODLoop
loop = TODLoop()

# specify covered tod input list
loop.add_tod_list("inputs/covered_tods.txt")

# load tod data
loop.add_routine(TODLoader(output_key="tod_data"))

# clean tod
loop.add_routine(CleanTOD(tod_key="tod_data", output_key="tod_data"))

# define glitch parameters
glitchp = {
    'nSig': 10, 
    'tGlitch' : 0.007, 
    'minSeparation': 30, 
    'maxGlitch': 50000, 
    'highPassFc': 6.0, 
    'buffer': 0
}

# compile cuts
loop.add_routine(CompileCuts(input_key="tod_data", glitchp=glitchp, output_dir="outputs/covered_tods/cuts__nSig_10"))

loop.run(0, 153)
