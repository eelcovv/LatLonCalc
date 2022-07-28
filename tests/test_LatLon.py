'''
Test routines for class LatLon3 in package LatLon3
Designed for use with pytest

Created on Sep 2, 2014

@author: gdelraye
'''

import pytest
import pyproj
from numpy import (exp, angle, deg2rad, rad2deg)
from numpy.testing import (assert_almost_equal, assert_equal)

from LatLon3.LatLon import (LatLon, string2latlon, Latitude, Longitude)


def test_LatLon_tostring():
    '''
    Test LatLon3 method to_string
    '''
    palmyra = LatLon(5.8833, -162.0833)  # test location is Palmyra Atoll
    # Built-in string conversion (calls to_string):
    assert str(palmyra) == '5.8833, -162.0833'  # Failure of __str__ method
    # to_string method with decimal degrees:
    assert palmyra.to_string('D') == ('5.8833', '-162.0833')  # Failure of degree decimal output
    # to_string method with degree minute seconds:
    assert_equal(palmyra.to_string('d%, %m%, %S%, %H', n_digits_seconds=2),
                 ('5, 52, 59.88, N', '162, 4, 59.88, W'))
    # to_string method with fancy separators:
    assert_equal(palmyra.to_string('H%_%d%deg %M%"', n_digits_decimal_minutes=3),
                 ('N_5deg 52.998"', 'W_162deg 4.998"'))


def test_LatLon_fromstring():
    '''
    Test LatLon3 method from_string
    '''
    lat_str, lon_str = '5.8833', '-162.0833'  # test location is Palmyra Atoll
    # Convert decimal degrees string to LatLon3 object:
    palmyra = string2latlon(lat_str, lon_str, 'D')
    assert str(
        palmyra) == '5.8833, -162.0833'  # Failure to convert from degree, minutes, second, hemisphere string
    lat_str, lon_str = '5, 52, 59.88, N', '162, 4, 59.88, W'
    # Convert degrees minutes second string with hemisphere identifier to LatLon3 object:
    palmyra = string2latlon(lat_str, lon_str, 'd%, %m%, %S%, %H')
    assert_almost_equal(palmyra.lat.decimal_degree, 5.8833)
    assert_almost_equal(palmyra.lon.decimal_degree,
                        -162.0833)  # Failure to convert from degree, minutes, second, hemisphere string
    lat_str, lon_str = 'N_5deg 52.998', 'W_162deg 4.998'
    # Convert degrees minutes second string with fancy separators to LatLon3 object:
    palmyra = string2latlon(lat_str, lon_str, 'H%_%d%deg %M')
    # convert to lat decimal degree to solve round of problem
    assert_almost_equal(palmyra.lat.decimal_degree,
                        Latitude(
                            5.8833).decimal_degree)  # Failure to convert from hemisphere, degree, minutes string
    assert_almost_equal(palmyra.lon.decimal_degree, Latitude(
        -162.0833).decimal_degree)  # Failure to convert from hemisphere, degree, minutes string


def test_LatLon_complex():
    '''
    Test LatLon3 method complex
    '''
    palmyra = LatLon(5.8833, -162.0833)  # test location is Palmyra Atoll
    complex_coords = palmyra.complex()  # Convert lat/lon coordinate to single complex number
    assert complex_coords.real == 5.8833  # Failed to retrieve latitude from complex coordinate
    assert complex_coords.imag == -162.0833  # Failed to retrieve longitude from complex coordinate


