AmarettoRestore
---------------

Change log - version 1.2.0.0
----------------------------

* Contains full support of unmanaged and managed disk based VMs' **DISK** restore


Requirements
------------

* Linux OS

You have to install before the first usage the followings:

* Python (2.7 or 3.4)
* Azure-Cli 2.0


Include module
--------------

Steps for include restore module
	>>> import amaretto
	>>> from amaretto import amarettorestore
	>>> amaretto.amarettorestore.storageUriFromCloud('AzureCloud')


Functions
---------
All steps are developed in this module for each and every restore steps such as download config.json, deallocate VM, delete VM object. Now I write down here the "huge" restore functions which contain the all necessary steps.

**restoreUnmanagedDiskFromVhd(vmName, resourceGroup, location, storageAccount, secretKey, sourceContainer, vmContainer = "vhds", sourceStorageAccount = "", sourceSecretKey = "")**

* Description: 
	Helps you to restore a restored Vm's vhds to their original location with their original names. Additionally it deletes the VM object itself which is a requirements for VM restore.
* Input: 
	* vmName: restorable VM's name
	* resourceGroup: resource group name where the VM is located
	* location: location where the resources are located. (westeurope, germanycentral, ...)
	* storageAccount: storage account name where the VM's vhds are stored
	* secretKey: 1st or 2nd access key for *storageAccount*.
	* sourceContainer: name of container where the restored vhds are stored 
	* vmContainer (optional): container name in *storageAccount* where the VM's vhds are stored. Defauld value: vhds
	* sourceStorageAccount (optional): You can define the source storage account name if you restored the vhds to different storage account than the VM's *storageAccount*. Defauld value: vaue of *storageAccount*
	* sourceSecretKey (optional): 1st or 2nd access key for *sourceStorageAccount*. if you restored the vhds to different storage account than the VM's *storageAccount*. Defauld value: vaue of *secretKey*

* Output: *True* if the operation is success and *False* if something went wrong.
* Note:
	* You have to use the following naming convenction for osdisk: *[vmname]-osdisk.vhd*
	* You have to use the following naming convenction for datadisk: *[vmname]-datadisk-[diskid].vhd* (where the diskid represents the value of lun)
* Example: 
	>>> vmName = "thisismyserver-1"
	>>> resourceGroup = "thisismyrg"
	>>> location = "westeurope"
	>>> storageAccount = "thisismystorage"
	>>> secretKey = "d22j/rr+a7br7LW6KDKV8KZkO2wCIe3m0MTKVr3Tt9B9NMZZsYxny8bvWvPwUGgZpDkE8gyAePjWCVu2IZ4LYw=="
	>>> sourceContainer = "vhd6bdda0e88c88408299246c468784656546a"
	>>>
	>>> amaretto.amarettorestore.restoreUnmanagedDiskFromVhd(vmName, resourceGroup, location, storageAccount, secretKey, sourceContainer)


**restoreManagedDiskFromVhd(vmName, resourceGroup, location, sourceStorageAccount, sourceSecretKey, sourceContainer, managedDiskAccountType = "Standard_LRS")**

* Description: 
	Helps you to restore a restored Vm's vhds to their original location with their original names. Additionally it deletes the VM object itself which is a requirements for VM restore.
* Input: 
	* vmName: restorable VM's name
	* resourceGroup: resource group name where the VM is located
	* location: location where the resources are located. (westeurope, germanycentral, ...)
	* sourceStorageAccount: storage account name where the VM's restored vhds are stored
	* secretKey: 1st or 2nd access key for *sourceStorageAccount*.
	* sourceContainer: name of container where the restored vhds are stored 
	* managedDiskAccountType (optional): sku of disk. Possible values: *Standard_LRS* or *Premium_LRS*. Default value: *Standard_LRS*


* Output: *True* if the operation is success and *False* if something went wrong.
* Note:
	* You have to use the following naming convenction for osdisk: *[vmname]-osdisk*
	* You have to use the following naming convenction for datadisk: *[vmname]-datadisk-[diskid]* (where the diskid represents the value of lun)
* Example: 
	>>> vmName = "thisismyserver-2"
	>>> resourceGroup = "thisismyrg"
	>>> location = "westeurope"
	>>> sourceStorageAccount = "thisismystorage"
	>>> sourceSecretKey = "d22j/rr+a7br7LW6KDKV8KZkO2wCIe3m0MTKVr3Tt9B9NMZZsYxny8bvWvPwUGgZpDkE8gyAePjWCVu2IZ4LYw=="
	>>> sourceContainer = "vhd6bdda0e88c88408299246c468784656546a"
	>>> 
	>>> amaretto.amarettorestore.restoreManagedDiskFromVhd(vmName, resourceGroup, location, sourceStorageAccount, sourceSecretKey, sourceContainer)
