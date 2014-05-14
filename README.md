QualtricsAutoSurveyor
=====================

A script to automate sending surveys via the Qualtrics REST API. The steps include:

1. Open a .csv in the same directory
2. Read in a list of individuals with associated information
3. Shuffle the users
4. Create a new Qualtrics panel and add unique users
5. Send the specified survey to those users
