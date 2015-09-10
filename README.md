# codescrape

Version 1.0

By: Nathan Adams

License: MIT

## Description

This library is to be used to archive project data. Since with the announcement of Google Code going to archive only - I wanted to create a library where you can grab source data before it is gone forever.

Use cases include:

Archive projects due to:

- Hosting service shutting down
- Authorities sending cease-and-desist against provider/project
- Historical/research/ or educational purposes

## Usage

Currently srchub and google code are supported. To use:

    from services.srchub import srchub
    shub = srchub()
    projects = shub.getProjects()
    
### Sample structure

    {'issues': [],
     'releases': [],
     'repoType': 1,
     'repoURL': u'git://beta.datanethost.net/bug60.git',
     'wikis': [test]}
	
or for google code

    from services.googlecode import googlecode
    gcode = googlecode()
    project = gcode.getProject("android-python27")
	
### Sample structure

    {'issues': [  libs/armeabi/libcom_googlecode_android_scripting_Exec.so  read problem ,
                  How to stop Python Script Service ? ,
                  Does not work on GoogleTV ,
                  App crashes when trying to launch camera on phone ,
                  com.android.pyton27.process.Process does not write log ,
                  test.py from python_scripts_r13 does not run ,
                  End all services ,
                  SL4A Title grey bar ,
                  Can not import md5, sha1 ,
                  Patch for /apk/src/com/googlecode/android_scripting/facade/FacadeConfiguration.java ,
                  Add PyCrypto module ,
                  myScript.py wont work ,
                  Microsoft Acess DB(.mdb) in Python APK ,
                  Unable to generate PyDroid.apk from the sample project Pydroid ,
                  Python sl4a sendText not working ,
                  Patch for /python-build/functions.sh ,
                  Using Home/Recent button restarts apk ,
                  Add modules ,
                  Errors using the ADT Bundle for Windows with android-python27 clone ,
                  errors building python_27.zip and python_extras_27.zip ,
                  How to use PyQT? ,
                  Bluetooth-based Scripts cannot launch from APK ,
                  Undocumented how to distribute egg libraries in self-contained APK ,
                  How to retrieve errors? ,
                  android-python27 - Permission issues after bundling Python 3 into my app ,
                  cannot load library ,
                  Executed APK is crashing in every scenario ,
                  Support for Samsung Chord API ,
                  LookupError: unknown encoding: hex ,
                  Log traceback on broken hello.py ,
                  How to run a python script with root privileges using PythonAPK? ,
                  Is there any way to use python-2.7.5 ,
                  How to Import SL4A Libraries ,
                  How to use SL4A on PyDroid ,
                  android-python installs but cannot launch doInBackground() ,
                  libssl might be affected by heartbleed bug ,
                  How can I pass String value from EditText In Android Activity to Python Script  and also make the activity able to retrieve the String result from a function in the python script ?  ,
                  Interaction with python file ,
                  Install on external storage ,
                  Can't install android-python27 to Samsung Galaxy 4 ,
                  how to create android app in eclipse using python code on windows 8 ],
     'releases': [PythonAPK.apk => https://android-python27.googlecode.com/files/PythonAPK.apk],
     'repoType': 2,
     'repoURL': 'https://code.google.com/p/android-python27/',
     'wikis': [Tutorial on how to run Python from the shell,
               Debugging your Python app in Android,
               Tutorial on how to install the Android SDK and Eclipse,
               Create scripts on your PC and run them on your Android device,
               Tutorial on how to create a custom RPC facade,
               Tutorial on how to create a custom APK,
               Tutorial on how to update with latest SL4A,
               Tutorial on how to change the Python builds,
               Tutorial on how to use the APK template,
               Tutorial on how to add your Python scripts to the template project,
               Overview on how Python embedding works.]}
	
Sourcehub library will pull all public projects since this list is easily accessed. Google Code does not have a public list persay. And I didn't want to scrape the search results, so I developed it to require you to pass in the project name. If you were to get your hands on a list of google code projects you could easily loop through them:

    from services.googlecode import googlecode
    gcode = googlecode()
    for project in someProjectList:
	    project = gcode.getProject(project)
        # do something with project
		
the project data structure is as follows:

project

- getRepoURL() -> Returns the URL of the repo
- getRepoType() -> Returns the type of repo (git, hg, or SVN)
- getReleases() -> Returns all downloads related to the project
- getIssues() -> Returns open issues
- getWikis() -> Returns wikis

