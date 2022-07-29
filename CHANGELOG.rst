=========
Changelog
=========

1.4.7 (JUL/29/2022)
===================
* dropped Python 2 support, upgraded to Python 3.9
* Fixed unit tests
* Renamed project to *latloncalc* to prevent name conflict. The module is now call *latlon*.
* Included tox setup
* Added documentation on read the docs

1.2.1 (MAY/20/2020)
===================
* Prepared for pypi and changed module name from latlon to latlon3

1.1.7 (SEPT/7/2017)
====================
* Bug fix exception in __init__ file.  Only relevant for making executable using pyinstaller

1.1.4 (JULY/28/2017)
====================
* Released for production

1.1.0 (JULY/03/2017)
====================

* Applied futurize script to allow to run latlon under Python 3.5
* Fixed some unit tests
* Fixed the comparative operator
* Made Docstrings compliant to Numpy Doc Style
* Tested on Python 3.5

1.0.2 (OCTOBER/14/2014)
=======================

* Class *GeoVector* is now an abstract class to ensure that any subclasses use the correct API
* Added methods *range180* and *range360* to class *Longitude* to interconvert between longitudes reported -180
  to 180 format and those reported in 0 to 360 format. To ensure that all operations such as hemisphere assignment
  work as expected, longitudes reported in 0 to 360 format are automatically converted into -180 to 180 format
  when the *Longitude* object is initialized.

1.0.1 (SEPTEMBER/2/2014)
========================

* Fixed issue with where attribute *theta* in *GeoVector* was treated in some cases like a heading (i.e. starting
  with due north and continuing clockwise) even though it was in fact an angle (i.e. starting with (1, 0) and
  continuing anti-clockwise). The attribute name has now been changed to *heading* to eliminate confusion. The
  local variable *theta* is used for computations involving angle.
* Added testing functions with *pytest* for class *latlon* and *GeoVector*
* Added *almost_equal* methods to class *latlon* and *GeoVector* to deal with float errors in decimal degree
  specification
* *latlon.project* now returns *(x, y)* instead of *(y, x)* to be more consistent with the accepted convention.

0.91 (AUGUST/28/2014)
=====================

* *degree*, *minute* and *second* attributes for *GeoCoord* class are now coerced to type *float*

0.90 (AUGUST/28/2014)
=====================

* Updated magic methods for *GeoCoord* class
* Added option for instantiating *latlon* from scalars

0.80 (AUGUST/27/2014)
=====================

* Added *GeoVector* class to handle vectors between two *LatLon* objects
* Cleaned up *__str__* and *__repr__* methods for *LatLon*, *Latitude*, *Longitude*, *GeoCoord*, and *GeoVector*
  classes

0.70 (AUGUST/27/2014)
=====================

* Deprecated *latlon.distance_sphere* method. From now on use *distance(other, ellipse = 'sphere')* instead
* Added *latlon.bearing* method to return the initial bearing between two *latlon* objects
* Added *latlon.offset* method to return a new latlon object that is computed from an initial latlon object plus
  a bearing and distance

0.60 (AUGUST/27/2014)
=====================

* Added compatibility with comparison, negation, addition and multiplication magic methods

0.50 (AUGUST/20/2014)
=====================

* First release

