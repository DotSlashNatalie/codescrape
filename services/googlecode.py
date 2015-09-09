from Service import Service
from Project import REPO_TYPES, Project
from Release import Release
from Issue import IssueComment, Issue
from Wiki import Wiki
from bs4 import BeautifulSoup


class googlecode(Service):

    DOMAIN = "https://code.google.com"

    # Since I want to stay on Google's good side
    # I'm going to write this method to parse a single project
    # You will need to provide your own project list to roll through
    # Such a list exists (although incomplete)
    # http://flossdata.syr.edu/data/gc/2012/2012-Nov/gcProjectInfo2012-Nov.txt.bz2
    def getProject(self, projectName):
        project = Project()
        sourceType = None
        projectURL = self.DOMAIN + "/p/" + projectName + "/"

        projectpageHTML = self.curl_get(projectURL).getvalue()
        projectpageSoup = BeautifulSoup(projectpageHTML, "html.parser")

        sourceURL = projectpageSoup.find(name="a", string="Source").get("href")
        sourceSoup = BeautifulSoup(self.curl_get(self.DOMAIN + "/p/" + sourceURL).getvalue(), "html.parser")
        sourceSoupText = sourceSoup.get_text()

        # get source
        if "git clone" in sourceSoupText:
            project.repoType = REPO_TYPES.git
            project.repoURL = "https://code.google.com/p/" + projectName + "/"
        elif "svn co" in sourceSoupText:
            project.repoType = REPO_TYPES.SVN
            project.repoURL = "http://" + projectName + ".googlecode.com/svn/"
        else:
            project.repoType = REPO_TYPES.hg
            project.repoURL = "https://code.google.com/p/" + projectName + "/"


        # get downloads
        project.releases = []
        downlaodsSoup = BeautifulSoup(self.curl_get(projectURL + "downloads/list").getvalue(), "html.parser")
        downloadSection = downlaodsSoup.find("table", "results")
        if "Your search did not generate any results." not in downlaodsSoup.get_text():
            downloadRows = downloadSection.find_all("tr")[1:]
            for downloadRow in downloadRows:
                cols = downloadRow.find_all("td")
                downloadTD = cols[1]
                downloadURL = "https://" + projectName + ".googlecode.com/files/" + downloadTD.a.text.replace("\n", "").strip(" ")
                fileName = downloadTD.a.text.replace("\n", "").strip(" ")
                release = Release()
                release.fileURL = downloadURL
                release.fileName = fileName
                project.releases.append(release)

        # get issues
        project.issues = []
        issuesSoup = BeautifulSoup(self.curl_get(projectURL + "issues/list").getvalue(), "html.parser")
        if "Your search did not generate any results." not in issuesSoup.get_text():
            issuesSection = issuesSoup.find("table", "results")
            for issueRow in issuesSection.find_all("tr")[1:]:
                issue = Issue()
                cols = issueRow.find_all("td")
                issueId = cols[1].text.replace("\n", "").strip()
                issueURL = projectURL + "issues/detail?id=" + issueId
                issueStatus = cols[3].text.replace("\n", "").strip(" ")
                issueSummary = cols[8].text.replace("\n", "")
                issueTitle = cols[8].text.replace("\n", "")
                issueAuthor = cols[5].text.replace("\n", "")

                #issue.author = issueAuthor
                issue.comments = []
                issue.status = issueStatus.strip(" ")
                issue.summary = issueSummary.strip(" ")
                issue.title = issueTitle
                issue.id = issueId

                # we must go deeper to get comments
                issueComments = BeautifulSoup(self.curl_get(issueURL).getvalue(), "html.parser")
                for comment in issueComments.find_all("div", "vt"):
                    #author = comment.find(class_="author").find("a").text
                    author = (comment.find(class_="author").find_all("a")[-1]).contents
                    date = comment.find("span", "date")["title"]
                    commentText = comment.find("pre").get_text()
                    issueComment = IssueComment()
                    issueComment.date = date
                    issueComment.author = author
                    issueComment.summary = commentText
                    issue.comments.append(issueComment)

                project.issues.append(issue)

        # get wiki pages
        project.wikis = []
        wikiSoup = BeautifulSoup(self.curl_get(projectURL + "w/list").getvalue(), "html.parser")
        if "Your search did not generate any results." not in wikiSoup.get_text():
            wikiSection = wikiSoup.find("table", "results")
            for wikiRow in wikiSection.find_all("tr")[1:]:
                wiki = Wiki()
                cols = wikiRow.find_all("td")
                wiki.pageName = cols[1].text.replace("\n", "").strip(" ")
                wiki.summary = cols[2].text.replace("\n", "").strip(" ")
                wiki.updated = cols[3].text.replace("\n", "").strip(" ")
                wikiURL = projectURL + "wiki/" + wiki.pageName
                wikiPageSoup = BeautifulSoup(self.curl_get(wikiURL).getvalue(), "html.parser")
                wikiContent = wikiPageSoup.find(id="wikicontent")
                wiki.htmlContent = wikiContent.prettify()
                wiki.textContent = wikiContent.get_text()
                project.wikis.append(wiki)

        return project