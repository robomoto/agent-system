# Android Device Management — Patterns

## Deployment Mode Selection

### Choose the right mode first — this sets everything else

| Use Case | Mode | Enrollment Method |
|----------|------|-------------------|
| Full control, no user freedom | Fully Managed Device (Device Owner) | QR code at OOBE, NFC, ADB |
| Single/fixed app set (kiosk) | Dedicated Device (subset of Fully Managed) | Same as above |
| Personal device + work separation | Work Profile | Play Store or MDM agent install |
| Kids' family device | Dedicated Device or Family Link | Depends on GMS certification |

### Dedicated Device (Kiosk) Setup Flow

```
1. Factory reset device
2. At OOBE "Connect to WiFi" screen: tap 6 times on any blank area → enter enrollment code
   OR: have MDM QR code ready to scan at OOBE
3. Install MDM agent (DPC app)
4. Set device owner: adb shell dpm set-device-owner <package>/<receiver>
   (only works with zero accounts on device and ADB debug on)
5. Configure kiosk policy: allowlist apps, disable status bar, lock launcher
6. Push approved apps via MDM
```

### ADB-Only Device Owner (no MDM server)

For personal use where you don't want a cloud MDM:
```bash
# Requirements: ADB enabled, NO Google accounts on device, factory-fresh preferred
adb shell dpm set-device-owner com.mypackage/.DeviceAdminReceiver

# Disable Play Store (prevent new installs)
adb shell pm disable-user --user 0 com.android.vending

# Disable browser (Chrome example)
adb shell pm disable-user --user 0 com.android.chrome

# List all packages (find what to disable)
adb shell pm list packages
```

### Managed Google Play vs Sideloading

- **Managed Google Play**: requires GMS certification. MDM can silently push Play Store apps.
- **Sideloading**: works on any Android 8+, GMS-certified or not.
  ```bash
  adb install -r app.apk       # Install or update
  adb install -g app.apk       # Grant all permissions at install time
  ```
- To allow future sideloads from specific sources without user prompt (Device Owner only):
  - Use `DevicePolicyManager.setSecureSetting()` to manage unknown sources per-package.

## Kiosk Launcher Options

| App | Cost | Notes |
|-----|------|-------|
| **SureLock** | Paid | Very polished, enterprise-grade |
| **Kioware** | Paid | Web kiosk focused |
| **Kids Place** | Free/paid | Consumer-grade, simple to configure |
| **Fully Kiosk Browser** | One-time fee | Best for web-app kiosks |
| **Headwind Kiosk** | Open source | Works with Headwind MDM |
| **Custom AOSP Launcher** | DIY | Full control, requires dev work |

## MDM Selection Guide

### Miradore (free cloud MDM)
- Free tier: up to unlimited devices for basic policies
- Supports: app management, kiosk mode, remote wipe, basic restrictions
- Hosted by Miradore; no self-hosting needed
- Best for: small personal deployments, non-technical users

### Headwind MDM (self-hosted)
- Open source (Apache 2.0), runs on Docker
- Full feature set: kiosk, app push, config files, device groups
- Requires a server (can run on home server alongside Audiobookshelf/Plex)
- Best for: privacy-conscious users, existing home server infrastructure

### VMware Workspace ONE / Jamf / Microsoft Intune
- Enterprise-grade; overkill and expensive for personal use
- Skip unless you already have these in place

## Content Restriction Patterns

### Browser Blocking
```bash
# Disable all browser packages
adb shell pm disable-user --user 0 com.android.chrome
adb shell pm disable-user --user 0 com.google.android.browser
adb shell pm disable-user --user 0 com.opera.browser
# Then use MDM allowlist to prevent any new browser installs
```

### App Install Prevention
- Device Owner mode: MDM blocks all installs outside the allowlist
- Without Device Owner: disable Play Store + disable "Install unknown apps" per package
- Nuclear option: Device Owner policy `setPackagesSuspended()` suspends any app

### DNS-Level Filtering
- Pi-hole or NextDNS on home network blocks domains for all devices
- Works even without MDM — complements app-level restrictions
- Does not work on mobile data (LTE), only WiFi
