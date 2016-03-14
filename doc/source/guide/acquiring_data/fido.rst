-------------------------------
Fido: Getting data from the net
-------------------------------

Fido is the recommended module for searching and acquiring solar and heliospheric data
in SunPy.  It provides a single interface that enables users to query and obtain data
through the VSO, the JSOC and other web locations.


Setup
^^^^^

Fido is in ``sunpy.net``.  It can be imported as follows:

    >>> from sunpy.net import Fido

Obtaining data via Fido is a two-stage process.  First you specify
the data you are interested in.  Fido then queries data provisioning services
if they can service the query, and if they can, a query is made
and a list o

You first ask the VSO to find the data you want.  The VSO
queries various data-providers looking for your data. If there is any data
that matches your request, you choose the data you want to download.
The VSO client handles the particulars of how the data from
the data provider is downloaded to your computer.

Constructing a Query
^^^^^^^^^^^^^^^^^^^^

Let's consider a simple request.  A user wants all the AIA 304 Angstrom data in
a particular in the time range 2013/08/09 00:00:00 - 01:00:00.  This is done by
specifying the attributes of the search and combining them in to a Fido search.

    >>> from sunpy.net import Fido
    >>> from sunpy.net.vso import attrs as a
    >>> import astropy.units as u
    >>> query = Fido.search(a.Instrument('AIA'), a.Wavelength(304*u.AA, 304*u.AA), a.Time('2013/08/09 00:00:00', '2013/08/09 01:00:00'))

This tells Fido to search for AIA data in the wavelength range 304 to 304 Angstroms in the time range
2013/08/09 00:00:00 - 01:00:00.  The commas between each attribute mean that the
attributes are combined using a logical AND operation.  Instead of using
a comma, you can also use '&', and so the above query can be equivalently written as

    >>> query = Fido.search(a.Instrument('AIA') & a.Wavelength(304*u.AA, 304*u.AA) & a.Time('2013/08/09 00:00:00', '2013/08/09 01:00:00'))

The output from Fido is a `sunpy.net.dataretriever.downloader_factory.UnifiedResponse` object.  It
holds the details of the results of the search.  For the query above,

    >>> len(query)
    >>> 1

meaning that Fido obtained one response, and the total number of files found is

    >>> query.file_num
    >>> 300


Let's say that the user now also wants to look for AIA 211 Angstrom in the same
time range.  This can be achieved using the logical OR operator '|'

    >>> query = Fido.search(a.Instrument('AIA') & (a.Wavelength(304*u.AA, 304*u.AA) | a.Wavelength(211*u.AA, 211*u.AA)) & a.Time('2013/08/09 00:00:00', '2013/08/09 01:00:00'))

With this query,

    >>> len(query)
    >>> 2

and

    >>> query.file_num
    >>> 600

There are two responses because Fido did one search for 304 Angstrom data, and
another for 211 Angstrom data.  The number of files found by each search can
be found using the `len` function on each element of the query.





Any VSO or JSOC attributes can be used in any combinations.

    >>> from sunpy.net import Fido
    >>> from sunpy.net.vso import attrs import as a
    >>> query = Fido.search(a.Instrument('lyra'), a.Time('2013/08/09', '2013/08/10'))
    >>> data = Fido.fetch(query)

Fido queries
Since LYRA is a known instrument source, Fido knows where to look for the data.  In

Fido
queries that service and returns the data that is available



SunPy maintains a list of locations where data from a given instrument can be found.
In the case when data can be found via the VSO and an instrument-specific location,
Fido defaults to using the instrument-specific location.  This is because the VSO
commonly acts as an intermediary between your request and the instrument-specific
location; therefore, going direct to the instrument-specific location is liable to
provide a speedier service.  If there are data that you are interested in that are
not currently available via the VSO and you know where it can be found online, please
contact the SunPy developers at sunpy-dev@googlegroups.com for inclusion via the
Fido interface.

-----------------------------
Downloading Data from the VSO
-----------------------------

The main interface which SunPy provides to search for and download data is provided by
SunPy's VSO module. This module provides an interface to the
`Virtual Solar Observatory (VSO) <http://virtualsolar.org>`_
which is a service which presents a homogeneous interface to heterogeneous
data-sets and services.  Using the VSO, a user can query multiple data providers
simultaneously, and then download the relevant data.  SunPy uses the VSO through the ``vso``
module, which was developed through support from the `European Space
Agency Summer of Code in Space (ESA-SOCIS) 2011
<http://sophia.estec.esa.int/socis2011/>`_.

Setup
-----

SunPy's VSO module is in ``sunpy.net``.  It can be imported as follows:

    >>> from sunpy.net import vso
    >>> client = vso.VSOClient()

This creates your client object. Obtaining data via the VSO is a two-stage process.
You first ask the VSO to find the data you want.  The VSO
queries various data-providers looking for your data. If there is any data
that matches your request, you choose the data you want to download.
The VSO client handles the particulars of how the data from
the data provider is downloaded to your computer.

Searching the VSO
-----------------

To search the VSO, your query needs at minimum a start time, an end
time, and an instrument.  Two styles of constructing the query are
supported by SunPy's VSO module.  The first style is very flexible, as
it allows users to issue complex queries in a single command.  This
query style is described below.

