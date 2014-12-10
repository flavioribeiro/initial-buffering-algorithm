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

def test_playlist_should_get_heavier_segment():
    segment_1 = Segment(30, 6)
    segment_2 = Segment(20, 5)
    segment_3 = Segment(100, 1)
    playlist = Playlist([segment_1, segment_2, segment_3])
    assert playlist.heavier_segment == segment_3

def test_playlist_should_get_lighter_segment():
    segment_1 = Segment(30, 6)
    segment_2 = Segment(20, 5)
    segment_3 = Segment(100, 1)
    playlist = Playlist([segment_1, segment_2, segment_3])
    assert playlist.lighter_segment == segment_2

def test_initial_buffering_for_bandwidth_greater_than_heavier_segment_should_be_zero():
    segment_1 = Segment(124, 1)
    playlist = Playlist([segment_1])
    assert calculate_initial_buffering(1000, playlist) == 0

def test_initial_buffering_for_bandwidth_smaller_than_lighter_segment_should_be_entire_playlist():
    segment_1 = Segment(10000000, 10)
    playlist = Playlist([segment_1])
    assert calculate_initial_buffering(1000, playlist) == 10

def test_initial_buffering_time():
    segment_1 = Segment(1000, 5)
    segment_2 = Segment(1150, 5)
    segment_3 = Segment(1200, 5)
    segment_4 = Segment(1100, 5)
    playlist = Playlist([segment_1, segment_2, segment_3, segment_4])
    assert calculate_initial_buffering(1600, playlist) == 20
    assert calculate_initial_buffering(1920, playlist) == 0

def test_delta_download_playback_should_return_the_difference_between_download_and_playback():
    segment_1 = Segment(1000, 4)
    segment_2 = Segment(1000, 8)
    segment_3 = Segment(1000, 12)
    bandwidth = 1000
    assert delta_download_playback(bandwidth, segment_1) == -4
    assert delta_download_playback(bandwidth, segment_2) == 0
    assert delta_download_playback(bandwidth, segment_3) == 4
