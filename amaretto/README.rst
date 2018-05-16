
AMArETTo - Azure MAnagEmenT by The1bit
--------------------------------------

Change log - version 0.0.2.11
-----------------------------
* **Storage**
	* Bugfix in copyFile function. SAS token related copy return value expandation.

Change log - version 0.0.2.10
-----------------------------

* **Storage**
	* Generate SAS Token for StorageAccount
	* SAS token length check has been modified

Change log - version 0.0.2.9
-----------------------------

* **Core** module: Contains functions for login to Azure and set default subscription
* **Restore** module: Contains full support of unmanaged and managed disk based VMs' **DISK** restore.
* **Storage** module: Can upload files to a storage account and store them according to their versions.


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

(install without cache: pip install amaretto --no-cache-dir  )

    Note: 
    After the update please execute the following command from shell 'pip show amaretto' If you can see that not the latest version is installed, please execute 'pip uninstall amaretto' to unistall it.


Core module
-----------
Steps for include restore module
	>>> import amaretto
	>>> from amaretto import amarettocore
	>>> amaretto.amarettocore.azureLogin()

You can find the detailed documentation in https://github.com/the1bit/amaretto/blob/master/amaretto/amarettocore.md.


Restore module
--------------
Steps for include restore module
	>>> import amaretto
	>>> from amaretto import amarettorestore
	>>> amaretto.amarettorestore.storageUriFromCloud('AzureCloud')

You can find the detailed documentation in https://github.com/the1bit/amaretto/blob/master/amaretto/amarettorestore.md.


Storage module
--------------
Steps for include storage module
	>>> import amaretto
	>>> from amaretto import amarettostorage
	>>> amaretto.amarettostorage.uploadAllFiles(fileVersion = '1.0.0.0', storageaccountName = <your storage account name>, sasToken = <sasToken for your storage account>, storageKey = <storageKey for your storage account>, filePath = <local path of flies>, modificationLimitMin = <1440 means you upload files which are older than one day>)

You can find the detailed documentation in https://github.com/the1bit/amaretto/blob/master/amaretto/amarettostorage.md.


Please read the license related information.


