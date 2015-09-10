class Release(object):

    fileName = ""
    summary = ""
    fileURL = ""
    checksum = None

    def getFileName(self):
        return self.fileName

    def getSummary(self):
        return self.summary

    def getFileURL(self):
        return self.fileURL

    def getChecksum(self):
        return self.checksum

    def __str__(self):
        return self.getFileName() + " => " + self.getFileURL()

    def __repr__(self):
        return str(self)