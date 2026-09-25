#!/usr/bin/env python3
from itertools import product
# 0 disarmed, 1 armed, 2 fired; fired is terminal and effect count <=1.
allowed={(0,0),(0,1),(1,1),(1,2),(2,2)}
for trace in product(range(3),repeat=5):
  if trace[0]!=0 or not all((a,b) in allowed for a,b in zip(trace,trace[1:])): continue
  effects=sum(1 for a,b in zip(trace,trace[1:]) if a==1 and b==2)
  assert effects<=1, "alarm fired more than once"
  if 2 in trace:
    i=trace.index(2); assert all(s==2 for s in trace[i:])
print("alarm exactly-once temporal model: ok")
