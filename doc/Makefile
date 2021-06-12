# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
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
	rm -rf build
	rm -rf source/examples
	find . -type d -name 'api' -exec rm -rf {} +

# build and upload html to the doc host
upload: html
	tar -C build/ -czf docs.tar.gz html
	scp docs.tar.gz web-redirect:/tmp/
	rm docs.tar.gz
