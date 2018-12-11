from todloop import TODLoop
from todloop.routines import DataLoader, SaveData
from todloop.cosig import FindEvents


# initialize TODLoop
loop = TODLoop()

# specify covered tod input list
loop.add_tod_list("inputs/covered_tods.txt")

# load cosigs
loop.add_routine(DataLoader(input_dir="outputs/nSig_10/cosigs",
                            output_key="cosig"))

# compile coincident signals and save data
loop.add_routine(FindEvents(input_key="cosig", output_key="events"))

# save data
loop.add_routine(SaveData(input_key="events", output_dir="outputs/nSig_10/events"))

loop.run(0, 153)
