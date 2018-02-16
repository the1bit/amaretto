
AMArETTo - Azure MAnagEmenT by The1bit
--------------------------------------
Basic install
^^^^^^^^^^^^^
To use (with caution), simply do::
    >>> import pip
    >>> pip.main(['install', '--user', 'amaretto'])
    >>> import amaretto
    >>> print amaretto.showMessage('Your message')
(install without cache: pip install amaretto --no-cache-dir)

Restore module
^^^^^^^^^^^^^^
	>>> import amaretto
	>>> from amaretto import amarettorestore
	>>> amaretto.amarettorestore.storageUriFromCloud('AzureCloud')


Please read the license related information.
