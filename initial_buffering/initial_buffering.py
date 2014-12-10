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

class Playlist(object):
    def __init__(self, segments):
        self.segments = segments

def calculate_download_time(bandwidth, segment):
    return (segment.size * 8) / bandwidth

def calculate_initial_segment(bandwidth, playlist):
    '''
    calculate initial startup segment in order to fill the buffer avoiding
    rebuffers during playback.
    '''
    initial_delta, remaining_delta, initial_segment = 0, 0, 0 
    for i, segment in enumerate(playlist.segments):
        download_time = calculate_download_time(bandwidth, segment)
        initial_delta += (segment.duration - download_time)

        for remaining_segment in playlist.segments[i:]:
            download_time = calculate_download_time(bandwidth, remaining_segment)
            remaining_delta += (remaining_segment.duration - download_time)

        if (initial_delta > 0 and initial_delta + remaining_delta >= 0):
            return initial_segment

        initial_segment = i

    return initial_segment

def calculate_startup_buffer(bandwidth, playlist):
    '''
    returns the amount in seconds that the user will need to wait until 
    playback starts
    '''
    segment = calculate_initial_segment(bandwidth, playlist)
    preload_amount_size = sum([s.size for s in playlist.segments[:segment]])
    return (preload_amount_size * 8 / bandwidth)