The second query style - known as the ``legacy query`` is useful for
making quick VSO queries, and is based on the function call to
`SSWIDL's VSO query client <http://docs.virtualsolar.org/wiki/VsoIDL>`_.

The section below first describe the more flexible query style.  The
next section then describes the legacy query.  The final section
describes how to download data from those query results.

Constructing a Query
^^^^^^^^^^^^^^^^^^^^

Let's start with a very simple query.  We could ask for all SOHO/EIT
data between January 1st and 2nd, 2001.

    >>> qr = client.query(vso.attrs.Time('2001/1/1', '2001/1/2'), vso.attrs.Instrument('eit'))

The variable ``qr`` is a Python list of
response objects, each one of which is a record found by the VSO. You can find how many
records were found by typing

    >>> len(qr)
    122

To get a little bit more information about the records found, try

    >>> print(qr) # doctest:+SKIP
    ...


Now, let's break down the arguments of ``client.query`` to understand
better what we've done.  The first argument:

    ``vso.attrs.Time('2001/1/1', '2001/1/2')``

sets the start and end times for the query (any date/time
format understood by SunPy's :ref:`parse_time function <parse-time>`
can be used to specify dates and time).  The second argument:

    ``vso.attrs.Instrument('eit')``

sets the instrument we are looking for. The third argument:

    ``vso.attrs.Wave(142*u.AA, 123*u.AA)``

sets the values for wavelength i.e, for wavemax(maximum value) and
similarly wavemin(for minimum value) for the query. Also the ``u.AA``
part comes from ``astropy.units.Quantity`` where `AA` is Angstrom. It
should be noted that specifying spectral units in arguments is
necessary or an error will be raised. To know more check
`astropy.units <https://astropy.readthedocs.org/en/stable/units/index.html>`_.

So what is going on here?
The notion is that a VSO query has a set of attribute objects -
described in ``vso.attrs`` - that are specified to construct the query.
For the full list of vso attributes, use

    >>> help(vso.attrs) # doctest:+SKIP

Note that due to a current bug in the VSO, we do not recommend that the
extent object ``vso.attrs.Extent`` be in your query.  Instead, we
recommend that any extent filtering you need to do be done on the
queries made without setting a value to the ``vso.attrs.Extent`` object.
As we will see, this query style can take more than two arguments,
each argument separated from the other by a comma.  Each of those
arguments are chained together using a logical ``AND``.

This query style allows you to combine these VSO attribute objects
in complex ways that are not possible with the legacy query style.

So, let's look for the EIT and MDI data on the same day:

    >>> qr=client.query(vso.attrs.Time('2001/1/1', '2001/1/2'), vso.attrs.Instrument('eit') | vso.attrs.Instrument('mdi'))
    >>> len(qr)
    3549
    >>> print(qr) # doctest:+SKIP
    ...

The two instrument types are joined together by the operator "|".
This is the ``OR`` operator.  Think of the above query as setting a set
of conditions which get passed to the VSO.  Let's say you want all the
EIT data from two separate days:

    >>> qr=client.query(vso.attrs.Time('2001/1/1', '2001/1/2') | vso.attrs.Time('2007/8/9', '2007/8/10'), vso.attrs.Instrument('eit') )
    >>> len(qr)
    227

Each of the arguments in this query style can be thought of as
setting conditions that the returned records must satisfy.  You can
set the wavelength; for example, to return the 171 Angstrom EIT results

    >>> import astropy.units as u
    >>> qr=client.query(vso.attrs.Time('2001/1/1', '2001/1/2'), vso.attrs.Instrument('eit'), vso.attrs.Wave(171*u.AA,171*u.AA) )
    >>> len(qr)

Downloading data
----------------
All queries return a query response list. This list can then used to get the data. This
list can also be edited as you see fit. For example you can further reduce the number of
results and only get those. So having located the data you want, you can download it using the
following command:

    >>> res=client.get(qr, path='/ThisIs/MyPath/to/Data/{file}.fits')

This downloads the query results into the directory
``/ThisIs/MyPath/to/Data`` naming each downloaded file with the
filename ``{file}`` obtained from the VSO , and appended with the suffix
``.fits``.  The ``{file}`` option uses the file name obtained by the VSO
for each file.  You can also use other properties of the query return
to define the path where the data is saved.  For example, to save the
data to a subdirectory named after the instrument, use

    >>> res=client.get(qr, path='/ThisIs/MyPath/to/Data/{instrument}/{file}.fits')

If you have set your default download directory in your sunpyrc configuration file
then you do not need to identify a path at all. All you data will be downloaded there.

Note that the download process is spawned in parallel to your existing
Python session.  This means that the remainder of your Python script
will continue as the download proceeds.  This may cause a problem if
the remainder of your script relies on the presence of the downloaded
data.  If you want to resume your script after all the data has been
downloaded then append ``.wait()`` to the ``get`` command above, i.e.,

     >>> res=client.get(qr, path='/Users/ireland/Desktop/Data/{instrument}/{file}.fits').wait()

More information on the options available can be found through the
standard Python ``help`` command.
