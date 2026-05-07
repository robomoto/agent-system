<!-- last_verified: 2026-05-04 -->
# Alberta → Washington Route — Specifics

This bundle entry is the route-specific overlay on top of `cbsa-export.md` and `cbp-import.md` for the most common Alberta-to-Washington personal vehicle import path.

## Route Choice — Two Reasonable Options

### Option A — Direct West Through BC, Cross Into WA (recommended for most buyers)

Drive AB → BC → cross into WA. The destination state (WA) is also the import state, so the vehicle's first and only US road miles are in WA. Single state insurance, single state DMV.

**Crossings (BC → WA)** that handle vehicle export/import:
- **Pacific Highway, BC ↔ Blaine, WA** (Truck Crossing) — best for vehicle moves; staffed for commercial-style entries; closest to I-5 south
- **Aldergrove, BC ↔ Lynden, WA** — secondary option
- **Sumas, BC ↔ Sumas, WA** — works but smaller staffing
- **Osoyoos, BC ↔ Oroville, WA** — eastern option, high-clearance into central WA

### Option B — Cross at Coutts/Sweetgrass and Drive West Through MT/ID/WA

Direct from southern Alberta to Montana, then west on I-90/US-2 through MT, ID, and into WA. Adds 800-1000 miles and three states' worth of transit insurance/registration considerations.

**Use only if**:
- The seller is in southern AB and the user wants to minimize Canadian driving
- The user has a specific reason (e.g., wants to visit Glacier en route)

**Adds complexity**:
- Driving through Montana and Idaho on a foreign-titled vehicle requires a transit/trip permit in **each** state, or insurance with broad transit coverage (most carriers will write it as "in transit to home state" but confirm)
- Reciprocity rules between Canadian provincial registration and US states are inconsistent — most states honor a 30-day visitor period but a vehicle being permanently imported and driven home is not a "visit"

## Alberta-Specific Export Steps

### 1. Pre-Sale Due Diligence

- **PPR lien search**: Alberta Personal Property Registry (alberta.ca/personal-property-registry). Search by VIN. CAD ~$10. Demonstrates clear title, required for export.
- **CarProof / Carfax Canada** report (~CAD 50): odometer history, accident reports, branded-title check. **Note: only works on 17-character (post-1981) VINs.** Pre-1981 vehicles (e.g., a 1968 GM with a 13-character VIN like `223378U134833`) cannot be looked up. Substitutes: provincial PPR lien search, NICB VINCheck (theft/total-loss flags), and asking the seller for any prior ownership paperwork they retained.
- **Pontiac Historical Services** report (PHS, USD $110 as of 2026): for any classic Pontiac, gives factory build sheet, options, dealer destination, paint/trim codes. Independent but invaluable for 9801 origin documentation.

### 2. Bill of Sale

**Terminology note**: Alberta does not issue "titles" the way US states do. There is no Alberta document called a "title." The functional equivalent for export purposes is:

1. The **Vehicle Registration Certificate** (the document Service Alberta issues — sometimes called "the registration" or "the ownership" colloquially)
2. A signed, notarized **Bill of Sale**
3. A **PPR lien search** showing no recorded liens

If the Alberta seller is confused by "clear Canadian title," the buyer should translate: *"I need your Vehicle Registration Certificate and a PPR lien search showing no liens, plus a notarized Bill of Sale."* See `seller-checklist-alberta.md` for a full plain-language packet to send the seller.

The Bill of Sale should be:

- In **English** (or English translation)
- **Notarized** (Alberta Commissioner for Oaths or notary, CAD ~$20-100). Not strictly required by CBSA but several CBP officers expect it.
- Include: VIN, year/make/model, sale price (CAD AND USD equivalent), date of sale, full names and addresses of buyer and seller, signatures, odometer reading, statement that the vehicle is sold "as-is for export to the United States"

### 3. Tax Treatment

- **No Alberta provincial sales tax** (AB is the only province with no PST). Buyer pays no provincial tax to Alberta.
- **GST**: Private sales between individuals are not GST-able. Dealer sales to a non-resident for export are typically zero-rated; if charged, the buyer can claim a rebate via CRA Form GST189 (Code 1A). Verify with the dealer at sale time.

### 4. CERS Filing

Submit the CERS export declaration via the CBSA portal **at least 72 hours** before the intended crossing time. Note in the declaration:
- Port of exit (matches the chosen crossing — if the user picks Pacific Highway, file for Pacific Highway)
- VIN, year/make/model
- Declared export value (CAD)
- Buyer (importer) name and address (US side)
- Estimated crossing date/time

