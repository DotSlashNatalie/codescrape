class IssueComment(object):


    author = ""
    title = ""
    summary = ""
    date = ""

    def getAuthor(self):
        return self.author

    def getTitle(self):
        return self.title

    def getSummary(self):
        return self.summary

    def getDate(self):
        return self.date



class Issue(IssueComment):

    status = ""
    comments = []
    id = -1

    def getId(self):
        return self.id

    def getStatus(self):
        return self.status

    def getCommnets(self):
        return self.comments

    def __str__(self):
        return self.getTitle()

    def __repr__(self):
        return str(self)