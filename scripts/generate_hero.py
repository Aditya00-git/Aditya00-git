#!/usr/bin/env python3
"""
Generate the theme-aware hero banner (dark.svg / light.svg).

Same structure as the reference profile.sh --live banner: a terminal
window with a VISUAL.MAP ascii-art panel on the left and a typed-out
SYSTEM.INFO field list on the right. Recolored to a flat greyscale/mono
palette to match the rest of this profile (stats.svg / langs.svg / ascii.svg),
instead of a blue/violet/emerald accent scheme.

Run: python3 scripts/generate_hero.py
Reads:  ascii.svg              (already-generated ascii portrait, reused as-is)
Writes: dark.svg, light.svg    (repo root)
"""
import re

THEMES = {
    "light": {
        "BG": "#FAF8F5", "PANEL_BAR": "#F3EEE7", "PANEL": "#FFFFFF",
        "TEXT": "#241C15", "LABEL": "#B8501F", "MUTED": "#6B5D4F",
        "DOTS": "rgba(36,28,21,0.22)", "BORDER": "rgba(36,28,21,0.10)",
        "BOX_STROKE": "rgba(184,80,31,0.30)", "ACCENT": ["#C2601F", "#0F7A6E", "#B8501F"],
        "ASCII": "#241C15", "LIVE": "#C2410C", "GLYPH": "#0F7A6E",
    },
    "dark": {
        "BG": "#141110", "PANEL_BAR": "#1C1815", "PANEL": "#141110",
        "TEXT": "#F5E9DD", "LABEL": "#E08A4E", "MUTED": "#B3A090",
        "DOTS": "rgba(245,233,221,0.18)", "BORDER": "rgba(245,233,221,0.08)",
        "BOX_STROKE": "rgba(224,138,78,0.30)", "ACCENT": ["#E08A4E", "#2DD4BF", "#E08A4E"],
        "ASCII": "#F5E9DD", "LIVE": "#F97316", "GLYPH": "#2DD4BF",
    },
}

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

FIELDS = [
    ("Subject", "Aditya Seswani"),
    ("Role", "Full-Stack Developer"),
    ("Education", "VIT Bhopal"),
    ("Status", "Reliance Foundation Scholar"),
    ("Motto", "Ship it, then make it not embarrassing"),
    ("Core.Lang", "Python, JavaScript, C++, Java, PHP"),
    ("Core.Backend", "Node.js, Express"),
    ("Core.Frontend", "HTML5, CSS3, Tailwind"),
    ("Core.Database", "MySQL, MongoDB"),
    ("Core.Infra", "Docker, Git"),
]

CONTACT = [
    ("Grid.Mail", "seswaniaditya@gmail.com"),
    ("Grid.Portfolio", "portfolio--adi.vercel.app"),
    ("Grid.LinkedIn", "in/aditya-seswani"),
    ("Grid.GitHub", "@Aditya00-git"),
]


def dots(n):
    return "." * max(n, 3)


def load_ascii_rows():
    """Pull the pre-rendered, animated ascii rows straight out of ascii.svg
    so the portrait itself is never regenerated / redrawn from scratch."""
    with open("ascii.svg") as f:
        data = f.read()
    start = data.find("<clipPath")
    end = data.rfind("</svg>")
    inner = data[start:end]
    # neutralize the theme-switching CSS class baked into ascii.svg —
    # we set fill explicitly per-theme in the wrapping <g> instead
    inner = inner.replace(' class="a"', "")
    return inner


