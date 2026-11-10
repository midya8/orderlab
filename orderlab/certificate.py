"""Independent exhaustive replay from ballot inversion distances. No DP solver import."""
from itertools import permutations,combinations
from .model import parse,keys

def verify(r):
 try:
  keys(r,['version','kind','input','total_weight','pairwise','pairs','pairwise_lower_bound','optimal_cost','cycle_tax','optimal_orders','possible_first','condorcet_winners','majority_cycles','dp','orders','descent'])
  if type(r['version'])is not int or r['version']!=1 or r['kind']!='orderlab-kemeny':raise ValueError('report type')
  n,bs=parse(r['input']);ranks=[{c:i for i,c in enumerate(b['order'])}for b in bs]
  def score(o):return sum(b['weight']*sum(pos[o[i]]>pos[o[j]]for i in range(len(o))for j in range(i+1,len(o)))for b,pos in zip(bs,ranks))
  matrix=[[sum(b['weight']for b,pos in zip(bs,ranks)if i!=j and pos[i]<pos[j])for j in range(n)]for i in range(n)]
  def equal(a,b):
   # Exact types as well as values: booleans cannot impersonate integer evidence.
   if type(a)is not type(b):raise ValueError('evidence type')
   if type(b)is dict:
    keys(a,b)
    for k in b:equal(a[k],b[k])
   elif type(b)is list:
    if len(a)!=len(b):raise ValueError('evidence length')
    for x,y in zip(a,b):equal(x,y)
   elif a!=b:raise ValueError('evidence mismatch')
  equal(r['total_weight'],sum(b['weight']for b in bs));equal(r['pairwise'],matrix)
  ps=[]
  for a,b in combinations(range(n),2):ps.append(dict(a=a,b=b,a_before_b=matrix[a][b],b_before_a=matrix[b][a],margin=matrix[a][b]-matrix[b][a],unavoidable=min(matrix[a][b],matrix[b][a])))
  equal(r['pairs'],ps);lower=sum(x['unavoidable']for x in ps);equal(r['pairwise_lower_bound'],lower)
  allorders=[list(o)for o in permutations(range(n))];scores={tuple(o):score(o)for o in allorders};best=min(scores.values());opts=[o for o in allorders if scores[tuple(o)]==best];equal(r['optimal_cost'],best);equal(r['cycle_tax'],best-lower);equal(r['optimal_orders'],opts);equal(r['possible_first'],sorted({o[0]for o in opts}));equal(r['condorcet_winners'],[i for i in range(n)if all(i==j or matrix[i][j]>matrix[j][i]for j in range(n))])
  # Exhaustively score every restricted permutation, not a recursive optimization.
  states=[]
  for mask in range(1<<n):
   members=[i for i in range(n)if mask>>i&1];perms=[list(x)for x in permutations(members)];sc=[score(x)for x in perms];v=min(sc);choices=sorted({o[0]for o,c in zip(perms,sc)if o and c==v});trs=[]
   for i in members:
    tail=[j for j in members if j!=i];tailbest=min(score(z)for z in permutations(tail));insert=score([i]+tail)-score(tail);trs.append(dict(first=i,rest=mask^(1<<i),insertion_cost=insert,tail_value=tailbest,candidate_value=insert+tailbest))
   states.append(dict(mask=mask,members=members,value=v,count=sum(c==v for c in sc),choices=choices,transitions=trs))
  equal(r['dp'],states);rows=[]
  for o in allorders:
   v=scores[tuple(o)];d=[]
   for i in range(n-1):
    z=o[:];z[i],z[i+1]=z[i+1],z[i];d.append(scores[tuple(z)]-v)
   rows.append(dict(order=o,cost=v,gap=v-best,adjacent_deltas=d,local=all(x>=0 for x in d),strict_local=all(x>0 for x in d),optimal=v==best))
  equal(r['orders'],rows);trace=[];o=r['input']['start'][:]
  while True:
   v=scores[tuple(o)];ds=[]
   for i in range(n-1):
    z=o[:];z[i],z[i+1]=z[i+1],z[i];ds.append(scores[tuple(z)]-v)
   moves=[i for i,x in enumerate(ds)if x<0];take=min(moves,key=lambda i:(ds[i],i))if moves else None;trace.append(dict(order=o[:],cost=v,adjacent_deltas=ds,chosen=take))
   if take is None:break
   o[take],o[take+1]=o[take+1],o[take]
  equal(r['descent'],trace);cycles=[]
  for k in range(3,n+1):
   for subset in combinations(range(n),k):
    a=subset[0]
    for tail in permutations(subset[1:]):
     c=(a,)+tail
     if all(matrix[c[i]][c[(i+1)%k]]>matrix[c[(i+1)%k]][c[i]]for i in range(k)):cycles.append(list(c))
  equal(r['majority_cycles'],sorted(cycles,key=lambda c:(len(c),c)))
  return True
 except(KeyError,TypeError,IndexError,OverflowError)as e:raise ValueError('malformed report')from e
