"""
.. currentmodule: gdshortener

    :synopsis: Module that enables the use of `is.gd - v.gd url shortener <http://is.gd/developers.php>`_.
"""

import HTMLParser
import urllib
import requests
import json

_V_GD_SHORTENER_URL_ = 'http://v.gd'
_IS_GD_SHORTENER_URL_ = 'http://is.gd'


class GDBaseException(Exception):
    """
        Base Exception class that handles `is.gd <http://is.gd/>`_  error codes.
        
        :param error_code: Error code obtained from is.gd. See `Interpreting error code section <http://is.gd/developers.php>`_ on is.gd dev guide.
        :type error_code: int.
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    """
    
    def __str__(self):
        return "Error code: [{error_code}] - Error description: [{error_description}]".format(error_code=self.error_code, error_description=self.error_description)
    
    def __repr__(self):
        return "<{error_instance}({error_code}, {error_description})>".format(error_instance=self.__class__.__name__, error_code=self.error_code, error_description=self.error_description)
    
    @property
    def error_code(self):
        """
            `is.gd <http://is.gd/>`_ error code:
            
            - error code *1*: there was a problem with the original long URL provided
            - error code *2*: there was a problem with the short URL provided (for custom short URLs)
            - error code *3*: our rate limit was exceeded (your app should wait before trying again)
            - error code *4*: any other error (includes potential problems with our service such as a maintenance period)
            
            :returns: int.
        """
        return self._error_code
    
    @property
    def error_description(self):
        """
            `is.gd <http://is.gd/>`_ description for this error.
            
            :returns: str.
        """
        return self._error_description
    
    def __init__(self, error_code=4, error_description=None):
        """
            Init the exception with code and description taken from `is.gd <http://is.gd/>`_.
            
            :param error_code: Error code obtained from is.gd. See `Interpreting error code section <http://is.gd/developers.php>`_ on is.gd dev guide.
            :type error_code: int.
            :param error_description: Error description obtained from is.gd
            :type error_description: str.
        """
        self._error_code = error_code
        self._error_description = error_description


class GDMalformedURLError(GDBaseException):
    """
        This exceptions identify a problem with the URL that had to be shortened.
        
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    """
    
    def __init__(self, error_description=None):
        """
            Init the exception with description taken from `is.gd <http://is.gd/>`_.
            
            :param error_description: Error description obtained from is.gd
            :type error_description: str.
        """
        GDBaseException.__init__(self, 1, error_description)
 

class GDShortURLError(GDBaseException):
    """
        This exceptions identify a problem with the shortened URL.
        
        Could be either an error on custom shortener URL or a copyright error on a URL (in which case it could had been disabled).
        
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    """
    
    def __init__(self, error_description=None):
        """
            Init the exception with description taken from `is.gd <http://is.gd/>`_.
            
            :param error_description: Error description obtained from is.gd
            :type error_description: str.
        """
        GDBaseException.__init__(self, 2, error_description)


class GDRateLimitError(GDBaseException):
    """
        This exceptions is raised when is.gd rate limit has been exceeded.
        
        :param error_description: Error description obtained from is.gd
        :type error_description: str.
    """
    
    def __init__(self, error_description=None):
        """
            Init the exception with description taken from `is.gd <http://is.gd/>`_.
            
            :param error_description: Error description obtained from is.gd
            :type error_description: str.            
        """
        GDBaseException.__init__(self, 3, error_description)       


class GDGenericError(GDBaseException):
    """
        This exceptions is raised when is.gd states a generic problem.
        
        Further informations are provided on error description.
        
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    """

    def __init__(self, error_description=None):
        """
            Init the exception with description taken from `is.gd <http://is.gd/>`_.

            :param error_description: Error description obtained from is.gd
            :type error_description: str.
        """
        GDBaseException.__init__(self, 4, error_description)


