.PHONY: all clean help

REPORT_PDF = report.pdf
REPORT_TEX = report.tex
REPORT_DEP = chapter-analyze.tex chapter-gantt.tex chapter-intro.tex
REPORT_DEP += chapter-requirements.tex chapter-state-of-the-art.tex
REPORT_DEP += chapter-tests.tex chapter-user-story.tex biblio.bib

all: $(REPORT_PDF)

$(REPORT_PDF): $(REPORT_TEX) $(REPORT_DEP) Makefile
	pdflatex -shell-escape $<
	bibtex report
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<

clean:
	rm -f *~ *.nav *.snm *.toc *.out *.aux *.log *.bbl *.blg
	rm -r _minted-report
	rm -f $(REPORT_PDF)


help:
	@ echo "------------------------------------------------------"
	@ echo "Usage:"
	@ echo "  make [all]   # build '$(REPORT_PDF)'"
	@ echo "  make clean   # clean temporary files and all pdf"
	@ echo "  make help    # print this help"
	@ echo "------------------------------------------------------"
