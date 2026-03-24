<!-- last_verified: 2026-03-16 -->
# Trauma-Informed Design Footguns

## 1. Assuming the User Has Privacy

The most dangerous assumption in DV/stalking product design is that the user controls their own device. Abusers commonly:
- Demand to see the victim's phone/devices
- Know the victim's passwords and PINs
- Have installed monitoring software on the victim's devices
- Check the victim's devices while they sleep
- Control the household WiFi and can see network traffic

**Never assume the user is the only person who will interact with the device.**

## 2. Hypervigilance Amplification

A device that constantly alerts to potential threats makes anxious people more anxious. If every BLE device triggers a notification, the user lives in a state of perpetual alarm. This is not protection — it's re-traumatization through technology.

**Threshold your alerts ruthlessly.** Only surface detections that represent genuine, actionable threats (correlation across multiple locations, known tracker signatures). Let the user live their life between alerts.

## 3. The "Smart" Feature That Betrays

Auto-correlating data streams (mood + surveillance events, location + health data) creates pre-built narratives that can be weaponized. What the designer sees as "helpful context" becomes ammunition for a defense attorney or an abuser.

**Keep data streams independent.** Let humans draw correlations in appropriate contexts (with an attorney, with an advocate). The device should store facts, not interpretations.

## 4. Stealth Mode That Isn't Stealthy

A "stealth mode" that changes the device's behavior (different screen, different BLE name, buzzer disabled) is only useful if the transition is invisible. If there's a noticeable lag, a screen flash, or a different boot sequence, a suspicious abuser will notice.

**Test stealth transitions from the abuser's perspective.** Can you tell the device just switched modes? Is the fake display convincing under scrutiny? Does the BLE name change appear in paired device lists?

## 5. Quick-Wipe as Security Theater

A quick-wipe that requires a complex button combination under duress is useless. A quick-wipe that leaves forensic traces is worse than useless (it shows the user had something to hide). A quick-wipe that's too easy to trigger accidentally destroys evidence.

**Quick-wipe is almost always the wrong solution.** The right solution is: evidence leaves the device automatically and continuously. The device is safe to hand over because the important data is already somewhere else.

## 6. Designing for the User You Want, Not the User You Have

DV/stalking victims are not security researchers. They may be:
- Exhausted from chronic stress and sleep deprivation
- Managing PTSD, depression, or anxiety
- Cognitively impaired by trauma
- Unfamiliar with technology
- Using the device intermittently (fear of discovery)
- In a rush (checking during the 5 minutes the abuser is in the shower)

**Design for the worst day, not the best day.** If a feature requires focus, patience, or technical knowledge, it will fail when it's needed most.

## 7. The Evidence Destruction Trap

Destroying evidence feels protective but can:
- Eliminate the victim's best chance at a protection order or conviction
- Be characterized as spoliation in court proceedings
- Remove the victim's own record of what happened to them
- Create a pattern where the abuser learns to trigger wipes ("show me your phone" → victim wipes → abuser learns the device has secrets)

**The priority should be evidence exfiltration, not evidence destruction.** Get the data to a safe place. Then the device doesn't matter.

## 8. Notification Design That Endangers

An alert that makes noise, lights up the screen, or changes the display while the abuser is present can:
- Reveal that the device is monitoring for threats
- Trigger the abuser's suspicion or anger
- Force the victim to explain what just happened
- Create a crisis in a moment the victim wasn't prepared for

**Alerts must be contextually safe.** The default should be silent, visual-only, and deniable ("oh that's just my step goal notification").

## 9. Collecting Data the User Can't Delete

If the user can't completely and verifiably delete data from the device, the device is a liability. Users must be able to:
- Delete any individual record
- Verify that deletion is complete (not just hidden)
- Trust that "deleted" means "unrecoverable" (not in a trash folder, not in a log, not in flash wear-leveling residue)

**If you can't guarantee complete deletion on embedded flash, be honest about that limitation.**

## 10. Forgetting That Discovery Escalates Violence

The single most important fact in DV/stalking safety: **discovery of counter-surveillance measures can trigger escalation to lethal violence.** An abuser who discovers that their victim is monitoring for trackers may interpret this as:
- The victim is planning to leave (a high-lethality trigger)
- The victim is building a legal case (threatening the abuser's freedom)
- The victim is outsmarting them (narcissistic injury)

**Every feature must pass the question: "If discovery of this feature triggers a violent escalation, is the protection it provides worth that risk?"**
