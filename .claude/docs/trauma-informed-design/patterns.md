# Trauma-Informed Design Patterns

## 1. The Dual-Use Device Problem

Counter-surveillance tools for DV/stalking victims face a fundamental tension: the device must be useful enough to justify carrying, innocent enough to survive discovery, and capable enough to provide real protection.

### Pattern: Genuine Primary Function
The device should BE what it claims to be. A "fitness tracker that secretly detects surveillance" is more robust than a "surveillance detector disguised as a fitness tracker." The difference matters when an abuser picks it up — real step data, real usage history, real wear patterns make the cover credible.

### Pattern: Silent Background Protection
Surveillance detection should never interrupt the primary experience unless it has actionable intelligence. The user should not need to "check" for threats. The device watches; the user lives their life. Alerts surface only when there's something the user can act on.

### Pattern: Layered Disclosure
- **Layer 0**: What anyone sees (fitness tracker UI, step counts)
- **Layer 1**: What the user sees with normal interaction (health features, settings)
- **Layer 2**: What the user sees with authentication (surveillance alerts, detection history)
- **Layer 3**: What a forensic examiner finds (encrypted detection database, device logs)

Each layer requires escalating access. An abuser who grabs the device sees Layer 0. An abuser who demands "show me what this does" sees Layer 1. Only the user (with PIN/pattern) reaches Layer 2.

## 2. Designing for Duress

### The Freeze Response
Under acute threat, users experience:
- Cognitive narrowing (can only process one thing at a time)
- Fine motor degradation (hands shake, can't hit small targets)
- Time distortion (seconds feel like minutes or vice versa)
- Decision paralysis (can't choose between options)

**Design implication**: Any action the user needs to take under duress must be a single, large, gross-motor action. Hold one button. Shake the device. No menus, no confirmation dialogs, no sequences.

### The Fawn Response
Some trauma survivors comply with demands as a survival strategy. If an abuser says "give me your phone" or "show me what that does," the user may hand over the device.

**Design implication**: The device must be safe to hand over. Whatever the abuser sees should be boring, plausible, and not reveal the user's counter-surveillance activity or sensitive health data.

### Dissociation
Under extreme stress, users may experience depersonalization, memory gaps, or emotional numbness. They may not remember what they did with the device during a crisis.

**Design implication**: Critical safety actions should be automatic, not user-initiated. Evidence should sync without user action. Alerts should persist until explicitly dismissed. The device should never require the user to "remember" to do something during a crisis.

## 3. The Abuser as Adversary

### Discovery Scenarios
1. **Casual discovery**: Abuser picks up device, looks at screen, puts it down. Must survive this.
2. **Suspicious investigation**: Abuser scrolls through menus, checks settings. Must survive this.
3. **Demanded demonstration**: Abuser says "show me everything on this." Must survive this with user cooperation.
4. **Technical examination**: Abuser connects to computer, checks app stores, Googles the device name. Must survive or at minimum not reveal surveillance data.
5. **Forensic examination**: Abuser hires technical expert or law enforcement seizes device. Encryption is the only protection here.

### Weaponization Patterns
Abusers weaponize discovered information by:
- **Undermining**: Using health data to attack credibility ("she's mentally unstable, look at her mood scores")
- **Controlling**: Using cycle data for reproductive coercion
- **Retaliating**: Escalating violence after discovering counter-surveillance
- **Legal leverage**: Using discovered features to claim victim was "spying" or "entrapping"

## 4. Evidence Handling

### What Prosecutors Actually Need
- **Timestamped records** of surveillance events (device X at location Y at time Z)
- **Pattern evidence** showing repeated, targeted behavior (same device following across multiple locations/days)
- **Contemporaneous documentation** (records made at or near the time of events, not reconstructed later)
- **Chain of custody** (who had access to the device and when)
- **No tampering indicators** (signed data, tamper-evident logs)

### What Defense Attorneys Attack
- Data integrity ("how do we know this wasn't fabricated?")
- User reliability ("the complainant was anxious/depressed/using substances — see their own device data")
- Device reliability ("this is a homebrew gadget, not a forensic tool")
- Selective presentation ("why was some data wiped? What was the user hiding?")
- Intent framing ("the complainant was conducting surveillance of my client")

### The Quick-Wipe Dilemma
Quick-wipe protects the user from immediate physical danger (abuser demanding to see data). But:
- It destroys evidence that may be needed for prosecution
- It can be characterized as spoliation of evidence in court
- It reveals the device has something to hide (a wiped device is suspicious)
- It may not be executable under duress (cognitive load, time pressure)

Best practice from DV advocacy: **get the evidence off the device as soon as possible.** The safest data is data that has already been transmitted to a secure location (advocate's office, cloud storage, attorney). The device should be a temporary collection point, not an evidence vault.

## 5. Safety Planning Integration

### NNEDV Safety Net Principles (adapted)
1. **Technology is not neutral** — it can help or harm depending on context
2. **The survivor is the expert on their situation** — tools should empower choices, not make decisions
3. **Safety planning is ongoing** — a single setup is not enough; risk changes over time
4. **Technology safety is part of overall safety** — device decisions connect to housing, legal, financial safety
5. **Discovery of safety tools can trigger escalation** — the tool itself can become a danger

### When a Safety Tool Becomes a Liability
A counter-surveillance device becomes net-negative when:
- Discovery risk is high and the abuser is violence-prone (device discovery triggers escalation)
- The user becomes dependent on the device for safety (false sense of security)
- The device creates evidence that can be used against the user
- The cognitive/emotional burden of using the device exceeds the protection it provides
- The device delays more effective interventions (leaving, getting a protection order, involving law enforcement)
