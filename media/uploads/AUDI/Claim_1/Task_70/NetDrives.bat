@echo off
rem =========================================================
rem 	Netzwerklaufwerke zuweisen
rem ---------------------------------------------------------
rem		Parameter
rem		%1	Sharename
rem			Es kann zu einem einzigen Share gesprungen werden. Dann wird nur dieses Laufwerk verbunden
rem			z.B. CAD
rem =========================================================



rem	20.05.2015	G: als \\pbsfs\Process....
rem	04.04.2014	F: als \\srvXP-FS\XP-Data
rem	05.09.2013	H: Laufewrk (SrvData\Acoustics) erstellt
rem 16.07.2013	Share CAD über Parameter %1 verknüpft
rem	Migration von SrvFS auf SrvFile1 für folgende Shares geändert:
rem		Transfer		am 06.07.2012
rem		IT-Tools, IT	am 06.07.2012
rem ---------------------------------------------
rem 13.01.2011	neues Laufwrek L: (TechDoc) für technische Dokumentation erstellt
rem 30.07.2010	N: Basic.RD umbenannt nach ESD (Freigaben wie auch Verzeichnisnamen)
rem 12.04.2010	I: Laufwerk für Personal-Auszubildende deaktiviert
rem		folgende bereits länger deaktivierte Verknüpfungen gelöscht:
rem		Airmover, Automot, Delphi, NewProd, MachineShop (ProNC), Industrial
rem 08.07.2009	N: Laufwerk (Basic.RD-Transfer) erstellt für Elsässer
rem 25.05.2009	H: Laufwerk (MachineShop-3710) erstellt für Hallensleben
rem 17.03.2009	T: Laufwerk (Proj-Man) in Spindle Laufwerk verschoben, Freigabe Proj-Man entfernt
rem 09.03.2009	L: Laufwerk verbunden mit \\PLG017.ec.minebea.local\pmdm
rem 05.12.2008	S: Laufwerk verbunden mit \\SrvIL\CAD
rem 17.10.2008	neues Laufwrek I: für Personal-Auszubildende erstellt
rem 06.09.2008	Verlagerung der Lifetestdaten vom M: in das Spindle Laufwerk U:\Spindle\4721 Reliability Engineering 
rem		Lifetest-Setup I: wird nicht weiter verwendet
rem 02.08.2008	Umzug auf EMC (SrvFS): Basic.RD N:, SW P:
rem 26.07.2008	Umzug auf EMC (SrvFS): New-Products L: und Delphi L: in BLDC integriert. 
rem					Keine eigene Freigabe und kein eigenes Laufwerk mehr.
rem 25.07.2008	Umzug auf EMC (SrvFS): HDD-Motor-Tech H:, BLDC K:, Transfer Q:, QC R:, Info V:, User O:
rem 23.07.2008	Umzug auf EMC (SrvFS): MachineShop H:, Tooling I:, Electronics-Shop J:, Spindle U:
rem 22.07.2008	Umzug auf EMC (SrvFS): Anbu I:, Empfang L:, GL J:, Fibu H:, Hauptabt M:, Material N:, Patente N:
rem		Personal I:, Proj-Man T:, Shipping L:, 
rem 30.06.2008	AV H: wird nicht mher verbunden nach Verlagerung der Daten zu Spindle
rem		Transfer wurde verlagert von SrvFS2 nach SrvFS1
rem 		IT-Tools wurde verlagert von SrvFS2 nach SrvLifetest
rem 12.06.2008	Final Cleaning K: wird nicht mher verbunden nach Verlagerung der Daten zu Spindle
rem 24.04.2008	Airmover wurde nach BLDC verlagert, Laufwerk I: entfernt
rem 11.04.2008	S: Laufwerk verbunden mit \\SrvIntralink2\CAD
rem 20.03.2008	trennen aller Netzwerklaufwerke am Anfang des Scriptes
rem 13.03.2008	Fibu Daten auf SrvFS1 verlagert und dort als Netzwerklaufwerk verbunden
rem 21.09.2007	ProNC Laufwerk N: geändert von SrvApp1\Pronc nach SrvFS2\ProNC
rem 02.08.2007	Laufwerk Validation wurde zu BLDC hinuzgefügt. Verknüpfung gelöscht.



set logfile=c:\pmdm\netstart.tmp

