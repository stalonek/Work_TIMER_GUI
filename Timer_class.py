import time
import sqlite3
import logging
import sys
from datetime import datetime

class Timer:
    """ Class for time counting management"""

    def __init__(self):
        self.start_time = None
        self.pause_start_time = None
        self.paused_time = 0
        self.is_paused = False
        self.current_time = None



    def get_formatted_time(self, elapsed_time):
        """Formatting time """

        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{int(hours):0>2}:{int(minutes):0>2}:{seconds:05.2f}"


    def get_date(self):
        """ Return current date value"""
        self.current_date = datetime.now()
        formatted_date = self.current_date.strftime("%d-%m-%Y")
        return formatted_date

    logging.info('Date has been retrieved')

    def start(self):
        """Start counter"""

        self.start_time = time.time()
        self.is_paused = False
        logging.info('Timer started')
        

    def print_current_time(self):
        """Print current time in each of the needed functiion"""

        self.current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"Time of current action: {self.current_time}")


    def stop(self):
        """Stop counter"""

        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.start_time = None
            logging.info("Timer stopped")
            print(f'Timer stopped: elapsed time is {self.get_formatted_time(elapsed_time)}')
            return self.get_formatted_time(elapsed_time)

    def pause(self):
        """Pause counter"""
        if self.start_time is not None and not self.is_paused:
            self.pause_start_time = time.time()
            self.is_paused = True
            elapsed_time = self.pause_start_time - self.start_time - self.paused_time
            print('Time paused')
            return self.get_formatted_time(elapsed_time)

    def resume(self):
        """Resume pause"""
        if self.is_paused:
            self.paused_time += time.time() - self.pause_start_time
            self.is_paused = False
            pause_duration = time.time() - self.pause_start_time
            print('Timer resumed')
            return self.get_formatted_time(pause_duration)



    def get_time(self):
        """ Returns current timer value"""

        if self.start_time is not None:
            if self.is_paused:
                return self.get_formatted_time(self.paused_time)
            else:
                return self.get_formatted_time(time.time()-self.start_time)
        else:
            logging.error('Timer was not started')