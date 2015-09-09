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
	
or for google code

    from services.googlecode import googlecode
    gcode = googlecode()
    project = gcode.getProject("android-python27")
	
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

