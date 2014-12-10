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
        self.total_duration = self.sum_attributes('duration')
        self.total_size = self.sum_attributes('size')
        self.heavier_segment = max(self.segments, key=lambda s: s.bandwidth)
        self.lighter_segment = min(self.segments, key=lambda s: s.bandwidth)

    def sum_attributes(self, attr, i=None):
        if i: return sum([getattr(s, attr) for s in self.segments[i+1:]])
        else: return sum([getattr(s, attr) for s in self.segments])

    def get_remaining_size(self, i):
        return self.sum_attributes('size', i)

    def get_remaining_duration(self, i):
        return self.sum_attributes('duration', i)

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

