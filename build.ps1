# PowerShell build script for SRT Translator
# Usage: .\build.ps1

Write-Host "🔨 Building SRT Translator..." -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found. Please run:" -ForegroundColor Red
    Write-Host "   python -m venv venv" -ForegroundColor Yellow
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "✓ Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Clean previous builds
Write-Host "🧹 Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Run PyInstaller
Write-Host "📦 Running PyInstaller..." -ForegroundColor Cyan
pyinstaller build.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Build completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: dist\SRT_Translator.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Copy .env file with your API keys to the same directory as the .exe"
    Write-Host "  2. Run SRT_Translator.exe"
    Write-Host ""
} else {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
