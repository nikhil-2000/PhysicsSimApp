@SETLOCAL

@REM Set the PYTHON path variable to your python command, like C:\Python33\python.exe
@IF "%PYTHON%" == "" echo Warning: PYTHON environment path not set.

@IF "%PYTHONPATH%" == "" SET PYTHONPATH=%CHDIR%
@IF "%PYTHON27_X86%" == "" SET PYTHON27_X86=c:\Python27-x86\python.exe
@IF "%PYTHON27_X64%" == "" SET PYTHON27_X64=c:\Python27-x64\python.exe
@IF "%PYTHON32_X86%" == "" SET PYTHON32_X86=c:\Python32-x86\python.exe
@IF "%PYTHON32_X64%" == "" SET PYTHON32_X64=c:\Python32-x64\python.exe
@IF "%PYTHON33_X86%" == "" SET PYTHON33_X86=c:\Python33-x86\python.exe
@IF "%PYTHON33_X64%" == "" SET PYTHON33_X64=c:\Python33-x64\python.exe
@IF "%PYTHON34_X86%" == "" SET PYTHON34_X86=c:\Python34-x86\python.exe
@IF "%PYTHON34_X64%" == "" SET PYTHON34_X64=c:\Python34-x64\python.exe
@IF "%PYTHON35_X86%" == "" SET PYTHON35_X86=c:\Python35-x86\python.exe
@IF "%PYTHON35_X64%" == "" SET PYTHON35_X64=c:\Python35-x64\python.exe
@IF "%PYTHON%" == "" SET PYTHON=%PYTHON27_X64%
@IF "%PYPY2%" == "" SET PYPY2=c:\pypy2-v5.4.1\pypy.exe
@IF "%PYPY3%" == "" SET PYPY3=c:\pypy3-v2.4\pypy.exe

@SET INTERP_X64=%PYTHON27_X64%;%PYTHON32_X64%;%PYTHON33_X64%;%PYTHON34_X64%;^
 %PYTHON35_X64%
@SET INTERP_X86=%PYTHON27_X86%;%PYTHON32_X86%;%PYTHON33_X86%;%PYTHON34_X86%;^
 %PYTHON35_X86%;%PYPY2%;%PYPY3%
@SET INTERPRETERS=%INTERP_X86%;%INTERP_X64%

@IF "%~1" == "" GOTO :all
@GOTO :%~1

:all
@CALL :clean
@GOTO :eof

:clean
@RMDIR /S /Q build
@RMDIR /S /Q dist
@FOR /d /r . %%d in (__pycache__) do @IF EXIST "%%d" RMDIR /S /Q "%%d"
@DEL /S /Q MANIFEST
@DEL /S /Q *.pyc

@GOTO :eof

:docs
@IF "%SPHINXBUILD%" == "" SET SPHINXBUILD=C:\Python27-x64\Scripts\sphinx-build.exe
@ECHO Creating docs package
@RMDIR /S /Q doc\html
@CD doc
@CALL make html
@MOVE /Y _build\html html
@RMDIR /S /Q _build
@CALL make clean
@CD ..
@GOTO :eof

:testall
@FOR /F "tokens=1 delims=" %%A in ('CHDIR') do @SET PYTHONPATH=%%A
@FOR %%A in (%INTERPRETERS%) do @%%A -B -m test.util.runtests
@GOTO :eof

@ENDLOCAL
