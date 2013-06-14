"""
.. currentmodule: gdshortener

    :synopsis: Module that enables the use of `is.gd - v.gd url shortener <http://is.gd/developers.php>`_.
"""

class GDBaseException(Exception):
    '''
        Base Exception class that handles `is.gd <http://is.gd/>`_  error codes.
        
        :param error_code: Error code obtained from is.gd. See `Interpreting error code section <http://is.gd/developers.php>`_ on is.gd dev guide.
        :type error_code: int.
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    '''
    
    def __str__(self):
        return "Error code: [{error_code}] - Error description: [{error_description}]".format(error_code = self.error_code, error_description = self.error_description)
    
    def __repr__(self):
        return "<{error_instance}({error_code}, {error_description})>".format(error_instance = self.__class__.__name__, error_code = self.error_code, error_description = self.error_description)
    
    @property
    def error_code(self):
        '''
            `is.gd <http://is.gd/>`_ error code:
            
            - error code *1*: there was a problem with the original long URL provided
            - error code *2*: there was a problem with the short URL provided (for custom short URLs)
            - error code *3*: our rate limit was exceeded (your app should wait before trying again)
            - error code *4*: any other error (includes potential problems with our service such as a maintenance period)
            
            :returns: int.
            
        '''
        return self._error_code
    
    @property
    def error_description(self):
        '''
            `is.gd <http://is.gd/>`_ description for this error.
            
            :returns: str.
        '''
        return self._error_description
    
    def __init__(self, error_code = 4, error_description = None):
        '''
            Init the exception with code and description taken from `is.gd <http://is.gd/>`_.
            
            :param error_code: Error code obtained from is.gd. See `Interpreting error code section <http://is.gd/developers.php>`_ on is.gd dev guide.
            :type error_code: int.
            :param error_description: Error description obtained from is.gd
            :type error_description: str.
        '''
        self._error_code = error_code
        self._error_description = error_description
        

class GDMalformedURLError(GDBaseException):
    '''
        This exceptions identify a problem with the URL that had to be shortened.
        
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    '''
    
    def __init__(self, error_description = None):
        '''
            Init the exception with description taken from `is.gd <http://is.gd/>`_.
            
            :param error_description: Error description obtained from is.gd
            :type error_description: str.            
        '''
        GDBaseException.__init__(self, 1, error_description)
 
        
class GDShortURLError(GDBaseException):
    '''
        This exceptions identify a problem with the shortened URL.
        
        Could be either an error on custom shortener URL or a copyright error on a URL (in which case it could had been disabled)
        
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    '''
    
    def __init__(self, error_description = None):
        '''
            Init the exception with description taken from `is.gd <http://is.gd/>`_.
            
            :param error_description: Error description obtained from is.gd
            :type error_description: str.            
        '''
        GDBaseException.__init__(self, 2, error_description)    
        
class GDRateLimitError(GDBaseException):
    '''
        This exceptions is raised when is.gd rate limit has been exceeded.
        
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    '''
    
    def __init__(self, error_description = None):
        '''
            Init the exception with description taken from `is.gd <http://is.gd/>`_.
            
            :param error_description: Error description obtained from is.gd
            :type error_description: str.            
        '''
        GDBaseException.__init__(self, 3, error_description)       
        
class GDGenericError(GDBaseException):
    '''
        This exceptions is raised when is.gd states a generic problem.
        
        Further informations are provided on error description.
        
        :param error_description: Error description obtained from is.gd
        :type error_description: str.        
    '''
    
    def __init__(self, error_description = None):
        '''
            Init the exception with description taken from `is.gd <http://is.gd/>`_.
            
            :param error_description: Error description obtained from is.gd
            :type error_description: str.            
        '''
        GDBaseException.__init__(self, 4, error_description)               