Print or save the CERS proof-of-report number.

### 5. Day of Crossing — CBSA Side

1. Arrive at the designated CBSA port during business hours (verify hours; some are M-F only for vehicle export)
2. Present documents: registration, Bill of Sale, lien search, CERS proof, photo ID
3. CBSA stamps the registration "EXPORTED" or surrenders it (varies by office); user keeps the stamped copy
4. Drive to the US side and continue at CBP

## Washington-Specific Import Considerations

(Detailed state-side titling work belongs to `state-vehicle-titling-specialist`. This section is just what affects the **border** decision.)

- **WA does not collect use tax at the border** — it is collected when titling at the WA Department of Licensing (DOL).
- **WA uses USD**; the bill of sale will need a USD equivalent for the entry summary. Use the Bank of Canada or CBP's daily rate at the date of entry.
- **WA emissions inspection**: WA discontinued routine emissions testing in 2020 statewide. Not a factor.
- **WA antique vehicle status (≥30 years)**: Available; this affects registration choice not the import itself. See state-titling specialist.

## Alternative Pattern — Pay-from-US, File-from-US

The default timeline above (Pattern A) assumes the buyer travels to Alberta, completes the sale at a registry agent on T-4, and files CERS the same afternoon. A second valid pattern (Pattern B) compresses time-in-Canada by paying remotely and filing CERS from the US:

```
T-11 to T-10: register CERS account (1-3 business day verification)
T-8 to T-5  : lock deal with seller — signed agreement, photos, wire transfer or escrow
T-4 morning : file CERS from the US with VIN, agreed value, planned port, crossing date
T-3, T-2    : 72-hour clock + travel preparation
T-1         : travel to Alberta
T-0 morning : registry agent — notarized Bill of Sale, signed-over registration, fresh PPR search
T-0 same day: drive to Pacific Highway, cross CBSA -> CBP
```

**Trade-offs**:

| | Pattern A (in-country, then file) | Pattern B (pay-from-US, file-from-US) |
|---|---|---|
| Time in Canada | 5-7 days | 1-2 days |
| Pricing risk | Locked at sale-day | Locked early |
| Counterparty risk | Inspect before paying | Wire to stranger before inspection |
| Buffer for issues | 4 days between sale and crossing | Issues compress into one day |
| CERS account | Needed only if buyer files | Buyer almost certainly files |
| Best for | First-time imports, unknown sellers, complex cars | Repeat buyers, well-documented sellers, simple transactions |

**Pattern B mitigations** (if the buyer chooses this path):

- Require live video walk-around of the vehicle before paying
- Require photo of seller's ID matching the registration certificate name
- Verify seller's phone number against publicly-listed address (reverse lookup)
- Deposit-then-balance structure: 20-30% deposit on signed agreement, balance by bank draft at registry agent
- Use an escrow service for vehicles >US$25K (e.g., escrow.com — vehicle category fee ~1% of value)
- Verify the registration certificate is genuine (call the seller's local Service Alberta registry to confirm format)

Pattern B is fine if executed carefully. The framework's default narrative uses Pattern A for the conservative recommendation; the underlying regulations support either.

## Ballpark Cost Stack — Alberta to Washington (1968 Firebird, $30K USD value, US Goods Returning accepted)

| Item | Estimated cost |
|---|---|
| Alberta PPR lien search | CAD 10-15 |
| Notary (Bill of Sale) | CAD 25-100 |
| PHS build sheet (optional, recommended) | USD $110 |
| CERS filing | $0 (free) |
| CBSA export | $0 |
| CBP duty (with 9801) | $0 (else $750 at 2.5%) |
| CBP MPF (formal entry) | ~USD 100-115 (≈ 0.3464% × $30K, capped) |
| Customs broker (optional) | USD 0-300 |
| Drive-home transit insurance (3-7 days) | USD 50-150 (see insurance team) |
| WA trip permit (3-day) | USD 30 each |
| WA use tax (paid at DOL, not border) | ~6.5% state + local 1-3.5% × $30K = ~USD 2,250-3,000 |
| WA title + first-year registration (antique) | USD ~75-150 |

**Federal-side total at the border**: ~USD 100-1,000 depending on 9801 acceptance and broker use.
**Total project cost beyond the purchase**: dominated by **WA use tax** (~$2,250-3,000), which is a state-side expense, not a border one.

## References

- See `cbsa-export.md`, `cbp-import.md`, `htsus-classification.md` for the underlying rules
- BC border crossings official wait-time list: borderlineups.com / cbsa-asfc.gc.ca
- WA DOL: dol.wa.gov/vehicleregistration
