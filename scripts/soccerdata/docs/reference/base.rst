.. _api-base:

Base Readers
============

The logic for downloading data from the web is implemented in the base classes
that are documented here. The base classes are not intended to be used directly
but rather to be subclassed by the specific readers which implement the logic
to parse the data.

The :class:`BaseRequestsReader` is a wrapper around the `requests` library
and is used by scrapers that do not require JavaScript to be executed. The
:class:`BaseSeleniumReader` is a wrapper around the `selenium` library and is
used by scrapers that require JavaScript to be executed.

.. autoclass:: soccerdata._common.BaseRequestsReader
   :inherited-members:
   :members:

.. autoclass:: soccerdata._common.BaseSeleniumReader
   :inherited-members:
   :members:
