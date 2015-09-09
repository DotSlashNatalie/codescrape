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