.. _faq:

FAQ
=====

**Is web scraping legal?**

Even though web scraping is ubiquitous, its legal status remains unclear. That
is because whether web scraping is legal will depend on many aspects.
It is always best to consult with a lawyer or legal expert to ensure that your
web scraping activities are legal and comply with all applicable laws and
regulations.

.. Currently, web scraping is not per se prohibited in the European Union but the
.. use of data mining tools is legally risky.
..
.. The sui generis database right protects the content of a database. What does
.. it mean for web scrapers? That you can scrape such data (and, therefore, copy
.. and collect contents of the protected database – which falls under the
.. definition of “extraction” under the analyzed Directive) as long as (a) you
.. don’t scrape a ‘substantial part, evaluated qualitatively and/or
.. quantitatively, of the contents of that database’ and you don’t re-use it
.. (meaning basically selling or publishing it); or (b) scraping falls under TDM
.. exception described below; or (c) you’ve received an appropriate licence.
..
.. However, the TDM exception is limited: the database owners are granted the
.. possibility to restrict the reproduction and extraction of the databases and
.. their content. That restriction must be made in a manner that will allow bots
.. and crawlers etc. to see that restriction (therefore, on a website there
.. should be installed for example a special program communicating visiting
.. scraping programs that scraping is prohibited). Any such restriction should,
.. in any case, permit scraping made for scientific research purposes (see art.
.. 3 (1) and 7(1) of the DSM Directive).
..
.. But there are more traps on your way. One of them is the possibility of
.. breaching the website’s Terms of Use if they prohibit web scraping.
.. As the situation is highly uncertain, it is advisable to be careful and, if
.. possible, rather avoid breaching terms of use made available in any form.

.. To minimize concerns, scraping should be discreet, respect websites’ terms of
.. service, check whether sites are using the robots.txt protocol to communicate
.. that scraping is prohibited, avoid personal data scraping and, if it is
.. necessary, make sure no GDPR violations are made and avoid scraping private or
.. classified information. If possible, it would be advisable to get a licence
.. for scraping.


**Something doesn’t work**

1. Have you updated to the newest version of soccerdata?
2. Clear the cache or run your script without caching enabled.
3. Does the log produce any warnings that sound like they might be related?
   Maybe the data you are looking for is not available or can not be processed
   correctly.
4. Open an issue on GitHub.
