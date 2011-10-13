from __future__ import absolute_import

"""
SunPy Map objects are constructed using the special :function:`Map()`
function. ::

>>> map = sunpy.Map('file.fits')

The result of a call to `Map` will be either a generic 
:class:`sunpy.map.BaseMap` object, or a subclass of :class:`sunpy.map.BaseMap` 
which deals with a specific type of data, e.g. :class:`AIAMap` or 
:class:`LASCOMap`.
"""
#pylint: disable=W0401

__all__ = ["header", "mapcube", "sources"]
__author__ = "Keith Hughitt"
__email__ = "keith.hughitt@nasa.gov"

import sys
from sunpy.map.io import read_file
from sunpy.map.basemap import BaseMap
from sunpy.map.basemap import UnrecognizedDataSouceError
from sunpy.map.header import MapHeader
from sunpy.map.sources import *

#pylint: disable=C0103,E1101
def Map(input_):
    """Map class factory
    
    Attempts to determine the type of data associated with input and returns
    an instance of either the generic BaseMap class or a subclass of BaseMap
    such as AIAMap, EUVIMap, etc.
    
    Parameters
    ----------
    input_ : filepath, data array
        The data source used to create the map object. This can be either a
        filepath to an image, a 2d list, or an ndarray.
        
    Returns
    -------
    out : BaseMap
        Returns a BaseMap or BaseMap subclass instance
    """
    if isinstance(input_, basestring):
        data, dict_header = read_file(input_)
        
        header = MapHeader(dict_header)

        for cls in BaseMap.__subclasses__():
            if cls.is_datasource_for(header):
                return cls(data, header)
        raise UnrecognizedDataSouceError
    else:
        return BaseMap(input_)