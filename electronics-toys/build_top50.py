#!/usr/bin/env python3
"""Score the 50 electronic-toy candidates. Usage: python3 -I build_top50.py <out_dir>
Ratings 1-5 (Demand, Ease of build, Compliance ease, Differentiation, India fit) are the author's judgement.
BOM (INR at ~1000 units) and prices are planning estimates, not quotes."""
import csv, sys
from pathlib import Path

# name, category, age, wireless(Y/N), BOM@1k, price incl GST, demand, ease, compliance, diff, india_fit
P = [
("Snap-together electronics lab (30 experiments)","A Learning & STEM kits","8+","N",420,1299,4,3,4,3,4),
("Soldering practice kits (LED, siren, flasher)","A Learning & STEM kits","12+","N",150,499,3,4,4,3,4),
("DIY AM/FM radio kit","A Learning & STEM kits","10+","N",180,599,3,4,3,3,4),
("Light/touch alarm science kit","A Learning & STEM kits","8+","N",160,449,3,4,4,2,3),
("Beginner microcontroller board + 20 projects","A Learning & STEM kits","10+","N",650,1799,3,3,3,3,4),
("Block-coding Bluetooth robot car kit","A Learning & STEM kits","8+","Y",1100,3299,4,2,2,3,4),
("Solar car / robot science kit","A Learning & STEM kits","8+","N",120,399,3,5,5,2,3),
("Weather station kit with LCD","A Learning & STEM kits","10+","N",480,1299,2,3,4,3,3),
("Motor & generator experiment set","A Learning & STEM kits","8+","N",220,699,3,4,4,2,4),
("Morse / buzzer circuit set","A Learning & STEM kits","8+","N",150,449,2,4,4,2,3),
("Line-follower robot kit","B Robots & motion","10+","N",700,1999,3,3,4,3,3),
("Obstacle-avoiding robot car (ultrasonic)","B Robots & motion","10+","N",800,2199,4,3,4,3,3),
("Gesture / IR remote car","B Robots & motion","8+","N",650,1799,3,3,4,3,3),
("Bristlebot vibration robot DIY","B Robots & motion","6+","N",70,299,2,5,5,2,3),
("Hydraulic + servo robot arm","B Robots & motion","10+","N",600,1799,3,3,4,3,3),
("Servo walking spider robot","B Robots & motion","10+","N",900,2499,3,2,4,3,3),
("RC sumo battle robot pair","B Robots & motion","8+","Y",1000,2999,3,2,2,3,3),
("Dancing / crawling robot toy with lights","B Robots & motion","3+","N",280,899,4,4,4,2,3),
("2.4 GHz RC rock crawler","C Remote control & vehicles","6+","Y",650,1799,5,3,3,2,3),
("360 stunt RC car","C Remote control & vehicles","6+","Y",600,1599,5,3,3,2,3),
("RC boat (water-safe)","C Remote control & vehicles","6+","Y",550,1599,3,3,3,2,3),
("Bump-and-go emergency vehicles with light & sound","C Remote control & vehicles","3+","N",200,599,5,5,4,2,4),
("Indoor mini RC helicopter","C Remote control & vehicles","8+","Y",700,1799,3,2,2,2,2),
("Battery train set with track","C Remote control & vehicles","3+","N",450,1299,4,4,4,2,4),
("2-player battery slot-car racer","C Remote control & vehicles","6+","N",750,2299,3,3,4,3,3),
("Kids keyboard 37-key with Indian instrument voices","D Music & sound","4+","N",780,2299,5,3,4,4,5),
("Karaoke mic + Bluetooth speaker","D Music & sound","4+","Y",520,1499,5,3,2,2,4),
("Tabla / dholak electronic pads","D Music & sound","4+","N",650,1999,3,3,4,5,5),
("Regional-language rhymes & stories player","D Music & sound","2+","N",330,999,5,4,4,4,5),
("Reader pen / interactive talking book","D Music & sound","3+","N",800,2499,4,2,4,3,5),
("Light-up piano / xylophone mat","D Music & sound","3+","N",350,999,3,4,4,2,3),
("Lullaby & night-light soother","D Music & sound","0+","N",300,899,4,3,2,3,4),
("Bilingual alphabet & number learning tablet","E Early-learning talking toys","3+","N",420,1199,5,4,4,3,5),
("Quiz buzzer game (multi-player)","E Early-learning talking toys","6+","N",350,999,3,4,4,3,5),
("Talking flashcard reader","E Early-learning talking toys","3+","N",450,1299,4,3,4,3,5),
("LED peg-board matching game","E Early-learning talking toys","4+","N",300,899,3,4,4,3,4),
("Handheld spelling & word game","E Early-learning talking toys","6+","N",380,1099,3,4,4,2,3),
("Counting abacus with light & sound","E Early-learning talking toys","3+","N",280,799,3,4,4,3,5),
("Learn-the-time voice clock","E Early-learning talking toys","4+","N",260,799,3,4,4,3,5),
("Star projector night lamp with lullabies","F Light & ambience gifting","3+","N",260,799,5,4,4,2,4),
("Colour-change kids sleep / wake-up lamp","F Light & ambience gifting","3+","N",320,999,3,4,3,3,3),
("Light-up glow spinner / LED fidget toys","F Light & ambience gifting","5+","N",55,249,4,5,4,1,3),
("Light-up party magic wand","F Light & ambience gifting","3+","N",70,299,4,5,4,1,4),
("DIY mood lamp kit","F Light & ambience gifting","8+","N",200,649,3,4,4,3,3),
("Whack-a-mole reaction game","G Games & pretend play","4+","N",380,1099,4,4,4,2,3),
("Handheld electronic cricket game","G Games & pretend play","6+","N",220,699,4,4,4,4,5),
("Kids digital camera","G Games & pretend play","4+","N",700,1999,4,3,3,2,3),
("Walkie-talkie pair","G Games & pretend play","6+","Y",600,1799,4,2,1,2,3),
("Doctor kit with light & sound stethoscope","G Games & pretend play","3+","N",220,699,4,4,4,2,4),
("Pretend kitchen with light & sound","G Games & pretend play","3+","N",520,1699,4,3,4,2,4),
]
assert len(P)==50
LAND, GST, CLOSE, SHIP, ADS, RET = 1.30, 0.18, 30, 80, 0.12, 0.08
def calc(r):
    n,c,a,w,bom,price,d,e,co,di,ind = r
    net=price/(1+GST); landed=bom*LAND
    fees=price*(0 if price<1000 else 0.08)+CLOSE+SHIP
    cont=net-landed-fees-net*ADS-RET*landed; pct=cont/net
    mi=5 if pct>=.35 else 4 if pct>=.25 else 3 if pct>=.15 else 2 if pct>=.05 else 1
    score=.30*d+.25*mi+.15*e+.10*co+.10*di+.10*ind
    return cont,pct,mi,score
