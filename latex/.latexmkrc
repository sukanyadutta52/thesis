# Use biber instead of bibtex for bibliography processing
$biber = 'biber %O %S';
$bibtex_use = 2;

# Enable shell escape by default
$pdflatex = 'pdflatex -shell-escape %O %S';

# Clean up temporary files when using outdir
$clean_ext = 'aux bcf fdb_latexmk fls idx ilg ind log out run.xml toc';

# Copy PDF to root after successful compilation
END {
    if (-f "thesis.pdf") {
        system("cp thesis.pdf ../thesis.pdf");
        print "PDF copied to root directory\n";
    }
}