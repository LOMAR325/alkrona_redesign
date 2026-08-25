import math, random, os
OUT = "/Users/User/Downloads/site test/assets/img"
os.makedirs(OUT, exist_ok=True)
UID = [0]
def uid(p="m"):
    UID[0] += 1
    return f"{p}{UID[0]}"
def P(x, y): return f"{x:.0f},{y:.0f}"
def R(v): return f"{v:.0f}"

# ---------- frames ----------
def frame(ang):
    a = math.radians(ang)
    return math.sin(a), -math.cos(a), math.cos(a), math.sin(a)   # dx,dy,px,py

def loc(bx, by, ang, x, y):
    """local coords: x = across, y = along the leaf axis"""
    dx, dy, px, py = frame(ang)
    return (bx + dx*y + px*x, by + dy*y + py*x)

def shape(bx, by, ang, L, W, kind="oval", bend=0.0):
    """closed leaf outline in local space, bent by `bend` across-axis at the tip"""
    def p(x, y):
        return loc(bx, by, ang, x + bend*(y/L)**2, y*L)
    if kind == "oval":
        pts = [(0,0), (-.92*W,.22,-.80*W,.72, 0,1.0), (.80*W,.72,.92*W,.22, 0,0)]
    elif kind == "round":
        pts = [(0,0), (-1.05*W,.10,-1.02*W,.78, 0,1.0), (1.02*W,.78,1.05*W,.10, 0,0)]
    elif kind == "heart":
        pts = [(0,.20), (-.34*W,.10,-.80*W,.02, -.88*W,.26), (-.96*W,.52,-.62*W,.80, -.34*W,.92),
               (-.16*W,.98,-.06*W,.99, 0,1.0),
               (.06*W,.99,.16*W,.98, .34*W,.92), (.62*W,.80,.96*W,.52, .88*W,.26),
               (.80*W,.02,.34*W,.10, 0,.20)]
    elif kind == "arrow":
        pts = [(0,.24), (-.42*W,.18,-.92*W,.06, -.88*W,-.12), (-.74*W,.22,-.98*W,.52, -.56*W,.74),
               (-.30*W,.92,-.10*W,.95, 0,1.0), (.10*W,.95,.30*W,.92, .56*W,.74),
               (.98*W,.52,.74*W,.22, .88*W,-.12), (.92*W,.06,.42*W,.18, 0,.24)]
    elif kind == "blade":
        pts = [(0,0), (-.62*W,.30,-.55*W,.80, 0,1.0), (.55*W,.80,.62*W,.30, 0,0)]
    elif kind == "paddle":
        pts = [(0,0), (-.80*W,.16,-.86*W,.86, 0,1.0), (.86*W,.86,.80*W,.16, 0,0)]
    else:
        pts = [(0,0), (-.92*W,.22,-.80*W,.72, 0,1.0), (.80*W,.72,.92*W,.22, 0,0)]
    d = f"M{P(*p(pts[0][0], pts[0][1]))}"
    for seg in pts[1:]:
        c1 = p(seg[0], seg[1]); c2 = p(seg[2], seg[3]); e = p(seg[4], seg[5])
        d += f" C{P(*c1)} {P(*c2)} {P(*e)}"
    return d + "Z"

def rib(bx, by, ang, L, bend=0.0, t0=0.0, t1=.94):
    a = loc(bx, by, ang, bend*t0*t0, L*t0)
    m = loc(bx, by, ang, bend*((t0+t1)/2)**2, L*(t0+t1)/2)
    b = loc(bx, by, ang, bend*t1*t1, L*t1)
    return f"M{P(*a)} Q{P(*m)} {P(*b)}"

def veins(bx, by, ang, L, W, n=6, bend=0.0, col="#08120e", op=.32, kind="pinnate"):
    o = []
    for i in range(n):
        t = .18 + i*(.68/max(1, n-1))
        a = loc(bx, by, ang, bend*t*t, L*t)
        for s in (-1, 1):
            vl = W*(1.0 - abs(t-.42)*.8)
            e = loc(bx, by, ang, bend*t*t + s*vl*.92, L*(t + vl/L*.55))
            o.append(f'<path d="M{P(*a)} L{P(*e)}" stroke="{col}" stroke-width="1.4" opacity="{op}" fill="none" stroke-linecap="round"/>')
    return "".join(o)

# ---------- archetypes ----------
def leaf(bx, by, ang, L, W, kind="oval", bend=0, fill="url(#lf1)", vein=True, vn=6, mask=None):
    m = f' mask="url(#{mask})"' if mask else ""
    o = [f'<g{m}><path d="{shape(bx,by,ang,L,W,kind,bend)}" fill="{fill}"/>',
         f'<path d="{rib(bx,by,ang,L,bend)}" fill="none" stroke="#08120e" stroke-width="{max(1.6,L*.011):.1f}" opacity=".42" stroke-linecap="round"/>']
    if vein: o.append(veins(bx, by, ang, L, W, vn, bend))
    o.append("</g>")
    return "".join(o)

def petiole(bx, by, ang, L, bend=0, w=6):
    return f'<path d="{rib(bx,by,ang,L,bend,0,1.0)}" fill="none" stroke="url(#stem)" stroke-width="{w}" stroke-linecap="round"/>'

