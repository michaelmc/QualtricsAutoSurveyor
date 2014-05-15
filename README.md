QualtricsAutoSurveyor
=====================

An automator for sending surveys via the Qualtrics REST API, geared toward exports of [Remedy](http://www.bmc.com/it-solutions/remedy-itsm.html "BMC Remedy") user data, but easily configurable for other types of users. Functionally, the steps are:

1. Open a .csv in the same directory
2. Read in a list of individuals with associated information from the .csv
3. Shuffle the users and select some subset of them (set to 25% rounded up currently)
4. Create a new Qualtrics panel and add unique users
5. Send the specified survey to those users with unique user tokens

This can be completely automated if you have some scheduled mechanism to update your .csv, and then run this script on a cronjob or other scheduler.

As-is, the script wants the .csv to be of the form:

<code>\<first name\>,\<last name\>,\<email address\>,\<unique identifier\>,\<other information\></code>

