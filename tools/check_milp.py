"""Optional HiGHS integer-tournament reference built directly from ranking ballots."""
import json,sys
from pathlib import Path
from itertools import combinations
import numpy as np
import scipy
from scipy.optimize import milp,Bounds,LinearConstraint
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from orderlab import analyze
from cases import cases
solves=0;worst=0.;constraints=0
for p in cases():
 n=p['candidates'];r=analyze(p)
 if n==1:assert r['optimal_cost']==0;continue
 pairs=list(combinations(range(n),2));index={pair:i for i,pair in enumerate(pairs)};coef=[];constant=0
 for a,b in pairs:
  ab=ba=0
  for row in p['ballots']:
   if row['order'].index(a)<row['order'].index(b):ab+=row['weight']
   else:ba+=row['weight']
  constant+=ab;coef.append(ba-ab)
 aa=[];lo=[];hi=[]
 for a,b,c in combinations(range(n),3):
  # x_ab + x_bc - x_ac must be 0 or 1. This forbids both triangle orientations.
  row=[0.]*len(pairs);row[index[a,b]]=1.;row[index[b,c]]=1.;row[index[a,c]]=-1.;aa.append(row);lo.append(0.);hi.append(1.)
 z=milp(np.array(coef,dtype=float),integrality=np.ones(len(pairs)),bounds=Bounds(np.zeros(len(pairs)),np.ones(len(pairs))),constraints=LinearConstraint(np.array(aa),lo,hi)if aa else None,options={'mip_rel_gap':0.})
 assert z.success,(z.status,z.message);v=float(z.fun)+constant;error=abs(v-r['optimal_cost']);worst=max(worst,error);assert error<=1e-8,(v,r['optimal_cost']);solves+=1;constraints+=len(aa)
 # Decode integral pair orientations and independently evaluate the resulting full order.
 x=np.rint(z.x).astype(int);assert np.max(np.abs(z.x-x))<=1e-8
 rank={i:0 for i in range(n)}
 for (a,b),v in zip(pairs,x):rank[b if v else a]+=1
 o=sorted(range(n),key=lambda i:rank[i]);assert sorted(rank.values())==list(range(n));score=sum(row['weight']*sum(row['order'].index(o[i])>row['order'].index(o[j])for i in range(n)for j in range(i+1,n))for row in p['ballots']);assert score==r['optimal_cost']
print(json.dumps(dict(scipy=scipy.__version__,reports=len(cases()),integer_solves=solves,triangle_constraints=constraints,worst_abs_error=worst,tolerance=1e-8)))