def monstera_leaf(bx, by, ang, L, W, bend=0, fill="url(#lf1)"):
    """solid blade with fenestrations + edge splits, cut by a mask"""
    mid = uid()
    holes = []
    for i in range(3):
        t = .30 + i*.19
        for s in (-1, 1):
            hx, hy = loc(bx, by, ang, bend*t*t + s*W*.34, L*t)
            rx, ry = W*.26*(1-abs(t-.44)*.7), W*.075
            rot = ang + s*66
            holes.append(f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="#000" transform="rotate({rot:.0f} {hx:.0f} {hy:.0f})"/>')
    for i in range(3):
        t = .22 + i*.21
        for s in (-1, 1):
            a  = loc(bx, by, ang, bend*t*t + s*W*.22, L*t)
            e  = loc(bx, by, ang, bend*t*t + s*W*1.30, L*(t+.030))
            e2 = loc(bx, by, ang, bend*t*t + s*W*1.30, L*(t-.030))
            holes.append(f'<path d="M{P(*a)} L{P(*e)} L{P(*e2)}Z" fill="#000"/>')
    m = (f'<mask id="{mid}"><rect x="0" y="0" width="900" height="1100" fill="#fff"/>' + "".join(holes) + '</mask>')
    return m + leaf(bx, by, ang, L, W, "round", bend, fill, vein=True, vn=5, mask=mid)

def notched_paddle(bx, by, ang, L, W, bend=0, fill="url(#lf1)"):
    mid = uid()
    holes = []
    for i in range(5):
        t = .22 + i*.16
        for s in (-1, 1):
            a = loc(bx, by, ang, bend*t*t + s*W*.34, L*t)
            e = loc(bx, by, ang, bend*t*t + s*W*1.2, L*(t+.05))
            e2 = loc(bx, by, ang, bend*t*t + s*W*1.2, L*(t-.035))
            holes.append(f'<path d="M{P(*a)} L{P(*e)} L{P(*e2)}Z" fill="#000"/>')
    m = f'<mask id="{mid}"><rect width="900" height="1100" fill="#fff"/>' + "".join(holes) + '</mask>'
    return m + leaf(bx, by, ang, L, W, "paddle", bend, fill, vein=True, vn=7, mask=mid)

def rosette(cx, cy, Rd, rings=4, kind="blade", f1="url(#lf1)", f2="url(#lf2)", glow="#7CFFC4"):
    o = []
    for r in range(rings):
        k = 1.0 - r*(.74/rings)
        n = max(4, 10 - r*2)
        rot = r*(180/n)
        for i in range(n):
            ang = rot + i*(360/n)
            L = Rd*k
            o.append(leaf(cx, cy, ang, L, L*.34, kind, L*.10, f1 if r % 2 == 0 else f2, vein=False))
    o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{Rd*.10:.0f}" fill="url(#core)"/>')
    return "".join(o)

def fan(bx, by, n, L, W, spread=52, kind="blade", f1="url(#lf1)", f2="url(#lf2)", bendf=.16, jitter=0):
    o = []
    for i in range(n):
        t = (i/max(1, n-1))*2 - 1
        ang = t*spread + jitter*math.sin(i*3.1)
        ln = L*(.62 + .38*(1 - abs(t)**1.6))
        o.append(leaf(bx + t*W*.35, by, ang, ln, W*(1 - .28*abs(t)), kind, t*ln*bendf, f1 if i % 2 else f2, vein=False))
    return "".join(o)

def basal(bx, by, specs, kind="round", f1="url(#lf1)", f2="url(#lf2)", vn=6, notch=False):
    """specs: list of (angle, petiole_len, leaf_len, leaf_width, bend)"""
    o = []
    for i, (ang, pl, ll, lw, bd) in enumerate(specs):
        o.append(petiole(bx, by, ang, pl, bd*.45, 6))
        tx, ty = loc(bx, by, ang, bd*.45, pl)
        fill = f1 if i % 2 else f2
        if notch:
            o.append(notched_paddle(tx, ty, ang, ll, lw, bd, fill))
        else:
            o.append(leaf(tx, ty, ang, ll, lw, kind, bd, fill, vein=True, vn=vn))
    return "".join(o)

def stalk(bx, by, H, specs, kind="oval", f1="url(#lf1)", f2="url(#lf2)", lean=14):
    """single trunk with alternating leaves. specs: (t_along, angle, len, width)"""
    tipx = bx + lean
    o = [f'<path d="M{P(bx,by)} C{P(bx-6,by-H*.45)} {P(bx+lean*.8,by-H*.72)} {P(tipx,by-H)}" fill="none" stroke="url(#stem)" stroke-width="9" stroke-linecap="round"/>']
    for i, (t, ang, ll, lw) in enumerate(specs):
        x = bx + lean*t*t
        y = by - H*t
        o.append(petiole(x, y, ang, ll*.22, 0, 4))
        tx, ty = loc(x, y, ang, 0, ll*.22)
        o.append(leaf(tx, ty, ang, ll, lw, kind, (18 if ang > 0 else -18), f1 if i % 2 else f2, vein=True, vn=6))
    return "".join(o)

def hanging(cx, cy, strands, f1="url(#lf1)", beads=False, size=40):
    """strands: list of (x_end, y_end, cx1,cy1, cx2,cy2, count)"""
    o = []
    for si, (ex, ey, c1x, c1y, c2x, c2y, n) in enumerate(strands):
        bx0 = cx + (si - (len(strands)-1)/2)*30
        d = f"M{P(bx0,cy)} C{P(c1x,c1y)} {P(c2x,c2y)} {P(ex,ey)}"
        o.append(f'<path d="{d}" fill="none" stroke="url(#stem)" stroke-width="3" stroke-linecap="round" opacity=".9"/>')
        for i in range(n):
            t = .10 + (i + .5)/n*.90
            mt = 1-t
            px = mt**3*bx0 + 3*mt*mt*t*c1x + 3*mt*t*t*c2x + t**3*ex
            py = mt**3*cy + 3*mt*mt*t*c1y + 3*mt*t*t*c2y + t**3*ey
            ddx = 3*mt*mt*(c1x-bx0) + 6*mt*t*(c2x-c1x) + 3*t*t*(ex-c2x)
            ddy = 3*mt*mt*(c1y-cy) + 6*mt*t*(c2y-c1y) + 3*t*t*(ey-c2y)
            base = math.degrees(math.atan2(ddx, -ddy))
            s = 1 if i % 2 else -1
            base = base*.35 + 180*.65 if abs(base-180) < 90 else base
            sc = 1.0 - .38*t
            if beads:
                r = size*.30*sc*(1 + .18*math.sin(i*1.9))
                o.append(f'<circle cx="{px+s*3:.0f}" cy="{py:.0f}" r="{r:.0f}" fill="{f1}"/>')
                o.append(f'<circle cx="{px+s*3-r*.32:.0f}" cy="{py-r*.34:.0f}" r="{r*.26:.0f}" fill="#eafff2" opacity=".38"/>')
            else:
                sz = size*sc
                o.append(leaf(px, py, base + s*58, sz, sz*.54, "heart", s*sz*.16, f1, vein=True, vn=3))
    return "".join(o)

def canes(bx, by, n, H, f1="url(#lf1)"):
    o = []
    for i in range(n):
        off = i - (n-1)/2
        x = bx + off*46
        h = H*(.70 + .30*(1 - abs(off)/max(1, n/2)))
        w = 30 - abs(off)*3.0
        o.append(f'<rect x="{x-w/2:.0f}" y="{by-h:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{w/2:.0f}" fill="url(#cane)"/>')
        for k in range(1, 6):
            ny = by - h*k/6
            o.append(f'<rect x="{x-w/2-2:.0f}" y="{ny:.0f}" width="{w+4:.0f}" height="3" rx="1.5" fill="#0a1512" opacity=".85"/>')
            o.append(f'<rect x="{x-w/2-2:.0f}" y="{ny+3:.0f}" width="{w+4:.0f}" height="1.4" fill="#9dffd8" opacity=".18"/>')
        for k in range(4):
            ly = by - h + h*.05 + k*(h*.20)
            s = 1 if (i + k) % 2 else -1
            for j in range(4):
                a = s*(30 + j*24)
                o.append(leaf(x, ly + j*8, a, 108 - j*13, 13, "blade", s*22, f1, vein=False))
    return "".join(o)

def canopy(cx, cy, RX, RY, count, size, kind="blade", f1="url(#lf1)", f2="url(#lf2)", seed=3, lobes=1):
    random.seed(seed)
    o = []
    for i in range(count):
        a = random.uniform(0, math.tau)
        r = math.sqrt(random.random())
        x = cx + math.cos(a)*RX*r
        y = cy + math.sin(a)*RY*r
        ang = math.degrees(math.atan2(x-cx, -(y-cy))) + random.uniform(-40, 40)
        s = size*random.uniform(.7, 1.25)
        fill = f1 if i % 2 else f2
        if lobes > 1:
            for l in range(lobes):
                la = ang - 46 + l*(92/(lobes-1))
                o.append(leaf(x, y, la, s*(1 - abs(l-(lobes-1)/2)*.14), s*.24, "blade", 0, fill, vein=False))
        else:
            o.append(leaf(x, y, ang, s, s*.42, kind, s*.08, fill, vein=False))
    return "".join(o)

def tree(bx, by, H, RX, RY, count, size, lobes=1, f1="url(#lf1)", f2="url(#lf2)", seed=3):
    o = [f'<path d="M{P(bx,by)} C{P(bx-9,by-H*.4)} {P(bx+10,by-H*.6)} {P(bx+2,by-H*.80)}" fill="none" stroke="url(#trunk)" stroke-width="16" stroke-linecap="round"/>']
    random.seed(seed+9)
    for i in range(5):
        s = -1 if i % 2 else 1
        y = by - H*(.38 + i*.11)
        L = (52 + i*10)*s
        o.append(f'<path d="M{P(bx,y)} Q{P(bx+L*.7, y-14)} {P(bx+L, y-34-i*6)}" fill="none" stroke="url(#trunk)" stroke-width="{7-i*.7:.0f}" stroke-linecap="round"/>')
    o.append(canopy(bx+2, by-H*.86, RX, RY, count, size, "oval", f1, f2, seed, lobes))
    return "".join(o)

def cactus(bx, by, H, f1="url(#lf1)", glow="#9B7CFF"):
    w = H*.30
    o = []
    def col(x, y, h, ww, fill):
        s = [f'<rect x="{x-ww/2:.0f}" y="{y-h:.0f}" width="{ww:.0f}" height="{h:.0f}" rx="{ww/2:.0f}" fill="{fill}"/>']
        for k in range(4):
            rx = x - ww/2 + ww*(k+.5)/4
            s.append(f'<path d="M{P(rx, y-h+ww*.4)} L{P(rx, y-ww*.3)}" stroke="#08120e" stroke-width="2" opacity=".38" stroke-linecap="round"/>')
            for a in range(5):
                ay = y - h + ww*.5 + a*(h/5.4)
                s.append(f'<circle cx="{rx:.0f}" cy="{ay:.0f}" r="1.8" fill="#d8ffee" opacity=".35"/>')
        return "".join(s)
    o.append(col(bx, by, H, w, f1))
    o.append(col(bx + w*.86, by, H*.62, w*.60, "url(#lf2)"))
    o.append(f'<path d="M{P(bx+w*.42, by-H*.52)} Q{P(bx+w*.86, by-H*.56)} {P(bx+w*.86, by-H*.42)}" fill="none" stroke="url(#lf2)" stroke-width="{w*.42:.0f}" stroke-linecap="round"/>')
    o.append(col(bx - w*.80, by, H*.44, w*.52, "url(#lf2)"))
    o.append(f'<path d="M{P(bx-w*.40, by-H*.34)} Q{P(bx-w*.80, by-H*.38)} {P(bx-w*.80, by-H*.26)}" fill="none" stroke="url(#lf2)" stroke-width="{w*.36:.0f}" stroke-linecap="round"/>')
    for (fx, fy) in [(bx, by-H-2), (bx+w*.86, by-H*.62-1)]:
        o.append(f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="13" fill="url(#core)"/>')
        for i in range(7):
            o.append(leaf(fx, fy, i*(360/7), 20, 7, "blade", 0, glow, vein=False))
    return "".join(o)

def spikes(bx, by, n, H, f1="url(#lf1)", flower="#C6A9FF"):
    o = []
    for i in range(n):
        t = (i/max(1, n-1))*2 - 1
        x = bx + t*118
        h = H*(.66 + .34*(1 - abs(t)**1.6)) * (0.9 + .12*math.sin(i*2.3))
        ang = t*16
        o.append(f'<path d="{rib(x,by,ang,h,t*24,0,1)}" fill="none" stroke="url(#stem)" stroke-width="4" stroke-linecap="round"/>')
        for k in range(3):
            ly = .18 + k*.16
            p = loc(x, by, ang, t*24*ly*ly, h*ly)
            s = 1 if k % 2 else -1
            o.append(leaf(p[0], p[1], ang + s*54, 42, 5, "blade", s*8, f1, vein=False))
        for k in range(13):
            u = .50 + k*.042
            p = loc(x, by, ang, t*24*u*u, h*u)
            rr = 11 - k*.55
            o.append(f'<ellipse cx="{p[0]:.0f}" cy="{p[1]:.0f}" rx="{rr:.0f}" ry="{rr*.78:.0f}" fill="{flower}" opacity="{.95-k*.03:.2f}"/>')
        tp = loc(x, by, ang, t*24, h*1.02)
        o.append(f'<circle cx="{tp[0]:.0f}" cy="{tp[1]:.0f}" r="10" fill="url(#core)"/>')
    return "".join(o)

def fern(bx, by, ang, L, W, bend=0, f1="url(#lf1)", n=16):
    o = [f'<path d="{rib(bx,by,ang,L,bend,0,1)}" fill="none" stroke="url(#stem)" stroke-width="4" stroke-linecap="round"/>']
    for i in range(n):
        t = .08 + (i/max(1, n-1))*.90
        prof = math.sin(t*math.pi)**.55
        p = loc(bx, by, ang, bend*t*t, L*t)
        fl = W*(.28 + .95*prof)
        for s in (-1, 1):
            fa = ang + s*(74 - 40*t) + bend*.06
            o.append(f'<path d="{shape(p[0],p[1],fa,fl,fl*.22,"blade",s*fl*.20)}" fill="{f1}" opacity=".96"/>')
            for k in range(3):
                q = loc(p[0], p[1], fa, s*fl*.20*(0.3+k*0.3)**2, fl*(.30+k*.24))
                o.append(f'<path d="{shape(q[0],q[1],fa+s*46,fl*.26,fl*.07,"blade",0)}" fill="{f1}" opacity=".8"/>')
    return "".join(o)

# ---------- pot ----------
def pot(cx, by, w, h, style="taper", accent="#7CFFC4"):
    tw = w; bw = w*(.64 if style == "taper" else .92 if style == "bowl" else .82)
    top = by - h
    o = [f'<path d="M{P(cx-tw/2,top)} L{P(cx+tw/2,top)} L{P(cx+bw/2,by)} Q{P(cx,by+10)} {P(cx-bw/2,by)} Z" fill="url(#potg)"/>',
         f'<path d="M{P(cx-tw/2,top)} L{P(cx-tw/2+7,top)} L{P(cx-bw/2+7,by-2)} L{P(cx-bw/2,by-2)} Z" fill="#eafff2" opacity=".08"/>',
         f'<path d="M{P(cx+tw/2,top)} L{P(cx+tw/2-4,top)} L{P(cx+bw/2-4,by-2)} L{P(cx+bw/2,by-2)} Z" fill="{accent}" opacity=".10"/>',
         f'<rect x="{cx-tw/2:.0f}" y="{top+h*.34:.0f}" width="{tw:.0f}" height="2" fill="{accent}" opacity=".22"/>',
         f'<ellipse cx="{cx:.0f}" cy="{top:.0f}" rx="{tw/2:.0f}" ry="{tw*.115:.0f}" fill="#08110e"/>',
         f'<ellipse cx="{cx:.0f}" cy="{top:.0f}" rx="{tw/2:.0f}" ry="{tw*.115:.0f}" fill="none" stroke="{accent}" stroke-width="2" opacity=".6"/>',
         f'<ellipse cx="{cx:.0f}" cy="{top+3:.0f}" rx="{tw/2-10:.0f}" ry="{tw*.088:.0f}" fill="#0c1814"/>']
    return "".join(o)

def hangpot(cx, by, w, h, accent="#7CFFC4"):
    top = by - h
    o = [f'<path d="M{P(cx-w*.44,top-96)} Q{P(cx-w*.30,top-30)} {P(cx-w*.40,top)}" fill="none" stroke="{accent}" stroke-width="1.6" opacity=".55"/>',
         f'<path d="M{P(cx+w*.44,top-96)} Q{P(cx+w*.30,top-30)} {P(cx+w*.40,top)}" fill="none" stroke="{accent}" stroke-width="1.6" opacity=".55"/>',
         f'<path d="M{P(cx,top-110)} L{P(cx,top-96)}" stroke="{accent}" stroke-width="2" opacity=".5"/>',
         f'<circle cx="{cx:.0f}" cy="{top-114:.0f}" r="6" fill="none" stroke="{accent}" stroke-width="2" opacity=".7"/>']
    o.append(f'<path d="M{P(cx-w/2,top)} L{P(cx+w/2,top)} Q{P(cx+w*.40,by)} {P(cx,by)} Q{P(cx-w*.40,by)} {P(cx-w/2,top)} Z" fill="url(#potg)"/>')
    o.append(f'<ellipse cx="{cx:.0f}" cy="{top:.0f}" rx="{w/2:.0f}" ry="{w*.13:.0f}" fill="#08110e"/>')
    o.append(f'<ellipse cx="{cx:.0f}" cy="{top:.0f}" rx="{w/2:.0f}" ry="{w*.13:.0f}" fill="none" stroke="{accent}" stroke-width="2" opacity=".6"/>')
    return "".join(o)

# ---------- scene ----------
def defs(pal, glow):
    c1, c2, c3 = pal
    return f'''<defs>
<radialGradient id="bg" cx="50%" cy="32%" r="80%"><stop offset="0" stop-color="#0e201c"/><stop offset="52%" stop-color="#071110"/><stop offset="1" stop-color="#03080a"/></radialGradient>
<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{glow}" stop-opacity=".38"/><stop offset="55%" stop-color="{glow}" stop-opacity=".09"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
<linearGradient id="lf1" x1="0" y1="1" x2=".35" y2="0"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<linearGradient id="lf2" x1="0" y1="1" x2=".65" y2="0"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c3}"/></linearGradient>
<linearGradient id="stem" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#1b3a30"/><stop offset="1" stop-color="{c2}" stop-opacity=".9"/></linearGradient>
<linearGradient id="trunk" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#16302a"/><stop offset="1" stop-color="{c2}" stop-opacity=".7"/></linearGradient>
<linearGradient id="cane" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#16342c"/><stop offset=".45" stop-color="{c2}"/><stop offset="1" stop-color="#0f2620"/></linearGradient>
<radialGradient id="core" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{glow}"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
<linearGradient id="potg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#182422"/><stop offset="1" stop-color="#090f0f"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{glow}" stop-opacity="0"/><stop offset=".5" stop-color="{glow}" stop-opacity=".55"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></linearGradient>
</defs>'''

def scene(name, W, H, pal, glow, body, floor_y=None, halo=(.5, .40, .46), grid=44):
    g = ""
    if grid:
        g = (f'<g opacity=".14" stroke="{glow}" stroke-width=".7">'
             + "".join(f'<path d="M0,{y} H{W}"/>' for y in range(0, H, grid))
             + "".join(f'<path d="M{x},0 V{H}"/>' for x in range(0, W, grid)) + '</g>')
    fl = ""
    if floor_y:
        fl = (f'<ellipse cx="{W/2:.0f}" cy="{floor_y}" rx="{W*.34:.0f}" ry="{H*.028:.0f}" fill="url(#halo)"/>'
              f'<rect x="{W*.12:.0f}" y="{floor_y}" width="{W*.76:.0f}" height="2" fill="url(#floor)"/>')
    hx, hy, hr = halo
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">'
           f'{defs(pal,glow)}<rect width="{W}" height="{H}" fill="url(#bg)"/>{g}'
           f'<ellipse cx="{W*hx:.0f}" cy="{H*hy:.0f}" rx="{W*hr:.0f}" ry="{W*hr:.0f}" fill="url(#halo)"/>{fl}{body}</svg>')
    open(os.path.join(OUT, name), "w").write(svg)
    return len(svg)

GREEN  = (("#0f4436", "#3fbe86", "#2ad6a5"), "#7CFFC4")
LIME   = (("#1d4a1c", "#93da3c", "#c9ff52"), "#B8FF3C")
TEAL   = (("#0b3f4a", "#2aa8b8", "#37e2d2"), "#2AE0D0")
VIOLET = (("#2b1f56", "#7d6bd6", "#ab8dff"), "#9B7CFF")
JADE   = (("#123f31", "#48c99a", "#8affd0"), "#5FF7C8")
ROSE   = (("#4a1f3a", "#c66aa0", "#ff9ecb"), "#FF9ECB")
W = H = 640; FY = 556

def plant_body(kind, glow="#7CFFC4", o=None):
    o = o or {}
    b = []
    if kind == "monstera":
        b.append(pot(320, FY, 152, 122, accent=glow))
        for (a, pl, L, bd) in [(-58, 108, 168, -34), (58, 108, 164, 34), (-22, 166, 186, -14), (24, 158, 180, 16), (0, 108, 142, 0)]:
            b.append(petiole(320, FY-118, a, pl, bd*.4, 7))
            t = loc(320, FY-118, a, bd*.4, pl)
            b.append(monstera_leaf(t[0], t[1], a, L, o.get("w", 84), bd))
    elif kind == "fiddle":
        b.append(pot(320, FY, 148, 118, accent=glow))
        b.append(stalk(320, FY-118, 336, [(.14, -76, 176, 70), (.34, 78, 184, 74), (.54, -70, 174, 68), (.72, 74, 160, 62), (.88, -46, 142, 56), (1.0, 24, 130, 50)], "oval"))
    elif kind == "rubber":
        b.append(pot(320, FY, 150, 118, accent=glow))
        b.append(stalk(320, FY-118, 320, [(.10, -62, 126, 56), (.28, 66, 130, 58), (.46, -56, 124, 54), (.63, 60, 118, 52), (.80, -44, 108, 48), (.94, 30, 96, 44)], "oval", lean=22))
    elif kind == "calathea":
        b.append(pot(320, FY, 152, 116, accent=glow))
        b.append(basal(320, FY-114, [(-64, 108, 150, 122, -46), (-27, 146, 162, 132, -18), (12, 150, 160, 130, 12), (48, 130, 150, 122, 38), (76, 98, 132, 108, 60)], "round", vn=7))
    elif kind == "bird":
        b.append(pot(320, FY, 150, 122, accent=glow))
        for (a, pl, L, wd, bd) in [(-38, 176, 176, 52, -34), (-13, 208, 196, 56, -12), (13, 204, 192, 56, 12), (38, 172, 172, 50, 34), (62, 132, 140, 44, 52)]:
            b.append(petiole(320, FY-120, a, pl, bd*.4, 6))
            t = loc(320, FY-120, a, bd*.4, pl)
            b.append(notched_paddle(t[0], t[1], a, L, wd, bd, "url(#lf1)" if a % 2 else "url(#lf2)"))
    elif kind == "anthurium":
        b.append(pot(320, FY, 152, 112, accent=glow))
        b.append(basal(320, FY-110, [(-66, 96, 168, 82, -40), (-30, 120, 196, 92, -16), (8, 124, 198, 94, 10), (44, 110, 176, 84, 34), (72, 86, 148, 72, 54)], "heart", vn=6))
    elif kind == "philo":
        b.append(pot(320, FY, 150, 114, accent=glow))
        b.append(basal(320, FY-112, [(-58, 104, 162, 76, -38), (-24, 132, 182, 84, -14), (10, 134, 180, 84, 12), (44, 118, 162, 76, 34), (-80, 76, 132, 62, -58), (76, 80, 136, 64, 56)], "heart", vn=5))
    elif kind == "alocasia":
        b.append(pot(320, FY, 148, 116, accent=glow))
        b.append(basal(320, FY-114, [(-30, 168, 168, 76, -20), (-8, 196, 186, 82, -6), (16, 188, 178, 80, 10), (42, 152, 152, 70, 30), (-54, 132, 140, 66, -40)], "arrow", vn=6))
    elif kind == "rosette":
        b.append(pot(320, FY, 194, 90, style="bowl", accent=glow))
        b.append(rosette(320, FY-104, o.get("R", 168), o.get("rings", 4), o.get("lk", "blade")))
    elif kind == "fan":
        b.append(pot(320, FY, 150, 118, accent=glow))
        b.append(fan(320, FY-118, o.get("n", 9), o.get("L", 340), o.get("W", 30), o.get("spread", 52), o.get("lk", "blade"), bendf=o.get("bendf", .16)))
    elif kind == "fern":
        b.append(pot(320, FY, 162, 106, style="bowl", accent=glow))
        for (a, L, bd) in [(-62, 230, -80), (-30, 282, -50), (0, 300, 6), (32, 278, 52), (64, 224, 84)]:
            b.append(fern(320, FY-106, a, L, o.get("W", 48), bd, n=o.get("n", 15)))
    elif kind == "hanging":
        b.append(hangpot(320, 268, 150, 104, accent=glow))
        b.append(fan(320, 164, 5, 92, 26, 58))
        b.append(hanging(320, 276, [
            (150, 486, 262, 350, 168, 372, 8), (238, 566, 288, 366, 236, 448, 10),
            (330, 610, 330, 372, 336, 494, 11), (420, 556, 372, 366, 424, 440, 10),
            (498, 478, 398, 350, 490, 366,  8)], beads=o.get("beads", False), size=o.get("s", 44)))
    elif kind == "canes":
        b.append(pot(320, FY, 168, 112, accent=glow))
        b.append(canes(320, FY-112, o.get("n", 5), 350))
    elif kind == "tree":
        b.append(pot(320, FY, 180, 118, accent=glow))
        b.append(tree(320, FY-116, 300, o.get("rx", 150), o.get("ry", 96), o.get("c", 46), o.get("s", 54), o.get("lobes", 1)))
    elif kind == "cactus":
        b.append(pot(320, FY, 156, 112, accent=glow))
        b.append(cactus(320, FY-112, 316, glow=glow))
    elif kind == "spikes":
        b.append(pot(320, FY, 168, 108, accent=glow))
        b.append(spikes(320, FY-108, o.get("n", 9), 330, flower=o.get("fl", "#C6A9FF")))
    return "".join(b)

def build(name, kind, pal, o=None):
    cols, glow = pal
    return scene(name, W, H, cols, glow, plant_body(kind, glow, o), floor_y=FY)

ART = [
    ("monstera-deliciosa", "monstera", GREEN, {}),
    ("monstera-obliqua",   "monstera", JADE,  {"w": 74}),
    ("fiddle-leaf-fig",    "fiddle",   GREEN, {}),
    ("rubber-tree",        "rubber",   VIOLET,{}),
    ("calathea-orbifolia", "calathea", TEAL,  {}),
    ("bird-of-paradise",   "bird",     JADE,  {}),
    ("anthurium-crystal",  "anthurium",ROSE,  {}),
    ("philodendron-pink",  "philo",    ROSE,  {}),
    ("alocasia-frydek",    "alocasia", LIME,  {}),
    ("echeveria-glow",     "rosette",  LIME,  {"R": 172, "rings": 4}),
    ("haworthia-zebra",    "rosette",  TEAL,  {"R": 152, "rings": 3, "lk": "blade"}),
    ("jade-prism",         "rosette",  JADE,  {"R": 162, "rings": 4, "lk": "oval"}),
    ("snake-plant",        "fan",      LIME,  {"n": 9, "L": 356, "W": 34, "spread": 34, "bendf": .10}),
    ("aloe-vera",          "fan",      TEAL,  {"n": 11, "L": 306, "W": 36, "spread": 68, "bendf": .22}),
    ("dracaena-spike",     "fan",      VIOLET,{"n": 15, "L": 322, "W": 22, "spread": 78, "bendf": .26}),
    ("boston-fern",        "fern",     GREEN, {"W": 50, "n": 15}),
    ("maidenhair-fern",    "fern",     JADE,  {"W": 40, "n": 18}),
    ("pothos-neon",        "hanging",  LIME,  {"s": 46}),
    ("string-of-pearls",   "hanging",  JADE,  {"s": 40, "beads": True}),
    ("bamboo-screen",      "canes",    TEAL,  {"n": 5}),
    ("japanese-maple",     "tree",     ROSE,  {"rx": 156, "ry": 100, "c": 40, "s": 58, "lobes": 5}),
    ("olive-tree",         "tree",     GREEN, {"rx": 158, "ry": 104, "c": 60, "s": 46}),
    ("columnar-cactus",    "cactus",   VIOLET,{}),
    ("lavender-row",       "spikes",   VIOLET,{"n": 9}),
]
tot = 0
for (n, k, p, o) in ART:
    tot += build(f"plant-{n}.svg", k, p, o)
print(f"{len(ART)} svgs, avg {tot//len(ART)}B, max {max(os.path.getsize(os.path.join(OUT,f'plant-{n}.svg')) for n,_,_,_ in ART)}B")

# ================= composites =================
def place(body, x, y, s, op=1.0):
    tx, ty = x - 320*s, y - 556*s
    o = f' opacity="{op}"' if op < 1 else ""
    return f'<g transform="translate({tx:.0f},{ty:.0f}) scale({s:.3f})"{o}>{body}</g>'

def scene2(name, W, H, cols, glow, body, bg=True, grid=44, floor=None, halo=(.5,.42,.5)):
    g = ""
    if grid:
        g = (f'<g opacity=".13" stroke="{glow}" stroke-width=".7">'
             + "".join(f'<path d="M0,{y} H{W}"/>' for y in range(0, H, grid))
             + "".join(f'<path d="M{x},0 V{H}"/>' for x in range(0, W, grid)) + '</g>')
    bgr = f'<rect width="{W}" height="{H}" fill="url(#bg)"/>' if bg else ""
    fl = ""
    if floor:
        fl = (f'<ellipse cx="{W/2:.0f}" cy="{floor}" rx="{W*.36:.0f}" ry="{H*.030:.0f}" fill="url(#halo)"/>'
              f'<rect x="{W*.08:.0f}" y="{floor}" width="{W*.84:.0f}" height="2" fill="url(#floor)"/>')
    hx, hy, hr = halo
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">'
           f'{defs(cols,glow)}{bgr}{g}'
           f'<ellipse cx="{W*hx:.0f}" cy="{H*hy:.0f}" rx="{W*hr:.0f}" ry="{W*hr*.9:.0f}" fill="url(#halo)"/>{fl}{body}</svg>')
    open(os.path.join(OUT, name), "w").write(svg)
    return len(svg)

def orbs(specs):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#core)" opacity="{op}"/>' for (x, y, r, op) in specs)

def rings(cx, cy, Rd, glow, n=3):
    o = []
    for i in range(n):
        r = Rd*(1 - i*.16)
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.0f}" fill="none" stroke="{glow}" stroke-width="1" opacity="{.20-i*.05:.2f}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{Rd:.0f}" fill="none" stroke="{glow}" stroke-width="1.5" opacity=".28" stroke-dasharray="3 14"/>')
    return "".join(o)

