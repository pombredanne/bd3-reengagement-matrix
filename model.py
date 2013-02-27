from collections import Counter
from itertools import chain
from datetime import datetime
import math

from bitdeli.model import model

@model
def model(profiles):
    
    def months(events):
        for hour, count in chain.from_iterable(events.itervalues()):
            yield datetime.utcfromtimestamp(hour * 3600).strftime('%Y-%m')
    
    for profile in profiles:
        for month, count in Counter(months(profile['events'])).iteritems():
            bin = min(int(math.log(count, 2)), 3) + 1
            yield '%s:%s' % (month, bin), profile.uid