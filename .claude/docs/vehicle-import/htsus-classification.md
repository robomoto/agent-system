<!-- last_verified: 2026-05-04 -->
# HTSUS Classification — Personally Imported Vehicles

The Harmonized Tariff Schedule of the United States determines duty owed at CBP. For privately-imported passenger vehicles from Canada, two analyses run in parallel and the user picks the better-supported one:

1. **Chapter 87** — vehicles classified by engine type, displacement, and use → 2.5% duty (passenger cars)
2. **Chapter 98 (heading 9801)** — US Goods Returning → 0% duty if the vehicle was originally manufactured in the US

For a US-built classic muscle car, **9801** is usually available and saves the duty. The agent's job is to assemble the evidence the user needs.

## Chapter 87 — Default Classification

Passenger vehicles fall under **8703**. Subheadings depend on engine type, displacement, and whether new or used.

| HTSUS | Description | Duty (general) |
|---|---|---|
| 8703.21.0190 | Used passenger vehicle, gasoline, ≤1000cc | 2.5% |
| 8703.22.0110/.0190 | Used passenger vehicle, gasoline, 1000-1500cc | 2.5% |
| **8703.23.0190** | **Used passenger vehicle, gasoline, 1500-3000cc** | **2.5%** |
| **8703.24.0190** | **Used passenger vehicle, gasoline, >3000cc** | **2.5%** |
| 8703.31.0090 | Used passenger vehicle, diesel, ≤1500cc | 2.5% |
| 8704.x | Trucks/cargo | **25%** ("Chicken Tax") |

A 1968 Firebird with the 350 cu in (5.7L) base engine: 8703.24 (>3000cc). With the 230 cu in straight-six (3.8L): 8703.24 still applies (just over 3L). Either way: 2.5% × declared value if 9801 is unavailable.

**Declared value**: the price actually paid (Bill of Sale), converted to USD at the day-of-entry rate published by CBP. The user cannot lowball the declared value — CBP officers are familiar with collector-car pricing (NADA Classic, Hagerty Valuation Tool) and will challenge values that look manipulative.

## Chapter 98, Heading 9801.00.10 — US Goods Returning

**Rule**: Articles of US origin that are returned to the US after having been exported, **without having been advanced in value or improved in condition** by any process of manufacture or other means while abroad, enter duty-free.

For a vehicle, the test is:

1. **Was it originally manufactured in the US?** (Look at VIN 1st digit and assembly plant code — for GM 1968s, the 11-digit VIN's plant code is the 6th character; see Pontiac VIN decode references.)
2. **Has it been "improved in condition" abroad?** Routine maintenance and ordinary repair are NOT "improvement". A Canadian rebuild of a US-origin engine is fine. A Canadian conversion (e.g., to right-hand-drive, or a major value-adding restoration done abroad) is risk territory.

**Documentation that supports a 9801 claim**:

| Evidence | Strength |
|---|---|
| Original window sticker / Pontiac Historical Services build sheet | Strongest |
| VIN decode showing US assembly plant (Lordstown OH or Norwood OH for 1968 Firebirds) | Strong |
| Photos of the trim tag / cowl tag with plant code | Strong |
| Statement from a marque historian (e.g., POCI, Pontiac Historic Services) | Moderate |
| User's own assertion alone | Weak — CBP wants documents |

**1968 Pontiac Firebird specifically**: Assembled at GM Lordstown Assembly (Ohio) and Norwood Assembly (Ohio) for the 1968 model year. VIN-decode plant code: **L** = Lordstown, **N** = Norwood. Either qualifies as US origin for 9801 purposes.

## Practical Recommendation for the User

1. Before the border, assemble the documentation pack:
   - Photos of the VIN plate and cowl tag
   - VIN decode (any reputable decoder will identify the assembly plant)
   - If available, Pontiac Historical Services (PHS) report (USD $110 as of 2026, good investment for any 1968 Firebird and adds collector-market value too)
2. Declare 9801.00.10 on the Form 7501 line for the vehicle, with 8703.24 as a fallback.
3. The CBP officer has discretion. If they reject 9801, duty falls to 8703.24 (2.5%). The user pays at the booth (credit card or cash; bank-issued checks may not be accepted at small ports).

## Other Possible 9801 / Chapter 98 Provisions (Edge Cases)

- **9801.00.20**: US articles returned after rental abroad, etc. — not applicable
- **9802.00.50**: Foreign articles returned after repair/alteration abroad — applies if a US-origin vehicle was sent abroad for restoration; duty only on the value added. Rare for our scenario.
- **9817.00.40**: Articles for the Olympics — humor only.

## Other Costs Driven by HTSUS

- **Merchandise Processing Fee (MPF)**: 0.3464% ad valorem, min ~$31, max ~$614 (2025-2026). Applies on formal entries (vehicles ≥ $2,500). Note: if 9801.00.10 is accepted, MPF still applies — it's a fee, not a duty.
- **Harbor Maintenance Fee**: not applicable to land-border imports.
- **State use tax**: NOT collected at CBP. Paid to the user's state DMV. See `state-vehicle-titling-specialist`.

## References

- HTSUS, current edition (USITC publishes annually): hts.usitc.gov
- 19 CFR 10.1 — US Goods Returning documentation
- 19 CFR 24.23 — Merchandise Processing Fee
- CBP Informed Compliance Publication: "What Every Member of the Trade Community Should Know About: Classification of Motor Vehicles"
