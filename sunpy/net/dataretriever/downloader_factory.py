# Author: Rishabh Sharma <rishabh.sharma.gunner@gmail.com>
# This module was developed under funding provided by
# Google Summer of Code 2014.

from sunpy.util.datatype_factory_base import BasicRegistrationFactory
from sunpy.util.datatype_factory_base import NoMatchError
from sunpy.util.datatype_factory_base import MultipleMatchError

from .. import attr
from .client import GenericClient

__all__ = ['Fido']


class UnifiedResponse(list):

    def __init__(self, lst):

        tmplst = []
        for block in lst:
            block[0].client = block[1]
            tmplst.append(block[0])
        super(UnifiedResponse, self).__init__(tmplst)
        self._numfile = 0
        for qblock in self:
            self._numfile += len(qblock)

    @property
    def file_num(self):
        return self._numfile

    def _repr_html_(self):
        ret = ''
        for block in self:
            ret += block._repr_html_()

        return ret

class downloadresponse(list):
    """
    List of Results object returned by clients servicing the query.
    """
    def __init__(self, lst):

        super(downloadresponse, self).__init__(lst)

    def wait(self, progress=True):
        """
        Waits for all files to download completely and then return.
        Returns
        -------
        list of file paths to which files have been downloaded.
        """
        filelist = []
        for resobj in self:
            filelist.extend(resobj.wait(progress=progress))

        return filelist


qwalker = attr.AttrWalker()

@qwalker.add_creator(attr.AttrAnd)
def _create(wlk, query, dobj):
    qresponseobj, qclient = dobj._get_registered_widget(*query.attrs)
    return [(qresponseobj, qclient)]


@qwalker.add_creator(attr.AttrOr)
def _create(wlk, query, dobj):
    qblocks = []
    for iattr in query.attrs:
        qblocks.extend(wlk.create(iattr, dobj))

    return qblocks


class UnifiedDownloaderFactory(BasicRegistrationFactory):

    def search(self, *query):
        """
        Query for data using multiple parameters.

        Parameters
        ----------
        query: A list of comma-separated Multiple parameters, VSO-styled query. Attributes from both the
        JSOC and the VSO can be used.

        Examples
        --------
        Most queries will specify a time range and an instrument

        Query for LYRA data from in the time range 2012/03/04 to 2012/03/06.
        >>> from sunpy.net.dataretriever import Fido
        >>> from sunpy.net.vso.attrs import Time, Instrument
        >>> unifresp = Fido.search(Time('2012/03/04','2012/03/06'), Instrument('lyra'))

        Get Nobeyama and RHESSI time series data in the same time range
        >>> unifresp = Fido.search(Time('2012/3/4','2012/3/6'), Instrument('norh') | Instrument('rhessi'))

        Get one AIA 304 angstrom image every 600 seconds in the specified
        timerange.
        >>> import astropy.units as u
        >>> from sunpy.net.vso.attrs import Wavelength, Sample
        >>> unifresp = Fido.search(Time('2012/3/4','2012/3/6'), Instrument('AIA'),
                       Wavelength(304*u.AA, 304*u.AA), Sample(60*10*u.s))

        Returns
        -------
        `UnifiedResponse`
        Container of responses returned by clients servicing the query.

        Notes
        -----
        and_ tranforms query into disjunctive normal form
        ie. query is now of form A & B or ((A & B) | (C & D))
        This helps in modularising query into parts and handling each of the
        parts individually.
        """
        query = attr.and_(*query)
        return UnifiedResponse(qwalker.create(query, self))

    def fetch(self, qr, wait=True, progress=True, **kwargs):
        """
        Downloads the files at the URLs contained within UnifiedResponse object.

        Parameters
        ----------
        qr : ` Object
            Container returned by query method.

        wait : `bool`
            fetch will wait until the download is complete before returning.

        progress : `bool`
            Show a progress bar while the download is running.

        Returns
        -------
        DownloadResponse Object
            List of Results object with an additional wait method.

        Example
        --------
        >>> unifresp = Fido.query(Time('2012/3/4','2012/3/6'), Instrument('AIA'))
        >>> downresp = Fido.fetch(unifresp)
        >>> file_paths = downresp.wait()
        """
        reslist = []
        for block in qr:
            reslist.append(block.client.get(block, **kwargs))

        results = downloadresponse(reslist)

        if wait:
            return results.wait(progress=progress)
        else:
            return results

    def __call__(self, *args, **kwargs):
        pass

    def _check_registered_widgets(self, *args, **kwargs):
        """Factory helper function"""
        candidate_widget_types = list()
        for key in self.registry:

            if self.registry[key](*args):
                candidate_widget_types.append(key)

        n_matches = len(candidate_widget_types)
        if n_matches == 0:
            if self.default_widget_type is None:
                raise NoMatchError("Query {0} can not be handled in its current form".format(args))
            else:
                return [self.default_widget_type]
        elif n_matches > 1:
            # This is a hack, VSO services all Instruments.
            # TODO: VSOClient._can_handle_query should know what values of
            # Instrument VSO can handle.
            for candidate_client in candidate_widget_types:
                if issubclass(candidate_client, GenericClient):
                    return [candidate_client]

            candidate_names = [cls.__name__ for cls in candidate_widget_types]
            raise MultipleMatchError("Too many candidates clients can service your query {0}".format(candidate_names))

        return candidate_widget_types

    def _get_registered_widget(self, *args, **kwargs):
        """Factory helper function"""
        candidate_widget_types = self._check_registered_widgets(*args)
        tmpclient = candidate_widget_types[0]()
        return tmpclient.query(*args), tmpclient


Fido = UnifiedDownloaderFactory(additional_validation_functions=['_can_handle_query'])