rows=sorted(P,key=lambda r:-calc(r)[3])
out=Path(sys.argv[1] if len(sys.argv)>1 else "."); out.mkdir(parents=True,exist_ok=True)
hdr=["Rank","Product","Category","Age","Wireless","BOM@1k (INR)","Price incl GST (INR)","GST","Net revenue","Landed cost","Referral %","Fees (referral+closing+ship)","Ads","Returns","Contribution/unit","Contribution %","Demand","Ease","Compliance ease","Differentiation","India fit","Margin index","Score","Wave"]
with open(out/"top50.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(hdr)
    for i,r in enumerate(rows,start=1):
        n,c,a,wl,bom,price,d,e,co,di,ind=r; x=i+1
        wave=1 if i<=10 else 2 if i<=25 else 3
        w.writerow([i,n,c,a,wl,bom,price,GST,f"=G{x}/(1+H{x})",f"=F{x}*{LAND}",0 if price<1000 else 0.08,f"=G{x}*K{x}+{CLOSE}+{SHIP}",f"=I{x}*{ADS}",f"={RET}*J{x}",f"=I{x}-J{x}-L{x}-M{x}-N{x}",f"=O{x}/I{x}",d,e,co,di,ind,f"=IF(P{x}>=0.35,5,IF(P{x}>=0.25,4,IF(P{x}>=0.15,3,IF(P{x}>=0.05,2,1))))",f"=0.3*Q{x}+0.25*V{x}+0.15*R{x}+0.1*S{x}+0.1*T{x}+0.1*U{x}",wave])
lines=["| Rank | Product | Category | Age | Wireless | BOM@1k ₹ | Price ₹ | Contribution ₹ | Margin | Score | Wave |","|---|---|---|---|---|---|---|---|---|---|---|"]
for i,r in enumerate(rows,start=1):
    cont,pct,mi,s=calc(r); wave=1 if i<=10 else 2 if i<=25 else 3
    lines.append(f"| {i} | {r[0]} | {r[1][2:]} | {r[2]} | {r[3]} | {r[4]} | {r[5]:,} | {cont:,.0f} | {pct:.0%} | {s:.2f} | {wave} |")
(out/"_table.md").write_text("\n".join(lines)+"\n")
from collections import Counter
print(Counter(r[1] for r in rows[:10])); print(sum(1 for r in rows if r[3]=="Y"),"wireless")
for i,r in enumerate(rows[:12],1): print(i,r[0],f"{calc(r)[1]:.0%}",f"{calc(r)[3]:.2f}")
print("negative contribution:",[r[0] for r in rows if calc(r)[0]<0])
