"""Subset dynamic programming with complete bounded order and local witnesses."""
from itertools import permutations
from .model import parse

def analyze(p):
 n,bs=parse(p);m=[[0]*n for _ in range(n)]
 for b in bs:
  for t,a in enumerate(b['order']):
   for c in b['order'][t+1:]:m[a][c]+=b['weight']
 N=1<<n;dp=[dict(mask=0,members=[],value=0,count=1,choices=[],transitions=[])];families={0:[[]]}
 for s in range(1,N):
  members=[i for i in range(n)if s>>i&1];trs=[]
  for i in members:
   rest=s^(1<<i);cost=sum(m[j][i]for j in members if j!=i);trs.append(dict(first=i,rest=rest,insertion_cost=cost,tail_value=dp[rest]['value'],candidate_value=cost+dp[rest]['value']))
  val=min(t['candidate_value']for t in trs);ch=[t['first']for t in trs if t['candidate_value']==val];families[s]=sorted([[i]+z for i in ch for z in families[s^(1<<i)]])
  dp.append(dict(mask=s,members=members,value=val,count=len(families[s]),choices=ch,transitions=trs))
 full=N-1;opt=dp[full]['value'];rows=[];lookup={}
 for perm in permutations(range(n)):
  o=list(perm);cost=sum(m[o[j]][o[i]]for i in range(n)for j in range(i+1,n));deltas=[m[o[i]][o[i+1]]-m[o[i+1]][o[i]]for i in range(n-1)];row=dict(order=o,cost=cost,gap=cost-opt,adjacent_deltas=deltas,local=all(x>=0 for x in deltas),strict_local=all(x>0 for x in deltas),optimal=cost==opt);rows.append(row);lookup[perm]=row
 current=p['start'][:];trace=[]
 while True:
  r=lookup[tuple(current)];moves=[dict(at=i,delta=d)for i,d in enumerate(r['adjacent_deltas'])if d<0];take=min(moves,key=lambda z:(z['delta'],z['at']))if moves else None
  trace.append(dict(order=current[:],cost=r['cost'],adjacent_deltas=r['adjacent_deltas'],chosen=None if take is None else take['at']))
  if take is None:break
  i=take['at'];current[i],current[i+1]=current[i+1],current[i]
 pairs=[dict(a=i,b=j,a_before_b=m[i][j],b_before_a=m[j][i],margin=m[i][j]-m[j][i],unavoidable=min(m[i][j],m[j][i]))for i in range(n)for j in range(i+1,n)]
 # Every strict simple majority cycle, canonicalized by smallest first vertex.
 cycles=[]
 for size in range(3,n+1):
  for c in permutations(range(n),size):
   if c[0]==min(c)and all(m[c[t]][c[(t+1)%size]]>m[c[(t+1)%size]][c[t]]for t in range(size)):cycles.append(list(c))
 cycles.sort(key=lambda c:(len(c),c));lb=sum(z['unavoidable']for z in pairs)
 return dict(version=1,kind='orderlab-kemeny',input=p,total_weight=sum(b['weight']for b in bs),pairwise=m,pairs=pairs,pairwise_lower_bound=lb,optimal_cost=opt,cycle_tax=opt-lb,optimal_orders=families[full],possible_first=sorted({o[0]for o in families[full]}),condorcet_winners=[i for i in range(n)if all(i==j or m[i][j]>m[j][i]for j in range(n))],majority_cycles=cycles,dp=dp,orders=rows,descent=trace)