echo ... connecting network drives
echo ======================================================== 	>> %logfile%
echo %date% - %time%  						>> %logfile%
echo ... connecting network drives 				>> %logfile%
echo Parameter 1: "%1" 				>> %logfile%


if "%1"=="" goto allDrives
set singleDrive=%1
goto %singleDrive%

:allDrives
rem --------------------------------------------------------------------
rem Variablen definieren, die die Vergabe von doppelt genutzten Laufwerksbezeichnungen nutzen
rem	G:	SK: \\pbsfs\
rem 	H:	Fibu, HDD-Motor-Tech, IT-Tools, MachineShop, Tooling-Manufacturing, Acoustics
rem 	I:	IT, Tooling, Personal, Personal-Auszubildende, Anbu, Tooling-NC (MachineShop)
rem 	J:	Electronics-Shop, GL
rem 	K:	KHK-CL, BLDC
rem 	L:	Empfang, Shipping, TechDoc, Material-PO
rem 	M:	Hauptabt
rem 	N:	ESD, Patente, Material, ProNC (manuell MachineShop)
rem	O:	User (alle)
rem 	P:	SW (alle)
rem 	Q:	Transfer (alle)
rem 	R:	QC (alle)
rem 	S:	CAD
rem 	T:	
rem	U:	Spindle, SpindleOil
rem 	V:	Info (alle)
rem 	W:	HMFBearing, Loga
rem		X:	ZEUS






rem =================================================================
rem	zuerst alle Netzwerklaufwerke trennen
rem -----------------------------------------------------------------

echo ... trenne alle Netzwerklaufwerke

net use f: /del /y					>> %logfile%
net use h: /del /y					>> %logfile%
net use i: /del /y					>> %logfile%
net use j: /del /y					>> %logfile%
net use k: /del /y					>> %logfile%
net use L: /del /y					>> %logfile%
net use m: /del /y					>> %logfile%
net use n: /del /y					>> %logfile%
net use o: /del /y					>> %logfile%
net use P: /del /y					>> %logfile%
net use Q: /del /y					>> %logfile%
net use R: /del /y					>> %logfile%
net use s: /del /y					>> %logfile%
net use t: /del /y					>> %logfile%
net use u: /del /y					>> %logfile%
net use V: /del /y					>> %logfile%
net use w: /del /y					>> %logfile%
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




rem =================================================================
rem 	Laufwerke für jeden PMDM User
rem =================================================================





rem =========================================================
rem	Netzwerklaufwerke fuer WinXP verbinden
rem =========================================================

net use f: /del
net use f: \\srvxp-fs\XP-Data /persistent:no
rem ---------------------------------------------------------




rem #################################################################
rem 	Laufwerk V:

rem -----------------------------------------------------------------
rem 	Info	

call \\srvfs\sw\scripts\connect.bat V: \\SrvFS\Info
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endV



rem #################################################################
rem 	Laufwerk P:

rem -----------------------------------------------------------------
rem 	SW

call \\srvfs\sw\scripts\connect.bat P: \\srvfs\SW
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endP



rem #################################################################
rem	Laufwerk Q:

rem -----------------------------------------------------------------
rem 	TRANSFER

call p:\scripts\connect.bat Q: \\srvfs\TRANSFER


rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
rem :endQ



rem #################################################################
rem 	Laufwerk R:

rem -----------------------------------------------------------------
rem 	QC

call P:\scripts\connect.bat R: \\SrvFS\QC
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
rem:endR




rem =================================================================
rem 	Laufwerke für bestimmte Gruppen
rem =================================================================


rem #################################################################
rem 	Laufwerk G:


rem -----------------------------------------------------------------
rem 	SK-Process

rem set share="\\PBSFS\Process engineering NMB-SK"
rem echo checking G: (SK-Process)
rem echo prüfe SK-Process mit Laufwerk G: 			>> %logfile%
rem if exist %share%\*.* (
rem  call P:\scripts\connect.bat G: %share%
rem  goto endG
rem )
rem -----------------------------------------------------------------
rem :endG



rem #################################################################
rem 	Laufwerk H:


rem -----------------------------------------------------------------
rem 	FIBU

set share=\\SrvFS\Fibu$
echo checking H: (Fibu)
echo prüfe Fibu mit Laufwerk H: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat H: %share%
  goto endH
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	HDD-Motor-Tech

