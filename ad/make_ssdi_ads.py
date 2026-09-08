"""
SSDI click-to-call creatives.

Written for a much tighter audience than the Roblox set: the buyer only pays
on a signed retainer, and only accepts callers aged 50-63 who worked 5 of the
last 10 years, see a doctor, are not already represented and are not already
receiving benefits. So the job of these ads is NOT to maximise taps. It is to
get people inside that box to ring and to keep everyone else scrolling.

Three angles, in the order I would bet on them:

  A. DENIED — the strongest. People already denied are further down the road,
     already believe they qualify, and are the ones who actually sign. Most
     first applications are refused, so the pool is large and it costs nothing
     to say the thing they most need to hear: a denial is not the end.

  B. AGE 50+ — SSA's own rules genuinely treat applicants over 50 differently.
     Saying so is true, specific, and self-selects the exact band the buyer
     buys. It is also the rare case where naming the age is a benefit to the
     reader rather than a filter imposed on them.

  C. WAITING — for people who applied and are stuck in the queue with no idea
     what happens next. High intent, low awareness that representation exists.

Policy note, same as the Roblox set: nothing here asserts knowledge about the
person seeing it. "Were you denied?" is a question about a fact they can check,
not a claim about their health, and every headline is framed around the
process rather than their condition.

Also deliberately absent: the word "free money", any benefit amount, and any
promise of approval. Numbers and guarantees are what get disability ads pulled.
"""
import os
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, "/var/lib/freelancer/projects/40328639/roblox-funnel/ad")
from make_ads import (NAVY, NAVY2, TEAL, TEAL_D, CREAM, WHITE, MUTED, INK, GREY,
                      B, R, f, block, pill)

GO = (15, 122, 61)


def gradient(d, W, H):
    for i in range(H):
        t = i / H
        d.line([(0, i), (W, i)],
               fill=(int(NAVY[0] + (NAVY2[0] - NAVY[0]) * t),
                     int(NAVY[1] + (NAVY2[1] - NAVY[1]) * t),
                     int(NAVY[2] + (NAVY2[2] - NAVY[2]) * t)))


def logo(d, x, y, on_dark=True, mark=52):
    d.rounded_rectangle([x, y, x + mark, y + mark], radius=14,
                        fill=WHITE if on_dark else NAVY)
    fm = f(B, 15)
    d.text((x + (mark - d.textlength("DBA", font=fm)) / 2, y + mark / 2 - 9),
           "DBA", font=fm, fill=NAVY if on_dark else WHITE)
    fb_ = f(B, 25)
    tx = x + mark + 14
    d.text((tx, y + 5), "Disability Benefit", font=fb_, fill=WHITE if on_dark else NAVY)
    w1 = d.textlength("Disability Benefit ", font=fb_)
    d.text((tx + w1, y + 5), "Advocate", font=fb_, fill=TEAL)


def footer_note(d, W, H, on_dark=True):
    fn = f(R, 18)
    txt = "Attorney Advertising · Not affiliated with the Social Security Administration"
    d.text(((W - d.textlength(txt, font=fn)) / 2, H - 50), txt,
           font=fn, fill=MUTED if on_dark else GREY)


def cta(d, W, H, text, bg=GO, size=33):
    """Anchored above the disclaimer, never flowed after the copy."""
    return pill(d, 84, H - 200, text, f(B, size), bg, WHITE, padx=34, pady=19)


def ticks(d, lines, x, y, font, fill, gap=56, dot=TEAL):
    for line in lines:
        d.ellipse([x, y + 6, x + 24, y + 30], fill=dot)
        d.line([x + 6, y + 18, x + 12, y + 24], fill=WHITE, width=4)
        d.line([x + 12, y + 24, x + 19, y + 12], fill=WHITE, width=4)
        d.text((x + 42, y), line, font=font, fill=fill)
        y += gap
    return y


