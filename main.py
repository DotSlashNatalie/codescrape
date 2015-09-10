from services.srchub import srchub
from services.googlecode import googlecode
from pprint import pprint

shub = srchub()

projects = shub.getProjects()
#gcode = googlecode()
#project = gcode.getProject("android-python27")
pprint (vars(projects[0]))