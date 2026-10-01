"""Generates HCTL.kicad_sym and HCTL.pretty footprint for HC621601A-M911-A (LCSC C5377836).
Datasheet coords (component side, origin = midpoint of locating posts, +y toward LED row).
KiCad y = -datasheet y."""
import uuid
from pathlib import Path
OUT=Path(__file__).resolve().parent.parent
u=lambda:str(uuid.uuid4())
NAME='HC621601A-M911-A'
FP='RJ45_HCTL_HC621601A-M911-A_Vertical_TH'
# ---- pads (datasheet y up) ----
pads=[]
for i in range(5):
    pads.append((2+2*i, 4.445-i*2.54, -6.35))
    pads.append((1+2*i, 5.715-i*2.54, -8.89))
leds={14:(-6.325,4.11),13:(-3.785,4.11),12:(3.785,4.11),11:(6.325,4.11)}
for n,(x,y) in leds.items(): pads.append((n,x,y))
pads.sort()
def f(v): return ('%.4f'%v).rstrip('0').rstrip('.')
L=[]
a=L.append
a(f'(footprint "{FP}"')
a(' (version 20241229)\n (generator "pcbnew")\n (generator_version "9.0")\n (layer "F.Cu")')
a(' (descr "HCTL HC621601A-M911-A, LCSC C5377836, vertical (top-entry) shielded RJ45 jack with 1x1 magnetics and 2 LEDs, through hole. Pad pattern from manufacturer drawing page 1.")')
a(' (tags "RJ45 HCTL HC621601A-M911-A C5377836 magjack")')
def prop(n,v,x,y,layer,hide=False):
    a(f' (property "{n}" "{v}" (at {f(x)} {f(y)} 0) (layer "{layer}") {"(hide yes) " if hide else ""}(uuid "{u()}") (effects (font (size 1 1) (thickness 0.15))))')
prop('Reference','REF**',0,-8.2,'F.SilkS')
prop('Value',NAME,0,12.2,'F.Fab')
prop('Datasheet','https://datasheet.lcsc.com/datasheet/pdf/a6450734ef0cdf4aa798ffe8304b55e8.pdf?productCode=C5377836',0,0,'F.Fab',True)
prop('Description','Vertical shielded RJ45 jack with magnetics and LEDs',0,0,'F.Fab',True)
a(' (attr through_hole)')
def line(x1,y1,x2,y2,layer,w):
    a(f' (fp_line (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) (stroke (width {w}) (type solid)) (layer "{layer}") (uuid "{u()}"))')
def rect(x1,y1,x2,y2,layer,w):
    a(f' (fp_rect (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) (stroke (width {w}) (type solid)) (fill no) (layer "{layer}") (uuid "{u()}"))')
# body outline on Fab: x +-8.05, datasheet y -10.2..+6.7 -> kicad y -6.7..10.2
rect(-8.05,-6.7,8.05,10.2,'F.Fab',0.1)
# courtyard
rect(-9.55,-7.1,9.55,11.1,'F.CrtYd',0.05)
# silk: top and bottom edges, side segments clear of shield pads (y 2.6..5.2)
line(-8.15,-6.8,8.15,-6.8,'F.SilkS',0.12)
line(-8.15,10.3,8.15,10.3,'F.SilkS',0.12)
for s in (-1,1):
    line(s*8.15,-6.8,s*8.15,2.2,'F.SilkS',0.12)
    line(s*8.15,5.6,s*8.15,10.3,'F.SilkS',0.12)
# pin 1 marker: small triangle below pin 1 row
x1=5.715
for p,q in [((x1,10.75),(x1-0.5,11.4)),((x1-0.5,11.4),(x1+0.5,11.4)),((x1+0.5,11.4),(x1,10.75))]:
    pass
