import pycurl
try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
from urllib import urlencode

class Service(object):

    def getProjects(self):
        pass

    def curl_post(self, url, postvals, header = []):
        buffer = StringIO()
        cobj = pycurl.Curl()
        cobj.setopt(pycurl.URL, url)
        cobj.setopt(pycurl.SSL_VERIFYPEER, 0)
        cobj.setopt(pycurl.SSL_VERIFYHOST, 0)
        cobj.setopt(pycurl.POST, 1)
        cobj.setopt(pycurl.WRITEDATA, buffer)
        postdata = urlencode(postvals)
        cobj.setopt(pycurl.POSTFIELDS, postdata)
        cobj.setopt(pycurl.HTTPHEADER, header)
        cobj.perform()
        cobj.close()
        return buffer

    def curl_get(self, url, header = []):
        buffer = StringIO()
        cobj = pycurl.Curl()
        cobj.setopt(pycurl.SSL_VERIFYPEER, 0)
        cobj.setopt(pycurl.SSL_VERIFYHOST, 0)
        cobj.setopt(pycurl.URL, url)
        cobj.setopt(pycurl.WRITEDATA, buffer)
        cobj.setopt(pycurl.HTTPHEADER, header)
        cobj.perform()
        cobj.close()
        return buffer