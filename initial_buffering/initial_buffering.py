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

def delta_download_playback(bandwidth, segment):
    time_to_download_segment = (segment.size * 8) / bandwidth
    return segment.duration - time_to_download_segment

def calculate_initial_buffering_segment(bandwidth, playlist):
    '''
    this function is responsible for calculate initial startup delay in order to
    fill the buffer avoiding rebuffers during playback.
    '''
    initial_spare, remaining_spare, initial_buffering_segment = 0, 0, 0
    for i, segment in enumerate(playlist.segments):
        initial_spare += delta_download_playback(bandwidth, segment)
        for remaining_segment in playlist.segments[i:]:
            remaining_spare += delta_download_playback(bandwidth, remaining_segment)
        if (initial_spare >= 0 and remaining_spare >= 0):
            return initial_buffering_segment
        elif (initial_spare > 0 and initial_spare + remaining_spare >= 0):
            return initial_buffering_segment

        initial_buffering_segment = i

    return initial_buffering_segment

