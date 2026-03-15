# Security Patch Guide

## ⚠️ Your Current Issue

Two security vulnerabilities in .NET SDK (from 2021):
- **GHSA-8p5g-gm8f-2vcw** - Elevation of privilege in .NET Education Bundle
- **GHSA-wx46-m3p3-whv8** - Elevation of privilege in .NET Install Tool

## 🚨 YES, Install Them!

These are legitimate security fixes. **Do this now:**

### Option 1: Update .NET SDK (RECOMMENDED)

The best fix is to update your entire .NET SDK to the latest version.

**Windows:**
```
1. Go to https://dotnet.microsoft.com/download
2. Download .NET 9.0 (latest as of Dec 2025)
3. Run installer
4. Restart your computer
```

**OR via command line:**
```powershell
# Use winget (if installed)
winget install Microsoft.DotNet.SDK.9

# Or download from:
# https://dotnet.microsoft.com/download/dotnet/9.0
```

### Option 2: Install Security Patches Only

If you can't update yet:

**Windows:**
```
1. Go to https://github.com/dotnet/announcements
2. Search for GHSA-8p5g-gm8f-2vcw and GHSA-wx46-m3p3-whv8
3. Download patches from Microsoft Security Advisory
```

## ✅ After Installing

Verify installation:
```powershell
dotnet --version
```

Should show **9.0** or higher.

## 🔒 VS Code Extensions

After updating .NET:

1. Open VS Code
2. Extensions → Search "C#"
3. Install latest C# Dev Kit (if you use it)
4. Reload VS Code

## Why This Matters

❌ **Old SDK** = potential privilege escalation on your machine  
✅ **Updated SDK** = secure, with latest features  

**Install today. Takes 5 minutes.**

---

For Erryn's Soul specifically:
- We're using Python (not .NET)
- But C# might be needed for cloud integrations
- Keep your system patched for security