set share=\\SrvFS\HDD-Motor-Tech
echo checking H: (HDD-Motor-Tech)
echo prüfe HDD-Motor-Tech mit Laufwerk H: 		>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat H: %share%
  goto endH
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	IT-Tools

set share=\\SrvFS\IT-Tools
rem ------------  wenn der Share auf SrvFS abgeschaltet wurde, dann den neuen Share auf SrvFile1 verwenden  ------------
if not exist %share% set share=\\SrvFile1\IT-Tools
echo checking H: (IT-Tools)
echo prüfe IT-Tools mit Laufwerk H:			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat H: %share%
  goto endH
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	MachineShop 
rem 	Zugriff auch von Tooling Manufacturing

set share=\\SrvFS\Tooling-Manufacturing
echo checking H: (Tooling-Manufacturing)
echo prüfe Tooling-Manufacturing mit Laufwerk H:			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat H: %share%
  goto endH
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	Acoustics

rem set share=\\SrvData\Acoustics
rem echo checking H: (Acoustics)
rem echo prüfe Acoustics mit Laufwerk H:			>> %logfile%
rem if exist %share%\*.* (
rem  call P:\scripts\connect.bat H: %share%
rem  goto endH
rem )
rem -----------------------------------------------------------------

rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



:endH




rem #################################################################
rem 	Laufwerk I:

rem -----------------------------------------------------------------
rem 	Accounting AS400


echo checking I: (AS400)
echo prüfe Accounting mit Laufwerk I:			>> %logfile%
if not exist c:\pmdm\remote.txt goto endAS400
net use i: /del /y
net use i: \\a61gm\qdls\efas\bank\oua1 /user:remote remote /persistent:no
goto endI

:EndAS400
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	Tooling

set share=\\SrvFS\Tooling
echo checking I: (Tooling)
echo prüfe Tooling mit Laufwerk I: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat I: %share%
  goto endI
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	Tooling-NC
rem	??? wo benötigt ???

rem set share=\\SrvFS\Tooling-NC
rem echo checking I: (Tooling-NC)
rem echo prüfe Tooling-NC mit Laufwerk I:			>> %logfile%
rem if exist %share%\*.* (
rem   call P:\scripts\connect.bat I: %share%
rem   goto endI
rem )
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	IT

set share=\\SrvFS\IT
rem ------------  wenn der Share auf SrvFS abgeschaltet wurde, dann den neuen Share auf SrvFile1 verwenden  ------------
if not exist %share% set share=\\SrvFile1\IT

echo checking I: (IT)
echo prüfe IT mit Laufwerk I: 				>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat I: %share%
  goto endI
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	Personal

set share=\\srvfs\Personal$
echo checking I: (Personal)
echo prüfe Personal mit Laufwerk I:			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat I: %share%
  goto endI
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	Personal-Auszubildende

rem set share=\\srvfs\Auszubildende_Personal
rem echo checking I: (Auszubildende_Personal)
rem echo prüfe Auszubildende_Personal mit Laufwerk I:			>> %logfile%
rem if exist %share%\*.* (
rem   call P:\scripts\connect.bat I: %share%
rem   goto endI
rem )
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	Anbu (Fibu: für digitale Fotos + Erläuterungen)

set share=\\SRVFS\Anbu
echo checking I: (Anbu)
echo prüfe Anbu mit Laufwerk I: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat I: %share%
  goto endI
)
rem -----------------------------------------------------------------


:endI




rem #################################################################
rem 	Laufwerk J:


rem -----------------------------------------------------------------
rem 	GL (Geschaeftsleitung)

set share=\\SrvFS\GL
echo checking J: (GL)
echo prüfe GL mit Laufwerk J: 				>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat J: %share%
  goto endJ
)


rem -----------------------------------------------------------------
rem 	Electronics-Shop

set share=\\SrvFS\Electronics-Shop
echo checking J: (Electronics-Shop)
echo prüfe Electronics-Shop mit Laufwerk J: 		>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat J: %share%
  goto endJ
)
rem -----------------------------------------------------------------



rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endJ





rem #################################################################
rem 	Laufwerk K:


rem -----------------------------------------------------------------
rem 	KHK-CL (Classic Line / DOS)

set share=\\SrvKHK\KHKalt
echo checking K: (KHK-CL)
echo prüfe KHK-CL mit Laufwerk K: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat K: %share%
  goto endK
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	BLDC

