"""Bounded strict-ranking input. No solver or report construction."""
import json

def integer(x):
 if type(x)is not int:raise ValueError('expected non-boolean integer')
 return x

def keys(x,ks):
 if type(x)is not dict or set(x)!=set(ks):raise ValueError('unexpected fields')

def order(x,n):
 if type(x)is not list or len(x)!=n or any(type(v)is not int for v in x)or sorted(x)!=list(range(n)):raise ValueError('order must be a complete strict permutation')
 return x

def parse(p):
 keys(p,['version','candidates','ballots','start'])
 if integer(p['version'])!=1:raise ValueError('version must be 1')
 n=integer(p['candidates'])
 if not 1<=n<=6:raise ValueError('candidate count must be 1..6')
 bs=p['ballots']
 if type(bs)is not list or not 1<=len(bs)<=16:raise ValueError('1..16 weighted ballot rows required')
 total=0
 for b in bs:
  keys(b,['order','weight']);order(b['order'],n);w=integer(b['weight'])
  if not 1<=w<=1000:raise ValueError('ballot weights must be 1..1000')
  total+=w
 if total>10000:raise ValueError('total ballot weight limit 10000')
 order(p['start'],n)
 return n,bs

def loads(text):
 def pairs(ps):
  out={}
  for k,v in ps:
   if k in out:raise ValueError('duplicate key')
   out[k]=v
  return out
 def no(_):raise ValueError('JSON decimals/constants forbidden')
 return json.loads(text,object_pairs_hook=pairs,parse_float=no,parse_constant=no)
