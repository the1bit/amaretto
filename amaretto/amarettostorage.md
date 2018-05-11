AmarettoStorage
---------------

Change log - version 1.0.2.0
----------------------------

* Generate SAS Token for StorageAccount
* SAS token length check has been modified


Change log - version 1.0.1.0
----------------------------

* Can upload files to a storage account.
* When you upload a new version of a file it moves to an other directory according its version number.
* The issue in Azure-Cli 2.0.30 - you cannot copy blobs inside storage account only with SAS token - has been fixed in **2.0.32**. [More information](http://www.the1bit.hu/technical-thursday-azure-cli-storage-account-bug-has-been-fixed)

Requirements
------------

* Linux OS

You have to install before the first usage the followings:

* Python (2.7 or 3.4)
* Azure-Cli 2.0


Include module
--------------

Steps for include storage module

```python
	import amaretto
	from amaretto import amarettostorage
	amaretto.amarettostorage.uploadAllFiles(fileVersion = '1.0.0.0', storageaccountName = <your storage account name>, sasToken = <sasToken for your storage account>, storageKey = <storageKey for your storage account>, filePath = <local path of flies>, modificationLimitMin = <1440 means you upload files which are older than one day>)
```

Functions
---------
All steps are developed in this module for each and every copy, upload, delete, manage version steps. Now I write down here how you can upload your files to Azure storage account.

**uploadAllFiles(fileVersion , storageaccountName, sasToken, storageKey = "none", releaseVersion = "latest", filePath = "./files/", containerName = "files", modificationLimitMin = "30")**

* Description: 
	Helps you to upload your files from a directory to your storage account. It uses version number during upload which determines the filesversions when a new version is available.
* Input: 
	* fileVersion: version of files
	* storageaccountName: Your storage account name in Azure
	* sasToken: SAS token which belongs to storage account
	* storageKey: SAS token which belongs to storage account
	* releaseVersion: Your files release version. Default: latest (in this "directory" you can find your files in Azure)
	* filePath: Local path of files
	* containerName: Storage account container name where you would like to upload your files. (It can be used for environemnt separation such as prod, dev)
	* modificationLimitMin: Value in minutes. The module skips that files which is younger than this range. 1440 means you upload files which are older than one day.

* Output: *Status* and *Result* in JSON format.
* Example: 

```python
	fileVersion = "1.0.0.0"
	storageaccountName = "thisismystorage"
	sasToken = "?sv=2017-07-29&ss=b&srt=sco&sp=rwdlac&se=2018-05-31T16:09:48Z&st=2018-05-03T08:59:48Z&spr=https&sig=dp7p3f9G%2B4hvEEoTVuiuIpPAMKssFh2r7AaapyDTl2E%4B"
	filePath = "./upload/"
	sourceContainer = "vhd6bdda0e88c88408299246c468784656546a"
	modificationLimitMin = "1440"

	amaretto.amarettostorage.uploadAllFiles(fileVersion = fileVersion, storageaccountName = storageaccountName, sasToken = sasToken, filePath = filePath, modificationLimitMin = modificationLimitMin)
```

**getStorageKeys(storageAccountName, operation = "live")**

* Description: 
	You can list both storage account keys to a storage account. (If you have access on that storage account)
* Input: 
	* storageaccountName: Your storage account name in Azure
	* operation: Default value is *live*. If you use different value you can test the function with Python unittest module. In test runing it won't list the storage account keys.


* Output: *Status* and *Result* in JSON format. Result contains both keys.
* Example: 

```python
	storageaccountName = "thisismystorage"

	amaretto.amarettostorage.getStorageKeys(storageaccountName = storageaccountName)
```

**newSASToken(storageAccountName, storageAccountKey, expirationInDays = "180", operation = "live"):**

* Description: 
	You can generate SAS Token for your storage account if you have enough access on that.
* Input: 
	* storageaccountName: Your storage account name in Azure
	* storageAccountKey: Key for storage account
	* expirationInDays: Expiration days of SAS Token from now. This is an optional paramaeter. If you don't define in parameterlist it will be 180 days.
	* operation: Default value is *live*. If you use different value you can test the function with Python unittest module. In test runing it won't list the storage account keys.


* Output: *Status* and *Result* in JSON format. Result contains the generated SAS token.
* Example: 

```python
	storageaccountName = "thisismystorage"
	storageAccountKey = "d22j/rr+a7br7LW6KDKV8KZkO2wCIe3m0MTKVr3Tt9B9NMZZsYxny8bvWvPwUGgZpDkE8gyAePjWCVu2IZ4LYw=="

	amaretto.amarettostorage.newSASToken(storageaccountName = storageaccountName, storageAccountKey = storageAccountKey)
```