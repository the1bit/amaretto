
AMArETTo - Azure MAnagEmenT by The1bit
--------------------------------------

Change log - version 0.0.2.5
----------------------------

* **Core** module: Contains functions for login to Azure and set default subscription
* **Restore** module: Contains full support of unmanaged and managed disk based VMs' **DISK** restore.

Requirements
------------

* Linux OS

You have to install before the first usage the followings:

* Python (2.7 or 3.4)
* Azure-Cli 2.0


Basic install
-------------

To use the tools you merely follow the following steps:
    >>> import pip
    >>> pip.main(['install', '--user', 'amaretto'])
    >>> import amaretto
    >>> print amaretto.showMessage('Your message')

(install without cache: pip install amaretto --no-cache-dir  )

    Note: 
    After the update please execute the following command from shell 'pip show amaretto' If you can see that not the latest version is installed, please execute 'pip uninstall amaretto' to unistall it.


Core module
-----------
Steps for include restore module
	>>> import amaretto
	>>> from amaretto import amarettocore
	>>> amaretto.amarettocore.azureLogin()

You can find the detailed documentation in `amarettocore.rst <https://github.com/the1bit/amaretto/blob/master/amaretto/amarettocore.rst>`_ .


Restore module
--------------
Steps for include restore module
	>>> import amaretto
	>>> from amaretto import amarettorestore
	>>> amaretto.amarettorestore.storageUriFromCloud('AzureCloud')

You can find the detailed documentation in `amarettorestore.rst <https://github.com/the1bit/amaretto/blob/master/amaretto/amarettorestore.rst>`_ .


Please read the license related information.