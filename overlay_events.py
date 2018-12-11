from todloop import TODLoop
from todloop.routines import DataLoader, SaveData
from todloop.cosig import FindEvents
from todloop.tod import TODLoader, FixOpticalSign
from routines import OverlayEvents

# list of events of interests
"""
list_of_events = [
    '0.119219',
    '1.235519'
    '19.49929',
    '20.19719',
    '23.78711',
    '27.32707',
    '31.185497',
    '37.124258',
    '37.172260',
    '38.3350',
    '38.30026',
    '39.28740',
    '49.110103'
]
"""
# read list of events from file
with open('list_of_events.txt', 'r') as f:
    data = f.readlines()

# clean events
list_of_events = [d[:-1] for d in data]

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
loop.add_routine(OverlayEvents(event_key="events", tod_key="tod_data",
                               list_of_events=list_of_events,
                               output_path='test.png'))

# loop.run(0, 153)
# loop.run(0, 50)
loop.run(0, 15)
