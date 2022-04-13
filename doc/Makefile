# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -j auto
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

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
	cd build/latex && latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode || true
	(test -f build/latex/*.pdf && echo pdf exists) || exit 1

# manually deploy to https://github.com/pyansys/pymapdl-docs
# WARNING: Use with care as this overwrites history of gh-pages
deploy: 
	@echo "*** Warning ***"
	@echo "You are about to deploy to 'PyMAPDL docs'."
	@echo "This overwrites the history of gh-pages."
	@echo "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo "Deploying..."
	touch build/html/.nojekyll
	echo "mapdldocs.pyansys.com" >> build/html/CNAME
	cd build/html && git init
	cd build/html && git add .
	cd build/html && git checkout -b gh-pages
	cd build/html && git commit -am "manual build"
	cd build/html && git remote add origin https://github.com/pyansys/pymapdl-docs
	cd build/html && git push -u origin gh-pages --force
	rm -rf build/html/.git