def build(theme_name, ascii_inner):
    t = THEMES[theme_name]
    W, H = 1180, 610
    email = "seswaniaditya@gmail.com"
    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{FONT}" role="img" aria-label="Aditya Seswani — profile.sh --live">')
    a('<defs>')
    a(f'<linearGradient id="accent_{theme_name}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{t["ACCENT"][0]}"><animate attributeName="stop-color" '
      f'values="{t["ACCENT"][0]};{t["ACCENT"][1]};{t["ACCENT"][2]};{t["ACCENT"][0]}" dur="10s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{t["ACCENT"][2]}"><animate attributeName="stop-color" '
      f'values="{t["ACCENT"][2]};{t["ACCENT"][0]};{t["ACCENT"][1]};{t["ACCENT"][2]}" dur="10s" repeatCount="indefinite"/></stop>'
      '</linearGradient>')
    a(f'<filter id="glow8_{theme_name}" x="-60%" y="-60%" width="220%" height="220%">'
      f'<feGaussianBlur stdDeviation="8"/></filter>')
    a(f'<clipPath id="winClip_{theme_name}"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="18"/></clipPath>')
    a('</defs>')

    a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="18" fill="{t["BG"]}"/>')
    a(f'<g clip-path="url(#winClip_{theme_name})">')
    a(f'<rect x="2" y="2" width="{W-4}" height="{H-4}" fill="{t["PANEL"]}"/>')
    a(f'<rect x="2" y="2" width="{W-4}" height="46" fill="{t["PANEL_BAR"]}"/>')
    a(f'<line x1="2" y1="48" x2="{W-2}" y2="48" stroke="{t["BORDER"]}"/>')
    a('<circle cx="30" cy="25" r="5.5" fill="#ff5f56"/>')
    a('<circle cx="50" cy="25" r="5.5" fill="#ffbd2e"/>')
    a('<circle cx="70" cy="25" r="5.5" fill="#27c93f"/>')
    a(f'<text x="{W/2:.0f}" y="29" text-anchor="middle" font-size="12" fill="{t["MUTED"]}">'
      f'{email} - % ./profile.sh --live</text>')

    # ---- left: VISUAL.MAP ----
    a(f'<text x="38" y="74" font-size="10" letter-spacing="3" fill="{t["MUTED"]}">VISUAL.MAP</text>')
    box_x, box_y, box_w, box_h = 36, 84, 460, 494
    a(f'<rect x="{box_x}" y="{box_y}" width="{box_w}" height="{box_h}" rx="10" fill="none" '
      f'stroke="url(#accent_{theme_name})" stroke-width="2" opacity="0.5" filter="url(#glow8_{theme_name})"/>')
    a(f'<rect x="{box_x}" y="{box_y}" width="{box_w}" height="{box_h}" rx="10" fill="{t["PANEL"]}" '
      f'stroke="{t["BOX_STROKE"]}"/>')
    scale = min(box_w / 568, box_h / 614) * 0.98
    tx = box_x + (box_w - 568 * scale) / 2
    ty = box_y + (box_h - 614 * scale) / 2
    KT = "0;0.55;0.62;0.85;0.92;1"
    DUR = "9s"
    # ascii portrait: visible, dips out mid-cycle, returns
    a(f'<g fill="{t["ASCII"]}">'
      f'<animate attributeName="opacity" values="1;1;0;0;0;1" keyTimes="{KT}" '
      f'dur="{DUR}" begin="3.2s" repeatCount="indefinite" fill="freeze"/>'
      f'<g transform="translate({tx:.1f},{ty:.1f}) scale({scale:.4f})">')
    a(ascii_inner)
    a('</g></g>')
    # code glyph: hidden, flickers in as a glitch during the dip, fades back out
    gcx, gcy = box_x + box_w / 2, box_y + box_h / 2
    a(f'<g opacity="0" font-family="{FONT}" font-weight="700" fill="{t["GLYPH"]}" '
      f'text-anchor="middle" transform="translate({gcx:.1f},{gcy:.1f})">'
      f'<animate attributeName="opacity" values="0;0;0.15;1;1;0.2;0;0" '
      f'keyTimes="0;0.53;0.57;0.62;0.85;0.89;0.93;1" dur="{DUR}" begin="3.2s" repeatCount="indefinite" fill="freeze"/>'
      f'<animateTransform attributeName="transform" type="translate" '
      f'values="{gcx-4:.1f} {gcy:.1f};{gcx-4:.1f} {gcy:.1f};{gcx+3:.1f} {gcy:.1f};{gcx:.1f} {gcy:.1f};'
      f'{gcx:.1f} {gcy:.1f};{gcx-3:.1f} {gcy:.1f};{gcx:.1f} {gcy:.1f};{gcx:.1f} {gcy:.1f}" '
      f'keyTimes="0;0.53;0.57;0.62;0.85;0.89;0.93;1" dur="{DUR}" begin="3.2s" repeatCount="indefinite" fill="freeze" additive="sum"/>'
      f'<text font-size="96" dy="30">&lt;/&gt;</text>'
      f'</g>')
    # scanline glitch bars during the transition window only
    for i in range(6):
        gy = box_y + 40 + i * (box_h - 80) / 5
        a(f'<rect x="{box_x+10}" y="{gy:.0f}" width="{box_w-20}" height="{2 + i%3}" '
          f'fill="{t["GLYPH"]}" opacity="0">'
          f'<animate attributeName="opacity" values="0;0;0.5;0;0" '
          f'keyTimes="0;0.55;0.585;0.62;1" dur="{DUR}" begin="{3.2+i*0.02:.2f}s" repeatCount="indefinite"/>'
          f'</rect>')

    # ---- right: SYSTEM.INFO ----
    rx = 522
    a(f'<text x="{rx}" y="106" font-size="13" letter-spacing="2" fill="{t["LABEL"]}">SYSTEM.INFO</text>')
    a(f'<line x1="{rx+44}" y1="102" x2="{W-55}" y2="102" stroke="{t["BORDER"]}"/>')
    a(f'<text x="{W-55}" y="106" text-anchor="end" font-size="12" fill="{t["LIVE"]}" font-weight="700">'
      f'<tspan>&#9679;</tspan> LIVE<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" '
      f'repeatCount="indefinite"/></text>')

    a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.6s" fill="freeze"/>'
      f'<rect x="{rx}" y="122" width="245" height="20" rx="4" fill="{t["PANEL_BAR"]}"/>'
      f'<text x="{rx+9}" y="136" font-size="14" font-weight="700" fill="{t["LABEL"]}">{email}</text>'
      f'<line x1="{rx+255}" y1="130" x2="{W-55}" y2="130" stroke="{t["BORDER"]}"/></g>')

    y = 162
    begin = 0.90
    for label, value in FIELDS:
        leader = dots(60 - len(label))
        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" '
          f'begin="{begin:.2f}s" fill="freeze"/>'
          f'<text x="{rx}" y="{y}" font-size="14" xml:space="preserve">'
          f'<tspan fill="{t["LABEL"]}">{label} </tspan><tspan fill="{t["DOTS"]}">{leader}</tspan>'
          f'<tspan fill="{t["TEXT"]}" font-weight="600"> {value}</tspan></text></g>')
        y += 23
        begin += 0.12

    a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
      f'<text x="{rx}" y="{y+8}" font-size="14" xml:space="preserve">'
      f'<tspan fill="{t["MUTED"]}">- Contact </tspan><tspan fill="{t["DOTS"]}">'
      f'{"-"*70}</tspan></text></g>')
    y += 31
    begin += 0.12
    for label, value in CONTACT:
        leader = dots(60 - len(label))
        a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" '
          f'begin="{begin:.2f}s" fill="freeze"/>'
          f'<text x="{rx}" y="{y}" font-size="14" xml:space="preserve">'
          f'<tspan fill="{t["LABEL"]}">{label} </tspan><tspan fill="{t["DOTS"]}">{leader}</tspan>'
          f'<tspan fill="{t["TEXT"]}" font-weight="600"> {value}</tspan></text></g>')
        y += 23
        begin += 0.12

    a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{begin+0.2:.2f}s" fill="freeze"/>'
      f'<text x="{rx}" y="{y+16}" font-size="14" fill="{t["MUTED"]}">&#9656; More about me &amp; projects '
      f'below in README &#8595; <tspan fill="{t["LABEL"]}">&#9608;'
      f'<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text></g>')

    a('</g>')  # close winClip group
    a(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="17" fill="none" '
      f'stroke="url(#accent_{theme_name})" stroke-width="3" opacity="0.5" filter="url(#glow8_{theme_name})"/>')
    a(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="17" fill="none" '
      f'stroke="url(#accent_{theme_name})" stroke-width="1.6"/>')
    a('</svg>')
    return "".join(s)


if __name__ == "__main__":
    ascii_inner = load_ascii_rows()
    for theme in ("light", "dark"):
        svg = build(theme, ascii_inner)
        fname = f"{theme}.svg"
        with open(fname, "w") as f:
            f.write(svg)
        print(f"wrote {fname}: {len(svg)//1024}KB")
