import random
from orderlab.controls import controls,model

def cases():
 out=[c['input']for c in controls()];rng=random.Random(719031)
 for n in range(1,7):
  for _ in range(10):
   rows=[]
   for __ in range(rng.randint(1,6)):
    o=list(range(n));rng.shuffle(o);rows.append((o,rng.randint(1,9)))
   start=list(range(n));rng.shuffle(start);out.append(model(n,rows,start))
 return out
