import sys
from kicad import Project

filePath0 = sys.argv[1]
filePath1 = sys.argv[2]

proj0 = Project(filePath0)
proj1 = Project(filePath1)
proj0.diffReport(proj1)
