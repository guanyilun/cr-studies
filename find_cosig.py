from todloop import TODLoop
from todloop.routines import DataLoader
from todloop.cosig import FindCosigs

# initialize TODLoop
loop = TODLoop()

# specify covered tod input list
loop.add_tod_list("inputs/covered_tods.txt")

# load cuts
loop.add_routine(DataLoader(input_dir="outputs/nSig_10/cuts",
                            output_key="cuts"))

# compile coincident signals and save data
loop.add_routine(FindCosigs(input_key="cuts", season='2017',
                            output_dir="outputs/nSig_10/cosigs"))

loop.run(0, 153)
