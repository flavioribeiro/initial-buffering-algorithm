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

def test_initial_segment():
    segment_1 = Segment(1000, 5) #1600bps
    segment_2 = Segment(1150, 5) #1840bps
    segment_3 = Segment(1200, 5) #1920bps
    segment_4 = Segment(1100, 5) #1760bps
    playlist = Playlist([segment_1, segment_2, segment_3, segment_4])
    assert calculate_initial_segment(1600, playlist) == 3
    assert calculate_initial_segment(1920, playlist) == 0
    assert calculate_initial_segment(1800, playlist) == 0

def test_initial_segment_bigger_playlist():
    segment_1 = Segment(1200, 5) #1920bps
    segment_2 = Segment(1150, 5) #1840bps
    segment_3 = Segment(1100, 5) #1760bps
    segment_4 = Segment(1000, 5) #1600bps
    segment_5 = Segment(800, 5) #1280bps
    segment_6 = Segment(600, 5) #960bps
    segment_7 = Segment(300, 5) #480bps
    playlist = Playlist([segment_1, segment_2, segment_3, segment_4, segment_5, segment_6, segment_7])
    assert calculate_initial_segment(1920, playlist) == 0
    assert calculate_initial_segment(1840, playlist) == 2
    assert calculate_initial_segment(1600, playlist) == 4
    assert calculate_initial_segment(600, playlist) == 6

def test_calculate_download_time():
    # no matter the duration of segment on this case :)
    segment_1 = Segment(1000, 4)
    segment_2 = Segment(1000, 8)
    segment_3 = Segment(1000, 12)
    bandwidth = 1000
    assert calculate_download_time(bandwidth, segment_1) == 8
    assert calculate_download_time(bandwidth, segment_2) == 8
    assert calculate_download_time(bandwidth, segment_3) == 8
