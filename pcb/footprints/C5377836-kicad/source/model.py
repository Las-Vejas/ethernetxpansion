"""Simplified datasheet-based HC621601A-M911-A vertical RJ45 model.
Run with Python 3 and cadquery >=2.7. Units: mm.
PCB component surface z=0; connector mating face +Z; mounting pegs at y=0.
See README for measured and approximated geometry.
"""
from pathlib import Path
import cadquery as cq
OUT=Path(__file__).resolve().parent
W,H,D=16.10,16.90,16.95
YC=-1.75 # rear/PCB outline extends y=-10.20 .. +6.70
parts=[]
def box(w,h,d,x=0,y=0,z=0):
 return cq.Workplane('XY').box(w,h,d,centered=(True,True,False)).translate((x,y,z))
def add(name,s,color):
 assert s.val().isValid(),name
 parts.append((name,s,color))
# Shell wall thickness 0.20 per material note. Simplify folds/seams.
outer=box(W,H,D,y=YC)
inner=box(W-.4,H-.4,D-.2,y=YC)
shell=outer.cut(inner)
# Main mating opening, latch recess. Opening details estimated from drawing/photo.
aperture=box(12.0,7.2,10.0,y=.15,z=D-9.8).union(box(4.5,2.0,10.0,y=4.5,z=D-9.8))
ledholes=box(3.0,1.9,1,x=-5.15,y=5.0,z=D-.4).union(box(3.0,1.9,1,x=5.15,y=5.0,z=D-.4))
shell=shell.cut(aperture).cut(ledholes)
add('nickel_shield',shell,(.67,.70,.74))
core=box(W-.44,H-.44,D-.3,y=YC,z=.02).cut(aperture).cut(ledholes)
add('LCP_housing',core,(.08,.085,.09))
add('yellow_LED',box(2.65,1.5,.6,x=-5.15,y=5.0,z=D-.75),(.95,.82,.04))
add('green_LED',box(2.65,1.5,.6,x=5.15,y=5.0,z=D-.75),(.04,.75,.12))
# Exposed contacts, visual approximations, not an electrical/contact design.
for i in range(8):
 add(f'contact_{i+1}',box(.35,.65,3.7,x=(i-3.5)*1.02,y=-3.1,z=D-7.5),(.84,.65,.21))
# Pin center locations reconstructed from component-side PCB drawing.
# 10 signal pins: 2.54 pitch each row; 1.27 stagger; row pitch 2.54.
for i in range(5):
 for n,x,y in [(2+2*i,4.445-i*2.54,-6.35),(1+2*i,5.715-i*2.54,-8.89)]:
  add(f'pin_{n}',box(.45,.35,3.2,x=x,y=y,z=-3.2),(.70,.72,.75))
for n,x in [(14,-6.325),(13,-3.785),(12,3.785),(11,6.325)]:
 add(f'LED_pin_{n}',box(.45,.35,3.3,x=x,y=4.11,z=-3.3),(.70,.72,.75))
for side in [-1,1]:
 # 3.20 hole, reduced nominal post diameter; snap detail simplified.
 peg=cq.Workplane('XY').circle(1.5).extrude(3.3).translate((side*5.715,0,-3.3))
 add(f'locating_post_{side}',peg,(.08,.085,.09))
 add(f'shield_tab_{side}',box(.35,1.2,3.35,x=side*7.95,y=-3.89,z=-3.35),(.67,.70,.74))
assembly=cq.Assembly(name='HC621601A_M911_A_C5377836')
for name,s,color in parts: assembly.add(s,name=name,color=cq.Color(*color))
assembly.export(str(OUT/'HC621601A-M911-A.step'))
compound=cq.Compound.makeCompound([s.val() for _,s,_ in parts])
cq.exporters.export(compound,str(OUT/'HC621601A-M911-A.stl'),tolerance=.035,angularTolerance=.08)
# Reimport the exported STEP and validate actual exported shape.
r=cq.importers.importStep(str(OUT/'HC621601A-M911-A.step')).val()
assert r.isValid()
b=r.BoundingBox()
print('STEP readback valid; solids:',len(r.Solids()),'bounds:',b.xlen,b.ylen,b.zlen)
