.PHONY: all clean help

PREZ_PDF = presentation.pdf
PREZ_TEX = presentation.tex
PREZ_DEP = prez-api-rest.tex prez-architecture.tex prez-conclusion.tex
PREZ_DEP += prez-intro.tex prez-requirements.tex prez-sequence-diagram.tex
PREZ_DEP += prez-tests.tex

all: $(PREZ_PDF)

$(PREZ_PDF): $(PREZ_TEX) $(PREZ_DEP) Makefile
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<

clean:
	rm -f *~ *.nav *.snm *.toc *.out *.aux *.log
	rm -r _minted-presentation
	rm -f $(PREZ_PDF)


help:
	@ echo "------------------------------------------------------"
	@ echo "Usage:"
	@ echo "  make [all]   # build '$(PREZ_PDF)'"
	@ echo "  make clean   # clean temporary files and all pdf"
	@ echo "  make help    # print this help"
	@ echo "------------------------------------------------------"