# Streaming VBR content over a fixed (and constant) bandwidth channel
#
# a VBR fashion leading to different segments having different sizes. If we knew the 
# following data prior to playback at the client - exact size of each segment in the content, 
# exact bandwidth of the channel(assume the bandwidth does not vary with time), duration of 
# content and of each segment - how would we determine a fixed initial buffering delay at the 
# client such that once we start the playback there is no buffering pause. Assume that the client
# has sufficient buffer memory to store the entire content, if required.

from __future__ import division

class Segment(object):
    def __init__(self, size_in_bytes, duration):
        self.size = size_in_bytes # this will vary according to motion between frames
        self.duration = duration
        self.bandwidth = (self.size*8/self.duration)

class Playlist(object):
    def __init__(self, segments):
        self.segments = segments

    def get_total_duration(self):
        return sum([s.duration for s in self.segments])

    def get_total_size(self):
        return sum([s.size for s in self.segments])

    def get_heavier_segment(self):
        return max(self.segments, key=lambda s: s.bandwidth)

    def get_lighter_segment(self):
        return min(self.segments, key=lambda s: s.bandwidth)

    def get_remaining_size(self, i):
        return sum([s.size for s in self.segments[i+1:]])

    def get_remaining_duration(self, i):
        return sum([s.duration for s in self.segments[i+1:]])

    total_duration = property(get_total_duration)
    total_size = property(get_total_size)
    heavier_segment = property(get_heavier_segment)
    lighter_segment = property(get_lighter_segment)

def delta_download_playback(bandwidth, segment):
    time_to_download_segment = (segment.size * 8) / bandwidth
    return segment.duration - time_to_download_segment

def calculate_initial_buffering(bandwidth, playlist):
    '''
    this function is responsible for calculate initial startup delay in order to
    fill the buffer avoiding rebuffers during playback.
    '''
    if (bandwidth) >= playlist.heavier_segment.bandwidth:
        return 0
    elif (bandwidth) <= playlist.lighter_segment.bandwidth:
        return playlist.total_duration

