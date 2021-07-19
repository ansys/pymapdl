---
name: Bug report
about: Create a report to help us improve
title: ''
labels: Bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**System Information:**
 - OS: [e.g. iOS]
 - Ansys version (E.g. 2020R2)
 - PyMAPDL version (E.g. 0.59.1)

**Additional context**
Add any other context about the problem here.

**Run a PyMAPDL report**

Please run the following code wherever you are experiencing the bug and paste the output below. This report helps us track down bugs and it is critical to addressing your bug:

```Python
from ansys.mapdl import core as pymapdl
print(pymapdl.Report())
```

```
# Paste your results here
```
