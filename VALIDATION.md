# Validation record

Local 0.1.0 validation, November 10, 2026. Public source, CI and Pages delivery are separate gates and must not be inferred from local checks.

| Check | Scope | Observed result |
| --- | --- | --- |
| Python unit suite | 18 tests; 76 developed/seeded profiles | Pass |
| Complete report census | 10,427 full orders; 1,542 subset states; 3,883 transitions; 22 cycles | Exact native replay |
| Primitive mutations | Every derived primitive in the first three developed reports, 1,100 mutations | All rejected |
| Node parity | 76 complete append-last JavaScript/prepend-first Python reports | Exact equality plus native replay |
| HiGHS reference | 65 non-singleton integer solves, 422 triangle constraints | Zero observed optimum cost error; tolerance 1e-8 |
| Installed wheel | Clean external environment, six module origins, sixteen controls, two CLI entrypoints | Pass; 32 tampered reports rejected |
| Chrome complete views | Sixteen controls at 1280/390/320 widths | 48 reports, 5,091 selected-order views, 846 subset views |
| Chrome visible ledgers | Direct ballot arithmetic oracle | 12,861 ballot rows; 70,464 pair rows; 24,132 swap rows; 2,019 transition rows |
| Chrome majority graph | All pairs, endpoints, strict/tied directions and arrow geometry | 252 edge instances |
| Chrome downloads | Trusted mouse click and native replay | 16 exact reports |
| Chrome interaction | Input edits, malformed/oversize input, disabled stale export, table scroll, 44px controls and document overflow | Pass |

Thirty-five screenshots captured across controls, widths, optimum/empty-subset states, invalid input and horizontally scrolled tables. Actual pixels inspected. Dense graph labels initially collided; graphs of four or more candidates now omit text labels, retain all strict/tied edges, and point to the complete exact support tables.

Counts describe developed finite cases only. The mutation suite is not a proof of rejection for every conceivable malformed input. HiGHS checks optimum cost, not every tied optimum; exhaustive replay checks complete finite families. Browser row checks independently recompute ledger arithmetic from ballots while also comparing canonical reports. Installed reproduction does not prove an unavailable remote deployment.
