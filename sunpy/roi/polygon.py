__authors__ = ["Jack Ireland"]
__email__ = "jackireland@gmail.com"

import numpy as np
import astropy.units as u
from sunpy.time import parse_time


class Polygon:
    """
    An object that defines an extent of a two dimensional shape.

    Parameters
    ----------
    coordinates :

    coordinate_system :

    time :


    Returns
    -------

    Examples
    --------

    """


    @u.quantity_input(coords=u.deg)
    def __init__(self, coordinates, coordinate_system, time=None):

        # Set the co-ordinates of the polygon
        self.coordinates = coordinates

        # Set the co-ordinate system
        self.coordinate_system = coordinate_system

        # Set the time
        if time is None:
            self.time = None
        else:
            self.time = parse_time(time)

        # Define the centroid of the
        self.centroid

    def mpl_polygon(self):
        """
        Return a matplotlib Polygon object.
        """
        return None

    def solar_rotate_each_vertex(self, new_time):
        """
        Return a new Polygon such that each vertex of the original polygon has
        been rotated to the new time, following solar rotation.

        :param new_time:
        :return:
        """
        return None

    def solar_rotate_by_centroid(self, new_time):
        """
        Return a new Polygon such that the centroid of the original polygon has
        been rotated to the new time, following solar rotation.

        :param new_time:
        :return:
        """
        return None