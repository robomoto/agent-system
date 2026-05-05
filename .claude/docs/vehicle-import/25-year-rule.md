<!-- last_verified: 2026-05-04 -->
# The 25-Year Rule (FMVSS) and 21-Year Rule (EPA)

Two distinct federal exemptions, often conflated. Both apply to most classic-vehicle imports but have different statutory bases and different age thresholds.

## NHTSA / DOT — 25 Years (FMVSS Exemption)

**Authority**: 49 CFR 591.5(i); Motor Vehicle Information and Cost Savings Act, 49 USC 30112(b)(9)

**Rule**: A motor vehicle "at least 25 years old" at the time of importation is exempt from Federal Motor Vehicle Safety Standards (FMVSS) conformity requirements. The vehicle does not need bumpers, airbags, daytime running lamps, side-impact protection, or any other FMVSS — it can be imported as-is in its as-built condition.

**Calculation**: The age is measured from the **date of manufacture** to the **date of importation**, not by model year. CBP looks at the vehicle's build plate (VIN-stamped or door-jamb sticker) to determine the build month/year.

- 1968 Pontiac Firebird: most production runs 1967-08-26 (start) through 1968-12 (end of model year). All such vehicles became 25 years old between 1992-08 and 1993-12. Comfortably exempt for any 2026 importation.

**Import process**:
- Box 1 on **Form HS-7** (DOT Declaration) is checked
- No DOT-Registered Importer (RI) required
- No conformance bond required
- No structural/safety modifications required

**Aftermath**:
- The vehicle remains exempt for life — it does not lose exemption when sold or re-titled
- States cannot require FMVSS conformity as a titling condition (federal preemption); they can require equipment that's part of state vehicle code (working headlights, seat belts if originally equipped, etc.)

## EPA — 21 Years (Emissions Exemption)

**Authority**: 40 CFR 85.1511(b)(2); 42 USC 7522

**Rule**: A vehicle that is **at least 21 years old** AND **in its original equipment configuration** is exempt from EPA emissions conformity requirements. Verified by EPA Form **3520-1**, exemption **Code E**.

**"Original equipment configuration"**: The engine, fuel system, and emission-control devices (if the vehicle was originally equipped with any) must be substantially as originally manufactured. Defined by EPA as "no modifications which would render the engine non-original or non-compliant with the standards applicable when manufactured."

- Period-correct rebuilds: OK.
- Replacing the original 350 with a period-correct GM 350: OK.
- LS swap, modern fuel injection retrofit on an exempt-by-age vehicle: gray area. Some interpret "≥21 years" as a hard cutoff; EPA enforcement focuses on whether the vehicle is being imported to circumvent emissions standards. For a 50+ year-old vehicle, this is rarely contested. Document the engine clearly.

**Pre-1968 vehicles**: Light-duty gasoline vehicles manufactured before model year 1968 generally predate federal emissions standards entirely. EPA Form 3520-1 still must be filed; the appropriate exemption code is typically the same Code E (age-based) — alternative codes exist but Code E is universally accepted for ≥21-year-old vehicles.

**Heavy-duty / non-road / motorcycle**: Different sub-paragraphs of 40 CFR 85.1511. Out of scope for passenger-car imports.

## Why Both Exemptions Matter

A vehicle could in theory be EPA-exempt (≥21 years) but not FMVSS-exempt (<25 years) — a 22-year-old import. That 4-year gap is where DOT-Registered Importers (RIs) thrive: they bring vehicles into FMVSS conformity for a fee. For our use case (1968 vehicle in 2026), both exemptions apply with margin.

## Calculation Worksheet (Agent Use)

Given: vehicle build date (month/year) and intended import date.

```
age_at_import = (import_year - build_year) + (1 if import_month >= build_month else 0) - (1 if import_month < build_month else 0)
```

For a 1968 model-year vehicle built between 1967-08 and 1968-12, imported May 2026:
- Lower bound: 2026-05 minus 1968-12 = 57 years 5 months
- Upper bound: 2026-05 minus 1967-08 = 58 years 9 months

Both well over 25 (FMVSS) and 21 (EPA) — no margin issues.

## What the Agent Should Always Confirm

1. The exact **month and year of manufacture** from the VIN/build plate (not just the model year)
2. The **engine configuration** is original or period-correct (for EPA Code E)
3. The user has **photographic evidence** of the build plate to take to the border
4. The **CBP officer's stamped HS-7 and 3520-1** are retained for state titling

## References

- 49 CFR 591.5 — Permitted importation of nonconforming motor vehicles
- 40 CFR 85.1511 — Exemptions for motor vehicles
- NHTSA Form HS-7 (current revision)
- EPA Form 3520-1 (current revision)
- 49 USC 30112; 42 USC 7522
