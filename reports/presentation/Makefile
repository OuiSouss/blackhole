.PHONY: all clean help

PREZ_PDF = presentation.pdf
PREZ_TEX = presentation.tex
PREZ_DEP = prez-api-rest.tex prez-conclusion.tex
PREZ_DEP += prez-intro.tex prez-requirements.tex prez-sequence-diagram.tex
PREZ_DEP += prez-tests.tex prez-use_cases.tex prez-ui.tex


all: $(PREZ_PDF)

$(PREZ_PDF): $(PREZ_TEX) $(PREZ_DEP) Makefile
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<

clean:
	rm -f *~ *.nav *.snm *.toc *.out *.aux *.log *.fdb_latexmk *.fls *.snm *.vrb
	rm -f $(PREZ_PDF)
	rm -rf _minted-presentation


help:
	@ echo "------------------------------------------------------"
	@ echo "Usage:"
	@ echo "  make [all]   # build '$(PREZ_PDF)'"
	@ echo "  make clean   # clean temporary files and all pdf"
	@ echo "  make help    # print this help"
	@ echo "------------------------------------------------------"
