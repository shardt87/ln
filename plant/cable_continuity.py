"""Cable continuity check: every cable rod end must touch another part (or grade). Prints the loose ends by item."""
import json,sys
from collections import Counter,defaultdict
G=json.load(open('/home/user/ln/plant/sw3x1_model.json'));I={i['id']:i for i in G['items']}
def bb(p):
    if p['kind'] in('box','prism'):return p['min']+p['max']
    if p['kind']=='rod':
        a,b,r=p['a'],p['b'],max(p['r'],p.get('r2',p['r']));return [min(a[0],b[0])-r,min(a[1],b[1])-r,min(a[2],b[2])-r,max(a[0],b[0])+r,max(a[1],b[1])+r,max(a[2],b[2])+r]
    xs,ys,zs=zip(*p['v']);return [min(xs),min(ys),min(zs),max(xs),max(ys),max(zs)]
P=G['parts'];B=[bb(p) for p in P];grid=defaultdict(list)
for k,b in enumerate(B):
    if b[3]-b[0]>400 or b[4]-b[1]>400: continue
    for gx in range(int(b[0]//10),int(b[3]//10)+1):
        for gy in range(int(b[1]//10),int(b[4]//10)+1): grid[(gx,gy)].append(k)
def touch(pt,me,m=.3):
    x,y,z=pt
    if z<=.15: return True                     # on grade / into the ground
    for k in grid.get((int(x//10),int(y//10)),()):
        if k==me: continue
        b=B[k]
        if b[0]-m<=x<=b[3]+m and b[1]-m<=y<=b[4]+m and b[2]-m<=z<=b[5]+m: return True
    return False
bad=defaultdict(list)
for k,p in enumerate(P):
    if p['kind']!='rod' or not str(p['color']).startswith('cable'): continue
    for e in (p['a'],p['b']):
        if not touch(e,k): bad[I[p['item']]['name']].append([round(v,1) for v in e])
tot=sum(len(v) for v in bad.values())
print('loose cable ends:',tot,'in',len(bad),'items')
for n,v in sorted(bad.items(),key=lambda t:-len(t[1]))[:40]: print(len(v),n[:80],v[:3])