class GDBaseShortener(object):
    """
        Base shortener for `is.gd - v.gd url shortener <http://is.gd/developers.php>`_.
        
        :type shortener_url: str.  
        :param shortener_url: base is.gd - v.gd API URL to create shorten link.

            Possible values are:
            
            1. **_IS_GD_SHORTENER_URL_** to obtain *is.gd* shortened url
            2. **_V_GD_SHORTENER_URL_** to obtain *v.gd* shortened url
            

        :param timeout: Timeout in seconds used to connect and obtain shortened URL from .gd service
        :type timeout: int.
        :param user_agent: User Agent used when querying .gd services
        :type user_agent: str.
    """
    
    def lookup(self, short_url):
        """
            Lookup an URL shortened with `is.gd - v.gd url service <http://is.gd/developers.php>`_ and return the real url
            
            :param short_url: the url shortened with .gd service
            :type short_url: str.
            
            :returns: str. -- The original url that was shortened with .gd service
            
            :raises: **IOError** when timeout with .gd service occurs
                **ValueError** if .gd response is malformed
                :class:`gdshortener.GDMalformedURLError` if the previously shortened URL provided is malformed
                :class:`gdshortener.GDShortURLError` if the custom URL requested is not available or disabled by .gd service
                :class:`gdshortener.GDRateLimitError` if the request rate is exceeded for .gd service
                :class:`gdshortener.GDGenericError` in case of generic error from .gd service (mainteinance)
        """
        if short_url is None or not isinstance(short_url, basestring) or len(short_url.strip()) == 0:
            raise GDMalformedURLError('The shortened URL must be a non empty string')
        # Build data for porst
        data = {
            'format': 'json',
            'shorturl': short_url
        }
        headers = {'User-Agent': self._user_agent}
        f_desc = requests.get("{0}/forward.php".format(self.shortener_url), params=data, headers=headers)
        response = json.loads(f_desc.text)
        if 'url' in response:
            # Success!
            return HTMLParser.HTMLParser().unescape(urllib.unquote(response['url']))
        else:
            # Error
            error_code = int(response['errorcode'])
            error_description = str(response['errormessage'])
            if error_code == 1:
                raise GDMalformedURLError(error_description)
            if error_code == 2:
                raise GDShortURLError(error_description)
            if error_code == 3:
                raise GDRateLimitError(error_description)
            if error_code == 4:
                raise GDGenericError(error_description)

    def shorten(self, url, custom_url=None, log_stat=False):
        """
            Shorten an URL using `is.gd - v.gd url shortener service <http://is.gd/developers.php>`_.
            
            :param url: URL that had to be shortened
            :type url: str.
            
            :param custom_url: if specified, the url generated will be http://is.gd/<custom_url> (or http://v.gd/<custom_url>).
            
                Please note that if this custom url is unavailable (because it is already used, for example), a :class:`gdshortener.GDShortURLError` will be raised
            
            :type custom_url: str.
            :param log_stat: States if the generated url has statistical analisys attached.
                If the stats are enabled, a special url will show the stats on this shortened url. This special url is returned as second parameters of this function.
                
                Please notice that a stat enabled shorten url counts double in .gd rate exceeding monitor system.
                
                More information on `.gd FAQ <http://is.gd/faq.php#stats>`_ and `.gd rate limit <http://is.gd/usagelimits.php>`_.
            :type log_stat: bool.
            :returns:  (str,str) -- Shortened URL obtained by .gd service and Stat URL if requested (otherwhise is ``None``).
            :raises: **IOError** when timeout with .gd service occurs
                **ValueError** if .gd response is malformed
                :class:`gdshortener.GDMalformedURLError` if the URL provided for shortening is malformed
                :class:`gdshortener.GDShortURLError` if the custom URL requested is not available
                :class:`gdshortener.GDRateLimitError` if the request rate is exceeded for .gd service
                :class:`gdshortener.GDGenericError` in case of generic error from .gd service (mainteinance)
        """
        if url is None or not isinstance(url, basestring) or len(url.strip()) == 0:
            raise GDMalformedURLError('The URL that had to be shorten must be a non empty string')
        # Build data to post
        data = {
            'format': 'json',
            'url': url,
            'logstats': 1 if log_stat else 0
        }
        if custom_url is not None and isinstance(custom_url, basestring) and len(custom_url.strip()) > 0:
            data['shorturl'] = custom_url
        headers = {'User-Agent': self._user_agent}
        f_desc = requests.get("{0}/create.php".format(self.shortener_url), params=data, headers=headers)
        response = json.loads(f_desc.text)
        if 'shorturl' in response:
            # Success!
            return (str(response['shorturl']),
                    None if not log_stat else '{0}/stats.php?url={1}'.format(self.shortener_url, str(response['shorturl'])[str(response['shorturl']).rindex('/') + 1:]))
        else:
            # Error
            error_code = int(response['errorcode'])
            error_description = str(response['errormessage'])
            if error_code == 1:
                raise GDMalformedURLError(error_description)
            if error_code == 2:
                raise GDShortURLError(error_description)
            if error_code == 3:
                raise GDRateLimitError(error_description)
            if error_code == 4:
                raise GDGenericError(error_description)

    def __init__(self, shortener_url=_IS_GD_SHORTENER_URL_, timeout=60,
                 user_agent='Mozilla/5.0 (compatible; GD Shortener Python Module - https://github.com/torre76/gd_shortener/)'):
        """
            Init URL Shortener class
            
            :type shortener_url: str.
            :param shortener_url: base is.gd - v.gd API URL to create shorten link.

                Possible values are:
                
                1. **_IS_GD_SHORTENER_URL_** to obtain *is.gd* shortened url
                2. **_V_GD_SHORTENER_URL_** to obtain *v.gd* shortened url
                

            :param timeout: Timeout in seconds used to connect and obtain shortened URL from .gd service
            :type timeout: int.
            :param user_agent: User Agent used when querying .gd services
            :type user_agent: str.
        """
        self.shortener_url = shortener_url
        self._timeout = timeout
        self._user_agent = user_agent