def test_LatLon_heading():
    '''
    Test LatLon3 methods heading_initial and heading_reverse
    '''
    palmyra, honolulu = LatLon(5.8833, -162.0833), LatLon(21.3,
                                                          -157.8167)  # locations: Palmyra Atoll and Honolulu, HI
    true_heading = 14.691  # Correct heading in from Palmyra to Honolulu to 3 decimal places
    forward_heading = palmyra.heading_initial(honolulu)  # Initial heading from palmyra to honolulu
    # Check heading from Palmyra Atoll to Honolulu using heading_initial:
    assert_almost_equal(forward_heading, true_heading, decimal=3)
    reverse_heading = honolulu.heading_reverse(palmyra)  # Reverse heading from honolulu to palmyra
    # Check heading from Palmyra Atoll to Honolulu using heading_reverse:
    assert_almost_equal(reverse_heading, true_heading, decimal=3)
    # Now for two locations with (for our purposes) the same longitude - Washington, DC and Lima, Peru:
    washington, lima = LatLon(Latitude(38, 54), Longitude(-77, -2)), LatLon(Latitude(-12, -3),
                                                                            Longitude(-77, -2))
    true_heading = -180.000  # Heading for directly south
    forward_heading = rad2deg(angle(exp(1j * deg2rad(washington.heading_initial(lima)))))
    # Check handling of equal longitude coordinates by heading_initial:
    try:
        assert_almost_equal(forward_heading, true_heading, decimal=3)
    except AssertionError:
        # now exactly south is 180 (not -180). Just a definition matter. Try again with 180 if -180 fails
        assert_almost_equal(forward_heading, -true_heading, decimal=3)
    reverse_heading = lima.heading_reverse(washington)
    # Check handling of equal longitude coordinates by heading_reverse:
    true_heading = 180.000  # Heading for directly south
    assert_almost_equal(reverse_heading, true_heading, decimal=3)
    # Now for two locations with (for our purposes) the same latitude - Alexandria, Egypt and Shanghai, China:
    alexandria, shanghai = LatLon(Latitude(31, 12), Longitude(29, 55)), LatLon(Latitude(31, 12),
                                                                               Longitude(121, 30))
    true_heading = 61.941  # Correct heading in from Alexandria to Shanghai to 3 decimal places
    forward_heading = alexandria.heading_initial(
        shanghai)  # Initial heading from Alexandria to Shanghai
    # Check handling of equal latitude coordinates by heading_initial:
    assert_almost_equal(forward_heading, true_heading, decimal=3)
    reverse_heading = shanghai.heading_reverse(
        alexandria)  # Reverse heading from Shanghai to Alexandria
    # Check handling of equal latitude coordinates by heading_initial:
    assert_almost_equal(reverse_heading, true_heading, decimal=3)


def test_LatLon_distance():
    '''
    Test LatLon3 method distance
    '''
    palmyra, honolulu = LatLon(5.8833, -162.0833), LatLon(21.3,
                                                          -157.8167)  # locations: Palmyra Atoll and Honolulu, HI
    true_distance = '1766.691'  # Distance from Palmyra to Honolulu in km
    wgs84_distance = palmyra.distance(honolulu)
    assert '%.3f' % (
        wgs84_distance) == true_distance  # Failed to calculate WGS84 distance from Palmyra to Honolulu
    wgs84_distance = honolulu.distance(palmyra)
    assert '%.3f' % (
        wgs84_distance) == true_distance  # Failed to calculate WGS84 distance from Honolulu to Palmyra
    # Now including the north pole:
    geographic_north = LatLon(90, 0)  # Longitude is meaningless in this case
    true_distance = '7645.673'  # Distance from Honolulu to North Pole in km
    wgs84_distance = honolulu.distance(geographic_north)
    assert '%.3f' % (
        wgs84_distance) == true_distance  # Failed to calculate WGS84 distance from north pole


def test_LatLon_offset():
    '''
    Test LatLon3 method offset
    '''
    palmyra, honolulu = LatLon(5.8833, -162.0833), LatLon(21.3,
                                                          -157.8167)  # locations: Palmyra Atoll and Honolulu, HI
    distance = palmyra.distance(honolulu)  # WGS84 distance is 1766.69130376 km
    initial_heading = palmyra.heading_initial(
        honolulu)  # Initial heading to Honolulu on WGS84 ellipsoid
    offset_hnl = palmyra.offset(initial_heading,
                                distance)  # Reconstruct lat/lon for Honolulu based on offset from Palmyra
    # Equality could also be tested with honolulu == offset_hnl, but would be subject to float errors
    assert honolulu.almost_equal(offset_hnl)
    vector = honolulu - palmyra  # Same process with GeoVectors
    vector_hnl = palmyra + vector  # Reconstruct lat/lon for Honolulu based on offset from Palmyra
    assert honolulu.almost_equal(vector_hnl)


def test_LatLon_project():
    '''
    Test LatLon3 method project
    '''
    palmyra = LatLon(5.8833, -162.0833)  # test location is Palmyra Atoll
    projection = pyproj.Proj(proj='utm', zone=3, ellps='WGS84')
    x, y = palmyra.project(projection)
    utm_x, utm_y = 822995, 651147  # True projected coordinates to the nearest meter
    assert int(x) == utm_x and int(
        y) == utm_y  # Error in computing projected coordinates for Palmyra Atoll'


def main():
    test_LatLon_tostring()
    test_LatLon_fromstring()
    test_LatLon_complex()
    test_LatLon_heading()
    test_LatLon_distance()
    test_LatLon_offset()
    test_LatLon_project()


if __name__ == "__main__":
    main()
