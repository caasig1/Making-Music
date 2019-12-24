"""CSC148 Assignment 1 - Making Music

=== CSC148 Summer 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains helper functions that should be imported and used by the
make_some_noise.py file to create numpy array representations of sine waves
and play numpy array representations of waves as sounds.

This file should not be modified in any way.
"""
from contextlib import redirect_stdout
import os
from typing import List
import numpy as np
from contextlib import contextmanager
import time
from warnings import warn

with open(os.devnull, 'w') as devnull:
    with redirect_stdout(devnull):
        import pygame

_SAMPLE_RATE = 44100
_BITS = 16
_MAX_SAMPLE = 2**(_BITS - 1) - 1
_MAX_CHANNELS = 3
_MAX_AMPLITUDE = int(_MAX_SAMPLE / _MAX_CHANNELS)

pygame.mixer.pre_init(_SAMPLE_RATE, -_BITS, 1)
pygame.mixer.init()
pygame.mixer.set_num_channels(_MAX_CHANNELS)

_AVAILABLE_CHANNELS = set()
for i in range(_MAX_CHANNELS):
    channel = pygame.mixer.Channel(i)
    _AVAILABLE_CHANNELS.add(channel)

@contextmanager
def _channel() -> None:
    try:
        channel = _AVAILABLE_CHANNELS.pop()
    except KeyError as e:
        msg = f'Only {_MAX_CHANNELS} sounds can be played at once'
        raise KeyError(msg) from e
    try:
        yield channel
    finally:
        _AVAILABLE_CHANNELS.add(channel)


def _play_sound(playable: object) -> None:
    with _channel() as channel:
        wave = playable.play() * _MAX_AMPLITUDE
        wave = pygame.sndarray.make_sound(
            np.ascontiguousarray(wave, dtype=np.int16))
        channel.play(wave)


def play_sound(playable: object) -> None:
    _play_sound(playable)
    time.sleep(playable.get_duration())


def play_sounds(playables: List[object]) -> None:
    if any(p.get_duration() - 1 > 0.01 for p in playables):
        msg = 'At least one of the sounds played has a '\
              'duration that is not exactly one second.'
        warn(msg)
    for playable in playables:
        _play_sound(playable)
    while pygame.mixer.get_busy():
        time.sleep(0.01)

def make_sine_wave_array(frequency: int, duration: float) -> np.ndarray:
    samples = int(_SAMPLE_RATE * duration)
    t = np.linspace(0, 1, samples, endpoint=False)
    return np.sin(2 * np.pi * frequency * t * duration)
