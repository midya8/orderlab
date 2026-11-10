"""Visible evidence oracle: direct input-ballot inversion arithmetic."""
import json,sys
from pathlib import Path
from itertools import combinations
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from orderlab import analyze
from orderlab.controls import controls

def text(o):return ' > '.join(map(str,o))
def yes(x):return'yes'if x else'no'
out=[]
for c in controls():
 p=c['input'];r=analyze(p);n=p['candidates'];ranks=[{v:i for i,v in enumerate(b['order'])}for b in p['ballots']]
 def score(o):return sum(b['weight']*sum(pos[o[i]]>pos[o[j]]for i in range(len(o))for j in range(i+1,len(o)))for b,pos in zip(p['ballots'],ranks))
 def support(a,b):return sum(z['weight']for z,pos in zip(p['ballots'],ranks)if pos[a]<pos[b])
 audits=[]
 for z in r['orders']:
  o=z['order'];pos={v:i for i,v in enumerate(o)};ballots=[];pairs=[];swaps=[]
  for i,(b,br)in enumerate(zip(p['ballots'],ranks)):
   d=sum(br[o[a]]>br[o[b]]for a in range(n)for b in range(a+1,n));ballots.append([str(i),text(b['order']),str(b['weight']),str(d),str(d*b['weight'])])
  for a,b in combinations(range(n),2):
   x,y=(a,b)if pos[a]<pos[b]else(b,a);cost=support(y,x);lb=min(support(a,b),support(b,a));pairs.append([f'{a}, {b}',f'{x} > {y}',str(cost),str(lb),str(cost-lb)])
  for i in range(n-1):
   t=o[:];t[i],t[i+1]=t[i+1],t[i];v=score(t);d=v-score(o);swaps.append([str(i),f'{o[i]}, {o[i+1]}',text(t),str(v),str(d),'improves'if d<0 else'ties'if d==0 else'worsens'])
  audits.append(dict(ballots=ballots,pairs=pairs,swaps=swaps))
 states=[]
 for s in r['dp']:
  rows=[]
  for t in s['transitions']:
   i=t['first'];members=[x for x in s['members']if x!=i];insert=sum(support(j,i)for j in members);rows.append([str(i),str(t['rest']),str(insert),str(t['tail_value']),str(insert+t['tail_value']),yes(insert+t['tail_value']==s['value'])])
  states.append(rows)
 edges=[]
 for a,b in combinations(range(n),2):
  ab,ba=support(a,b),support(b,a);x,y=(a,b)if ab>=ba else(b,a);edges.append(dict(a=x,b=y,tie=ab==ba))
 out.append(dict(report=json.dumps(r,sort_keys=True,separators=(',',':')),audits=audits,states=states,edges=edges,matrix=[[str(i),*[str(x)for x in row]]for i,row in enumerate(r['pairwise'])],pairs=[[str(z[k])for k in ['a','b','a_before_b','b_before_a','margin','unavoidable']]for z in r['pairs']],cycles=[[text(z+[z[0]]),', '.join(str(support(z[i],z[(i+1)%len(z)])-support(z[(i+1)%len(z)],z[i]))for i in range(len(z)))]for z in r['majority_cycles']],optima=[[text(o)]for o in r['optimal_orders']],descent=[[str(i),text(z['order']),str(z['cost']),', '.join(map(str,z['adjacent_deltas'])),'stop'if z['chosen']is None else str(z['chosen'])]for i,z in enumerate(r['descent'])],orders=[[text(z['order']),str(z['cost']),str(z['gap']),', '.join(map(str,z['adjacent_deltas'])),yes(z['local']),yes(z['strict_local']),yes(z['optimal'])]for z in r['orders']],dp=[[str(z['mask']),', '.join(map(str,z['members'])),str(z['value']),str(z['count']),', '.join(map(str,z['choices']))]for z in r['dp']]))
print(json.dumps(out,separators=(',',':')))
