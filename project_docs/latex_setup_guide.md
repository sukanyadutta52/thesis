# LaTeX Setup Guide for Windows

## Installing MiKTeX

1. **Download MiKTeX:**
   - Visit: https://miktex.org/download
   - Download the Windows installer (64-bit recommended)
   - Current version: MiKTeX 24.1

2. **Installation Steps:**
   - Run the installer as administrator
   - Choose "Install for all users" (recommended)
   - Select installation directory (default is fine)
   - Configure settings:
     - Paper size: A4
     - Install missing packages: "Yes" (automatic)
   - Complete installation

3. **Post-Installation:**
   - Open MiKTeX Console
   - Check for updates: "Updates" → "Check for updates"
   - Install essential packages:
     - babel-english
     - biblatex
     - biber
     - apa7 (for APA style)

## Installing TeXstudio

1. **Download TeXstudio:**
   - Visit: https://www.texstudio.org/
   - Download Windows installer
   - Choose stable version

2. **Installation:**
   - Run installer
   - Default settings are fine
   - Will auto-detect MiKTeX

3. **Configuration:**
   - Open TeXstudio
   - Options → Configure TeXstudio
   - Build settings:
     - Default Compiler: PdfLaTeX
     - Default Bibliography: Biber
   - Editor settings:
     - Line numbers: Show
     - Word wrap: Soft wrap at window edge

## Compiling Your Thesis

### In TeXstudio:
1. Open `latex/main.tex`
2. Press F5 (Quick Build) or:
   - Tools → Build & View
3. For bibliography:
   - Tools → Bibliography (F8)
   - Then compile twice more (F5)

### Command Line:
```bash
cd D:\Thesis\latex
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## Alternative: VS Code Setup

If you prefer VS Code:

1. **Install VS Code Extensions:**
   - LaTeX Workshop (James Yu)
   - LaTeX Utilities

2. **Settings (settings.json):**
```json
{
  "latex-workshop.latex.autoBuild.run": "onFileChange",
  "latex-workshop.latex.tools": [
    {
      "name": "pdflatex",
      "command": "pdflatex",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "%DOC%"
      ]
    },
    {
      "name": "biber",
      "command": "biber",
      "args": ["%DOCFILE%"]
    }
  ],
  "latex-workshop.latex.recipes": [
    {
      "name": "pdflatex → biber → pdflatex × 2",
      "tools": [
        "pdflatex",
        "biber",
        "pdflatex",
        "pdflatex"
      ]
    }
  ]
}
```

## Troubleshooting

### Common Issues:

1. **"LaTeX Error: File not found"**
   - Install missing package via MiKTeX Console
   - Or let MiKTeX auto-install (if configured)

2. **Bibliography not showing:**
   - Run Biber after first compilation
   - Compile main.tex twice after Biber

3. **PDF not updating:**
   - Close PDF viewer
   - Delete auxiliary files (.aux, .bbl, etc.)
   - Recompile

4. **Encoding issues:**
   - Ensure files saved as UTF-8
   - Use `\usepackage[utf8]{inputenc}`

### Useful Commands:

```bash
# Clean auxiliary files
del *.aux *.bbl *.blg *.log *.out *.toc *.bcf *.run.xml

# Full compilation
pdflatex main && biber main && pdflatex main && pdflatex main

# Check LaTeX installation
pdflatex --version
biber --version
```

## Additional Tools

### Reference Management:
- **Zotero** (recommended)
  - Install Better BibTeX plugin
  - Export to .bib format
  
- **Mendeley**
  - Direct BibTeX export

### Spell Checking:
- TeXstudio has built-in spell check
- VS Code: Install "Spell Right" extension

### Version Control:
- Use Git (already initialized)
- Commit regularly:
```bash
git add .
git commit -m "Chapter X progress"
```

## LaTeX Resources

### Documentation:
- [Overleaf Documentation](https://www.overleaf.com/learn)
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)
- [CTAN Package Archive](https://ctan.org/)

### Thesis-Specific:
- [TU Darmstadt Templates](https://www.tu-darmstadt.de/studieren/abschluss/templates)
- [Academic Writing Guide](https://www.ulb.tu-darmstadt.de/schreiben)

### Quick References:
- [LaTeX Symbols](http://detexify.kirelabs.org/classify.html)
- [Table Generator](https://www.tablesgenerator.com/)
- [TikZ Examples](https://texample.net/tikz/examples/)

## Daily Workflow

1. **Morning Setup:**
   ```bash
   cd D:\Thesis
   git pull (if using remote)
   ```

2. **Writing Session:**
   - Open TeXstudio/VS Code
   - Open main.tex
   - Write in relevant chapter file
   - Compile regularly (F5)

3. **End of Session:**
   ```bash
   git add .
   git commit -m "Daily progress: [description]"
   git push (if using remote)
   ```

## Tips for Thesis Writing

1. **Use separate files for chapters:**
   ```latex
   \input{chapters/introduction}
   \input{chapters/theory}
   ```

2. **Comments for TODOs:**
   ```latex
   % TODO: Add citation for this claim
   % FIXME: Revise this paragraph
   ```

3. **Draft mode for faster compilation:**
   ```latex
   \documentclass[draft]{book}
   ```

4. **Custom commands for repeated terms:**
   ```latex
   \newcommand{\CDA}{Critical Discourse Analysis}
   ```

---

*For immediate help, check TeXstudio Help menu or search Stack Exchange*