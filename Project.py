from enum import enum

REPO_TYPES = enum("SVN", "git", "hg", "NA")

class Project(object):

    repoURL = ""
    releases = []
    issues = []
    wikis = []
    repoType = REPO_TYPES.NA

    def getRepoURL(self):
        return self.repoURL

    def getReleases(self):
        return self.releases

    def getIssues(self):
        return self.issues

    def getRepoType(self):
        return self.repoType

    def getWikis(self):
        return self.wikis