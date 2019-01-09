.PHONY: all clean help

REPORT_PDF = report.pdf
REPORT_TEX = report.tex
REPORT_DEP =

all: $(REPORT_PDF)

$(REPORT_PDF): $(REPORT_TEX) $(REPORT_DEP) Makefile
	pdflatex -shell-escape $<
	bibtex report
	pdflatex -shell-escape $<
	pdflatex -shell-escape $<

clean:
	rm -f *~ *.nav *.snm *.toc *.out *.aux *.log
	rm -f $(REPORT_PDF)


help:
	@ echo "------------------------------------------------------"
	@ echo "Usage:"
	@ echo "  make [all]   # build '$(REPORT_PDF)'"
	@ echo "  make clean   # clean temporary files and all pdf"
	@ echo "  make help    # print this help"
	@ echo "------------------------------------------------------"
