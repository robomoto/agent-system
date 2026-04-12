# Android Device Management — Pitfalls & Footguns

## Device Owner Enrollment

### Footgun: Accounts prevent Device Owner enrollment
If ANY Google account has been added to the device, `adb shell dpm set-device-owner` will fail with:
```
java.lang.IllegalStateException: Not allowed to set the device owner because there are already some accounts on the device
```
**Fix:** Factory reset and do not add any accounts before running the DPC setup.

### Footgun: Device Owner is very hard to remove
Once set, Device Owner can only be removed by:
1. Factory resetting the device, OR
2. The DPC app explicitly removing itself (`dpm.clearDeviceOwnerApp()`)

There is no ADB command to remove Device Owner without a factory reset (without root). Be certain before enrolling.

### Footgun: ADB debug must stay off after enrollment on locked devices
Once you lock down a device with Device Owner, if you disable ADB debugging via policy, you lose remote ADB access. Configure ADB access carefully before locking down.

## Google Play Services / GMS

### Footgun: Budget tablets often lack GMS certification
Signs of a non-certified device:
- No Google Play Store installed
- "Device not certified" error if you try to install Play Store
- Google Play Services may be present but limited

**Impact:** Family Link won't work. Managed Google Play won't work. Apps that use Firebase Cloud Messaging may not receive push notifications.

**Mitigation:** Sideload all APKs directly. Use a non-GMS-dependent MDM (Headwind works fine on non-certified devices).

### Footgun: Aurora Store is NOT the same as Play Store for MDM purposes
Aurora Store can download Play Store APKs, but it bypasses the managed Play Store. MDM app policies don't apply to apps installed via Aurora. Use direct APK sideloading for managed deployments.

## Kiosk Mode

### Footgun: Safe mode bypasses kiosk launchers
On many Android devices, holding Power → holding "Power off" reboots into Safe Mode, which disables third-party launchers, including your kiosk launcher. A child can escape this way.

**Fix:** Device Owner policy can prevent booting into Safe Mode:
```
DevicePolicyManager.setKeyguardDisabledFeatures() 
```
Or via MDM: enforce "block safe mode" policy.

### Footgun: Hardware buttons still work in some kiosk launchers
Volume buttons, power button long-press, recent apps button — these can escape some kiosk launchers.

**Fix:** `DevicePolicyManager.setLockTaskPackages()` with proper lock task features disables these in true lock-task mode.

### Footgun: Kids Place / launcher-replacement kiosks don't survive reboots reliably
Third-party launcher replacements (Kids Place, etc.) don't have Device Owner permissions. A reboot may restore the default launcher. They also don't prevent app installs via ADB.

**Fix:** Use MDM-backed kiosk mode for reliable, persistent enforcement.

## App Management

### Footgun: `pm disable-user` doesn't survive factory reset
All `adb shell pm disable-user` changes are wiped on factory reset. If you re-image the device, you need to re-run all disable commands.

**Fix:** Script it. Keep a `setup-device.sh` that sideloads APKs and disables unwanted packages.

### Footgun: System update apps can re-enable disabled packages
OEM update mechanisms sometimes re-enable or re-install system apps after an OTA update.

**Fix:** With Device Owner, use `setSystemUpdatePolicy()` to control when/if OTA updates apply. Also pin the OS version if possible.

## ADB Backup / Restore

### Footgun: adb backup is deprecated and broken on Android 12+
Starting Android 12, Google deprecated `adb backup`. Many apps opt out via `android:allowBackup="false"`. You will NOT get a complete device clone via adb backup.

**Fix:** Use MDM policy as the source of truth. Configure the policy once, enroll both devices. The policy is the "image."

### Footgun: APK reinstall doesn't restore app data
Reinstalling an APK via `adb install` gives you a fresh install — no saved data, no login state.

**Fix:** For apps where login state matters (Plex, Audiobookshelf), the user must log in manually after install. This is expected behavior. Document it in the setup checklist.

## Family Link

### Footgun: Family Link requires the child's Google account to be supervised
You can't apply Family Link to an existing adult Google account. The child must have a supervised Google account (child under 13 or manually supervised teen account).

### Footgun: Family Link doesn't block all browsers
Family Link can block specific apps, but if a new browser is installed (or a PWA is created), Family Link may not catch it. Combined with an MDM allowlist, this gap is closed.

### Footgun: Family Link supervision ends at 13 (or 18 in some regions)
The child can opt out of supervision when they reach the age threshold. Plan for this eventually.
