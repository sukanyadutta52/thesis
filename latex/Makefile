# Makefile for thesis compilation
THESIS = thesis
ROOT_DIR = ..

.PHONY: all clean full-build copy-pdf help build rebuild

# Default target
all: $(THESIS).pdf copy-pdf

# Full compilation with bibliography
full-build: clean
	pdflatex --shell-escape $(THESIS).tex
	biber $(THESIS)
	pdflatex --shell-escape $(THESIS).tex
	pdflatex --shell-escape $(THESIS).tex
	$(MAKE) copy-pdf

# Quick compilation (no bibliography)
quick:
	pdflatex --shell-escape $(THESIS).tex
	$(MAKE) copy-pdf

# Copy PDF to root directory
copy-pdf: $(THESIS).pdf
	@echo "Copying $(THESIS).pdf to root directory..."
	@rm -f $(ROOT_DIR)/$(THESIS).pdf 2>/dev/null || true
	@if cp $(THESIS).pdf $(ROOT_DIR)/$(THESIS).pdf 2>/dev/null; then \
		echo "PDF copied successfully!"; \
	else \
		echo "Warning: Could not copy PDF (file may be open in Windows)"; \
		echo "Please close the PDF viewer and run 'make copy-pdf' again"; \
	fi

# Build using latexmk (like root Makefile)
build:
	mkdir -p build/chapters/chapter_1 build/chapters/chapter_2 build/chapters/chapter_3 build/chapters/chapter_4 build/chapters/chapter_5 build/chapters/chapter_6 build/chapters/chapter_7 build/svg-inkscape
	latexmk -pdf -shell-escape -interaction=nonstopmode -outdir=build $(THESIS).tex
	@echo "Copying $(THESIS).pdf to root directory..."
	@rm -f $(ROOT_DIR)/$(THESIS).pdf 2>/dev/null || true
	@if cp build/$(THESIS).pdf $(ROOT_DIR)/$(THESIS).pdf 2>/dev/null; then \
		echo "PDF copied successfully!"; \
	else \
		echo "Warning: Could not copy PDF (file may be open in Windows)"; \
		echo "Please close the PDF viewer and run 'make copy-pdf' again"; \
	fi

# Rebuild target
rebuild: clean build

# Clean build artifacts (but keep root PDF)
clean:
	rm -f *.aux *.bbl *.bcf *.blg *.idx *.ilg *.ind *.log *.out *.run.xml *.synctex.gz *.toc *.lof *.lot *.fdb_latexmk *.fls
	rm -rf build/
	rm -f *.pdf
	rm -f $(ROOT_DIR)/$(THESIS).pdf

# Clean everything (same as clean now)
clean-all: clean

# Help
help:
	@echo "Available targets:"
	@echo "  all        - Quick build and copy PDF to root"
	@echo "  build      - Build using latexmk with build directory"
	@echo "  rebuild    - Clean and build using latexmk"
	@echo "  full-build - Complete build with bibliography"
	@echo "  quick      - Quick build (no bibliography)"
	@echo "  copy-pdf   - Copy PDF to root directory"
	@echo "  clean      - Clean build artifacts"
	@echo "  clean-all  - Clean everything including root PDF"
	@echo "  help       - Show this help"