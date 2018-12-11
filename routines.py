import matplotlib.pyplot as plt
import numpy as np
from todloop import Routine
from todloop.utils.pixels import PixelReader
from todloop.utils.events import timeseries
from scipy.interpolate import interp1d


class PlotEvents(Routine):
    """A routine that plot events"""
    def __init__(self, event_key, tod_key):
        Routine.__init__(self)
        self._event_key = event_key
        self._tod_key = tod_key

    def execute(self, store):
        array= self.get_array()
        pr = PixelReader(season='2017', array= array)
        self.logger.info('Plotting glitches ...')

        # retrieve tod_data
        tod_data = store.get(self._tod_key)  

        # retrieve events
        events_data = store.get(self._event_key)  
        events = events_data['events']
        nsamps = events_data['nsamps']
        
        # plot functions
        # plot all pixels affected given an array of pixel ids
        # and a starting time and ending time
        plt.figure(figsize=(8,8))

        def plotter(ax, pixels, start_time, end_time):
            for pid in pixels:
                ctime, d1, d2, d3, d4 = timeseries(tod_data, pid, start_time, end_time, pr)
                ax.set_title('Pixels affected from ' +str(start_time)+ '-' + str(end_time)+ ' at 90 GHz')
                ax.set_xlabel('TOD_ID: %d    TOD_NAME: %s' % (self.get_id(), self.get_name()))  # CHANGE TOD TRACK NAME
                ax.plot(d1,'.-')
                ax.plot(d2,'.-')
                ax.plot(d3,'.-')
                ax.plot(d4,'.-')

        # trim the beginning and ending glitches, these are usually related to
        # re-biasing and not interesting
        TRIM = 100
        events_trim = [e for e in events if (e['start'] > TRIM and e['end'] < nsamps-TRIM)]
        self.logger.info('nsamps: %d' % nsamps)

        # plot all pixels affected in a event one by one for all events
        for event in events_trim:
            self.logger.info(event)
            pixels_affected = event['pixels_affected']
            start_time = event['start']
            end_time = event['end']
            fig, ax = plt.subplots()
            plotter(ax, pixels_affected, start_time, end_time)
            fig.savefig("outputs/nSig_10/plots/%s.png" % event['id'])
            plt.close('all')


class OverlayEvents(Routine):
    def __init__(self, event_key, tod_key, list_of_events,
                 output_path):
        """This routine takes in a list of events (ids) and over lay them on
        top of each other. The program will loop through events stored
        in each pickle file and filter out the events specified. These
        events are them scaled to 0 and 1 and plotted in an overlaying
        plot to visualize the difference in time decay profile.

        Args:
            event_key (str): a key to retrieve events in data store
            tod_key (str): a key to retrieve tod data in data store
            list_of_events (list): a list of event ids to overlay
            output_path (str): the path to output the figure

        """
        Routine.__init__(self)
        self._list_of_events = list_of_events
        self._event_key = event_key
        self._tod_key = tod_key
        self._output_path = output_path
        self._ax = None
        self._fig = None
        

    def initialize(self):
        self._fig, self._ax = plt.subplots(figsize=(8,8))

    def execute(self, store):
        # get pixel reader
        pr = PixelReader(season='2017', array=self.get_array())

        # retrieve events data from data store
        events_data = store.get(self._event_key)
        events = events_data['events']
        nsamps = events_data['nsamps']

        # retrieve tod data
        tod_data = store.get(self._tod_key)

        # loop through the given event id and see if it is in the
        # retrieved events list.
        for event in events:
            # check if the event is of interests
            if event['id'] in self._list_of_events:
                self.logger.info('Found event: %s' % event['id'])
                # retrieve event information
                # pick only one pixel for plotting
                pixels = event['pixels_affected']
                start_time = event['start']
                end_time = event['end']

                # loop over pixels
                for pid in pixels:
                    # get time series
                    ctime, d1, d2, d3, d4 = timeseries(tod_data, pid,
                                                       start_time,
                                                       end_time, pr,
                                                       buffer=20)

                    for d in [d1, d2, d3, d4]:
                        # rescale them
                        d = (d - np.min(d)) / (np.max(d) - np.min(d))

                        # find maximum index
                        d_i = np.argmax(d)

                        # only start from maximum
                        d_y = d[d_i:]
                        d_x = np.arange(0, len(d_y))

                        # make a smooth curve
                        f = interp1d(d_x, d_y, kind='cubic')
                        d_x_new = np.linspace(0, len(d_y)-1, 100)
                        self._ax.plot(d_x_new, f(d_x_new), 'r-', alpha=0.1)

    def finalize(self):
        self._fig.savefig(self._output_path)
        

