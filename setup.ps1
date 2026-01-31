$InstallDir = "$HOME\ytp-downloader"
Write-Host "=== YouTube Playlist Downloader Installer ==="
Write-Host "Installing to: $InstallDir"

# Create directory
if (-not (Test-Path -Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir | Out-Null
}
Set-Location -Path $InstallDir

# Download
Write-Host "Downloading..."
$ZipUrl = "https://github.com/tereachar134/yt-playlist-Downloader/archive/refs/heads/main.zip"
Invoke-WebRequest -Uri $ZipUrl -OutFile "main.zip"

# Unzip
Write-Host "Extracting..."
Expand-Archive -Path "main.zip" -DestinationPath . -Force

# Run
Set-Location -Path "yt-playlist-Downloader-main"
Write-Host "Starting..."
.\install_and_run.bat
