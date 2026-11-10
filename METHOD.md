# Method and exactness

## Objective

For candidates `a != b`, let `M[a,b]` be the total supplied weight of ballots ranking `a` before `b`. The diagonal is zero and `M[a,b] + M[b,a]` equals total weight.

For a strict total order `o`, the weighted Kendall inversion cost is

```
C(o) = sum over i < j of M[o[j],o[i]].
```

This equals the sum of each ballot's multiplicity times its number of pairwise inversions against `o`. Minimize `C` over every permutation. This is classical Kemeny rank aggregation, not Borda scoring or a learned ranker. Integer multiplicities are equivalent to repeated ballots.

## Independent pairs are a lower bound, not an order

```
L = sum over a < b of min(M[a,b], M[b,a])
C* = min over total orders o of C(o)
cycle_tax = C* - L >= 0
```

Every order pays at least each pair's minimum. The minimizing directions can conflict with transitivity. `cycle_tax` is only a field name for extra weighted disagreement imposed by a single total order. It is not a number of majority cycles, a causal attribution to individual cycles, or a claim that arbitrary cycle counts determine the gap. All strict simple majority cycles are listed, with the smallest ID first to remove rotation duplicates. A reverse cycle is a distinct orientation. Pairwise ties do not create strict edges.

A strict Condorcet winner beats every other candidate by strict pairwise weight. With one candidate the universal condition is vacuous. `possible_first` reports every candidate appearing first in at least one exact optimum, not a selected social winner.

## Exact subset recurrence

Let `F(S)` be the minimum inversion cost on ballots restricted to subset `S`.

```
F({}) = 0
F(S) = min over i in S [F(S without i) + sum over j in S without i M[j,i]]
```

For any order of `S` beginning with `i`, its cost splits into the cost of the tail and disagreements placing `i` before every tail member. The latter term does not depend on tail order. An optimal order with first candidate `i` must therefore have an optimal tail; replacing a worse tail improves the complete order. Taking the minimum over every possible first candidate is exhaustive. This classical recurrence is explicitly credited to Betzler et al., Theorem 4, in [SOURCES.md](SOURCES.md).

Python retains every minimizing first choice and prepends it to every optimal tail. These disjoint first-candidate families give every optimum exactly once; empty subset has one empty ordering. There are `2^n` subset states and `n * 2^(n-1)` transitions. With a precomputed pair matrix, computing all insertion sums naively uses `O(n^2 * 2^n)` arithmetic operations. Materializing full tied families, every full order, cycles and replay adds separate factorial/output-size work. This is not an end-to-end subset-only complexity claim.

JavaScript computes optimum values by the equivalent append-last recurrence: placing `i` last adds `sum M[i,j]` over remaining members. It then constructs the same canonical prepend-first evidence. Full-order costs are computed directly from ballots rather than the Python pair-matrix scoring path.

## Local search is explicitly weaker

For adjacent `a,b` in an order, swapping them changes no other pair orientation. The exact neighbor-cost delta is `M[a,b] - M[b,a]`. A local order has every delta nonnegative. A strict local order has every delta positive. Singleton orders satisfy both predicates vacuously.

The trace takes the most negative delta, chooses the leftmost position among equal improvements, and stops if no delta is negative. Cost strictly decreases, so revisiting an order is impossible and the finite trace terminates. Zero-cost plateau moves are not taken. `start` affects this trace alone. No claim is made that this policy matches every local-Kemenization algorithm in the literature or finds a global optimum.

For the default profile: `M[0,1]=5`, `M[1,2]=5`, `M[2,0]=4`, total weight 7. Independent pair costs are 2, 2 and 3, giving `L=7`. Exact `0>1>2` costs 8. Start `1>2>0` costs 10 and both adjacent swaps worsen it, by 3 and 1. Local/global gap is 2; `cycle_tax` is 1. These are arithmetic on the supplied developed profile, not experimental generalization.

## Replay trust boundary

The checker imports the input validator but neither the DP solver nor report construction. It computes ballot positions and scores every permutation of every subset directly. From those exhaustive scores it checks every claimed subset value, first choice and optimum count. It separately verifies the complete optimum family, full order census, swapped-neighbor costs, trace policy, pair counts and simple cycles. Exact recursive type matching rejects booleans impersonating integer evidence, missing or added fields, omissions, changed ordering and any changed derived primitive exercised by the mutation suite.

This is an executable certificate for a bounded finite profile, not a proof assistant or cryptographic attestation. A self-consistent report for a changed input is a report for that changed input; replay does not authenticate the user's intended ballots. Resource caps and strict schema validation limit work but do not make arbitrary untrusted files safe in every environment.

## Independent mixed-integer reference

For `a<b`, binary `x_ab=1` means `a` precedes `b`. Minimize

```
sum over a<b [M[a,b] + (M[b,a]-M[a,b]) * x_ab]
```

For every `a<b<c`, impose `0 <= x_ab + x_bc - x_ac <= 1`. These bounds eliminate both orientations of a directed triangle. A tournament without directed triangles is transitive: any shortest directed cycle of length at least four has a chord yielding a shorter directed cycle. Thus feasible binary solutions encode total orders. The script builds all coefficients directly from ballots, asks SciPy/HiGHS for integrality with bounds 0..1 and zero relative MIP gap, checks optimum cost within `1e-8`, checks integrality within `1e-8`, decodes an order by predecessor counts and directly rescores it. It is an independent numerical reference for one optimal cost, not the exact all-family replay.

## Scope

At most six candidates, sixteen complete strict ballot rows, positive integer weights at most 1,000 and total weight at most 10,000. Full cost is at most 150,000; all numerical browser arithmetic is exact within safe integer range. No incomplete ballots, input ties, fractional weights, candidate names, learned preferences, fairness, strategy resistance, privacy guarantee, real political application or practical scalability is inferred. Labels only sort deterministic evidence. Developed examples and seeded profiles test implementation properties; they are not an independent benchmark or held-out evaluation.