# keep marker inside courtyard: arrow just under the bottom silk line
line(x1,10.5,x1-0.45,10.95,'F.SilkS',0.12); line(x1,10.5,x1+0.45,10.95,'F.SilkS',0.12)
a(f' (fp_text user "${{REFERENCE}}" (at 0 2) (layer "F.Fab") (uuid "{u()}") (effects (font (size 1 1) (thickness 0.15))))')
# pads
for n,x,y in pads:
    shape='rect' if n==1 else 'circle'
    sz,dr=(1.6,0.9) if n<=10 else (1.7,1.02)
    a(f' (pad "{n}" thru_hole {shape} (at {f(x)} {f(-y)}) (size {sz} {sz}) (drill {dr}) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (uuid "{u()}"))')
for s in (-1,1):
    a(f' (pad "SH" thru_hole circle (at {f(s*7.95)} {f(3.89)}) (size 2.6 2.6) (drill 1.63) (layers "*.Cu" "*.Mask") (remove_unused_layers no) (uuid "{u()}"))')
for s in (-1,1):
    a(f' (pad "" np_thru_hole circle (at {f(s*5.715)} 0) (size 3.2 3.2) (drill 3.2) (layers "*.Cu" "*.Mask") (uuid "{u()}"))')
a(f' (model "${{KIPRJMOD}}/3dshapes/{NAME}.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
a(' (embedded_fonts no)\n)')
(OUT/'HCTL.pretty'/f'{FP}.kicad_mod').write_text('\n'.join(L)+'\n')

# ---- symbol ----
names={1:'VCC_CT',2:'TD1+',3:'TD1-',4:'TD2+',5:'TD2-',6:'TD3+',7:'TD3-',8:'TD4+',9:'TD4-',10:'GND_BS'}
S=[]
b=S.append
b('(kicad_symbol_lib\n (version 20241209)\n (generator "kicad_symbol_editor")\n (generator_version "9.0")')
b(f' (symbol "{NAME}"\n  (exclude_from_sim no)\n  (in_bom yes)\n  (on_board yes)')
def sp(n,v,x,y,hide=True):
    b(f'  (property "{n}" "{v}" (at {x} {y} 0) (effects (font (size 1.27 1.27)){" (hide yes)" if hide else ""}))')
sp('Reference','J',-10.16,17.78,False)
sp('Value',NAME,10.16,17.78,False)
sp('Footprint',f'HCTL:{FP}',0,0)
sp('Datasheet','https://datasheet.lcsc.com/datasheet/pdf/a6450734ef0cdf4aa798ffe8304b55e8.pdf?productCode=C5377836',0,0)
sp('Description','Vertical shielded RJ45 jack, 10/100/1000BASE, 1x1 magnetics, green+yellow LEDs, through hole (HCTL)',0,0)
sp('LCSC','C5377836',0,0)
sp('ki_keywords','RJ45 magjack HCTL',0,0)
b(f'  (symbol "{NAME}_0_1"')
b('   (rectangle (start -10.16 15.24) (end 10.16 -12.7) (stroke (width 0.254) (type default)) (fill (type background)))')
b('  )')
b(f'  (symbol "{NAME}_1_1"')
def pin(num,name,x,y,ang):
    b(f'   (pin passive line (at {x} {y} {ang}) (length 2.54) (name "{name}" (effects (font (size 1.27 1.27)))) (number "{num}" (effects (font (size 1.27 1.27)))))')
for k,n in enumerate(range(1,11)):
    pin(n,names[n],-12.7,round(12.7-2.54*k,2),0)
for k,(n,nm) in enumerate([(13,'LED_Y_A'),(14,'LED_Y_K'),(11,'LED_G_A'),(12,'LED_G_K')]):
    pin(n,nm,12.7,round(7.62-2.54*k-(2.54 if k>=2 else 0),2),180)
pin('SH','SHIELD',0,-15.24,90)
b('  )\n  (embedded_fonts no)\n )\n)')
(OUT/'HCTL.kicad_sym').write_text('\n'.join(S)+'\n')
print('ok')