class ISGDShortener(GDBaseShortener):
    """
        Shortener for `is.gd url shortener <http://is.gd/developers.php>`_.

        :param timeout: Timeout in seconds used to connect and obtain shortened URL from .gd service
        :type timeout: int.  
        :param user_agent: User Agent used when querying .gd services
        :type user_agent: str.
    """

    def __init__(self, timeout=60, user_agent='Mozilla/5.0 (compatible; GD Shortener Python Module - https://github.com/torre76/gd_shortener/)'):
        """
            Init URL Shortener class
            
            :param timeout: Timeout in seconds used to connect and obtain shortened URL from .gd service
            :type timeout: int.
            :param user_agent: User Agent used when querying .gd services
            :type user_agent: str.
        """
        GDBaseShortener.__init__(self, _IS_GD_SHORTENER_URL_, timeout, user_agent)


class VGDShortener(GDBaseShortener):
    """
        Shortener for `v.gd url shortener <http://is.gd/developers.php>`_.

        :param timeout: Timeout in seconds used to connect and obtain shortened URL from .gd service
        :type timeout: int.       
        :param user_agent: User Agent used when querying .gd services
        :type user_agent: str.    
    """

    def __init__(self, timeout=60, user_agent='Mozilla/5.0 (compatible; GD Shortener Python Module - https://github.com/torre76/gd_shortener/)'):
        """
            Init URL Shortener class
            
            :param timeout: Timeout in seconds used to connect and obtain shortened URL from .gd service
            :type timeout: int.
            :param user_agent: User Agent used when querying .gd services
            :type user_agent: str.
        """
        GDBaseShortener.__init__(self, _V_GD_SHORTENER_URL_, timeout, user_agent)
