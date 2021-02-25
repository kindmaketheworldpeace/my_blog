@echo off

setlocal EnableDelayedExpansion
set cu_date=%date:~0,4%-%date:~5,2%-%date:~8,2%
set cu_time=%time:~0,8%

set s7zPath=C:
set winTmp=C:\Windows\Temp
if exist %winTmp%\update.cfg (del /F /Q %winTmp%\update.cfg) else (echo there's no update.cfg file)

rem if /i %timevar% LSS 10 ( set timevar=0%time:~1,1% )
rem set filename_time=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%

set filename_time=%date:~3,4%%date:~8,2%%date:~11,2%%time:~0,2%%time:~3,2%%time:~6,2%
:length
set/a n+=1
if not "!filename_time:~%n%!"=="" goto :length
echo,%n%

if not %n%==14 (echo filename_time_stamp error, the script will exit !) & goto :EOF
echo filename_time_stamp is %filename_time%, that's good!

rem function switch
:loop
IF NOT "%1"=="" (
    IF "%1"=="-t" (
        SET SWWIN_TARGET_DIR=%2
        SHIFT
    )
    IF "%1"=="-p" (
        SET SWWIN_GSE_HOME=%2
        SHIFT
    )
    IF "%1"=="-n" (
        SET SWWIN_PLUGIN_NAME=%2
        SHIFT
    )
    IF "%1"=="-f" (
        SET SWWIN_PACKAGE=%2
        SHIFT
    )
    IF "%1"=="-z" (
        SET SWWIN_TMP=%2
        SHIFT
    )
    IF "%1"=="-m" (
        SET SWWIN_UPGRADE_TYPE=%2
        SHIFT
    )
    IF "%1"=="-u" (
        echo %filename_time%>%winTmp%\update.cfg
    )
    SHIFT
    GOTO :loop
)

rem GSE folder
IF NOT EXIST %SWWIN_GSE_HOME% (echo %SWWIN_GSE_HOME% folder not found , plz check!) & goto :EOF

rem 目标文件夹判断
if not "%SWWIN_TARGET_DIR%"=="official" if not "%SWWIN_TARGET_DIR%"=="1" if not "%SWWIN_TARGET_DIR%"=="external" if not "%SWWIN_TARGET_DIR%"=="2" if not "%SWWIN_TARGET_DIR%"=="scripts" if not "%SWWIN_TARGET_DIR%"=="3" echo error , -t must with official or 1, external or 2, scripts or 3, plz check ! & goto :EOF (
    if "%SWWIN_TARGET_DIR%"=="official" (
        set WIN_GSE_BINDIR=%SWWIN_GSE_HOME%\plugins\bin
        set WIN_GSE_ETCDIR=%SWWIN_GSE_HOME%\plugins\etc
        set WIN_GSE_BINDIR_1=%SWWIN_GSE_HOME%\plugins
        set WIN_GSE_ETCDIR_1=%SWWIN_GSE_HOME%\plugins
    ) else (
    if "%SWWIN_TARGET_DIR%"=="1" (
        set WIN_GSE_BINDIR=%SWWIN_GSE_HOME%\plugins\bin
        set WIN_GSE_ETCDIR=%SWWIN_GSE_HOME%\plugins\etc
        set WIN_GSE_BINDIR_1=%SWWIN_GSE_HOME%\plugins
        set WIN_GSE_ETCDIR_1=%SWWIN_GSE_HOME%\plugins
    )
)

if not "%SWWIN_TARGET_DIR%"=="official" if not "%SWWIN_TARGET_DIR%"=="1" if not "%SWWIN_TARGET_DIR%"=="external" if not "%SWWIN_TARGET_DIR%"=="2" if not "%SWWIN_TARGET_DIR%"=="scripts" if not "%SWWIN_TARGET_DIR%"=="3" echo error , -t must with official or 1, external or 2, scripts or 3, plz check ! & goto :EOF (
    if "%SWWIN_TARGET_DIR%"=="external" (
        set WIN_GSE_BINDIR=%SWWIN_GSE_HOME%\external_plugins\%SWWIN_PLUGIN_NAME%\bin
        set WIN_GSE_ETCDIR=%SWWIN_GSE_HOME%\external_plugins\%SWWIN_PLUGIN_NAME%\etc
    ) else (
    if "%SWWIN_TARGET_DIR%"=="2" (
        set WIN_GSE_BINDIR=%SWWIN_GSE_HOME%\external_plugins\%SWWIN_PLUGIN_NAME%\bin
        set WIN_GSE_ETCDIR=%SWWIN_GSE_HOME%\external_plugins\%SWWIN_PLUGIN_NAME%\etc
    )
)

if not "%SWWIN_TARGET_DIR%"=="official" if not "%SWWIN_TARGET_DIR%"=="1" if not "%SWWIN_TARGET_DIR%"=="external" if not "%SWWIN_TARGET_DIR%"=="2" if not "%SWWIN_TARGET_DIR%"=="scripts" if not "%SWWIN_TARGET_DIR%"=="3" echo error , -t must with official or 1, external or 2, scripts or 3, plz check ! & goto :EOF (
    if "%SWWIN_TARGET_DIR%"=="scripts" (
        set WIN_GSE_BINDIR=%SWWIN_GSE_HOME%\external_scripts\
        set WIN_GSE_ETCDIR=%SWWIN_GSE_HOME%\external_scripts\
    ) else (
    if "%SWWIN_TARGET_DIR%"=="3" (
        set WIN_GSE_BINDIR=%SWWIN_GSE_HOME%\external_scripts\
        set WIN_GSE_ETCDIR=%SWWIN_GSE_HOME%\external_scripts\
    )
)

rem WIN_GSE_BINDIR WIN_GSE_BINDIR目录判断
IF NOT EXIST %WIN_GSE_BINDIR% IF NOT EXIST %WIN_GSE_BINDIR% echo error , %WIN_GSE_BINDIR% or %WIN_GSE_ETCDIR% folder not found , plz check ! & goto :EOF

rem 备份
:backup
    rem set filename_time=%date:~3,4%%date:~8,2%%date:~11,2%%time:~0,2%%time:~3,2%%time:~6,2%
    set WIN_backup_filename=%SWWIN_PLUGIN_NAME%-%filename_time%.zip
    %s7zPath%\7z.exe a -tzip %SWWIN_GSE_HOME%\%WIN_backup_filename% %WIN_GSE_BINDIR% %WIN_GSE_ETCDIR%
    rem move /Y %TMP%\%WIN_backup_filename% %SWWIN_GSE_HOME%\
goto:del_old_files

rem 暂时不管，此段注释掉
if 1==0 (
    if %REMOVE% == 1 (
    rem   cd %WIN_GSE_BINDIR%\bin
    rem    ./stop.sh ${SWWIN_PLUGIN_NAME} || { echo "stop plugin $SWWIN_PLUGIN_NAME failed"; exit 1; }
    echo goon
    rem    rm -rf $BINDIR/bin/${SWWIN_PLUGIN_NAME} $ETCDIR/${SWWIN_PLUGIN_NAME}.conf
    rem    exit $?
    )deloldfiles
)

rem 删除老文件操作
:del_old_files
if not "%SWWIN_UPGRADE_TYPE%"=="APPEND" echo error , -m must with APPEND, plz check ! & goto :EOF (
    if "%SWWIN_UPGRADE_TYPE%"=="APPEND" (
    echo "removing plugin files"
    IF NOT EXIST %WIN_GSE_BINDIR% (
    echo %WIN_GSE_BINDIR% folder not found , plz check!
    goto EOF
    )
    taskkill /f /im %SWWIN_PLUGIN_NAME%.exe
    rem rmdir /q /s %WIN_GSE_BINDIR% >>error.log 2>&1
)
goto:unzip_config

rem 解压配置到目标路径
:unzip_config
echo "coming into"
%s7zPath%\7z.exe x -aoa %SWWIN_TMP%\%SWWIN_PACKAGE% -o%SWWIN_GSE_HOME%
set TAR_FILE_NAME=%SWWIN_PACKAGE:~0,-4%.tar
%s7zPath%\7z.exe x -aoa %SWWIN_GSE_HOME%\%TAR_FILE_NAME% -o%SWWIN_GSE_HOME%
goto:recover_config

rem 恢复配置文件
:recover_config
if exist %winTmp%\update.cfg (for /f %%i in ('type %winTmp%\update.cfg') do set update_cfg_timestamp=%%i ) else (echo there's no need recover_config)
echo %update_cfg_timestamp%

if "%update_cfg_timestamp%"=="" echo (no need recover_config) & goto :config_file_check (
    ) else (
    %s7zPath%\7z.exe x -aoa %SWWIN_GSE_HOME%\%WIN_backup_filename% -o%WIN_GSE_ETCDIR_1% etc
    )
)
goto:config_file_check

:config_file_check
rem 输出看看更新后的信息. debug时用
dir %WIN_GSE_BINDIR%\%SWWIN_PLUGIN_NAME%.exe %WIN_GSE_ETCDIR%\%SWWIN_PLUGIN_NAME%.conf | findstr /c:%SWWIN_PLUGIN_NAME%.exe /c:%SWWIN_PLUGIN_NAME%.conf
type %WIN_GSE_ETCDIR%\%SWWIN_PLUGIN_NAME%.conf
goto:eof

:EOF