hero = (rings(450, 436, 374, "#7CFFC4", 3)
        + orbs([(120, 210, 26, .5), (784, 300, 20, .45), (700, 720, 30, .38), (150, 700, 18, .42), (832, 540, 14, .38)])
        + place(plant_body("monstera", "#7CFFC4"), 450, 878, 1.72))
scene2("hero-specimen.svg", 900, 900, ("#0f4436", "#3fbe86", "#2ad6a5"), "#7CFFC4", hero, bg=False, grid=0, halo=(.5, .46, .44))

CW, CH, CF = 760, 560, 496
COLL = [
 ("indoor",     GREEN,  [("monstera", (300, 486), .86), ("fiddle", (556, 470), .60), ("calathea", (108, 502), .48)]),
 ("outdoor",    TEAL,   [("canes", (566, 486), .68), ("tree", (272, 478), .80), ("spikes", (94, 502), .44)]),
 ("succulents", LIME,   [("rosette", (300, 494), .80), ("cactus", (556, 470), .56), ("rosette", (118, 502), .44)]),
 ("rare",       ROSE,   [("anthurium", (292, 486), .84), ("alocasia", (554, 474), .58), ("philo", (106, 502), .46)]),
 ("hanging",    JADE,   [("hanging", (300, 476), .84), ("hanging", (572, 436), .54), ("fern", (108, 502), .44)]),
 ("statement",  VIOLET, [("cactus", (300, 486), .84), ("fan", (560, 486), .52), ("rosette", (108, 500), .46)]),
]
for (nm, pal, items) in COLL:
    cols, glow = pal
    body = orbs([(96, 120, 30, .32), (664, 150, 22, .28)])
    for (kind, (x, y), sc) in items:
        body += place(plant_body(kind, glow, {}), x, y, sc, 1.0 if sc > .7 else .70)
    scene2(f"collection-{nm}.svg", CW, CH, cols, glow, body, floor=CF, halo=(.42, .44, .5))

