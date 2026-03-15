@echo off
echo ====================================
echo Testing Zsteg Installation
echo ====================================
echo.

echo Checking zsteg version...
zsteg --version
echo.

echo Checking zsteg help...
zsteg --help
echo.

echo ====================================
echo If you see help text above, zsteg is working!
echo.
echo To analyze an image, use:
echo   zsteg image.png
echo   zsteg image.png --all
echo ====================================
pause
