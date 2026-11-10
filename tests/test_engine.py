import copy,json,subprocess,sys,unittest
from itertools import permutations
from pathlib import Path
from orderlab import analyze,verify
from orderlab.controls import controls
from orderlab.model import parse,loads
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from cases import cases

class Tests(unittest.TestCase):
 def test_developed_cases(self):
  rs=[analyze(p)for p in cases()]
  for r in rs:
   self.assertTrue(verify(r));self.assertGreaterEqual(r['cycle_tax'],0)
   self.assertEqual(r['dp'][-1]['count'],len(r['optimal_orders']))
   for o in r['optimal_orders']:
    for i in range(len(o)-1):self.assertGreaterEqual(r['pairwise'][o[i]][o[i+1]]-r['pairwise'][o[i+1]][o[i]],0)
   if r['condorcet_winners']:self.assertEqual(r['possible_first'],r['condorcet_winners'])
  print('REPORTS',len(rs),'ORDERS',sum(len(r['orders'])for r in rs),'STATES',sum(len(r['dp'])for r in rs),'TRANSITIONS',sum(len(s['transitions'])for r in rs for s in r['dp']),'CYCLES',sum(len(r['majority_cycles'])for r in rs))
 def test_counterexample(self):
  r=analyze(controls()[0]['input']);self.assertEqual((r['pairwise_lower_bound'],r['optimal_cost'],r['cycle_tax']),(7,8,1));self.assertEqual(r['optimal_orders'],[[0,1,2]]);self.assertEqual(r['descent'],[dict(order=[1,2,0],cost=10,adjacent_deltas=[3,1],chosen=None)]);self.assertEqual(r['majority_cycles'],[[0,1,2]])
 def test_all_ties_retained(self):
  r=analyze(controls()[9]['input']);self.assertEqual(len(r['optimal_orders']),720);self.assertEqual(len(r['orders']),720);self.assertTrue(all(x['local']for x in r['orders']));self.assertFalse(any(x['strict_local']for x in r['orders']))
 def test_singleton_vacuous_strict_local(self):
  r=analyze(controls()[4]['input']);self.assertEqual(r['optimal_cost'],0);self.assertTrue(r['orders'][0]['strict_local']);self.assertEqual(r['condorcet_winners'],[0])
 def test_scaling(self):
  p=controls()[0]['input'];r=analyze(p);p=copy.deepcopy(p)
  for b in p['ballots']:b['weight']*=2
  z=analyze(p);self.assertEqual(z['optimal_orders'],r['optimal_orders']);self.assertEqual(z['optimal_cost'],2*r['optimal_cost']);self.assertEqual(z['cycle_tax'],2*r['cycle_tax'])
 def test_duplicate_split(self):self.assertEqual({k:v for k,v in analyze(controls()[0]['input']).items()if k!='input'},{k:v for k,v in analyze(controls()[8]['input']).items()if k!='input'})
 def test_ballot_order_invariance(self):
  p=copy.deepcopy(controls()[10]['input']);r=analyze(p);p['ballots'].reverse();z=analyze(p);self.assertEqual({k:v for k,v in r.items()if k!='input'},{k:v for k,v in z.items()if k!='input'})
 def test_candidate_relabeling(self):
  for c in controls():
   p=copy.deepcopy(c['input']);n=p['candidates'];r=analyze(p)
   for b in p['ballots']:b['order']=[n-1-i for i in b['order']]
   p['start']=[n-1-i for i in p['start']];z=analyze(p);self.assertTrue(verify(z));self.assertEqual(z['optimal_cost'],r['optimal_cost']);self.assertEqual(sorted([[n-1-i for i in o]for o in r['optimal_orders']]),z['optimal_orders'])
 def test_reversal(self):
  for c in controls():
   p=copy.deepcopy(c['input']);r=analyze(p)
   for b in p['ballots']:b['order'].reverse()
   p['start'].reverse();z=analyze(p);self.assertTrue(verify(z));self.assertEqual(r['optimal_cost'],z['optimal_cost']);self.assertEqual(sorted([o[::-1]for o in r['optimal_orders']]),z['optimal_orders'])
 def test_descent_strictly_decreases(self):
  r=analyze(controls()[13]['input']);self.assertGreater(len(r['descent']),1)
  for a,b in zip(r['descent'],r['descent'][1:]):self.assertLess(b['cost'],a['cost']);self.assertEqual(b['cost']-a['cost'],a['adjacent_deltas'][a['chosen']])
 def test_checker_import_independence(self):subprocess.run([sys.executable,'-c','from orderlab import verify;import sys;assert "orderlab.engine" not in sys.modules'],check=True)
 def test_primitive_forgery_rejection(self):
  count=0
  for c in controls()[:3]:
   r=analyze(c['input']);paths=[]
   def walk(x,path):
    if type(x)is dict:
     for k,v in x.items():
      if path or k!='input':walk(v,path+[k])
    elif type(x)is list:
     for i,v in enumerate(x):walk(v,path+[i])
    else:paths.append(path)
   walk(r,[])
   for path in paths:
    z=copy.deepcopy(r);a=z
    for key in path[:-1]:a=a[key]
    x=a[path[-1]];a[path[-1]]=x+1 if type(x)is int else not x if type(x)is bool else 'changed'
    with self.assertRaises(ValueError,msg=str(path)):verify(z)
   count+=len(paths)
  print('PRIMITIVE_FORGERIES',count)
 def test_missing_and_extra_evidence(self):
  r=analyze(controls()[0]['input'])
  for key in r:
   z=copy.deepcopy(r);del z[key]
   with self.assertRaises(ValueError):verify(z)
  for z in [dict(r,extra=0),dict(r,optimal_cost=True),dict(r,orders=[]),dict(r,dp=[]),dict(r,pairwise=[[False]*3]*3)]:
   with self.assertRaises(ValueError):verify(z)
 def test_strict_input(self):
  p=controls()[0]['input']
  for key,v in [('version',True),('candidates',0),('candidates',7),('candidates',True),('candidates',3.0),('ballots',[]),('ballots',[dict(order=[0,0,1],weight=1)]),('ballots',[dict(order=[0,1,2],weight=0)]),('ballots',[dict(order=[0,1,2],weight=True)]),('start',[0,0,1])]:
   z=copy.deepcopy(p);z[key]=v
   with self.assertRaises(ValueError):parse(z)
  for text in ['{"x":1,"x":2}','{"x":1.0}','{"x":1e0}','{"x":NaN}']:
   with self.assertRaises(ValueError):loads(text)
 def test_input_bounds_and_unknowns(self):
  base=controls()[0]['input']
  for bs in [[dict(order=[0,1,2],weight=1001)],[dict(order=[0,1,2],weight=1000)]*11,[dict(order=[0,1,2],weight=1)]*17,[dict(order=[0,1,2],weight=1,extra=0)]]:
   p=copy.deepcopy(base);p['ballots']=bs
   with self.assertRaises(ValueError):parse(p)
  p=copy.deepcopy(base);p['extra']=0
  with self.assertRaises(ValueError):parse(p)
  p=copy.deepcopy(base);p['ballots']=[dict(order=[0,1,2],weight=1000)]*10;self.assertTrue(verify(analyze(p)))
 def test_report_boolean_integer_types(self):
  r=analyze(controls()[0]['input'])
  for path in [['pairwise',0,0],['dp',0,'count'],['orders',0,'cost'],['descent',0,'cost']]:
   z=copy.deepcopy(r);a=z
   for k in path[:-1]:a=a[k]
   a[path[-1]]=bool(a[path[-1]])
   with self.assertRaises(ValueError):verify(z)
 def test_cli_rejects_deep_and_oversized_json(self):
  import tempfile
  with tempfile.TemporaryDirectory()as d:
   f=Path(d)/'input.json'
   for text in ['['*2000+']'*2000,'x'*65537]:
    f.write_text(text);r=subprocess.run([sys.executable,'-m','orderlab','run',str(f)],capture_output=True,text=True);self.assertEqual(r.returncode,2);self.assertFalse(r.stdout);self.assertNotIn('Traceback',r.stderr)
 def test_cli(self):
  r=subprocess.run([sys.executable,'-m','orderlab','demo'],capture_output=True,text=True,check=True);self.assertTrue(verify(json.loads(r.stdout)))
  r=subprocess.run([sys.executable,'-m','orderlab','run'],capture_output=True,text=True);self.assertEqual(r.returncode,2);self.assertFalse(r.stdout)
if __name__=='__main__':unittest.main()
