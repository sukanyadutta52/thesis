.PHONY: build clean all

# Default target
all: build

# Build the thesis
build:
	cd latex && mkdir -p build/chapters/chapter_1 build/chapters/chapter_2 build/chapters/chapter_3 build/chapters/chapter_4 build/chapters/chapter_5 build/chapters/chapter_6 build/chapters/chapter_7
	cd latex && latexmk -pdf -interaction=nonstopmode -outdir=build thesis.tex
	cd latex && cp build/thesis.pdf .

# Clean all build files
clean:
	cd latex && latexmk -C -outdir=build
	cd latex && rm -f thesis.pdf
	cd latex && rm -rf build

# Clean and rebuild
rebuild: clean build