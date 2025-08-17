@echo off
echo Starting clean build...

cd latex

REM Clean previous files
if exist thesis.pdf del /q thesis.pdf
if exist build rmdir /s /q build

REM Create build directory and copy sources
mkdir build
xcopy /e /i /q chapters build\chapters
copy /y thesis.tex build\
xcopy /e /i /q bibliography build\bibliography

REM Build in temp directory
cd build
echo Running first pdflatex...
"C:\texlive\2025\bin\windows\pdflatex.exe" -interaction=nonstopmode thesis.tex

echo Running biber...
"C:\texlive\2025\bin\windows\biber.exe" thesis

echo Running second pdflatex...
"C:\texlive\2025\bin\windows\pdflatex.exe" -interaction=nonstopmode thesis.tex

echo Running final pdflatex...
"C:\texlive\2025\bin\windows\pdflatex.exe" -interaction=nonstopmode thesis.tex

REM Move PDF back and clean up
cd ..
copy build\thesis.pdf .
rmdir /s /q build\chapters
rmdir /s /q build\bibliography
del build\thesis.tex

echo Build complete! PDF: latex\thesis.pdf
echo Temp files in: latex\build\