set share=\\SrvFS\BLDC
echo checking K: (BLDC)
echo prüfe BLDC mit Laufwerk K: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat K: %share%
  goto endK
)
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endK




rem #################################################################
rem 	Laufwerk L:


rem -----------------------------------------------------------------
rem 	Empfang

set share=\\SRVFS\Empfang
echo checking L: (Empfang)
echo prüfe Empfang mit Laufwerk L: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat L: %share%
  goto endL
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	Shipping

set share=\\SrvFS\Shipping
echo checking L: (Shipping)
echo prüfe Shipping mit Laufwerk L: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat L: %share%
  goto endL
)


rem -----------------------------------------------------------------
rem 	TechDoc

set share=\\SrvFS\TechDoc
echo checking L: (TechDoc)
echo prüfe TechDoc mit Laufwerk L: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat L: %share%
  goto endL
)


if %username%==itservice goto end-po
rem -----------------------------------------------------------------
rem 	Material-PO

set share=\\PLG017.ec.minebea.local\pmdm
echo checking L: (Material-PO auf \\PLG017.ec.minebea.local\pmdm)
echo prüfe Material-PO mit Laufwerk L: 			>> %logfile%
if exist %share%\*.* (
 call P:\scripts\connect.bat L: %share%
 goto endL
)
rem -----------------------------------------------------------------
:end-po

rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endL




rem #################################################################
rem 	Laufwerk M:


rem -----------------------------------------------------------------
rem 	HAUPABT	Gruppe Haupabteilunglsleiter

set share=\\SrvFS\hauptabt
echo checking M: (Hauptabt)
echo prüfe HAUPTABT mit Laufwerk M: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat M: %share%
  goto endM
)
rem -----------------------------------------------------------------


:endM




rem #################################################################
rem 	Laufwerk N:

rem -----------------------------------------------------------------
rem 	ESD


set share=\\SrvFS\ESD
echo checking N: (ESD)
echo prüfe ESD mit Laufwerk N: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat N: %share%
  goto endN
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	Material (Einkauf)

set share=\\SrvFS\Material
echo checking N: (Material)
echo prüfe Material mit Laufwerk N: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat N: %share%
  goto endN
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	PATENTE

set share=\\SrvFS\Patente
echo checking N: (Patente)
echo prüfe PATENTE mit Laufwerk N: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat N: %share%
  echo ... kopiere HEIDI.MDE
  echo ... kopiere HEIDI.MDE 				>> %logfile%
  if exist N:\PatentDB\HEIDI.mde xcopy N:\PatentDB\HEIDI.mde c:\dbman\patente\ /y/v
  goto endN
)
rem -----------------------------------------------------------------


rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endN





rem #################################################################
rem 	Laufwerk S:

rem -----------------------------------------------------------------
rem 	CAD
:CAD
net use s: /del

set share=\\SrvFS\CAD
rem set share=\\SrvIL\CAD
echo checking S: (CAD)
echo prüfe CAD mit Laufwerk S: 				>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat S: %share%
  goto endS
)
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endS
echo singleDrive = "%singleDrive%" 				>> %logfile%

if not "%singleDrive%"=="" goto EndDrives
echo ... nach CAD 				>> %logfile%
echo ------------------- 				>> %logfile%



rem #################################################################
rem 	Laufwerk T:

rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endT




rem #################################################################
rem 	Laufwerk U:

rem -----------------------------------------------------------------
rem 	Spindle


set share=\\SrvFS\Spindle
echo checking U: (Spindle)
echo prüfe Spindle mit Laufwerk U: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat U: %share%
  goto endU
)
rem -----------------------------------------------------------------


rem -----------------------------------------------------------------
rem 	SpindleOil


set share=\\SrvFS\SpindleOil
echo checking U: (SpindleOil)
echo prüfe SpindleOil mit Laufwerk U: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat U: %share%
  goto endU
)
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
rem		SpindleStudents (Software-Tools)

set share=\\SrvFS\Spindle-Software-Tools
echo checking U: (Spindle-Software-Tools)
echo prüfe Spindle-Software-Tools mit Laufwerk U: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat U: %share%
  goto endU
)

:endU




rem #################################################################
rem 	Laufwerk W:

rem -----------------------------------------------------------------
rem 	HMF Bearing (\BLDC\Airmover\HMF Bearing)

