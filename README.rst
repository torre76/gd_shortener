GD Shortener
=============

Python Module for `is.gd - v.gd <http://is.gd/apishorteningreference.php>`_ URL Shortener.

What is this?
-------------

*GD Shortener* allow Python software to access `is.gd - v.gd <http://is.gd/apishorteningreference.php>`_ URL shortener service.

Using this module you could shorten an URL to a small one like *Twitter* does for its link.

This service is provided by `is.gd - v.gd <http://is.gd/apishorteningreference.php>`_ and, thru the classes in this module, you could view stats on shortened URLs and obtain reverse lookup on URLs. 

Install
-------

To install *GD Shortener*, run the following command::

    pip install gdshortener
	
Usage
-----


After install, to use *GD Shortener* is sufficient to import the package, choose the implementing class `ISGDShortener` or `VGDShortener` (it maps to is.gd or v.gd) and use the following code:

.. code-block:: python 
	 
	import gdshortener
	
	s = gdshortener.ISGDShortener()
	print s.shorten('http://www.google.com')
	
If you want statistic usage on a URL use:

.. code-block:: python
	
	print s.shorten(url = 'http://www.google.com', log_stat = True)
	
If you want a custom URL use:

.. code-block:: python
	
	print s.shorten(url = 'http://www.google.com', custom_url = 'Pippus')
	
If you have an already shortened URL and want a reverse lookup:

.. code-block:: python
	
	print s.lookup('http://is.gd/Pippus')
	
License
-------

*GD Shortener* is licensed under LGPL. See LICENSE.txt for details.
