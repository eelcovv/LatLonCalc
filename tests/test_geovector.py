"""
Test routines for class GeoVector in package LatLon
Designed for use with pytest

Created on Sep 2, 2014

@author: gdelraye
"""

import math
from LatLon import GeoVector


def test_constructor():
    """
    Test GeoVector constructor
    """
    dx, dy = 10., 10.
    magnitude = math.sqrt(dx ** 2 + dy ** 2)  # Calculate vector length
    initial_heading = 45.  # Compass heading
    vector1 = GeoVector(dx=dx, dy=dy)
    vector2 = GeoVector(initial_heading=initial_heading, distance=magnitude)
    assert vector1.almost_equals(vector2)  # Error in Updating GeoVector angle and magnitude from dx and dy


def test_magic():
    """
    Test Geovector magic methods
    """
    vector1 = GeoVector(dx=0, dy=1)
    vector2 = GeoVector(dx=1, dy=0)
    assert -vector1.dy == -1  # Unexpected behavior in __neg__ method
    vector1add2 = vector1 + vector2
    assert vector1add2.dx == 1 and vector1add2.dy == 1  # Failed to construct correct vector with __add__ method
    assert abs(vector1add2.magnitude - math.sqrt(2)) < 0.00001  # Failed to get correct magnitude with __add__ method
    vector2sub1 = vector2 - vector1
    assert vector2sub1.dx == 1 and vector2sub1.dy == -1  # Failed to construct correct vector using __sub__ method
    assert vector2sub1.magnitude == vector1add2.magnitude  # Failed to properly compute magnitude with __add__ method
    assert vector2sub1.heading - 90 == vector1add2.heading  # Failed to properly compute heading with __sub__ method
    vector1x2 = vector1 * 2
    assert vector1.heading == vector1x2.heading  # Unexpected behavior for heading attribute with __mul__ method
    assert vector1x2 > vector1  # __cmp__ method giving unexpected result
    assert vector1x2.almost_equals(vector1 + vector1)  # Failed to recreate vector by addition and multiplication
    assert str(vector1x2) == '0.0, 2'  # String conversion failed
