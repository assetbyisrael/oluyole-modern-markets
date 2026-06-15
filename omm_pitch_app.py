from flask import Flask, request, send_file, render_template_string
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io, os

app = Flask(__name__)

# Brand Colors from OMM Product Paper
NAVY = colors.HexColor("#0A1628")
BLUE = colors.HexColor("#1B3A6B")
MID_BLUE= colors.HexColor("#2856A3")
RED = colors.HexColor("#8B1A1A")
CREAM = colors.HexColor("#FAF6F0")
WHITE = colors.Color(1, 1, 1)
GOLD = colors.HexColor("#C8A84B")
LIGHT_BLUE = colors.HexColor("#E8EEF8")
DARK_RED= colors.HexColor("#6B0F0F")

W, H = A4

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OMM Pitch Generator | Oluyole Modern Market</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
font-family: 'Segoe UI', Arial, sans-serif;
background: #0A1628;
color: #FAF6F0;
min-height: 100vh;
}
.hero {
background: linear-gradient(135deg, #0A1628 0%, #1B3A6B 60%, #0A1628 100%);
padding: 48px 32px 36px;
text-align: center;
border-bottom: 3px solid #C8A84B;
}
.hero-badge {
display: inline-block;
background: #8B1A1A;
color: #FAF6F0;
font-size: 11px;
font-weight: 700;
letter-spacing: 2px;
text-transform: uppercase;
padding: 6px 18px;
border-radius: 2px;
margin-bottom: 18px;
}
.hero h1 {
font-family: Georgia, serif;
font-size: 2.6rem;
font-weight: 700;
color: #FAF6F0;
line-height: 1.15;
margin-bottom: 10px;
}
.hero h1 span { color: #C8A84B; }
.hero p {
font-size: 1rem;
color: #B0C4DE;
max-width: 560px;
margin: 0 auto;
line-height: 1.6;
}
.stats-bar {
display: flex;
justify-content: center;
gap: 0;
background: #C8A84B;
padding: 0;
}
.stat {
flex: 1;
text-align: center;
padding: 14px 10px;
border-right: 1px solid rgba(10,22,40,0.25);
color: #0A1628;
}
.stat:last-child { border-right: none; }
.stat-num { font-size: 1.4rem; font-weight: 800; display: block; }
.stat-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; opacity: 0.8; }
.form-wrap {
max-width: 720px;
margin: 40px auto;
background: #112040;
border-radius: 8px;
padding: 40px 44px;
box-shadow: 0 8px 40px rgba(0,0,0,0.5);
border: 1px solid rgba(200,168,75,0.2);
}
.form-wrap h2 {
font-family: Georgia, serif;
font-size: 1.5rem;
color: #C8A84B;
margin-bottom: 8px;
}
.form-wrap p { color: #8BA4C8; font-size: 0.9rem; margin-bottom: 28px; line-height: 1.5; }
.field-group {
display: grid;
grid-template-columns: 1fr 1fr;
gap: 16px;
}
.field-group.single { grid-template-columns: 1fr; }
.field { display: flex; flex-direction: column; margin-bottom: 18px; }
.field label { font-size: 0.78rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #8BA4C8; margin-bottom: 7px; }
.field input, .field select {
background: #0A1628;
border: 1px solid rgba(200,168,75,0.3);
border-radius: 4px;
color: #FAF6F0;
font-size: 0.95rem;
padding: 11px 14px;
outline: none;
transition: border 0.2s;
}
.field input:focus, .field select:focus { border-color: #C8A84B; }
.field select option { background: #0A1628; }
.divider {
border: none;
border-top: 1px solid rgba(200,168,75,0.15);
margin: 28px 0 20px;
}
.section-label {
font-size: 0.7rem;
letter-spacing: 2px;
text-transform: uppercase;
color: #C8A84B;
font-weight: 700;
margin-bottom: 16px;
}
.submit-btn {
display: block;
width: 100%;
background: #8B1A1A;
color: #FAF6F0;
font-size: 1rem;
font-weight: 700;
letter-spacing: 1.5px;
text-transform: uppercase;
padding: 16px;
border: none;
border-radius: 4px;
cursor: pointer;
margin-top: 28px;
transition: background 0.2s;
}
.submit-btn:hover { background: #6B0F0F; }
.footer { text-align: center; padding: 28px; color: #3A5278; font-size: 0.8rem; }
@media (max-width: 580px) {
.field-group { grid-template-columns: 1fr; }
.form-wrap { padding: 28px 18px; }
.hero h1 { font-size: 1.8rem; }
.stats-bar { flex-wrap: wrap; }
.stat { min-width: 50%; }
}
</style>
</head>
<body>
<div class="hero">
<span class="hero-badge">Land Republic x Oluyole LGA</span>
<h1>Oluyole Modern Market<br><span>Pitch Generator</span></h1>
<p>Generate a fully personalized, print-ready investment pitch PDF for any prospect, tailored to their profile, goals, and the exact shop category they need.</p>
</div>
<div class="stats-bar">
<div class="stat"><span class="stat-num">4</span><span class="stat-label">Roads Converge</span></div>
<div class="stat"><span class="stat-num">50k+</span><span class="stat-label">Daily Footfall</span></div>
<div class="stat"><span class="stat-num">400%</span><span class="stat-label">Projected ROI</span></div>
<div class="stat"><span class="stat-num">25yr</span><span class="stat-label">Max Lease</span></div>
<div class="stat"><span class="stat-num">3,000+</span><span class="stat-label">Traders Displaced</span></div>
</div>
<form class="form-wrap" method="POST" action="/generate">
<h2>Prospect Information</h2>
<p>Fill in the prospect's details and goals. The generator will build a personalized PDF pitch document around them.</p>
<p class="section-label">Prospect Details</p>
<div class="field-group">
<div class="field">
<label>Title</label>
<select name="title">
<option>Mr.</option>
<option>Mrs.</option>
<option>Miss</option>
<option>Dr.</option>
<option>Prof.</option>
<option>Engr.</option>
<option>Chief</option>
<option>Alhaji</option>
<option>Alhaja</option>
<option>Barrister</option>
</select>
</div>
<div class="field">
<label>First Name</label>
<input type="text" name="first_name" placeholder="e.g. Chukwuemeka" required>
</div>
</div>
<div class="field-group">
<div class="field">
<label>What They Do</label>
<input type="text" name="occupation" placeholder="e.g. Business Owner, Civil Servant" required>
</div>
<div class="field">
<label>Profile Type</label>
<select name="profile">
<option value="nigeria">Nigeria-Based</option>
<option value="diaspora">Diaspora Investor</option>
</select>
</div>
</div>
<div class="field-group single">
<div class="field">
<label>Primary Investment Goal</label>
<select name="goal">
<option value="invest">Invest in Commercial Property</option>
<option value="rental">Earn Rental Income</option>
<option value="business">Secure a Business Space</option>
<option value="diversify">Diversify Investment Portfolio</option>
<option value="diaspora">Diaspora Investment Back Home</option>
</select>
</div>
</div>
<div class="field-group single">
<div class="field">
<label>Recommended Shop Category</label>
<select name="category">
<option value="all">Show All Categories</option>
<option value="standard">Standard Unit</option>
<option value="classic">Classic Unit</option>
<option value="executive">Executive Unit</option>
</select>
</div>
</div>

<hr class="divider">
<p class="section-label">Agent Information</p>
<div class="field-group">
<div class="field">
<label>Agent Name</label>
<input type="text" name="agent_name" placeholder="Your full name" required>
</div>
<div class="field">
<label>Agent Phone</label>
<input type="text" name="agent_phone" placeholder="+234 xxx xxx xxxx" required>
</div>
</div>
<div class="field-group">
<div class="field">
<label>Agent Email</label>
<input type="email" name="agent_email" placeholder="you@example.com">
</div>
<div class="field">
<label>Property URL (optional)</label>
<input type="text" name="property_url" placeholder="landrepublic.co/...">
</div>
</div>

<button type="submit" class="submit-btn">Generate Pitch PDF</button>
</form>
<div class="footer">Oluyole Modern Market &mdash; Developed by Land Republic in partnership with Oyo State Government through Oluyole Local Government</div>
</body>
</html>
"""

def build_styles():
    return {
        "hero_title": ParagraphStyle("hero_title", fontName="Times-Bold",
            fontSize=26, textColor=WHITE, leading=32, alignment=TA_CENTER,
            spaceAfter=6),
        "hero_sub": ParagraphStyle("hero_sub", fontName="Times-Italic",
            fontSize=12, textColor=colors.HexColor("#C8D8F0"), leading=17,
            alignment=TA_CENTER, spaceAfter=4),
        "hero_badge": ParagraphStyle("hero_badge", fontName="Helvetica-Bold",
            fontSize=8, textColor=GOLD, leading=12, alignment=TA_CENTER,
            spaceAfter=10),
        "section_label": ParagraphStyle("section_label", fontName="Helvetica-Bold",
            fontSize=8, textColor=GOLD, leading=12, alignment=TA_LEFT,
            spaceBefore=14, spaceAfter=6),
        "section_title": ParagraphStyle("section_title", fontName="Times-Bold",
            fontSize=16, textColor=NAVY, leading=20, alignment=TA_LEFT,
            spaceBefore=6, spaceAfter=8),
        "body": ParagraphStyle("body", fontName="Helvetica",
            fontSize=9.5, textColor=colors.HexColor("#2C2C2C"), leading=15,
            alignment=TA_JUSTIFY, spaceAfter=8),
        "body_white": ParagraphStyle("body_white", fontName="Helvetica",
            fontSize=9.5, textColor=WHITE, leading=15, alignment=TA_JUSTIFY, spaceAfter=6),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica",
            fontSize=9.5, textColor=colors.HexColor("#2C2C2C"), leading=14,
            leftIndent=12, spaceAfter=4),
        "bullet_white": ParagraphStyle("bullet_white", fontName="Helvetica",
            fontSize=9.5, textColor=WHITE, leading=14, leftIndent=12, spaceAfter=4),
        "cta_main": ParagraphStyle("cta_main", fontName="Times-Bold",
            fontSize=18, textColor=GOLD, leading=24, alignment=TA_CENTER,
            spaceAfter=6),
        "cta_sub": ParagraphStyle("cta_sub", fontName="Helvetica",
            fontSize=9.5, textColor=WHITE, leading=14, alignment=TA_CENTER,
            spaceAfter=4),
        "small_label": ParagraphStyle("small_label", fontName="Helvetica-Bold",
            fontSize=7.5, textColor=GOLD, leading=11, alignment=TA_CENTER),
        "table_head": ParagraphStyle("table_head", fontName="Helvetica-Bold",
            fontSize=8.5, textColor=WHITE, leading=12, alignment=TA_CENTER),
        "table_cell": ParagraphStyle("table_cell", fontName="Helvetica",
            fontSize=8.5, textColor=NAVY, leading=12, alignment=TA_CENTER),
        "table_cell_bold": ParagraphStyle("table_cell_bold", fontName="Helvetica-Bold",
            fontSize=8.5, textColor=NAVY, leading=12, alignment=TA_LEFT),
        "footnote": ParagraphStyle("footnote", fontName="Helvetica-Oblique",
            fontSize=7.5, textColor=colors.HexColor("#888888"), leading=11,
            alignment=TA_CENTER),
    }

GOAL_PARAGRAPHS = {
    "invest": (
        "As someone who invests with intent, you already know that timing in commercial real estate is not a suggestion, "
        "it is a competitive advantage. Oluyole Modern Market sits at the convergence of four of Ibadan's highest-traffic "
        "corridors, where tens of thousands of people and naira circulate daily without interruption. This is not a "
        "speculative play on an emerging location. New Garage is already established, already loud with commerce, and "
        "already congested with informal traders who need structured space, which means the demand for these units existed "
        "before the first block was laid. What is being offered here is the rare opportunity to lock in at pre-delivery "
        "pricing, in a government-backed project with a 25-year lease, full title security, and a minimum 400% ROI "
        "projection over the lease duration. Investors who understand the Nigerian commercial real estate cycle know that "
        "the best entry point is always before the ribbon-cutting, and that point is now."
    ),
    "rental": (
        "The most reliable form of income is the kind that does not depend on you showing up every morning. A shop unit "
        "at Oluyole Modern Market is a rental income engine positioned inside one of Ibadan's most active trade corridors, "
        "where foot traffic is not driven by marketing campaigns but by geographic inevitability. Four major roads feed "
        "into this location daily, 50,000 commuters and vendors pass through within a 5km radius, and over 3,000 informal "
        "traders are currently being displaced from unstructured market setups, actively searching for legible, secure "
        "commercial space to relocate into. What that means for you as a rental income investor is a ready tenant pool "
        "before your shop is even allocated. Rental yields in this corridor start from N500,000 to N1.2 million per year "
        "per unit, with projected rent reviews every two years, and Land Republic offers an optional professional "
        "management model so the income flows without the stress of landlord logistics."
    ),
    "business": (
        "If you have been running your business from a rented space that is never quite right, never quite yours, then "
        "this is the upgrade worth making. A shop at Oluyole Modern Market gives you a purpose-built, secured commercial "
        "space at one of Ibadan's most visible trade intersections, with your own government-issued lease agreement and "
        "a 20 to 25-year tenure that lets you build your brand into a location without the anxiety of arbitrary rent "
        "increases or landlord disputes. The market is designed for real business, not makeshift commerce: paved roads, "
        "electricity, water, fire safety, on-site security, and an admin office are all part of the infrastructure. And "
        "because you are entering at the pre-delivery phase, your entry cost is significantly lower than it will be once "
        "the market opens and surrounding commercial rents begin to reflect the upgraded infrastructure."
    ),
    "diversify": (
        "A well-structured portfolio does not concentrate all its weight in one asset class, and commercial real estate "
        "in a high-demand corridor like Oluyole offers something that equity markets and residential properties rarely "
        "do simultaneously: predictable cash flow, physical asset ownership, and capital appreciation tied to government "
        "infrastructure investment. The Oluyole corridor hosts nearly 50% of all industries in Oyo State, with multinationals "
        "like Pepsi, P&G, British American Tobacco, and 7Up operating within the same industrial ecosystem that feeds "
        "foot traffic to this market daily. Owning a unit here is not just a property purchase, it is an equity position "
        "in one of Ibadan's most structurally embedded commercial zones, backed by a public-private partnership that "
        "insulates the investment from the political instability risks that often concern portfolio-conscious investors."
    ),
    "diaspora": (
        "Owning a productive asset back home should not feel like gambling from a distance. Oluyole Modern Market is "
        "one of the few commercial real estate opportunities in Nigeria that has been structured specifically with the "
        "concerns of the diaspora investor in mind: government-backed title through Oluyole Local Government, a "
        "professionally managed facility that operates without requiring your physical presence, transparent payment "
        "plans across 3 or 6 months, and a lease agreement that holds regardless of administrative changes in government. "
        "The asset generates rental income in naira, which in an inflationary environment like Nigeria's is itself a "
        "form of local currency hedge, and with optional professional management, you receive your returns without "
        "needing to navigate the Lagos to Ibadan expressway every quarter. This is the kind of home investment that "
        "makes sense from wherever you are in the world."
    ),
}

PROFILE_TAGS = {
    "nigeria": "Nigeria-Based Investor",
    "diaspora": "Diaspora Investor",
}

def make_hero(styles, title, first_name, occupation, goal_label):
    elems = []
    hero_text = [
        Paragraph("LAND REPUBLIC x OLUYOLE LOCAL GOVERNMENT, OYO STATE", styles["hero_badge"]),
        Spacer(1, 6),
        Paragraph(f"Prepared Exclusively for {title} {first_name}", styles["hero_title"]),
        Spacer(1, 6),
        Paragraph(
            f"A personalized investment brief for a {occupation} whose primary focus is to {goal_label.lower()}",
            styles["hero_sub"]
        ),
        Spacer(1, 12),
        Paragraph(
            "Oluyole Modern Market, New Garage Axis, Ibadan, Oyo State",
            ParagraphStyle("loc", fontName="Helvetica-Bold", fontSize=9,
                textColor=GOLD, alignment=TA_CENTER)
        ),
    ]
    tbl = Table([[hero_text]], colWidths=[W - 2*25*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING", (0,0), (-1,-1), 28),
        ("BOTTOMPADDING", (0,0), (-1,-1), 24),
        ("LEFTPADDING", (0,0), (-1,-1), 20),
        ("RIGHTPADDING", (0,0), (-1,-1), 20),
        ("LINEBELOW", (0,0), (-1,-1), 3, GOLD),
    ]))
    elems.append(tbl)
    return elems

def make_stats_bar(styles):
    stats = [
        ("4", "Roads Converge"),
        ("50,000+", "Daily Footfall"),
        ("400%+", "Projected ROI"),
        ("25 Years", "Max Lease"),
        ("3,000+", "Displaced Traders"),
        ("18 Months", "Delivery"),
    ]
    row = []
    for num, label in stats:
        cell_content = [
            Paragraph(num, ParagraphStyle("sn", fontName="Helvetica-Bold",
                fontSize=13, textColor=NAVY, alignment=TA_CENTER, leading=16)),
            Paragraph(label, ParagraphStyle("sl", fontName="Helvetica",
                fontSize=7, textColor=NAVY, alignment=TA_CENTER, leading=10)),
        ]
        row.append(cell_content)
    col_w = (W - 50*mm) / len(stats)
    tbl = Table([row], colWidths=[col_w]*len(stats))
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), GOLD),
        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("LINEAFTER", (0,0), (-2,-1), 0.5, colors.HexColor("#A08030")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    return [tbl]

def make_location_section(styles):
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph("LOCATION INTELLIGENCE", styles["section_label"]))
    elems.append(Paragraph("Why New Garage Is Not Just Another Address", styles["section_title"]))
    body = (
        "New Garage is one of those intersections in Ibadan that functions less like a location and more like a system, "
        "a place where four major arteries (Akala Expressway, Podo Road, Challenge, and the Lagos-Ibadan Expressway) "
        "converge and create a commercial vortex that has been active for decades before this market was conceived. "
        "The daily footfall here is not manufactured by marketing or driven by a single anchor tenant. It is the "
        "organic consequence of geography, of industrial density, and of the fact that Oluyole hosts nearly 50% of "
        "all industries in Oyo State, including multinationals like Pepsi, Procter & Gamble, British American Tobacco, "
        "and 7Up, whose thousands of workers, suppliers, and support vendors pass through this corridor every single day."
    )
    elems.append(Paragraph(body, styles["body"]))
    body2 = (
        "What makes this particularly compelling for a commercial investor is that infrastructure is already following "
        "the commercial gravity: the Akala road dualization is underway, the New Garage terminal is in proximity, and "
        "the government has formalized the market upgrade through a public-private partnership with Land Republic, "
        "meaning the structural conditions that drive long-term commercial real estate value appreciation are already "
        "in motion. You are not betting on a location becoming relevant. You are arriving at one that already is, "
        "and locking in before the prices reflect that reality."
    )
    elems.append(Paragraph(body2, styles["body"]))
    loc_data = [
        ["Location", "New Garage Axis, Oluyole LGA, Ibadan, Oyo State"],
        ["Road Access", "Akala Expressway, Podo Road, Challenge, Lagos-Ibadan Expressway"],
        ["Industrial Proximity", "Adjacent to Oluyole Industrial Estate (largest in Ibadan)"],
        ["Footfall Radius", "50,000+ commuters and vendors within 5km daily"],
        ["Government Backing", "Partnership with Oluyole Local Government, Oyo State"],
        ["Infrastructure", "Akala dualization underway, New Garage terminal nearby"],
    ]
    tbl = Table(loc_data, colWidths=[50*mm, W - 50*mm - 50*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), LIGHT_BLUE),
        ("BACKGROUND", (1,0), (1,-1), WHITE),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [CREAM, WHITE]),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("TEXTCOLOR", (0,0), (0,-1), BLUE),
        ("TEXTCOLOR", (1,0), (1,-1), NAVY),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("LINEBELOW", (0,0), (-1,-2), 0.5, colors.HexColor("#D0D8E8")),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#B0C0D8")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    elems.append(tbl)
    return elems

def make_commercial_context(styles):
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph("THE COMMERCIAL REAL ESTATE CASE", styles["section_label"]))
    elems.append(Paragraph("Income-Generating Assets in High-Density Corridors", styles["section_title"]))
    body = (
        "Commercial real estate in a proven trade corridor behaves differently from residential property. "
        "It does not depend on sentiment, it does not stall because of interest rate anxiety, and it does not "
        "sit idle while the owner waits for appreciation. It generates income from the first day a tenant occupies "
        "it, and in a location like New Garage, finding that tenant is not a challenge because the demand for "
        "structured commercial space in this corridor is already in excess of supply. Over 3,000 informal traders "
        "are currently operating without secure, formal shop spaces in this axis and actively seeking to transition "
        "into structured environments. That is not a projection. That is an existing, documented demand pool."
    )
    elems.append(Paragraph(body, styles["body"]))
    body2 = (
        "When you own a unit at Oluyole Modern Market, you are not managing a property, you are managing a "
        "cashflow position. The shop itself sits on government-allocated land with a 20 to 25-year lease, "
        "your rental income starts from N500,000 to N1.2 million per unit annually with projected reviews every "
        "two years, and your capital recovery is modeled at 8 years or less, leaving the remaining 12 to 17 years "
        "of the lease as net-positive yield. The minimum 400% ROI projection over the full lease period is not a "
        "sales line. It is a function of the location's commercial density, the government's infrastructural "
        "commitment, and the structural undersupply of formal retail space in Ibadan's most industrially active zone."
    )
    elems.append(Paragraph(body2, styles["body"]))
    return elems

def make_size_illustration(styles):
    elems = []
    elems.append(Spacer(1, 10))
    elems.append(Paragraph("SHOP SIZE REFERENCE", styles["section_label"]))
    elems.append(Paragraph("Understanding What Your Space Looks Like", styles["section_title"]))
    size_data = [
        [
            Paragraph("STANDARD UNIT", styles["table_head"]),
            Paragraph("CLASSIC UNIT", styles["table_head"]),
            Paragraph("EXECUTIVE UNIT", styles["table_head"]),
        ],
        [
            Paragraph("10ft x 10.5ft\n(3m x 3.2m)", ParagraphStyle("sz", fontName="Helvetica-Bold",
                fontSize=11, textColor=BLUE, alignment=TA_CENTER, leading=16)),
            Paragraph("12ft x 13ft\n(3.5m x 3.8m)", ParagraphStyle("sz", fontName="Helvetica-Bold",
                fontSize=11, textColor=RED, alignment=TA_CENTER, leading=16)),
            Paragraph("~Extended\nPremium Space", ParagraphStyle("sz", fontName="Helvetica-Bold",
                fontSize=11, textColor=NAVY, alignment=TA_CENTER, leading=16)),
        ],
        [
            Paragraph("Ideal for: boutique, phone accessories, provisions, pharmacy kiosk, financial services agent",
                ParagraphStyle("sz2", fontName="Helvetica", fontSize=7.5,
                    textColor=colors.HexColor("#444444"), alignment=TA_CENTER, leading=11)),
            Paragraph("Ideal for: clothing, electronics, hardware, foodstuff, beauty supply, professional office",
                ParagraphStyle("sz2", fontName="Helvetica", fontSize=7.5,
                    textColor=colors.HexColor("#444444"), alignment=TA_CENTER, leading=11)),
            Paragraph("Ideal for: supermarket, showroom, stockroom-enabled trade, corporate anchor tenant",
                ParagraphStyle("sz2", fontName="Helvetica", fontSize=7.5,
                    textColor=colors.HexColor("#444444"), alignment=TA_CENTER, leading=11)),
        ],
        [
            Paragraph("Lease: 20 years", styles["small_label"]),
            Paragraph("Lease: 25 years", styles["small_label"]),
            Paragraph("Lease: 25 years", styles["small_label"]),
        ],
    ]
    cw = (W - 50*mm) / 3
    tbl = Table(size_data, colWidths=[cw, cw, cw])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), BLUE),
        ("BACKGROUND", (1,0), (1,0), RED),
        ("BACKGROUND", (2,0), (2,0), NAVY),
        ("BACKGROUND", (0,1), (0,1), LIGHT_BLUE),
        ("BACKGROUND", (1,1), (1,1), colors.HexColor("#FDECEA")),
        ("BACKGROUND", (2,1), (2,1), colors.HexColor("#E8EEF8")),
        ("BACKGROUND", (0,2), (-1,2), CREAM),
        ("BACKGROUND", (0,3), (-1,3), colors.HexColor("#E8EEF8")),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("LINEAFTER", (0,0), (-2,-1), 0.5, colors.HexColor("#C0C8D8")),
        ("LINEBELOW", (0,0), (-1,-2), 0.5, colors.HexColor("#C0C8D8")),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#8899BB")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    elems.append(tbl)
    elems.append(Spacer(1, 4))
    elems.append(Paragraph(
        "Note: Executive unit dimensions are premium-tier and confirmed upon allocation. All sizes are as per the official product paper.",
        styles["footnote"]
    ))
    return elems

def make_pricing_table(styles, category):
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph("SHOP CATEGORIES AND PRICING", styles["section_label"]))
    elems.append(Paragraph("Your Investment Entry Points", styles["section_title"]))
    all_cats = {
        "standard": {
            "name": "Standard", "upstairs": "N6,450,000", "downstairs": "N7,525,000",
            "deposit": "N1,000,000", "lease": "20 Years", "size": "10ft x 10.5ft (3m x 3.2m)",
        },
        "classic": {
            "name": "Classic", "upstairs": "N8,600,000", "downstairs": "N9,675,000",
            "deposit": "N2,000,000", "lease": "25 Years", "size": "12ft x 13ft (3.5m x 3.8m)",
        },
        "executive": {
            "name": "Executive", "upstairs": "N16,125,000", "downstairs": "N17,200,000",
            "deposit": "N2,000,000", "lease": "25 Years", "size": "Extended Premium",
        },
    }
    if category == "all":
        show = ["standard", "classic", "executive"]
    else:
        show = [category]
    headers = ["Category", "Upstairs", "Downstairs", "Deposit", "Lease", "Size"]
    header_row = [Paragraph(h, styles["table_head"]) for h in headers]
    rows = [header_row]
    for cat in show:
        d = all_cats[cat]
        rows.append([
            Paragraph(d["name"], ParagraphStyle("cn", fontName="Helvetica-Bold",
                fontSize=9, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(d["upstairs"], ParagraphStyle("cv", fontName="Helvetica-Bold",
                fontSize=9, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph(d["downstairs"], ParagraphStyle("cv", fontName="Helvetica-Bold",
                fontSize=9, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph(d["deposit"], ParagraphStyle("cv", fontName="Helvetica",
                fontSize=8.5, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(d["lease"], ParagraphStyle("cv", fontName="Helvetica",
                fontSize=8.5, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(d["size"], ParagraphStyle("cv", fontName="Helvetica",
                fontSize=7.5, textColor=colors.HexColor("#B0C4DE"), alignment=TA_CENTER)),
        ])
    cw_total = W - 50*mm
    col_ws = [cw_total*0.14, cw_total*0.18, cw_total*0.18, cw_total*0.16, cw_total*0.13, cw_total*0.21]
    tbl = Table(rows, colWidths=col_ws)
    style_cmds = [
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("LINEBELOW", (0,0), (-1,-2), 0.5, colors.HexColor("#3A5080")),
        ("BOX", (0,0), (-1,-1), 1, BLUE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        bg = BLUE if i % 2 == 1 else MID_BLUE
        style_cmds.append(("BACKGROUND", (0,i), (-1,i), bg))
    tbl.setStyle(TableStyle(style_cmds))
    elems.append(tbl)
    elems.append(Spacer(1, 6))
    notes_data = [
        [
            Paragraph("Payment Plan", ParagraphStyle("nl", fontName="Helvetica-Bold",
                fontSize=8, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph("Title", ParagraphStyle("nl", fontName="Helvetica-Bold",
                fontSize=8, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph("Lease Countdown", ParagraphStyle("nl", fontName="Helvetica-Bold",
                fontSize=8, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph("Bank Account", ParagraphStyle("nl", fontName="Helvetica-Bold",
                fontSize=8, textColor=GOLD, alignment=TA_CENTER)),
        ],
        [
            Paragraph("3 or 6 months, interest-free", ParagraphStyle("nv", fontName="Helvetica",
                fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph("Government Allocation (Oluyole LGA)", ParagraphStyle("nv", fontName="Helvetica",
                fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph("Starts after project delivery", ParagraphStyle("nv", fontName="Helvetica",
                fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph("LAND REPUBLIC-OLUYOLE MARKET\nProvidus Bank: 1307642762", ParagraphStyle("nv",
                fontName="Helvetica", fontSize=7.5, textColor=WHITE, alignment=TA_CENTER, leading=11)),
        ],
    ]
    cw2 = cw_total / 4
    tbl2 = Table(notes_data, colWidths=[cw2]*4)
    tbl2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#0D2040")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LINEAFTER", (0,0), (-2,-1), 0.5, colors.HexColor("#2A4070")),
        ("LINEBELOW", (0,0), (-1,0), 0.5, GOLD),
        ("BOX", (0,0), (-1,-1), 1, BLUE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    elems.append(tbl2)
    return elems

def make_why_it_works(styles):
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph("THE INVESTMENT CASE", styles["section_label"]))
    elems.append(Paragraph("Four Reasons This Works", styles["section_title"]))
    reasons = [
        ("01", "Structural Demand, Not Manufactured Interest",
         "3,000+ informal traders are actively being displaced from unstructured setups in this corridor, "
         "creating a captive tenant pool that was formed by market forces, not marketing."),
        ("02", "Government-Backed Title Security",
         "A public-private partnership with Oluyole Local Government means your lease is protected "
         "by institutional authority, not an individual's goodwill, regardless of any future administrative changes."),
        ("03", "8-Year Capital Recovery on a 25-Year Asset",
         "Your purchase price is recovered in 8 years or less through rental income, leaving up to 17 years "
         "of net yield from a fully paid-for asset, which is the mathematics of compounding commercial real estate."),
        ("04", "Infrastructure Appreciation Already in Motion",
         "Akala road dualization is underway, the New Garage terminal is nearby, and the market upgrade is "
         "formalized. These are not future promises. They are present conditions accelerating value."),
    ]
    for num, title, desc in reasons:
        row = [
            [Paragraph(num, ParagraphStyle("rn", fontName="Times-Bold", fontSize=22,
                textColor=GOLD, alignment=TA_CENTER, leading=28))],
            [
                Paragraph(title, ParagraphStyle("rt", fontName="Helvetica-Bold", fontSize=9.5,
                    textColor=NAVY, leading=13, spaceAfter=4)),
                Paragraph(desc, ParagraphStyle("rd", fontName="Helvetica", fontSize=8.5,
                    textColor=colors.HexColor("#333333"), leading=13)),
            ]
        ]
        tbl = Table([row[0:1] + [row[1]]], colWidths=[18*mm, W - 50*mm - 18*mm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,0), LIGHT_BLUE),
            ("BACKGROUND", (1,0), (1,0), CREAM),
            ("TOPPADDING", (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("LEFTPADDING", (0,0), (0,0), 4),
            ("LEFTPADDING", (1,0), (1,0), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("LINEBELOW", (0,0), (-1,-1), 0.5, colors.HexColor("#C8D4E8")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 3))
    return elems

def make_comparison_table(styles):
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph("MARKET COMPARISON", styles["section_label"]))
    elems.append(Paragraph("How OMM Compares to Typical Investment Options", styles["section_title"]))
    headers = ["Factor", "OMM Shop Unit", "Residential Land", "Stock Market"]
    rows = [
        headers,
        ["Title Security", "Gov. Allocation (LGA)", "Varies (C of O / Gazette)", "N/A"],
        ["Income Frequency", "Monthly rental flow", "Capital gain only", "Dividends (irregular)"],
        ["Inflation Hedge", "Rent reviews every 2yrs", "Partial", "Low in naira terms"],
        ["Entry Risk", "Low (gov. backed)", "Medium (title risk)", "Medium to High"],
        ["Hands-Free Option", "Yes (managed model)", "No", "Broker-dependent"],
        ["Projected ROI", "400%+ over lease", "Varies widely", "Varies by stock"],
        ["Liquidity", "Resalable (lease transfer)", "Illiquid short-term", "Liquid"],
    ]
    col_ws = [(W - 50*mm)*0.28, (W - 50*mm)*0.28, (W - 50*mm)*0.24, (W - 50*mm)*0.20]
    tbl = Table(rows, colWidths=col_ws)
    style_cmds = [
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0,1), (0,-1), NAVY),
        ("TEXTCOLOR", (1,1), (1,-1), BLUE),
        ("TEXTCOLOR", (2,1), (-1,-1), colors.HexColor("#555555")),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("LINEBELOW", (0,0), (-1,-2), 0.5, colors.HexColor("#D0D8E8")),
        ("BOX", (0,0), (-1,-1), 1, BLUE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0,i), (-1,i), CREAM))
        else:
            style_cmds.append(("BACKGROUND", (0,i), (-1,i), WHITE))
            style_cmds.append(("BACKGROUND", (1,i), (1,i), colors.HexColor("#EEF4FF")))
    tbl.setStyle(TableStyle(style_cmds))
    elems.append(tbl)
    return elems

def make_cta(styles, agent_name, agent_phone, agent_email, property_url, title, first_name):
    elems = []
    elems.append(Spacer(1, 16))
    inner = [
        Paragraph("NEXT STEP", ParagraphStyle("ct0", fontName="Helvetica-Bold",
            fontSize=8, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6)),
        Paragraph(f"Your unit at Oluyole Modern Market is waiting, {title} {first_name}.",
            styles["cta_main"]),
        Spacer(1, 6),
        Paragraph(
            "Units are allocated on a first-come, first-served basis, and with infrastructure upgrades already "
            "underway in this corridor, the pricing advantage available at the pre-delivery stage is time-bound. "
            "Reach your agent directly to confirm your preferred category, arrange a site inspection, and secure "
            "your position before availability narrows.",
            ParagraphStyle("ctab", fontName="Helvetica", fontSize=9, textColor=WHITE,
                alignment=TA_CENTER, leading=14, spaceAfter=12)
        ),
        Spacer(1, 8),
    ]
    contact_info = [[
        Paragraph(f"Agent: {agent_name}", ParagraphStyle("ci", fontName="Helvetica-Bold",
            fontSize=9.5, textColor=GOLD, alignment=TA_CENTER)),
        Paragraph(f"Phone: {agent_phone}", ParagraphStyle("ci", fontName="Helvetica-Bold",
            fontSize=9.5, textColor=GOLD, alignment=TA_CENTER)),
    ]]
    if agent_email:
        contact_info[0].append(
            Paragraph(f"Email: {agent_email}", ParagraphStyle("ci", fontName="Helvetica",
                fontSize=9, textColor=WHITE, alignment=TA_CENTER))
        )
    contact_row = contact_info[0]
    cw = (W - 50*mm) / len(contact_row)
    ctbl = Table([contact_row], colWidths=[cw]*len(contact_row))
    ctbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#0A1628")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LINEAFTER", (0,0), (-2,-1), 0.5, colors.HexColor("#3A5278")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    inner.append(ctbl)
    if property_url:
        inner.append(Spacer(1, 8))
        inner.append(Paragraph(f"www.{property_url.replace('https://','').replace('http://','').rstrip('/')}",
            ParagraphStyle("url", fontName="Helvetica-Oblique", fontSize=8.5,
                textColor=colors.HexColor("#8BA4C8"), alignment=TA_CENTER)))
    inner.append(Spacer(1, 8))
    inner.append(Paragraph(
        "Account Name: LAND REPUBLIC-OLUYOLE MARKET | Providus Bank | 1307642762",
        ParagraphStyle("acct", fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#B0C4DE"),
            alignment=TA_CENTER)
    ))
    tbl = Table([[inner]], colWidths=[W - 50*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BLUE),
        ("TOPPADDING", (0,0), (-1,-1), 20),
        ("BOTTOMPADDING", (0,0), (-1,-1), 20),
        ("LEFTPADDING", (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
        ("LINEABOVE", (0,0), (-1,0), 3, GOLD),
    ]))
    elems.append(tbl)
    return elems

def build_pdf(form):
    title = form.get("title", "Mr.")
    first_name = form.get("first_name", "Valued Investor")
    occupation = form.get("occupation", "Professional")
    goal = form.get("goal", "invest")
    profile = form.get("profile", "nigeria")
    category = form.get("category", "all")
    agent_name = form.get("agent_name", "Your Agent")
    agent_phone = form.get("agent_phone", "+234 000 000 0000")
    agent_email = form.get("agent_email", "")
    property_url = form.get("property_url", "landrepublic.co/properties/oluyole-modern-market")
    goal_labels = {
        "invest": "Invest in Commercial Property",
        "rental": "Earn Rental Income",
        "business": "Secure a Business Space",
        "diversify": "Diversify Investment Portfolio",
        "diaspora": "Diaspora Investment Back Home",
    }
    goal_label = goal_labels.get(goal, "Invest")
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm,
        topMargin=18*mm, bottomMargin=18*mm,
        title=f"OMM Pitch - {title} {first_name}")
    styles = build_styles()
    story = []
    story += make_hero(styles, title, first_name, occupation, goal_label)
    story += make_stats_bar(styles)
    story.append(Spacer(1, 16))
    story.append(Paragraph("YOUR INVESTMENT BRIEF", styles["section_label"]))
    profile_text = PROFILE_TAGS.get(profile, "Investor")
    story.append(Paragraph(
        f"Personalized for: {title} {first_name} ({occupation}) | Profile: {profile_text} | Goal: {goal_label}",
        ParagraphStyle("pid", fontName="Helvetica-Bold", fontSize=8.5,
            textColor=BLUE, leading=13, spaceAfter=8)
    ))
    story.append(Paragraph(GOAL_PARAGRAPHS.get(goal, GOAL_PARAGRAPHS["invest"]), styles["body"]))
    story += make_location_section(styles)
    story += make_commercial_context(styles)
    story += make_size_illustration(styles)
    story += make_pricing_table(styles, category)
    story += make_why_it_works(styles)
    story += make_comparison_table(styles)
    story += make_cta(styles, agent_name, agent_phone, agent_email, property_url, title, first_name)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GOLD))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "This document is a private investment brief prepared for the named prospect only. "
        "All figures are sourced directly from the official Oluyole Modern Market product paper by Land Republic. "
        "ROI projections are based on current market rent benchmarks and are subject to market conditions. "
        "This is not a financial advice document.",
        styles["footnote"]
    ))
    doc.build(story)
    buf.seek(0)
    return buf

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML)

@app.route("/generate", methods=["POST"])
def generate():
    form = request.form
    pdf_buf = build_pdf(form)
    first_name = form.get("first_name", "prospect").replace(" ", "_")
    filename = f"OMM_Pitch_{first_name}.pdf"
    return send_file(
        pdf_buf,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