set share=\\SRVFS\HMFBearing
echo checking W: (HMFBearing)
echo prüfe HMFBearing mit Laufwerk W: 			>> %logfile%
if exist %share%\*.* (
  call P:\scripts\connect.bat W: %share%
  goto endW
)
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


rem -----------------------------------------------------------------
rem 	Loga (\\SrvLoga\Loga$)

set share=\\SrvLoga\Loga$
echo checking W: (Loga)
echo prüfe Loga mit Laufwerk W: 			>> %logfile%

rem nicht verbinden als Domain Admin
if exist \\srvfs\it goto endW

if exist %share%\*.* (
  call P:\scripts\connect.bat W: %share%
  goto endW
)
rem +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:endW





rem =========================================================
rem 	Verbinde User-Laufwerk O:
rem =========================================================


set betr-sys=WIN2000
if not exist %systemroot%\security\*.* set betr-sys=WINNT


rem prüfen ob Home-Verzeichnis schon erstellt wurde
rem bei neuen Benutzern wird das Home Verzeichnis angelegt
if exist \\SrvFS\user$\%username%\*.* goto HomeExist
if not exist \\SrvFS\user$\%username%\*.* goto HomeErr2
goto HomeErr2

rem echo ... Homeverzeichnis wird erstellt für Benutzer %username% 
rem md \\SrvFS\user$\%username%
rem if errorlevel==1 goto HomeErr1
rem if errorlevel==0 goto HomeErr0
rem echo sonstiger Fehler bei User %username% auf PC %computername% mit Betriessystem %betr-sys% 
rem echo sonstiger Fehler beim erstellen des Homeverzeichnisses (User %username% auf PC %computername% mit Betriessystem %betr-sys%) >> Q:\_khk\nwlogin\home\new-user.err
rem echo sonstiger Fehler beim erstellen des Homeverzeichnisses (User %username% auf PC %computername% mit Betriessystem %betr-sys%) >> %logfile%
rem goto endHome

rem :HomeErr1
rem echo Fehler 1 bei User %username% auf PC %computername% mit Betriessystem %betr-sys% 
rem echo Fehler 1 beim erstellen des Homeverzeichnisses (User %username% auf PC %computername% mit Betriessystem %betr-sys%) >> Q:\_khk\nwlogin\home\new-user.err
rem echo Fehler 1 beim erstellen des Homeverzeichnisses (User %username% auf PC %computername% mit Betriessystem %betr-sys%) >> %logfile%
rem goto endHome

rem :HomeErr0
rem rem Benutzerverzeichnis erfolgreich angelegt
rem echo %username%	Benutzerverzeichnis erfolgreich angelegt >> Q:\_khk\nwlogin\home\new-user.txt
rem echo %username%	Benutzerverzeichnis erfolgreich angelegt >> %logfile%

:HomeErr2
rem Kein Benutzerverzeichnis vorhanden
echo Kein Benutzerverzeichnis für %username% vorhanden >> Q:\_khk\nwlogin\home\new-user.txt
echo Kein Benutzerverzeichnis für %username% vorhanden >> %logfile%
goto endHome

rem Benutzerrechte anpassen (Benutzer: Schreiben, PMDM-Alle: keine Rechte)
rem echo Benuetzerrechte für %username% werden angepasst >> %logfile%
rem cacls %username% /e /g des001\%username%:c /r des001\pmdm-alle >> Q:\_khk\nwlogin\home\new-user.txt
rem goto HomeExist


:HomeExist
echo checking O: (%username%)
echo Das Home Verzeichnis auf SrvFS existiert bereits >> %logfile%
if %betr-sys%==WIN2000 goto HomeW2K
if %betr-sys%==WINNT goto HomeNT4

echo.
echo Betriebssystem wurde nicht korrekt ausgewertet  >> %logfile%
echo Betriebssystem: %betr-sys% >> %logfile%
goto EndHome


:HomeW2K
echo Win2000; Verbinde O: mit \\SrvFS\user$\%username% >> %logfile%

net use o: \\SrvFS\user$\%username%
rem pause
goto EndHome

:HomeNT4
echo WinNT
echo NT4; Verbinde Z: mit \\SrvFS\user$ >> %logfile%
net use z: /del > nul
net use z: \\SrvFS\user$

echo ... SUBST O: mit Z:\%username% >> %logfile%
subst o: /d
net use o: /del > nul
subst o: z:\%username% 
echo. >> %logfile%
:endHome
rem ------------------------------------------------------------------------


:EndDrives
