# OrderLab

OrderLab combines complete rankings into a total order with the least weighted
pairwise disagreement. Supply strict rankings and integer multiplicities, then
compare exact Kemeny optima with an adjacent-swap local search. A local search
can stop even when a better order exists.

The browser shows the pairwise majority graph, subset recurrence, every complete
order's cost and the descent trace. Export a report and replay it with the
independent Python checker. The implementation stops at six candidates so all
optimal orders can be retained and checked.

This implements classical rank aggregation, not a new method or a learned
ranker. The examples are constructed controls, not held-out evaluation. The
package and browser need no paid API, server or runtime dependency.

## The counterexample

| Ballot | Multiplicity |
| --- | ---: |
| 0 > 1 > 2 | 3 |
| 1 > 2 > 0 | 2 |
| 2 > 0 > 1 | 2 |

Starting at `1 > 2 > 0`, cost is **10**. Its adjacent swaps increase cost by **3** and **1**, so it is a strict adjacent-local minimum. The unique global optimum `0 > 1 > 2` costs **8**. The pairwise-independent lower bound is **7**. The local/global gap is **2**; the optimum exceeds the independent pair bound by **1**.

The cycle `0 > 1 > 2 > 0` has majority margins `3, 3, 1`. Breaking its cheapest edge costs one extra unit, not an entire ballot and not a count of cycles. See [METHOD.md](METHOD.md) for definitions, proof and limits.

## Run locally

Python 3.10+, Node 22+ for tests. The Python package and browser engine have no runtime packages.

```sh
python -m pip install .
orderlab demo > report.json
orderlab verify report.json
python -m orderlab run examples/strict_local_gap.json > report.json
python -m orderlab verify report.json
python -m http.server 8000 --directory docs
# Open http://localhost:8000
```

The CLI writes a canonical JSON report, or `{"valid":true}` for successful replay. A rejected input or report exits 2 and writes a diagnostic to stderr, without a success object. `run` input is capped at 64 KiB; report replay at 8 MiB.

## Input contract

```json
{"version":1,"candidates":3,"ballots":[{"order":[0,1,2],"weight":3},{"order":[1,2,0],"weight":2},{"order":[2,0,1],"weight":2}],"start":[1,2,0]}
```

One to six candidates, IDs `0..n-1`. Every ballot and `start` is a complete strict permutation; the first ID is ranked best. One to sixteen ballot rows; each weight is a positive integer at most 1,000; total weight at most 10,000. Weights are supplied multiplicities, not inferred reliability. Duplicate ballot rows are allowed and add their weights. No tied, missing or partial input rankings. JSON decimals, exponents, booleans in integer fields, duplicate keys, unknown fields and non-finite constants are rejected. `start` affects only the local trace, never the global family.

Ties between aggregate costs are different from ties inside input ballots: all optimal total orders are retained and sorted by ID for reproducible evidence, not selected as a hidden preference rule. The all-tie six-candidate control retains all **720** orders. A one-candidate profile has no adjacent swaps; both local predicates hold vacuously.

## Implementation and checks

- `orderlab/engine.py`: prepend-first exact subset DP, complete full-order census and strict descent.
- `docs/order-engine.js`: independently structured append-last DP and direct ballot-inversion full-order scoring, with exact report parity.
- `orderlab/certificate.py`: no solver import. Enumerates every restricted permutation and evaluates ballot inversions directly. Checks values, choices, counts, transitions, completeness of all optimal orders, every adjacent delta, cycles and the entire trace. It shares only the input validator.
- `tools/check_milp.py`: optional independent binary linear-ordering formulation solved by SciPy/HiGHS. Built directly from ballots, with all triangle constraints. Checks one optimum cost per non-singleton profile and independently decodes and scores the returned order. This floating-point reference is not the exact certificate and does not prove the full tied family.
- `tools/browser_expected.py`: direct ballot oracle for every selected-order ledger and subset transition shown in Chrome. Browser exports are passed to the native checker.

The exact checks use bounded integer arithmetic and exhaustive enumeration. Python uses integers. Browser totals are bounded by `10000 * choose(6,2) = 150000`; counts are at most `6! = 720`, safely inside exact JavaScript integer range.

## Reproduce the checks

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/test_engine.cjs
python tools/check_assets.py
python tools/check_installed.py
python -m pip install -r requirements-reference.txt
python tools/check_milp.py
CHROME_BIN=/path/to/chrome node --test tests/test_browser.cjs
```

The browser test uses actual Chrome and trusted mouse events for downloads. Set `ORDERLAB_SCREEN_DIR=/tmp/orderlab-screens` to retain screenshots. Chrome startup and teardown wait for process readiness; inference assertions do not retry. See [VALIDATION.md](VALIDATION.md) for measured counts and scope.

## Limits and attribution

Kemeny aggregation is generally computationally hard; this work intentionally stops at six candidates. The complete report and independent checker enumerate factorial-size families. The subset DP alone has `2^n` states and `n * 2^(n-1)` transitions; those bounds are not claims about the end-to-end census/checker runtime. Local descent crosses only strictly improving adjacent swaps, never tied plateaus; its endpoint is not a global certificate.

The objective measures disagreement with the supplied ballots. It does not infer relevance, truth, fairness or what those ballots ought to mean; this is not a real-election study or a scalability result. [SOURCES.md](SOURCES.md) credits the classical definition, local/global distinction and exact subset recurrence; the project code, controls, interface and evidence format are original. MIT license.
