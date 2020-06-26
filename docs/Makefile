# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python3.7 -msphinx
SPHINXPROJ    = pyansys
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf examples/
	rm -f errors.txt

deploy:
	rm -rf /tmp/pyansys
	cd /tmp; git clone --single-branch --branch gh-pages https://$(github_pat)@github.com/akaszynski/pyansys.git
	rm -rf /tmp/pyansys/*
	cp -r _build/html/* /tmp/pyansys/
	touch /tmp/pyansys/.nojekyll
	cd /tmp/pyansys; git add .
	cd /tmp/pyansys; git commit -am "Manual build"
	cd /tmp/pyansys; git push


# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
