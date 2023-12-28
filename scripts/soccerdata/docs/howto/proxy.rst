How to use a proxy server
-------------------------

You can setup a SOCKS5 proxy with Tor.
Checkout the `installation guide`_ on the Tor website for installation
instructions. After installing Tor, make sure to start it up before scraping.
This can easily be done by running the ``tor`` command from your terminal (in
a separate window), Tor will start up and run on “localhost:9050” by default.
Once Tor is running, you can enable the extension by setting ``proxy='tor'``.

.. code:: python

   ws = sd.WhoScored(proxy='tor')

The code snippet above assumes you have a Tor proxy running on
"localhost:9050". Many distributions indeed default to having a SOCKS proxy
listening on port 9050, but some may not. In particular, the Tor Browser
Bundle defaults to listening on port 9150. You can specify a custom host and
port as

.. code:: python

   ws = sd.WhoScored(proxy={
        "http": "socks5://127.0.0.1:9150",
        "https": "socks5://127.0.0.1:9150",
    })


.. _installation guide: https://community.torproject.org/onion-services/setup/install/
