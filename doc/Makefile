# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -j auto
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
LINKCHECKDIR  = $(SPHINXBUILD)/linkcheck

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


# customized clean due to examples gallery
clean:
	rm -rf $(BUILDDIR)/*
	rm -rf source/examples/gallery_examples
	find . -type d -name "_autosummary" -exec rm -rf {} +

# customized clean due to examples gallery
clean-except-examples:
	rm -rf $(BUILDDIR)/*
	rm -rf images/auto-generated
	find . -type d -name "_autosummary" -exec rm -rf {} +

# customized to build the pdf rather than using latexpdf due to various issues
# with our docs like GIFs being written as PNG.
pdf:
	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	python validate_png.py  # clean-up GIFs mislabeled as PNG
	cd $(SPHINXBUILD)/latex && latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode || true
	(test -f $(SPHINXBUILD)/latex/*.pdf && echo pdf exists) || exit 1

checklinks:
	$(SPHINXBUILD) -b linkcheck $(SPHINXOPTS) $(LINKCHECKDIR)
	@echo
	@echo "Check finished. Report is in $(LINKCHECKDIR)."

# manually deploy to https://github.com/pyansys/pymapdl-docs
# WARNING: Use with care as this overwrites history of gh-pages
deploy: 
	@echo "*** Warning ***"
	@echo "You are about to deploy to 'PyMAPDL docs'."
	@echo "This overwrites the history of gh-pages."
	@echo "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo "Deploying..."
	touch $(SPHINXBUILD)/html/.nojekyll
	echo "mapdl.docs.pyansys.com" >> build/html/CNAME
	cd $(SPHINXBUILD)/html && git init
	cd $(SPHINXBUILD)/html && git add .
	cd $(SPHINXBUILD)/html && git checkout -b gh-pages
	cd $(SPHINXBUILD)/html && git commit -am "manual build"
	cd $(SPHINXBUILD)/html && git remote add origin https://github.com/pyansys/pymapdl-docs
	cd $(SPHINXBUILD)/html && git push -u origin gh-pages --force
	rm -rf $(SPHINXBUILD)/html/.git
