# Android Device Management — Reference

## Key ADB Commands

```bash
# Device info
adb shell getprop ro.build.version.release          # Android version
adb shell getprop ro.product.model                   # Device model
adb shell getprop ro.product.manufacturer

# Package management
adb shell pm list packages                           # All packages
adb shell pm list packages -3                        # Third-party only
adb shell pm list packages | grep chrome             # Find specific app
adb shell pm disable-user --user 0 <package>         # Disable app
adb shell pm enable <package>                        # Re-enable app
adb install -r -g app.apk                            # Install + grant permissions

# Device Owner
adb shell dpm set-device-owner <package>/<receiver>  # Set device owner
adb shell dpm remove-active-admin <package>/<receiver> # Remove (if not owner)

# Check GMS certification
adb shell pm path com.google.android.gsf            # If absent: no GMS

# Useful for setup scripting
adb devices                                          # List connected devices
adb -s <serial> install app.apk                     # Target specific device
```

## Android Enterprise APIs (Device Owner)

| Policy | API | Notes |
|--------|-----|-------|
| Block app installs | `setPackageInstallationGranted(false)` | Prevents all new installs |
| Whitelist apps | `setPackagesSuspended()` inverse, or use MDM | Suspend non-approved apps |
| Disable safe mode | `setKeyguardDisabledFeatures()` | Requires Device Owner |
| Lock task mode | `setLockTaskPackages()` | Pins specified apps |
| Block USB data | `setSecureSetting("adb_enabled", "0")` | Disables ADB remotely |
| System update policy | `setSystemUpdatePolicy()` | Defer or block OTA |
| Screen lock policy | `setPasswordMinimumLength()` etc. | Enforce PIN/password |
| Factory reset protection | `setFactoryResetProtectionPolicy()` | Requires specific Google account |

## MDM Tools Reference

### Headwind MDM (self-hosted)
- Repo: https://github.com/h-mdm/hmdm-server
- Docker compose: one command setup
- Agent APK: download from Headwind server after setup
- Port: 8080 (HTTP) or 443 (HTTPS with nginx reverse proxy)
- Enrollment: QR code or 6-digit code
- App push: upload APK to Headwind, assign to device group

### Miradore
- Web console: https://www.miradore.com
- Free tier limits: basic app management, device restrictions, remote wipe
- Android enrollment: install Miradore client from Play Store or APK, enter enrollment key
- Kiosk mode: available in paid tier (check current pricing)

## Common Package Names

| App | Package |
|-----|---------|
| Google Chrome | `com.android.chrome` |
| Google Play Store | `com.android.vending` |
| Google Play Services | `com.google.android.gms` |
| Gmail | `com.google.android.gm` |
| YouTube | `com.google.android.youtube` |
| Settings | `com.android.settings` |
| Audiobookshelf | `com.audiobookshelf.app` |
| Plex | `com.plexapp.android` |

## Audiobookshelf Server: User Permissions

In Audiobookshelf server settings, per-user permissions:
- **Library access**: restrict to specific libraries
- **Download**: enable/disable download permission per user
- **Manage items**: enable/disable (disable for kids)
- **Upload**: enable/disable (disable for kids)
- **Delete items**: enable/disable (disable for kids)

Recommended children's account setup:
1. Create dedicated "Kids" library on server
2. Create child user account
3. Grant access only to "Kids" library
4. Disable: manage items, upload, delete
5. Enable: download (if offline listening desired)

## Plex Managed Users

Requires Plex Pass.

Setup:
1. plex.tv → Settings → Managed Users → Add Managed User
2. Set content rating limit per user (G, PG, PG-13, etc.)
3. Set a PIN so child cannot switch accounts on device
4. Share only specific libraries with the managed user

Library sharing without Plex Pass (limited):
- Can share entire libraries to a separate Plex account
- No rating-based filtering
- No PIN enforcement

## Sora (OverDrive) — Student Library App

If the intended app is Sora by OverDrive (not OpenAI):
- Package: `com.overdrive.mobile.android.sora`
- Available on Google Play
- Designed for K-12 school library access
- Students sign in via school credentials (Clever, ClassLink, Google, or school code)
- Content is curated by the school/library — inherently age-appropriate
- Works offline (download books/audiobooks)
- No parental controls needed — content is managed by the institution

## Sora (OpenAI) — Video Generation AI

If the intended app is OpenAI Sora:
- Requires OpenAI account (18+ in most regions, 13+ with parental consent)
- Generates arbitrary video from text prompts
- No parental supervision mode
- Android app availability was limited as of mid-2025 — verify current status
- Not recommended as a kids' app — content generation is unpredictable despite safety filters

## Device Imaging Alternatives

Since true disk imaging requires root (not available on locked budget tablets):

**Option A: MDM as source of truth (recommended)**
- Configure policy in MDM dashboard
- Enroll both devices — both receive identical configuration automatically
- Update policy once to update both devices

**Option B: ADB setup script**
```bash
#!/bin/bash
# setup-device.sh — run on each device after factory reset

# Install apps
adb install -g audiobookshelf.apk
adb install -g plex.apk
adb install -g sora.apk

# Disable unwanted system apps
adb shell pm disable-user --user 0 com.android.chrome
adb shell pm disable-user --user 0 com.android.vending
adb shell pm disable-user --user 0 com.google.android.youtube

# Push config files if needed
adb push config/ /sdcard/config/

echo "Device setup complete. Log in to each app manually."
```

**Option C: Swift Backup (partial app data)**
- Backs up apps that allow backup (allowBackup=true)
- Audiobookshelf and Plex may or may not allow backup
- Won't backup account credentials (login state)
- Good for: settings/preferences within apps, downloaded content
