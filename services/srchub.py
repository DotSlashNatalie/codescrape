from Service import Service
from Project import REPO_TYPES, Project
from Release import Release
from Issue import IssueComment, Issue
from Wiki import Wiki
from bs4 import BeautifulSoup

class srchub(Service):

    DOMAIN = "https://beta.datanethost.net"

    def getProjects(self):
        # Perhaps I should provide more API endpoints to make scraping easier...
        projectlist = self.curl_get(self.DOMAIN + "/projects/").getvalue()
        soup = BeautifulSoup(projectlist, "html.parser")
        links = soup.find("ul", "prjlistclass")
        projects = []
        for link in links.find_all("a"):
            project = Project()
            sourceType = None
            projectURL = self.DOMAIN + link.get("href")
            projectName = projectURL.split("/")[-2]

            projectpageHTML = self.curl_get(projectURL).getvalue()
            projectpageSoup = BeautifulSoup(projectpageHTML, "html.parser")

            sourceURL = projectpageSoup.find(name="a", string="Source").get("href")
            sourceSoup = BeautifulSoup(self.curl_get(self.DOMAIN + sourceURL).getvalue(), "html.parser")
            sourceSoupText = sourceSoup.get_text()

            # get source
            if "git clone" in sourceSoupText:
                project.repoType = REPO_TYPES.git
                project.repoURL = "git://beta.datanethost.net/" + projectName + ".git"
            elif "svn co" in sourceSoupText:
                project.repoType = REPO_TYPES.SVN
                project.repoURL = self.DOMAIN + "/svn/" + projectName + "/"
            else:
                project.repoType = REPO_TYPES.hg
                project.repoURL = self.DOMAIN + "/hg/" + projectName + "/"


            # get downloads
            project.releases = []
            downlaodsSoup = BeautifulSoup(self.curl_get(projectURL + "downloads/").getvalue(), "html.parser")
            downloadSection = downlaodsSoup.find("table", "uploads")
            if "No downloads were found." not in downlaodsSoup.get_text():
                downloadRows = downloadSection.find_all("tr")[1:]
                for downloadRow in downloadRows:
                    cols = downloadRow.find_all("td")
                    downloadTD = cols[0]
                    downloadURL = self.DOMAIN + "/p/" + projectName + "/downloads/get/" + downloadTD.a.text
                    fileName = downloadTD.a.text
                    release = Release()
                    release.fileURL = downloadURL
                    release.fileName = fileName
                    project.releases.append(release)

            # get issues
            project.issues = []
            issuesSoup = BeautifulSoup(self.curl_get(projectURL + "issues/").getvalue(), "html.parser")
            if "No issues were found." not in issuesSoup.get_text():
                issuesSection = issuesSoup.find("table", "recent-issues")
                for issueRow in issuesSection.find_all("tr")[1:]:
                    issue = Issue()
                    cols = issueRow.find_all("td")
                    issueId = cols[0].text
                    issueURL = projectURL + "issues/" + issueId + "/"
                    issueStatus = cols[2].text
                    issueSummary = cols[1].text
                    issueTitle = cols[1].find("a").text
                    issueAuthor = cols[3].text
                    issue.author = issueAuthor
                    issue.comments = []
                    issue.status = issueStatus
                    issue.summary = issueSummary
                    issue.title = issueTitle
                    issue.id = issueId
                    # we must go deeper to get comments
                    issueComments = BeautifulSoup(self.curl_get(issueURL).getvalue(), "html.parser")
                    for comment in issueComments.find_all("div", "issue-comment"):
                        author = comment.find("p").get_text().split("by")[1].split(",")[0]
                        date = comment.find("span").get_text()
                        commentText = comment.find("pre").get_text()
                        issueComment = IssueComment()
                        issueComment.date = date
                        issueComment.author = author
                        issueComment.summary = commentText
                        issue.comments.append(issueComment)

                    project.issues.append(issue)

            # get wiki pages
            project.wikis = []
            wikiSoup = BeautifulSoup(self.curl_get(projectURL + "doc/").getvalue(), "html.parser")
            if "No documentation pages were found." not in wikiSoup.get_text():
                wikiSection = wikiSoup.find("table", "recent-issues")
                for wikiRow in wikiSection.find_all("tr")[1:]:
                    wiki = Wiki()
                    cols = wikiRow.find_all("td")
                    wiki.pageName = cols[0].text
                    wiki.summary = cols[1].text
                    wiki.updated = cols[2].text
                    wikiURL = projectURL + "page/" + wiki.pageName + "/"
                    wikiPageSoup = BeautifulSoup(self.curl_get(wikiURL).getvalue(), "html.parser")
                    wikiContent = wikiPageSoup.find(id="wiki-content")
                    wiki.htmlContent = wikiContent.prettify()
                    wiki.textContent = wikiContent.get_text()
                    project.wikis.append(wiki)


            projects.append(project)

        return projects