def hud(W, H, glow):
    o = [f'<g stroke="{glow}" fill="none" opacity=".45">',
         f'<circle cx="{W*.70:.0f}" cy="{H*.34:.0f}" r="46" stroke-width="1.2"/>',
         f'<circle cx="{W*.70:.0f}" cy="{H*.34:.0f}" r="72" stroke-width="1" stroke-dasharray="2 10"/>',
         f'<path d="M{W*.70-66:.0f},{H*.34:.0f} h20 M{W*.70+46:.0f},{H*.34:.0f} h20 M{W*.70:.0f},{H*.34-66:.0f} v20 M{W*.70:.0f},{H*.34+46:.0f} v20" stroke-width="1.4"/>',
         '</g>']
    for i in range(10):
        o.append(f'<rect x="{W*.07+i*13:.0f}" y="{H*.84:.0f}" width="5" height="{6+((i*7) % 24)}" fill="{glow}" opacity="{.22+(i % 3)*.2:.2f}"/>')
    o.append(f'<rect x="{W*.07:.0f}" y="{H*.11:.0f}" width="54" height="3" fill="{glow}" opacity=".75"/>')
    return "".join(o)

for (nm, pal, kind, px, py, ps) in [("light", TEAL, "monstera", 250, 486, .80),
                                    ("water", JADE, "calathea", 240, 452, .78),
                                    ("soil", LIME, "rosette", 246, 372, .74),
                                    ("pests", ROSE, "anthurium", 244, 470, .76),
                                    ("light2", VIOLET, "fan", 250, 500, .74)]:
    cols, glow = pal
    scene2(f"guide-{nm}.svg", 760, 460, cols, glow,
           place(plant_body(kind, glow, {}), px, py, ps) + hud(760, 460, glow),
           grid=38, halo=(.60, .38, .44))

atm = (orbs([(180, 160, 40, .38), (980, 220, 28, .32), (1400, 180, 34, .28), (620, 300, 22, .28)])
       + place(plant_body("fern", "#7CFFC4"), 250, 700, .78, .5)
       + place(plant_body("monstera", "#7CFFC4"), 800, 720, .94, .8)
       + place(plant_body("canes", "#7CFFC4"), 1340, 700, .76, .5))
scene2("atmosphere.svg", 1600, 720, ("#0f4436", "#3fbe86", "#2ad6a5"), "#7CFFC4", atm, grid=48, floor=636, halo=(.5, .44, .4))
print("composites done")
