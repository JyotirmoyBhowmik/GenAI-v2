@echo off
REM GenAI Platform - Create Backup
REM Creates a full backup of the platform

echo ============================================================
echo GenAI Platform - Backup Creation
echo ============================================================
echo.

python -c "from backend.backup.backup_manager import BackupManager; bm = BackupManager(); backup_id = bm.create_backup(); print(f'\nBackup created successfully: {backup_id}')"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Backup creation failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Backup completed successfully!
echo ============================================================
echo.
echo To restore, run: python scripts\restore_backup.py
echo.

pause
