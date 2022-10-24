@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build
set LINKCHECKDIR=\%BUILDDIR%\linkcheck

if "%1" == "" goto help
if "%1" == "clean" goto clean
if "%1" == "clean-all" goto clean-all
if "%1" == "clean-examples" goto clean-examples
if "%1" == "linkcheck" goto linkcheck


%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:clean
rmdir /s /q %BUILDDIR% > /NUL 2>&1 
for /d /r %SOURCEDIR% %%d in (_autosummary) do @if exist "%%d" rmdir /s /q "%%d"
goto end

:clean-all
rmdir /s /q %BUILDDIR% > /NUL 2>&1 
rmdir /s /q source\examples\gallery_examples > /NUL 2>&1 
for /d /r %SOURCEDIR% %%d in (_autosummary) do @if exist "%%d" rmdir /s /q "%%d"
goto end

:clean-examples
rmdir /s /q source\examples\gallery_examples > /NUL 2>&1
goto end

:linkcheck
%SPHINXBUILD% -b %1 %SPHINXOPTS% %SOURCEDIR% %LINKCHECKDIR%
echo "Check finished. Report is in %LINKCHECKDIR%."
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
