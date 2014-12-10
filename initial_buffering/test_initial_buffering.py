# unit tests for initial_buffering.py

from initial_buffering import *

def test_segment_should_store_size_and_duration():
    segment = Segment(123000, 5)
    assert segment.duration == 5
    assert segment.size == 123000

def test_playlist_should_store_segments():
    segment_1 = Segment(123000, 5)
    segment_2 = Segment(102000, 5)
    playlist = Playlist([segment_1, segment_2])
    assert len(playlist.segments) == 2
    assert playlist.segments[0] == segment_1
    assert playlist.segments[1] == segment_2


