
AmarettoCore
------------


Change log - version 1.1.1.0
----------------------------

* Contains functions for login to Azure and set default subscription


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
	>>> from amaretto import amarettocore
	>>> amaretto.amarettocore.azureLogin()


Functions
---------

**azureLogin()**

* Description: 
	Helps you to login to Azure. When you execute this it asks the subscriptionCloud, subscriptionLocation and subscriptionId for Azure subsription. Then you have to type the username and password for your subscription.
* Input: -
* Output: -
* Note:
	It does not set the default subscription (if you have more than 1 subscription for same account). For this operation you can use the *defaultSubscription* function.
* Example: 
	>>> amaretto.amarettocore.azureLogin()


**defaultSubscription(subscriptionID)**

* Description: 
	Helps you to select the default subscription among the subscriptions which belong to your account.
* Input: default subscription Id. 
* Output: *True* if the operation is success and *False* if something went wrong.
* Note:
* Example: 
	>>> amaretto.amarettocore.defaultSubscription("57a1gdff-e67c-5432-9876-gdh18j5j4677")	

**getDefaultSubscription()**

* Description: 
	Helps you to get the default subscription related information.
* Input: - 
* Output: JSON wit envirinment name, subscription id, subscription name and username
* Note:
* Example: 
	>>> amaretto.amarettocore.getDefaultSubscription()	
