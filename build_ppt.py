"""Generate the PawPal+ demo deck following CodePath's "Engineer's Pitch" format:
Problem -> Logic -> Reliability -> Reflection. Simple, first-person, 6 slides."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---- Palette ------------------------------------------------------------------
NAVY = RGBColor(0x1A, 0x23, 0x32)      # titles / cover
TEAL = RGBColor(0x14, 0x8F, 0x93)      # accent 1
ORANGE = RGBColor(0xF2, 0x8C, 0x28)    # accent 2
LIGHT = RGBColor(0xF6, 0xF8, 0xF9)     # slide background
INK = RGBColor(0x2A, 0x33, 0x3B)       # body text
MUTE = RGBColor(0x5C, 0x6B, 0x73)      # secondary text
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def rect(slide, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
    sp = slide.shapes.add_shape(shape, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    sp.line.fill.background(); sp.shadow.inherit = False
    return sp


def text(slide, x, y, w, h, lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         gap=6, ls=1.05):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for i, (txt, size, color, bold) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(gap); p.line_spacing = ls
        r = p.add_run(); r.text = txt
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = "Calibri"
    return tb


def header(slide, step, title, accent):
    """One quiet header line: the pitch question, in first person."""
    rect(slide, Inches(0.7), Inches(0.7), Inches(0.14), Inches(0.85), accent)
    text(slide, Inches(1.0), Inches(0.62), Inches(11.4), Inches(0.4),
         [(step.upper(), 13, accent, True)], gap=2)
    text(slide, Inches(1.0), Inches(0.98), Inches(11.4), Inches(0.7),
         [(title, 32, NAVY, True)], gap=0)


def bullets(slide, items, y=Inches(2.2), size=19, gap=14, x=Inches(1.0),
            w=Inches(11.3)):
    tb = slide.shapes.add_textbox(x, y, w, Inches(4.5))
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.line_spacing = 1.1
        rb = p.add_run(); rb.text = "•  "
        rb.font.size = Pt(size); rb.font.bold = True; rb.font.color.rgb = ORANGE
        rt = p.add_run(); rt.text = it
        rt.font.size = Pt(size); rt.font.color.rgb = INK; rt.font.name = "Calibri"
    return tb


# ============================================================ 1 — TITLE
s = prs.slides.add_slide(BLANK); bg(s, NAVY)
rect(s, 0, SH - Inches(2.3), SW, Inches(0.12), TEAL)
rect(s, 0, SH - Inches(2.18), SW, Inches(0.06), ORANGE)
paw = rect(s, Inches(0.9), Inches(1.6), Inches(1.15), Inches(1.15), TEAL, MSO_SHAPE.OVAL)
pf = paw.text_frame; pf.paragraphs[0].alignment = PP_ALIGN.CENTER
pr = pf.paragraphs[0].add_run(); pr.text = "🐾"; pr.font.size = Pt(42)
text(s, Inches(0.9), Inches(3.1), Inches(11.5), Inches(1.3),
     [("PawPal+", 58, WHITE, True)], gap=0)
text(s, Inches(0.95), Inches(4.35), Inches(11.5), Inches(0.9),
     [("A pet-care planner that decides what matters first — and shows its work.",
       22, RGBColor(0xD6, 0xE2, 0xE5), False)], gap=0)
text(s, Inches(0.95), SH - Inches(1.9), Inches(11.5), Inches(0.5),
     [("My final project demo  ·  built by Giridhar", 15, TEAL, True)], gap=0)

# ============================================================ 2 — THE PROBLEM
s = prs.slides.add_slide(BLANK); bg(s, LIGHT)
header(s, "The Problem — what I solved", "Caring for a pet is a lot to track", ORANGE)
bullets(s, [
    "Owners juggle feeding, meds, walks, and grooming — every single day.",
    "The tasks that matter most for a pet's health are the easiest to forget.",
    "A plain to-do list doesn't tell you what to do first, or why.",
    "I wanted a planner that makes that call — and explains it.",
], y=Inches(2.3), size=20, gap=18)

# ============================================================ 3 — THE LOGIC
s = prs.slides.add_slide(BLANK); bg(s, LIGHT)
header(s, "The Logic — how the AI thinks", "It looks things up, then plans in steps", TEAL)
text(s, Inches(1.0), Inches(1.95), Inches(6.2), Inches(0.5),
     [("An agentic loop: retrieve → prioritize → plan → check → fix.", 15, MUTE, False)], gap=0)


def step_row(y, n, title, body):
    circ = rect(s, Inches(0.95), y, Inches(0.5), Inches(0.5), TEAL, MSO_SHAPE.OVAL)
    cf = circ.text_frame; cf.paragraphs[0].alignment = PP_ALIGN.CENTER
    cr = cf.paragraphs[0].add_run(); cr.text = n
    cr.font.size = Pt(17); cr.font.bold = True; cr.font.color.rgb = WHITE
    text(s, Inches(1.65), y - Inches(0.06), Inches(5.4), Inches(0.4),
         [(title, 16, NAVY, True)], gap=0)
    text(s, Inches(1.65), y + Inches(0.32), Inches(5.4), Inches(0.6),
         [(body, 12.5, MUTE, False)], gap=0, ls=1.05)


step_row(Inches(2.55), "1", "Look it up",
         "Pulls care guidance for each task from a small knowledge base.")
step_row(Inches(3.55), "2", "Prioritize",
         "Boosts safety-first tasks: meds › feeding › walks › grooming.")
step_row(Inches(4.55), "3", "Plan & check",
         "Builds the day, then scans for time clashes and overlaps.")
step_row(Inches(5.55), "4", "Fix & score",
         "Resolves conflicts and reports a 0–1 confidence score.")

# right column — the live app, in a soft frame
FRAME_X, FRAME_Y, FRAME_W = Inches(7.35), Inches(1.95), Inches(5.3)
img_w = FRAME_W - Inches(0.2)
img_h = Emu(int(img_w * 1248 / 1800))
rect(s, FRAME_X, FRAME_Y, FRAME_W, img_h + Inches(0.65), WHITE, MSO_SHAPE.ROUNDED_RECTANGLE)
text(s, FRAME_X + Inches(0.2), FRAME_Y + Inches(0.12), FRAME_W - Inches(0.4), Inches(0.35),
     [("THE LIVE APP", 11, TEAL, True)], gap=0)
s.shapes.add_picture("assets/app_screenshot.png",
                     FRAME_X + Inches(0.1), FRAME_Y + Inches(0.5), width=img_w, height=img_h)
text(s, Inches(1.0), Inches(6.55), Inches(6.2), Inches(0.6),
     [("Every step is logged to a trace — you can read why the plan came out this way.",
       12.5, INK, False)], gap=0, ls=1.05)

# ============================================================ 4 — RELIABILITY
s = prs.slides.add_slide(BLANK); bg(s, LIGHT)
header(s, "The Reliability — how I know it works", "Tested, and honest when it's unsure", ORANGE)


def stat(x, num, label, color):
    rect(s, x, Inches(2.2), Inches(2.7), Inches(1.75), color, MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x, Inches(2.42), Inches(2.7), Inches(0.9),
         [(num, 40, WHITE, True)], align=PP_ALIGN.CENTER, gap=0)
    text(s, x, Inches(3.4), Inches(2.7), Inches(0.5),
         [(label, 12.5, WHITE, False)], align=PP_ALIGN.CENTER, gap=0)


stat(Inches(0.7), "11/11", "automated tests pass", TEAL)
stat(Inches(3.55), "1.00", "confidence when the plan fits", ORANGE)
stat(Inches(6.4), "4", "cases I checked by hand", NAVY)
bullets(s, [
    "Tests cover the boosts, the scheduling, conflict detection, and skips.",
    "Guardrails: empty names and no-task runs are caught, not crashed.",
    "When a task can't fit the day, it's skipped and the confidence drops — no pretending.",
], y=Inches(4.3), size=17, gap=13)

# ============================================================ 5 — REFLECTION
s = prs.slides.add_slide(BLANK); bg(s, LIGHT)
header(s, "The Reflection — what surprised me", "Small ideas, surprisingly big payoff", TEAL)
bullets(s, [
    "A tiny knowledge base + simple boosts beat a plain scheduler — no big model needed.",
    "Just showing the reasoning trace made the tool feel far more trustworthy.",
    "The AI helped most with clean class design early on.",
    "It also steered me wrong once: it checked conflicts by exact start-time only, "
    "missing overlaps — I caught it and fixed it with proper slot checks.",
], y=Inches(2.3), size=19, gap=16)
text(s, Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.5),
     [("Biggest lesson: a system you can see into is easier to trust than one that's just \"smart.\"",
       15, MUTE, False)], gap=0)

# ============================================================ 6 — THANK YOU
s = prs.slides.add_slide(BLANK); bg(s, NAVY)
rect(s, 0, Inches(3.3), SW, Inches(0.12), TEAL)
rect(s, 0, Inches(3.42), SW, Inches(0.06), ORANGE)
text(s, 0, Inches(2.25), SW, Inches(1.1),
     [("Thanks — questions?  🐾", 46, WHITE, True)], align=PP_ALIGN.CENTER, gap=0)
text(s, 0, Inches(3.75), SW, Inches(0.6),
     [("Happy to walk through the code or the planner trace.", 20,
       RGBColor(0xD6, 0xE2, 0xE5), False)], align=PP_ALIGN.CENTER, gap=0)
text(s, 0, Inches(4.55), SW, Inches(0.5),
     [("github.com/Giridhar555/ai110-module2show-pawpal-starter", 14, TEAL, True)],
     align=PP_ALIGN.CENTER, gap=0)

prs.save("PawPal_Plus_Presentation.pptx")
print("Saved PawPal_Plus_Presentation.pptx with", len(prs.slides._sldIdLst), "slides")
