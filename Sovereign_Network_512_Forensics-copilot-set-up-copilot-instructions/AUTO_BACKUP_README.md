# Auto-Backup System Setup

## Quick Start

**Windows (Easiest):**
```
Double-click: START_AUTO_BACKUP.bat
```

**Terminal:**
```powershell
python auto_git_backup.py 5
```
(5 = minutes between backups, default is 5)

## How It Works

- Runs every 5 minutes (or custom interval)
- Automatically stages and commits all changes
- Non-intrusive: only commits if changes exist
- Press Ctrl+C to stop

## Schedule It (Windows)

To run in background on startup:

1. Right-click desktop → New → Shortcut
2. Target: `C:\Users\stu43\OneDrive\Erryn\Erryns Soul 2025\START_AUTO_BACKUP.bat`
3. Name: "Erryn Auto-Backup"
4. Right-click shortcut → Properties → Advanced → Check "Run as administrator"

**OR** use Task Scheduler:

1. Search "Task Scheduler"
2. Right-click "Task Scheduler Library" → Create Basic Task
3. Name: "Erryn Auto-Backup"
4. Trigger: "At log on" → Current user
5. Action: Start a program
   - Program: `C:\Users\stu43\OneDrive\Erryn\Erryns Soul 2025\.venv\Scripts\python.exe`
   - Arguments: `auto_git_backup.py 5`
   - Start in: `C:\Users\stu43\OneDrive\Erryn\Erryns Soul 2025`

## What Gets Backed Up

✅ All code changes  
✅ Memory logs  
✅ Cost tracker data  
✅ Avatar images  
✅ Configuration files  

## View Backups

```powershell
# Show last 10 commits
git log --oneline -10

# See what changed in last backup
git diff HEAD~1 HEAD

# Push to GitHub (if configured)
git push origin main
```

## Safety

- Automatic commits are read-only operations
- Nothing gets deleted
- You can always `git reset` to any previous version
- All backups stored in `.git/` folder (~100MB for years of work)

---

**Your code is now protected!** ✨
