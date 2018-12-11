import matplotlib
matplotlib.use("TKAgg")
from todloop import TODLoop
from todloop.routines import DataLoader, SaveData
from todloop.cosig import FindEvents
from todloop.tod import TODLoader, FixOpticalSign
from routines import PlotEvents

# initialize TODLoop
loop = TODLoop()

# specify covered tod input list
loop.add_tod_list("inputs/covered_tods.txt")

# load TOD 
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
# load events
loop.add_routine(DataLoader(input_dir="outputs/nSig_10/events",
                            output_key="events"))

# plot events 
loop.add_routine(PlotEvents(event_key="events", tod_key="tod_data"))


loop.run(91, 153)
