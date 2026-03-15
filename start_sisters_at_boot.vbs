Set WshShell = CreateObject("WScript.Shell")

' Path to the script
scriptPath = "C:\path\to\your\start_all_sisters.py" 

' Create a startup shortcut
startupFolder = WshShell.SpecialFolders("Startup") 
WshShell.ShellExecute "cmd.exe", "/C start python " & scriptPath, startupFolder, 1, 0