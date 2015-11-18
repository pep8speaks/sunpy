"""SOHO Map subclass definitions"""
from __future__ import absolute_import, print_function, division
#pylint: disable=W0221,W0222,E1101,E1121

__author__ = "Jack Ireland"
__email__ = "jack.ireland@nasa.gov"


from astropy.units import Quantity

from sunpy.map import GenericMap
from sunpy.sun import sun

__all__ = ['CoimbraSpectroheliographMap']


class CoimbraSpectroheliographMap(GenericMap):
    """Coimbra Spectroheliograph Image Map.

    References
    ----------
    * `University of Coimbra Astronomical Observatory <http://www.uc.pt/en/fctuc/dmat/departamento/oauc>`_
    """

    def __init__(self, data, header, **kwargs):

        GenericMap.__init__(self, data, header, **kwargs)

        # Fill in some missing info
        self.meta['detector'] = "Coimbra University"
        self.meta['waveunit'] = "Angstrom"
        self._fix_dsun()
        self._nickname = self.detector

    @property
    def rsun_obs(self):
        """
        Returns the solar radius as measured in arcseconds.
        """
        return Quantity(self.meta['solar_r'] * self.meta['cdelt1'], 'arcsec')

    def _fix_dsun(self):
        """Determines the Earth-Sun distance and adds it to the meta header."""
        self.meta['dsun_obs'] = sun.sunearth_distance(self.date).to('m').value

    @classmethod
    def is_datasource_for(cls, data, header, **kwargs):
        """Determines if header corresponds to an EIT image"""
        return (header.get('origin') == 'Coimbra University') and \
               (header.get('telescop') == 'Spectroheliograph')

    @property
    def measurement(self):
        """
        Returns the type of data taken.
        """
        return "white-light"


