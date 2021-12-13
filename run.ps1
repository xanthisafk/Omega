Write-Output "Checking if config files exists.."
if (Test-Path -path .\config.json){
    Write-Output "Config file exists; starting bot"
    Write-Output "Installing requirements"
    Start-Process PowerShell -ArgumentList "python.exe -m pip install -r requirements.txt" -Wait
    Write-Output "Installed requirements"
    Set-Location files
    Write-Output "Launching Lavalink"
    Start-Process PowerShell -ArgumentList "java.exe -jar lavalink.jar"
    Start-Sleep -Seconds 3
    Write-Output "Launched Lavalink"
    Set-Location ..
    python.exe -m main
}
else{
    Write-Output "Config file does not exist; running setup"
    Start-Process PowerShell -ArgumentList "python.exe setup.py" -Wait
    Write-Output "Setup complete; starting bot"
    Start-Process PowerShell -ArgumentList "python.exe -m pip install -r requirements.txt" -Wait
    Write-Output "Installed requirements"
    Set-Location files
    Start-Process PowerShell -ArgumentList "java.exe -jar lavalink.jar"
    Write-Output "Started Lavalink"
    Start-Sleep -Seconds 3
    Set-Location ..
    python.exe -m main
}