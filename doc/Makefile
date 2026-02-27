# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.

SPHINXBUILDORIG = sphinx-build
SOURCEDIR     = source
BUILDDIR      = _build
LINKCHECKDIR  = $(BUILDDIR)/linkcheck
SPHINXOPTS    = -j auto --color
LINKCHECKOPTS = -d $(BUILDDIR)/.doctrees -W --keep-going --color

# For codespaces
ON_CS  = $$(echo $(ON_CODESPACES) | tr A-Z a-z) # to lowercase
SPHINXBUILD := $(shell [ $(ON_CS) = "true" ] && echo "xvfb-run $(SPHINXBUILDORIG)" || echo "$(SPHINXBUILDORIG)")
MSG = $(shell [ $(ON_CS) = "true" ] && echo "On codespaces. Using xvfb.")

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILDORIG) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
ifeq ($(strip $(MSG)), )
else
	$(info $(MSG))
endif

	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# customized clean due to examples gallery
clean:
	@echo "Cleaning everything."
	rm -rf $(BUILDDIR)/*
	rm -rf images/auto-generated
	rm -rf source/examples/gallery_examples
	find . -type d -name "_autosummary" -exec rm -rf {} +

# customized clean due to examples gallery
clean-except-examples:
	@echo "Cleaning everything except the examples."
	rm -rf $(BUILDDIR)/*
	find . -type d -name "_autosummary" -exec rm -rf {} +

# clean only examples
clean-examples:
	@echo "Cleaning only the examples."
	rm -rf source/examples/gallery_examples

# customized to build the pdf rather than using latexpdf due to various issues
# with our docs like GIFs being written as PNG.
pdf:
ifeq ($(strip $(MSG)), )
else
	$(info $(MSG))
endif

	@$(SPHINXBUILD) -M latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	python post_process_tex.py  # post-process latex file after sphinx build and before latex build
	cd $(BUILDDIR)/latex && latexmk -r latexmkrc -pdf *.tex -interaction=nonstopmode || true
	(test -f $(BUILDDIR)/latex/pymapdl-Documentation-*.pdf && echo "pdf exists!") || exit 1
	qpdf --check $(BUILDDIR)/latex/pymapdl-Documentation-*.pdf && echo "File is OK" && exit 0 || echo "File is corrupt" && exit 1

linkcheck:
ifeq ($(strip $(MSG)), )
else
	$(info $(MSG))
endif

	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(LINKCHECKOPTS)
	@echo
	@echo "Check finished. Report is in $(LINKCHECKDIR)."

html-noexamples:
ifeq ($(strip $(MSG)), )
else
	$(info $(MSG))
endif

	@echo "Building gallery without running examples."
	@$(SPHINXBUILD) -D plot_gallery=0 -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

start-webserver:
	@echo "Starting Python server."
	@(./start_webserver.sh)

stop-webserver:
	@echo "Stopping web server"
	@(./stop_webserver.sh)
