# You have a HLS stream with content at just 1 bitrate. This content has been encoded in
# a VBR fashion leading to different segments having different sizes. If we knew the 
# following data prior to playback at the client - exact size of each segment in the content, 
# exact bandwidth of the channel(assume the bandwidth does not vary with time), duration of 
# content and of each segment - how would we determine a fixed initial buffering delay at the 
# client such that once we start the playback there is no buffering pause. Assume that the client
# has sufficient buffer memory to store the entire content, if required.

class Segment(object):
    def __init__(self, size_in_bytes, duration):
        self.size = size_in_bytes # this will vary according to motion between frames
        self.duration = duration

class Playlist(object):
    def __init__(self, segments):
        self.segments = segments

    def get_total_duration(self):
        return sum([s.duration for s in self.segments])

    def get_total_size(self):
        return sum([s.size for s in self.segments])

    total_duration = property(get_total_duration)
    total_size = property(get_total_size)


