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

def test_playlist_should_have_total_duration():
    segment_1 = Segment(123000, 5)
    segment_2 = Segment(402000, 10)
    playlist = Playlist([segment_1, segment_2])
    assert playlist.total_duration == 15

def test_playlist_should_have_total_size_in_bytes():
    segment_1 = Segment(30, 1)
    segment_2 = Segment(20, 1)
    segment_3 = Segment(10, 1)
    playlist = Playlist([segment_1, segment_2, segment_3])
    assert playlist.total_size == 60