# ------------------------------------------------------------------ A. denied
def ad_denied(path, W=1080, H=1080):
    img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img)
    gradient(d, W, H); d.rectangle([0, 0, W, 8], fill=TEAL); logo(d, 84, 78)

    y = 246
    pill(d, 84, y, "DISABILITY CLAIMS", f(B, 24), TEAL_D, WHITE)
    y += 92
    y = block(d, "Denied disability? That is not the end of it.",
              f(B, 66), 84, y, W - 168, WHITE, lh=1.17)
    y += 28
    y = block(d, "Most first applications are refused. Many are later approved on "
                 "appeal — and the rules are different once you are over 50.",
              f(R, 31), 84, y, W - 200, (196, 212, 228), lh=1.36)
    y += 34
    y = block(d, "A free phone review tells you where you stand. No cost, no obligation.",
              f(B, 31), 84, y, W - 200, WHITE, lh=1.34)
    cta(d, W, H, "Call now — free review  →")
    footer_note(d, W, H)
    img.save(path, quality=94); return path


# ------------------------------------------------------------------- B. 50+
def ad_over50(path, W=1080, H=1080):
    img = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 150], fill=NAVY); logo(d, 84, 49)
    d.rectangle([0, 150, W, 158], fill=TEAL)

    y = 232
    pill(d, 84, y, "IF YOU ARE 50 OR OVER", f(B, 24), (214, 238, 238), TEAL_D)
    y += 88
    y = block(d, "Over 50 and unable to work? The rules are on your side.",
              f(B, 62), 84, y, W - 168, NAVY, lh=1.16)
    y += 24
    y = block(d, "Social Security applies different standards once you reach 50, and "
                 "again at 55. Many people never find out that applies to them.",
              f(R, 29), 84, y, W - 190, GREY, lh=1.36)
    y += 28
    y = ticks(d, ["Worked 5 of the last 10 years",
                  "Off work 12 months, or expected to be",
                  "Not already receiving benefits"],
              88, y, f(B, 28), INK, gap=50)
    cta(d, W, H, "See if you qualify — free  →", bg=TEAL_D)
    footer_note(d, W, H, on_dark=False)
    img.save(path, quality=94); return path


# --------------------------------------------------------------- C. waiting
def ad_waiting(path, W=1080, H=1080):
    img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img)
    gradient(d, W, H); d.rectangle([0, 0, W, 8], fill=TEAL); logo(d, 84, 78)

    y = 240
    pill(d, 84, y, "STILL WAITING?", f(B, 24), TEAL_D, WHITE)
    y += 92
    y = block(d, "Applied months ago and heard nothing back?",
              f(B, 64), 84, y, W - 168, WHITE, lh=1.17)
    y += 30
    y = block(d, "You do not have to wait it out alone. A representative can take over "
                 "the paperwork, chase the decision and handle an appeal if it comes to "
                 "that.",
              f(R, 30), 84, y, W - 200, (196, 212, 228), lh=1.36)
    y += 32
    y = block(d, "Nothing to pay upfront — representatives are paid only if your claim "
                 "is approved.",
              f(B, 30), 84, y, W - 200, WHITE, lh=1.34)
    cta(d, W, H, "Talk to someone — free  →")
    footer_note(d, W, H)
    img.save(path, quality=94); return path


# --------------------------------------------------------- vertical of A
def ad_denied_v(path, W=1080, H=1350):
    img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img)
    gradient(d, W, H); d.rectangle([0, 0, W, 10], fill=TEAL); logo(d, 84, 96, mark=58)

    y = 330
    pill(d, 84, y, "DISABILITY CLAIMS", f(B, 26), TEAL_D, WHITE)
    y += 104
    y = block(d, "Denied disability? That is not the end of it.",
              f(B, 78), 84, y, W - 168, WHITE, lh=1.16)
    y += 38
    y = block(d, "Most first applications are refused. Many are later approved on "
                 "appeal — and the rules are different once you are over 50.",
              f(R, 34), 84, y, W - 190, (196, 212, 228), lh=1.36)
    y += 44
    y = block(d, "A free phone review tells you where you stand. No cost, no obligation.",
              f(B, 34), 84, y, W - 190, WHITE, lh=1.34)
    cta(d, W, H, "Call now — free review  →", size=35)
    footer_note(d, W, H)
    img.save(path, quality=94); return path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for fn, name in [(ad_denied,   "ssdi_a_denied.jpg"),
                     (ad_over50,   "ssdi_b_over50.jpg"),
                     (ad_waiting,  "ssdi_c_waiting.jpg"),
                     (ad_denied_v, "ssdi_a_vertical.jpg")]:
        p = fn(os.path.join(here, name))
        print("wrote", os.path.basename(p), Image.open(p).size)
