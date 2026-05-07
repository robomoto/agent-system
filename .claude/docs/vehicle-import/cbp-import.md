<!-- last_verified: 2026-05-04 -->
# CBP Import — Privately Imported Vehicle from Canada

US-side procedure for a privately imported vehicle entering through a land border. Authority: 19 CFR (CBP), 49 CFR 591 (NHTSA/DOT), 40 CFR 85 (EPA). The vehicle must be released by CBSA on the Canadian side first (see `cbsa-export.md`).

## The Three Federal Forms

At the CBP booth (or secondary inspection if directed), the user presents:

| Form | Issuer | Purpose | Boxes Commonly Used (vehicle ≥25 yrs) |
|---|---|---|---|
| **CBP Form 7501** (Entry Summary) | CBP | Customs entry — duty calculation and entry record | Filled by CBP officer or self-prepared. Informal entry < $2,500 USD; formal entry ≥ $2,500 (most classic vehicles). |
| **HS-7** (DOT/NHTSA Declaration) | DOT — DS-7 in some refs | FMVSS conformance / exemption | **Box 1**: ≥25 years old → exempt from FMVSS. (49 CFR 591.5(i)) |
| **EPA 3520-1** (EPA Engine Declaration) | EPA | Emissions conformance / exemption | **Code E** (≥21 years old, original engine config) for most pre-2005 vehicles. (40 CFR 85.1511) |

CBP keeps copies; the user keeps the **stamped originals** to present to the state DMV later. Without the CBP-stamped HS-7 and 3520-1, no state will title the vehicle.

## 25-Year and 21-Year Exemptions (Critical for Classics)

### NHTSA — 25-year FMVSS exemption (49 CFR 591.5(i))

Vehicles **manufactured at least 25 years before the date of importation** are exempt from FMVSS conformance. Calculated by **month of manufacture**, not model year. The build plate or VIN-decode build date is the controlling fact.

- 1968 model year vehicles built in late 1967 or 1968: well over 25 years old by any 2026 import date. Exemption applies.
- HS-7 Box 1 is the correct exemption box.
- No DOT-Registered Importer (RI) is required.
- No bond is required.

### EPA — 21-year exemption (40 CFR 85.1511(b)(2))

Vehicles **at least 21 years old** AND in **original-equipment configuration** are exempt from EPA emissions standards. EPA 3520-1 exemption code is typically **E** (with the year-of-manufacture noted). For pre-1968 light-duty gas vehicles, additional codes may apply (the original-emission-equipment requirement is moot for vehicles predating federal emission rules).

- "Original configuration" means the engine has not been replaced with a newer non-conforming engine. A period-correct rebuild is fine. An LS swap on an exempt-by-age vehicle creates a fact question — verify before relying on the exemption.

### Newer-than-25-year vehicles (NOT applicable to a 1968 Firebird, but for general agent knowledge)

Vehicles under 25 years old must conform to FMVSS or be imported through a DOT-Registered Importer (RI) under a Conformance Bond, with significant cost (often US$15,000-50,000+ for conversion + bond). EPA conformance similarly required unless ≥21 years and original config.

## HTSUS Classification — Where the Duty Comes From

See `htsus-classification.md` for full analysis. Headline classifications:

| HTSUS Heading | Description | Duty Rate |
|---|---|---|
| **8703.23.0190** | Passenger vehicle, gasoline, 1500-3000cc, used | 2.5% |
| **8703.24.0190** | Passenger vehicle, gasoline, >3000cc, used | 2.5% |
| **9801.00.10** | **US Goods Returning** — articles of US origin returned without improvement abroad | **Free (0%)** |

A 1968 Firebird with its original GM-built drivetrain, US-assembled, qualifies for **9801.00.10** treatment — duty-free — provided the user can document US origin. CBP will accept VIN-decode evidence + build sheet + original window sticker (if available). Without documentation, classification falls to 8703 and 2.5% duty applies on declared value.

## AES / ITN — Generally NOT Required for This Direction

The Automated Export System (AES, now part of ACE AESDirect) and Internal Transaction Number (ITN) requirements are **export** requirements (15 CFR 30), governing what leaves the US. A vehicle **entering** the US from Canada does not need a US-side AES filing. For a US-bound vehicle export, no Canadian-side CERS declaration is filed either — under CBSA Memorandum D20-1-1 ¶ 20 (October 2024 revision), the Canadian export obligation for a US-bound vehicle is documentation-on-request only (VIN documentation presented at the CBSA booth if asked). For non-US-destination exports from Canada, a CERS declaration would be the Canadian export declaration — but that fact pattern does not arise on a Canada-to-US import.

**Exception**: a vehicle that originated in the US, was registered there, exported earlier, and is now being re-exported back through the US — different fact pattern, requires separate analysis.

## Sales Tax / Use Tax at the Border

CBP does **not** collect state sales/use tax. CBP collects federal duty (and the US Customs Merchandise Processing Fee, MPF, if formal entry — minimum ~$31, max ~$614 in 2025-2026). The user pays state use tax to their home-state DMV at registration, NOT at the border.

## Informal vs. Formal Entry

| Threshold | Type | Implications |
|---|---|---|
| < $2,500 USD declared value | Informal | Simpler, no MPF, often handled at the booth |
| ≥ $2,500 USD declared value | Formal | Form 7501 required, MPF applies (~$31 min — $614 max), CBP may require entry filed via ABI by a broker; for personal vehicle imports, CBP regularly accepts self-filed formal entries at the port |

A 1968 Firebird in driver-grade condition will exceed $2,500. Plan on formal entry. The user can self-file at the port — a broker is optional, ~$150-300.

## Document Set at the Booth

| Document | Source |
|---|---|
| Original Alberta registration / Canadian title (CBSA-stamped or with export evidence) | Seller / CBSA stamp |
| Notarized Bill of Sale (English) | Buyer + seller |
| HS-7 (filled by user, stamped by CBP) | DOT form, blank copies at port |
| EPA 3520-1 (filled by user, stamped by CBP) | EPA form, blank copies at port |
| Form 7501 if formal entry | CBP officer or self-filed |
| Photo ID + proof of US residence (utility bill, lease) | User |
| Evidence of US origin (for 9801) — build sheet, VIN decode, window sticker | User research |
| Proof of insurance covering the US drive home | User's insurer |

## Costs (Import Side)

| Cost | Range (USD) | Notes |
|---|---|---|
| Duty (HTSUS 8703.23, if applicable) | 2.5% × declared value | $0 if 9801.00.10 accepted |
| Merchandise Processing Fee (formal entry) | ~$31 (min) to $614 (max) | Based on entry value, ad valorem 0.3464% |
| Optional customs broker | $150-300 | Not required |
| State use tax | Paid later at DMV, NOT to CBP | See state-vehicle-titling-specialist |

## References

- 19 CFR Part 24 (CBP fees), Part 142 (entry of merchandise)
- 49 CFR 591 (DOT importation)
- 40 CFR 85, Subpart P (EPA importation)
- HTSUS Chapter 87, Chapter 98
- CBP Publication: "Importing a Motor Vehicle" (current edition)
- NHTSA "Importing a Motor Vehicle" guidance
- EPA Form 3520-1 instructions
