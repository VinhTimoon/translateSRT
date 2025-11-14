# PowerShell setup script
# Quick setup for SRT Translator project

Write-Host "=== SRT Translator - Quick Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "1. Checking Python version..." -ForegroundColor Yellow
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCheck) 
{
    Write-Host "ERROR: Python not found! Please install Python 3.10+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
$pythonVersion = python --version 2>&1
Write-Host "OK: Found $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "2. Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") 
{
    Write-Host "Virtual environment already exists. Skip." -ForegroundColor Yellow
} 
else 
{
    python -m venv venv
    if ($LASTEXITCODE -eq 0) 
    {
        Write-Host "OK: Virtual environment created" -ForegroundColor Green
    } 
    else 
    {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Activate virtual environment
Write-Host "3. Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "OK: Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "4. Installing dependencies..." -ForegroundColor Yellow
Write-Host "(This may take 2-3 minutes)" -ForegroundColor Gray
pip install -r requirements.txt --quiet --disable-pip-version-check
if ($LASTEXITCODE -eq 0) 
{
    Write-Host "OK: All dependencies installed" -ForegroundColor Green
} 
else 
{
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Setup .env file
Write-Host "5. Setting up configuration..." -ForegroundColor Yellow
if (Test-Path ".env") 
{
    Write-Host ".env file already exists. Skip." -ForegroundColor Yellow
} 
else 
{
    Copy-Item ".env.example" ".env"
    Write-Host "OK: Created .env file from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Edit .env file with your API keys!" -ForegroundColor Yellow
    Write-Host "Open: notepad .env" -ForegroundColor Cyan
}
Write-Host ""

# Create config directory
Write-Host "6. Creating config directory..." -ForegroundColor Yellow
$configDir = Join-Path $env:USERPROFILE ".srt_translator"
if (-not (Test-Path $configDir)) 
{
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    Write-Host "OK: Config directory created at $configDir" -ForegroundColor Green
} 
else 
{
    Write-Host "OK: Config directory exists" -ForegroundColor Green
}
Write-Host ""

# Summary
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit .env file with your Gemini API keys:" -ForegroundColor White
Write-Host "     notepad .env" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Get API keys from:" -ForegroundColor White
Write-Host "     https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. Run the application:" -ForegroundColor White
Write-Host "     python main.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  4. Or test first:" -ForegroundColor White
Write-Host "     python test_demo.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Tip: Keep this PowerShell window open (virtual env is activated)" -ForegroundColor Cyan
Write-Host ""
