@echo off

REM For Python 2.7, 3.5, 3.6
call:build_wheel "C:\Python27\python.exe"
call:build_wheel "C:\Program Files\Python35\python.exe"
call:build_wheel "C:\Program Files\Python36\python.exe"

rem for /r %i in (*) do echo %i
rem for %f in (.\*) do @echo %f



PAUSE
goto:eof

::--------------------------------------------------------
::-- Build and test a python wheel
::--------------------------------------------------------
:build_wheel

"%~1" -m pip install pip --upgrade pip --user -q --no-cache-dir
"%~1" -m pip install wheel --user -q --no-cache-dir
"%~1" -m pip install setuptools --user --upgrade -q --no-cache-dir
"%~1" -m pip install numpy --user -q --no-cache-dir
"%~1" -m pip install vtk --user -q

"%~1" %~dp0setup.py -q bdist_wheel

rem for testing
"%~1" -m pip uninstall pyansys

rem this is annoying
FOR %%G IN (%~dp0dist\*) DO "%~1" -m pip install %%G --user -q
"%~1" %~dp0tests\test_pyansys.py
goto:eof
