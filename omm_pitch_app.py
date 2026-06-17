"""
Oluyole Modern Market Pitch Generator - Corrected & Upgraded
Run: python3 omm_pitch_app.py
Then open: http://localhost:5001

Requirements: pip install flask reportlab
"""

from flask import Flask, request, send_file, render_template_string
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io

app = Flask(__name__)

# Brand Colors
NAVY     = colors.HexColor("#0A1628")
BLUE     = colors.HexColor("#1B3A6B")
MID_BLUE = colors.HexColor("#2856A3")
RED      = colors.HexColor("#8B1A1A")
CREAM    = colors.HexColor("#FAF6F0")
WHITE    = colors.Color(1, 1, 1)
GOLD     = colors.HexColor("#C8A84B")
LIGHT_BLUE = colors.HexColor("#E8EEF8")
DARK_RED = colors.HexColor("#6B0F0F")

W, H = A4


# ---- GOAL PARAGRAPHS (all re-written to match Israel's voice directives) ----
GOAL_PARAGRAPHS = {
    "invest": (
        "As someone who invests with intent, you already understand that timing in commercial real estate is not a suggestion "
        "but a competitive advantage. Oluyole Modern Market sits at the convergence of four of Ibadan's highest-traffic corridors, "
        "where tens of thousands of people and naira circulate daily without interruption. "
        "This is not a speculative play on an emerging location. New Garage is already established, already loud with commerce, "
        "and already congested with informal traders who need structured space, which means the demand for these units existed "
        "before the first block was laid. What is being offered here is the rare opportunity to lock in at pre-delivery pricing "
        "in a government-backed project with a 25-year lease, full title security, and a minimum 400% ROI projection over the lease duration. "
        "Investors who understand the Nigerian commercial real estate cycle know that the best entry point is always before the ribbon-cutting, "
        "and that point is now."
    ),
    "rental": (
        "The most reliable form of income is the kind that does not depend on you showing up every morning. "
        "A shop unit at Oluyole Modern Market is a rental income engine positioned inside one of Ibadan's most active trade corridors, "
        "where foot traffic is not driven by marketing campaigns but by geographic inevitability. "
        "Four major roads feed into this location daily, 50,000 commuters and vendors pass through within a 5km radius, "
        "and over 3,000 informal traders are currently being displaced from unstructured market setups and actively searching "
        "for legible, secure commercial space to relocate into. "
        "What that means for you as a rental income investor is a ready tenant pool before your shop is even allocated. "
        "Rental yields in this corridor start from N500,000 to N1.2 million per year per unit with projected rent reviews every two years, "
        "and Land Republic offers an optional professional management model so the income flows without the stress of landlord logistics."
    ),
    "business": (
        "A shop at Oluyole Modern Market gives you a purposefully built and secured commercial space at one of Ibadan's most visible trade intersections, "
        "with your own government-issued lease agreement and a 20 to 25-year tenure that lets you build your brand into a location "
        "without the anxiety of arbitrary rent increases or landlord disputes. "
        "This market already existed and people already know it. What is being built is modern, well-structured, and neatly composed "
        "within a working commercial ecosystem, not a new market trying to find its roots. "
        "The infrastructure tells the story: paved roads, electricity, water, fire safety, on-site security, and an admin office are all part of the setup. "
        "And because you are entering at the pre-delivery phase, your entry cost is significantly lower than it will be once the market opens "
        "and surrounding commercial rents begin to reflect the upgraded infrastructure."
    ),
    "diversify": (
        "A well-structured portfolio does not concentrate all its weight in one asset class, and commercial real estate "
        "in a high-demand corridor like Oluyole offers something that equity markets and residential properties rarely do simultaneously: "
        "predictable cash flow, physical asset ownership, and capital appreciation tied to government infrastructure investment. "
        "The Oluyole corridor hosts nearly 50% of all industries in Oyo State, with multinationals like Pepsi, P&G, British American Tobacco, "
        "and 7Up operating within the same industrial ecosystem that feeds foot traffic to this market daily. "
        "Owning a unit here is not just a property purchase. It is an equity position in one of Ibadan's most structurally embedded commercial zones, "
        "backed by a public-private partnership that insulates the investment from the political instability risks that often concern portfolio-conscious investors."
    ),
    "diaspora": (
        "Owning a productive asset back home should not feel like gambling from a distance. "
        "Oluyole Modern Market is one of the few commercial real estate opportunities in Nigeria structured with the diaspora investor in mind: "
        "government-backed title through Oluyole Local Government, a professionally managed facility that operates without requiring your physical presence, "
        "transparent payment plans across 3 or 6 months, and a lease agreement that holds regardless of administrative changes in government. "
        "The asset generates rental income in naira, which in an inflationary environment like Nigeria's is itself a form of local currency hedge, "
        "and with optional professional management you receive your returns without needing to navigate the Lagos to Ibadan expressway every quarter. "
        "This is the kind of home investment that makes sense from wherever you are in the world."
    ),
}

GOAL_LABELS = {
    "invest":    "Invest in Commercial Property",
    "rental":    "Earn Rental Income",
    "business":  "Secure a Business Space",
    "diversify": "Diversify Investment Portfolio",
    "diaspora":  "Diaspora Investment Back Home",
}

PROFILE_TAGS = {
    "nigeria":  "Nigeria-Based Investor",
    "diaspora": "Diaspora Investor",
}


# ---- HTML FORM (with preview support) ----
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OMM Pitch Generator | Oluyole Modern Market</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #0A1628; color: #FAF6F0; min-height: 100vh; }

  /* HERO */
  .hero { background: linear-gradient(135deg, #0A1628 0%, #1B3A6B 60%, #0A1628 100%); padding: 48px 32px 36px; text-align: center; border-bottom: 3px solid #C8A84B; }
  .hero-badge { display: inline-block; background: #8B1A1A; color: #FAF6F0; font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 6px 18px; border-radius: 2px; margin-bottom: 18px; }
  .hero h1 { font-family: Georgia, serif; font-size: 2.6rem; font-weight: 700; color: #FAF6F0; line-height: 1.15; margin-bottom: 10px; }
  .hero h1 span { color: #C8A84B; }
  .hero p { font-size: 1rem; color: #B0C4DE; max-width: 560px; margin: 0 auto; line-height: 1.6; }

  /* STATS */
  .stats-bar { display: flex; justify-content: center; background: #C8A84B; }
  .stat { flex: 1; text-align: center; padding: 14px 10px; border-right: 1px solid rgba(10,22,40,0.25); color: #0A1628; }
  .stat:last-child { border-right: none; }
  .stat-num { font-size: 1.4rem; font-weight: 800; display: block; }
  .stat-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; opacity: 0.8; }

  /* FORM */
  .form-wrap { max-width: 720px; margin: 40px auto; background: #112040; border-radius: 8px; padding: 40px 44px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); border: 1px solid rgba(200,168,75,0.2); }
  .form-wrap h2 { font-family: Georgia, serif; font-size: 1.5rem; color: #C8A84B; margin-bottom: 8px; }
  .form-wrap > p { color: #8BA4C8; font-size: 0.9rem; margin-bottom: 28px; line-height: 1.5; }
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .field-group.single { grid-template-columns: 1fr; }
  .field { display: flex; flex-direction: column; margin-bottom: 18px; }
  .field label { font-size: 0.78rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #8BA4C8; margin-bottom: 7px; }
  .field input, .field select { background: #0A1628; border: 1px solid rgba(200,168,75,0.3); border-radius: 4px; color: #FAF6F0; font-size: 0.95rem; padding: 11px 14px; outline: none; transition: border 0.2s; }
  .field input:focus, .field select:focus { border-color: #C8A84B; }
  .field select option { background: #0A1628; }
  .divider { border: none; border-top: 1px solid rgba(200,168,75,0.15); margin: 28px 0 20px; }
  .section-label { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: #C8A84B; font-weight: 700; margin-bottom: 16px; }

  /* BUTTONS */
  .btn-row { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 28px; }
  .submit-btn { flex: 1; background: #8B1A1A; color: #FAF6F0; font-size: 0.95rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 16px; border: none; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
  .submit-btn:hover { background: #6B0F0F; }
  .submit-btn.secondary { background: #C8A84B; color: #0A1628; }
  .submit-btn.secondary:hover { background: #b8962e; }

  /* PREVIEW CARD */
  .preview-wrap { max-width: 820px; margin: 0 auto 60px; padding: 0 16px; }
  .pv-card { background: #fff; border-radius: 8px; overflow: hidden; border: 1px solid #ddd; }
  .pv-hero { background: #0A1628; padding: 44px 40px 36px; border-bottom: 3px solid #C8A84B; }
  .pv-badge { display: inline-block; background: #8B1A1A; color: #FAF6F0; font-size: 9px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 5px 14px; border-radius: 2px; margin-bottom: 16px; }
  .pv-hero h2 { font-family: Georgia, serif; font-size: clamp(20px, 3vw, 28px); color: #fff; line-height: 1.25; margin-bottom: 10px; }
  .pv-hero p { font-size: 12px; color: #B0C4DE; line-height: 1.7; max-width: 480px; }
  .pv-stats { display: flex; background: #C8A84B; }
  .pv-stat { flex: 1; text-align: center; padding: 12px 8px; border-right: 1px solid rgba(10,22,40,0.2); }
  .pv-stat:last-child { border-right: none; }
  .pv-stat-n { display: block; font-size: 16px; font-weight: 800; color: #0A1628; }
  .pv-stat-l { display: block; font-size: 7px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: rgba(10,22,40,0.65); margin-top: 2px; }
  .pv-sec { padding: 28px 40px; border-bottom: 1px solid #e8e8e8; background: #fff; }
  .pv-sec.cream { background: #FAF6F0; }
  .pv-sec.dark { background: #0A1628; }
  .pv-sec.gold-bg { background: #C8A84B; }
  .pv-slbl { font-size: 8px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #C8A84B; display: block; margin-bottom: 10px; }
  .pv-sec.dark .pv-slbl { color: #e8c96b; }
  .pv-sec.gold-bg .pv-slbl { color: rgba(10,22,40,0.6); }
  .pv-sec h3 { font-family: Georgia, serif; font-size: 18px; color: #0A1628; margin-bottom: 12px; line-height: 1.3; }
  .pv-sec.dark h3 { color: #fff; }
  .pv-sec.gold-bg h3 { color: #0A1628; font-size: 22px; }
  .pv-sec p { font-size: 13px; color: #333; line-height: 1.8; }
  .pv-sec.dark p { color: rgba(255,255,255,0.72); }
  .pv-sec.gold-bg p { color: rgba(10,22,40,0.72); }

  /* LOCATION TABLE */
  .loc-tbl { width: 100%; border-collapse: collapse; margin-top: 14px; }
  .loc-tbl td { padding: 9px 12px; font-size: 12px; border-bottom: 1px solid #e0e8f0; vertical-align: middle; }
  .loc-tbl td:first-child { font-weight: 700; color: #1B3A6B; background: #E8EEF8; width: 38%; }
  .loc-tbl td:last-child { color: #222; }
  .loc-tbl tr:nth-child(even) td:last-child { background: #FAF6F0; }

  /* SHOP SIZE TABLE */
  .size-tbl { width: 100%; border-collapse: collapse; margin-top: 14px; }
  .size-tbl th { padding: 10px 8px; text-align: center; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #fff; }
  .size-tbl th.std { background: #1B3A6B; }
  .size-tbl th.cls { background: #8B1A1A; }
  .size-tbl th.exe { background: #0A1628; }
  .size-tbl td { padding: 10px 8px; text-align: center; font-size: 12px; border: 1px solid #dde4f0; }
  .size-tbl .sz-dim { font-size: 15px; font-weight: 700; line-height: 1.3; }
  .size-tbl .sz-dim.std { color: #1B3A6B; background: #E8EEF8; }
  .size-tbl .sz-dim.cls { color: #8B1A1A; background: #FDECEA; }
  .size-tbl .sz-dim.exe { color: #0A1628; background: #E8EEF8; }
  .size-tbl .sz-use { color: #444; background: #FAF6F0; font-size: 11px; line-height: 1.6; }
  .size-tbl .sz-lse { font-size: 10px; font-weight: 700; color: #C8A84B; background: #E8EEF8; }

  /* PRICING TABLE */
  .price-tbl { width: 100%; border-collapse: collapse; margin-top: 14px; }
  .price-tbl th { background: #0A1628; color: #C8A84B; font-size: 8.5px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 10px 8px; text-align: center; }
  .price-tbl td { padding: 10px 8px; text-align: center; font-size: 12px; border-bottom: 1px solid rgba(58,80,128,0.3); }
  .price-tbl tr:nth-child(odd) td { background: #1B3A6B; color: #FAF6F0; }
  .price-tbl tr:nth-child(even) td { background: #2856A3; color: #FAF6F0; }
  .price-tbl td.cat { font-weight: 700; color: #fff; }
  .price-tbl td.amt { font-weight: 700; color: #C8A84B; font-size: 14px; }

  /* PAYMENT NOTE */
  .pay-note { margin-top: 12px; background: #0D2040; border: 1px solid #1B3A6B; border-radius: 4px; }
  .pay-note-row { display: flex; border-bottom: 1px solid rgba(200,168,75,0.2); }
  .pay-note-row:last-child { border-bottom: none; }
  .pay-cell { flex: 1; padding: 10px 14px; border-right: 1px solid rgba(58,80,128,0.4); }
  .pay-cell:last-child { border-right: none; }
  .pay-lbl { font-size: 8px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #C8A84B; display: block; margin-bottom: 4px; }
  .pay-val { font-size: 12px; color: #FAF6F0; line-height: 1.5; }

  /* WHY IT WORKS */
  .why-items { margin-top: 14px; }
  .why-item { display: flex; gap: 14px; margin-bottom: 10px; background: #FAF6F0; border-bottom: 1px solid #dde4f0; padding: 14px; }
  .why-num { font-family: Georgia, serif; font-size: 28px; font-weight: 700; color: #C8A84B; min-width: 40px; line-height: 1; }
  .why-content h4 { font-size: 13px; font-weight: 700; color: #0A1628; margin-bottom: 6px; }
  .why-content p { font-size: 12px; color: #444; line-height: 1.6; }

  /* COMPARISON */
  .comp-tbl { width: 100%; border-collapse: collapse; margin-top: 14px; }
  .comp-tbl th { background: #0A1628; color: #C8A84B; font-size: 8.5px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 9px 10px; text-align: left; }
  .comp-tbl td { padding: 9px 10px; font-size: 12px; border-bottom: 1px solid #dde4f0; color: #333; }
  .comp-tbl td:first-child { font-weight: 700; color: #0A1628; }
  .comp-tbl td.omm { color: #1B3A6B; font-weight: 600; background: #EEF4FF; }
  .comp-tbl tr:nth-child(even) td { background: #FAF6F0; }
  .comp-tbl tr:nth-child(even) td.omm { background: #EEF4FF; }

  /* CTA */
  .cta-block { background: #1B3A6B; border-top: 3px solid #C8A84B; padding: 32px 40px; }
  .cta-block .pv-slbl { color: #e8c96b; }
  .cta-block h3 { font-family: Georgia, serif; font-size: 22px; color: #C8A84B; margin-bottom: 10px; line-height: 1.3; }
  .cta-block p { font-size: 13px; color: rgba(255,255,255,0.78); line-height: 1.8; margin-bottom: 18px; }
  .cta-contacts { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
  .cta-ci { background: #0A1628; border-radius: 3px; padding: 10px 16px; }
  .cta-ci-l { font-size: 8px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #C8A84B; display: block; margin-bottom: 3px; }
  .cta-ci-v { font-size: 12px; color: #fff; font-weight: 500; }
  .cta-sig { font-size: 11px; color: rgba(255,255,255,0.45); margin-top: 10px; }

  .footer { text-align: center; padding: 28px; color: #3A5278; font-size: 0.8rem; }

  @media (max-width: 580px) {
    .field-group { grid-template-columns: 1fr; }
    .form-wrap { padding: 28px 18px; }
    .hero h1 { font-size: 1.8rem; }
    .stats-bar, .pv-stats { flex-wrap: wrap; }
    .stat, .pv-stat { min-width: 50%; }
    .pv-sec, .pv-hero, .cta-block { padding: 22px 18px; }
    .btn-row { flex-direction: column; }
  }
</style>
</head>
<body>

<div class="hero">
  <span class="hero-badge">Land Republic x Oluyole LGA</span>
  <h1>Oluyole Modern Market<br><span>Pitch Generator</span></h1>
  <p>Generate a fully personalised, print-ready investment pitch PDF for any prospect, tailored to their profile, goals, and the exact shop category they need.</p>
</div>
<div class="stats-bar">
  <div class="stat"><span class="stat-num">4</span><span class="stat-label">Roads Converge</span></div>
  <div class="stat"><span class="stat-num">50k+</span><span class="stat-label">Daily Footfall</span></div>
  <div class="stat"><span class="stat-num">400%</span><span class="stat-label">Projected ROI</span></div>
  <div class="stat"><span class="stat-num">25yr</span><span class="stat-label">Max Lease</span></div>
  <div class="stat"><span class="stat-num">3,000+</span><span class="stat-label">Displaced Traders</span></div>
</div>

<form class="form-wrap" method="POST" action="/generate">
  <h2>Prospect Information</h2>
  <p>Fill in the prospect's details and goals. The generator builds a personalised pitch document around them.</p>

  <p class="section-label">Prospect Details</p>
  <div class="field-group">
    <div class="field">
      <label>Title</label>
      <select name="title">
        <option>Mr.</option><option>Mrs.</option><option>Miss</option>
        <option>Dr.</option><option>Prof.</option><option>Engr.</option>
        <option>Chief</option><option>Alhaji</option><option>Alhaja</option>
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
      <label>Shop Category to Recommend</label>
      <select name="category">
        <option value="all">All Three Categories (Standard, Classic, Executive)</option>
        <option value="standard">Standard Unit</option>
        <option value="classic">Classic Unit</option>
        <option value="executive">Executive Unit</option>
      </select>
    </div>
  </div>

  <hr class="divider">
  <p class="section-label">Consultant Information</p>
  <div class="field-group">
    <div class="field">
      <label>Consultant Name</label>
      <input type="text" name="agent_name" placeholder="Your full name" required>
    </div>
    <div class="field">
      <label>Phone Number</label>
      <input type="text" name="agent_phone" placeholder="+234 xxx xxx xxxx" required>
    </div>
  </div>
  <div class="field-group">
    <div class="field">
      <label>Email Address</label>
      <input type="email" name="agent_email" placeholder="you@example.com">
    </div>
    <div class="field">
      <label>Property URL (optional)</label>
      <input type="text" name="property_url" placeholder="landrepublic.co/...">
    </div>
  </div>
  <div class="field-group">
    <div class="field">
      <label>Social Media Handle (optional)</label>
      <input type="text" name="agent_social" placeholder="e.g. @asset_by_israel">
    </div>
    <div class="field">
      <label>Tagline (optional)</label>
      <input type="text" name="agent_tagline" placeholder="e.g. Your Favorite Real Estate Consultant">
    </div>
  </div>

  <div class="btn-row">
    <button type="submit" name="action" value="preview" class="submit-btn secondary">Preview Pitch</button>
    <button type="submit" name="action" value="pdf" class="submit-btn">Download PDF</button>
  </div>
</form>

{% if preview %}
<div class="preview-wrap">
<div class="pv-card">

  <!-- HERO -->
  <div class="pv-hero">
    <span class="pv-badge">Land Republic x Oluyole Local Government, Oyo State</span>
    <h2>Prepared Exclusively for You, {{ full_title }}</h2>
    <p>{{ hero_sub }}</p>
  </div>

  <!-- STATS -->
  <div class="pv-stats">
    <div class="pv-stat"><span class="pv-stat-n">4</span><span class="pv-stat-l">Roads Converge</span></div>
    <div class="pv-stat"><span class="pv-stat-n">50,000+</span><span class="pv-stat-l">Daily Footfall</span></div>
    <div class="pv-stat"><span class="pv-stat-n">400%+</span><span class="pv-stat-l">Projected ROI</span></div>
    <div class="pv-stat"><span class="pv-stat-n">25 Yrs</span><span class="pv-stat-l">Max Lease</span></div>
    <div class="pv-stat"><span class="pv-stat-n">3,000+</span><span class="pv-stat-l">Displaced Traders</span></div>
    <div class="pv-stat"><span class="pv-stat-n">18 Mo</span><span class="pv-stat-l">Delivery</span></div>
  </div>

  <!-- INVESTMENT BRIEF -->
  <div class="pv-sec">
    <span class="pv-slbl">{{ full_title }}, This Is the Investment Brief</span>
    <h3>Oluyole Modern Market Is for Someone Like You</h3>
    <p>{{ goal_para }}</p>
  </div>

  <!-- LOCATION -->
  <div class="pv-sec cream">
    <span class="pv-slbl">{{ full_title }}, Let Us Talk About the Location</span>
    <h3>New Garage Is Not Just Another Address</h3>
    <p>New Garage is one of those intersections in Ibadan that functions less like a location and more like a system, where four major arteries (Akala Expressway, Podo Road, Challenge, and the Lagos-Ibadan Expressway) converge and create a commercial vortex that has been active for decades before this market was conceived. The daily footfall here is not manufactured by marketing. It is the organic consequence of geography and industrial density, with Oluyole hosting nearly 50% of all industries in Oyo State, including multinationals like Pepsi, Procter &amp; Gamble, British American Tobacco, and 7Up, whose thousands of workers, suppliers, and vendors pass through this corridor every single day.</p>
    <p style="margin-top:12px;">The infrastructure is already following the commercial gravity: the Akala road dualization is underway, the New Garage terminal is in proximity, and the government has formalized the market upgrade through a public-private partnership with Land Republic, meaning the structural conditions that drive long-term commercial real estate value appreciation are already in motion.</p>
    <table class="loc-tbl">
      <tr><td>Location</td><td>New Garage Axis, Oluyole LGA, Ibadan, Oyo State</td></tr>
      <tr><td>Road Access</td><td>Akala Expressway, Podo Road, Challenge, Lagos-Ibadan Expressway</td></tr>
      <tr><td>Industrial Proximity</td><td>Adjacent to Oluyole Industrial Estate (largest in Ibadan)</td></tr>
      <tr><td>Daily Footfall</td><td>50,000+ commuters and vendors within a 5km radius</td></tr>
      <tr><td>Government Backing</td><td>Partnership with Oluyole Local Government, Oyo State</td></tr>
      <tr><td>Infrastructure</td><td>Akala dualization underway, New Garage terminal nearby</td></tr>
    </table>
  </div>

  <!-- COMMERCIAL CONTEXT -->
  <div class="pv-sec">
    <span class="pv-slbl">{{ full_title }}, Here Is the Commercial Real Estate Case</span>
    <h3>Income-Generating Assets in a High-Density Corridor</h3>
    <p>Commercial real estate in a proven trade corridor behaves differently from residential property. It does not depend on sentiment, it does not stall because of interest rate anxiety, and it does not sit idle while the owner waits for appreciation. It generates income from the first day a tenant occupies it, and in a location like New Garage, finding that tenant is not a challenge because the demand for structured commercial space here already exceeds supply. Over 3,000 informal traders are currently operating without secure, formal shop spaces in this axis and actively seeking to transition into structured environments. That is not a projection. That is an existing, documented demand pool.</p>
    <p style="margin-top:12px;">When you own a unit at Oluyole Modern Market, you are managing a cashflow position, not just a property. The shop sits on government-allocated land with a 20 to 25-year lease, rental income starts from N500,000 to N1.2 million per unit annually with projected reviews every two years, and capital recovery is modeled at 8 years or less, leaving the remaining 12 to 17 years of the lease as net-positive yield.</p>
  </div>

  <!-- SHOP SIZES -->
  <div class="pv-sec cream">
    <span class="pv-slbl">{{ full_title }}, Here Is What Each Space Looks Like</span>
    <h3>Shop Size Reference</h3>
    <table class="size-tbl">
      <thead>
        <tr><th class="std">Standard Unit</th><th class="cls">Classic Unit</th><th class="exe">Executive Unit</th></tr>
      </thead>
      <tbody>
        <tr>
          <td class="sz-dim std">10ft x 10.5ft<br><small>(3m x 3.2m)</small></td>
          <td class="sz-dim cls">12ft x 13ft<br><small>(3.5m x 3.8m)</small></td>
          <td class="sz-dim exe">18ft x 21ft<br><small>(5.5m x 6.4m)</small></td>
        </tr>
        <tr>
          <td class="sz-use">Boutique, phone accessories, provisions, pharmacy kiosk, financial services agent</td>
          <td class="sz-use">Clothing, electronics, hardware, foodstuff, beauty supply, professional office</td>
          <td class="sz-use">Supermarket, showroom, stockroom-enabled trade, corporate anchor tenant</td>
        </tr>
        <tr>
          <td class="sz-lse">Lease: 20 Years</td>
          <td class="sz-lse">Lease: 25 Years</td>
          <td class="sz-lse">Lease: 25 Years</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- PRICING -->
  <div class="pv-sec dark">
    <span class="pv-slbl">{{ full_title }}, Here Are the Shop Categories and Pricing</span>
    <h3>Your Investment Entry Points</h3>
    <table class="price-tbl">
      <thead>
        <tr><th>Category</th><th>Upstairs</th><th>Downstairs</th><th>Deposit</th><th>Lease</th><th>Size</th></tr>
      </thead>
      <tbody>
        {% if show_standard %}
        <tr><td class="cat">Standard</td><td class="amt">N6,450,000</td><td class="amt">N7,525,000</td><td>N1,000,000</td><td>20 Years</td><td>10ft x 10.5ft</td></tr>
        {% endif %}
        {% if show_classic %}
        <tr><td class="cat">Classic</td><td class="amt">N8,600,000</td><td class="amt">N9,675,000</td><td>N2,000,000</td><td>25 Years</td><td>12ft x 13ft</td></tr>
        {% endif %}
        {% if show_executive %}
        <tr><td class="cat">Executive</td><td class="amt">N16,125,000</td><td class="amt">N17,200,000</td><td>N2,000,000</td><td>25 Years</td><td>18ft x 21ft</td></tr>
        {% endif %}
      </tbody>
    </table>
    <div class="pay-note">
      <div class="pay-note-row">
        <div class="pay-cell"><span class="pay-lbl">Payment Plan</span><span class="pay-val">3 or 6 months, interest-free</span></div>
        <div class="pay-cell"><span class="pay-lbl">Title</span><span class="pay-val">Government Allocation (Oluyole LGA)</span></div>
        <div class="pay-cell"><span class="pay-lbl">Lease Countdown</span><span class="pay-val">Starts after project delivery</span></div>
      </div>
      <div class="pay-note-row">
        <div class="pay-cell" style="flex: 3;"><span class="pay-lbl">Bank Account</span><span class="pay-val">LAND REPUBLIC-OLUYOLE MARKET &nbsp;&middot;&nbsp; Providus Bank &nbsp;&middot;&nbsp; 1307642762</span></div>
      </div>
    </div>
  </div>

  <!-- WHY IT WORKS -->
  <div class="pv-sec cream">
    <span class="pv-slbl">{{ full_title }}, at a Quick Glance, Here Is Why This Generally Works</span>
    <h3>Four Reasons This Investment Makes Sense</h3>
    <div class="why-items">
      <div class="why-item"><div class="why-num">01</div><div class="why-content"><h4>Structural Demand, Not Manufactured Interest</h4><p>3,000+ informal traders are actively being displaced from unstructured setups in this corridor, creating a captive tenant pool that was formed by market forces, not marketing.</p></div></div>
      <div class="why-item"><div class="why-num">02</div><div class="why-content"><h4>Government-Backed Title Security</h4><p>A public-private partnership with Oluyole Local Government means your lease is protected by institutional authority, not an individual's goodwill, regardless of any future administrative changes.</p></div></div>
      <div class="why-item"><div class="why-num">03</div><div class="why-content"><h4>8-Year Capital Recovery on a 25-Year Asset</h4><p>Your purchase price is recovered in 8 years or less through rental income, leaving up to 17 years of net yield from a fully paid-for asset. That is the mathematics of compounding commercial real estate.</p></div></div>
      <div class="why-item"><div class="why-num">04</div><div class="why-content"><h4>Infrastructure Appreciation Already in Motion</h4><p>Akala road dualization is underway, the New Garage terminal is nearby, and the market upgrade is formalized. These are present conditions accelerating value, not future promises.</p></div></div>
    </div>
  </div>

  <!-- COMPARISON -->
  <div class="pv-sec">
    <span class="pv-slbl">{{ full_title }}, Let Us Also Do a Quick Market Comparison</span>
    <h3>How OMM Compares to Typical Investment Options</h3>
    <table class="comp-tbl">
      <thead><tr><th>Factor</th><th>OMM Shop Unit</th><th>Residential Land</th><th>Stock Market</th></tr></thead>
      <tbody>
        <tr><td>Title Security</td><td class="omm">Gov. Allocation (LGA)</td><td>Varies (C of O / Gazette)</td><td>N/A</td></tr>
        <tr><td>Income Frequency</td><td class="omm">Monthly rental flow</td><td>Capital gain only</td><td>Dividends (irregular)</td></tr>
        <tr><td>Inflation Hedge</td><td class="omm">Rent reviews every 2yrs</td><td>Partial</td><td>Low in naira terms</td></tr>
        <tr><td>Entry Risk</td><td class="omm">Low (gov. backed)</td><td>Medium (title risk)</td><td>Medium to High</td></tr>
        <tr><td>Hands-Free Option</td><td class="omm">Yes (managed model)</td><td>No</td><td>Broker-dependent</td></tr>
        <tr><td>Projected ROI</td><td class="omm">400%+ over lease</td><td>Varies widely</td><td>Varies by stock</td></tr>
        <tr><td>Liquidity</td><td class="omm">Resalable (lease transfer)</td><td>Illiquid short-term</td><td>Liquid</td></tr>
      </tbody>
    </table>
  </div>

  <!-- CTA -->
  <div class="cta-block">
    <span class="pv-slbl">Next Step</span>
    <h3>{{ full_title }}, Your Unit at Oluyole Modern Market Is Waiting</h3>
    <p>Units are allocated on a first-come, first-served basis, and with the infrastructure upgrade already underway in this corridor, the price advantage available at the pre-delivery stage is time-bound. Let us have a conversation or a consultation call so we can talk about your preferred category, payment structure, and any questions you might have. We can also arrange a site inspection and secure your position in this commercial space.</p>
    <div class="cta-contacts">
      <div class="cta-ci"><span class="cta-ci-l">Call / WhatsApp</span><span class="cta-ci-v">{{ agent_phone }}</span></div>
      <div class="cta-ci"><span class="cta-ci-l">Email</span><span class="cta-ci-v">{{ agent_email }}</span></div>
      {% if property_url %}
      <div class="cta-ci"><span class="cta-ci-l">View Property</span><span class="cta-ci-v">{{ property_url }}</span></div>
      {% endif %}
    </div>
    <div class="cta-ci" style="display:inline-block;margin-bottom:14px;"><span class="cta-ci-l">Bank Account</span><span class="cta-ci-v">LAND REPUBLIC-OLUYOLE MARKET &nbsp;&middot;&nbsp; Providus Bank &nbsp;&middot;&nbsp; 1307642762</span></div>
    <p class="cta-sig">Prepared by <strong>{{ agent_name }}</strong>{% if agent_social %} &nbsp;&middot;&nbsp; {{ agent_social }}{% endif %}{% if agent_tagline %} &nbsp;&middot;&nbsp; {{ agent_tagline }}{% endif %}</p>
  </div>

</div>
</div>
{% endif %}

<div class="footer">Oluyole Modern Market &mdash; Developed by Land Republic in partnership with Oyo State Government through Oluyole Local Government</div>
</body>
</html>
"""


# ---- PDF BUILDER ----
def build_styles():
    return {
        "hero_badge": ParagraphStyle("hero_badge", fontName="Helvetica-Bold",
            fontSize=8, textColor=GOLD, leading=12, alignment=TA_CENTER, spaceAfter=10),
        "hero_title": ParagraphStyle("hero_title", fontName="Times-Bold",
            fontSize=24, textColor=WHITE, leading=30, alignment=TA_CENTER, spaceAfter=6),
        "hero_sub": ParagraphStyle("hero_sub", fontName="Times-Italic",
            fontSize=11, textColor=colors.HexColor("#C8D8F0"), leading=16,
            alignment=TA_CENTER, spaceAfter=4),
        "section_label": ParagraphStyle("section_label", fontName="Helvetica-Bold",
            fontSize=8, textColor=GOLD, leading=12, alignment=TA_LEFT,
            spaceBefore=14, spaceAfter=6),
        "section_title": ParagraphStyle("section_title", fontName="Times-Bold",
            fontSize=15, textColor=NAVY, leading=20, alignment=TA_LEFT,
            spaceBefore=4, spaceAfter=8),
        "body": ParagraphStyle("body", fontName="Helvetica",
            fontSize=9.5, textColor=colors.HexColor("#2C2C2C"), leading=15,
            alignment=TA_JUSTIFY, spaceAfter=8),
        "body_white": ParagraphStyle("body_white", fontName="Helvetica",
            fontSize=9.5, textColor=WHITE, leading=15, alignment=TA_JUSTIFY, spaceAfter=6),
        "cta_main": ParagraphStyle("cta_main", fontName="Times-Bold",
            fontSize=17, textColor=GOLD, leading=22, alignment=TA_CENTER, spaceAfter=6),
        "cta_sub": ParagraphStyle("cta_sub", fontName="Helvetica",
            fontSize=9, textColor=WHITE, leading=14, alignment=TA_CENTER, spaceAfter=4),
        "small_label": ParagraphStyle("small_label", fontName="Helvetica-Bold",
            fontSize=7.5, textColor=GOLD, leading=11, alignment=TA_CENTER),
        "table_head": ParagraphStyle("table_head", fontName="Helvetica-Bold",
            fontSize=8, textColor=WHITE, leading=11, alignment=TA_CENTER),
        "table_cell": ParagraphStyle("table_cell", fontName="Helvetica",
            fontSize=8.5, textColor=NAVY, leading=12, alignment=TA_CENTER),
        "footnote": ParagraphStyle("footnote", fontName="Helvetica-Oblique",
            fontSize=7.5, textColor=colors.HexColor("#888888"), leading=11,
            alignment=TA_CENTER),
    }


def make_hero(styles, title, first_name, occupation, goal_label):
    full_title = f"{title} {first_name}"
    elems = []
    inner = [
        Paragraph("LAND REPUBLIC x OLUYOLE LOCAL GOVERNMENT, OYO STATE", styles["hero_badge"]),
        Spacer(1, 6),
        Paragraph(f"Prepared Exclusively for You, {full_title}", styles["hero_title"]),
        Spacer(1, 6),
        Paragraph(
            f"Oluyole Modern Market is for someone like you, a {occupation} whose primary focus is to {goal_label.lower()}",
            styles["hero_sub"]
        ),
        Spacer(1, 10),
        Paragraph("New Garage Axis, Ibadan, Oyo State", ParagraphStyle("loc",
            fontName="Helvetica-Bold", fontSize=9, textColor=GOLD, alignment=TA_CENTER)),
    ]
    tbl = Table([[inner]], colWidths=[W - 2 * 25 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 28),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 24),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("LINEBELOW", (0, 0), (-1, -1), 3, GOLD),
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
        row.append([
            Paragraph(num, ParagraphStyle("sn", fontName="Helvetica-Bold",
                fontSize=12, textColor=NAVY, alignment=TA_CENTER, leading=15)),
            Paragraph(label, ParagraphStyle("sl", fontName="Helvetica",
                fontSize=6.5, textColor=NAVY, alignment=TA_CENTER, leading=9)),
        ])
    col_w = (W - 50 * mm) / len(stats)
    tbl = Table([row], colWidths=[col_w] * len(stats))
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.HexColor("#A08030")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return [tbl]


def make_investment_brief(styles, title, first_name, goal, goal_label, profile):
    elems = []
    elems.append(Spacer(1, 14))
    full_title = f"{title} {first_name}"
    elems.append(Paragraph(
        f"{full_title.upper()}, THIS IS THE INVESTMENT BRIEF", styles["section_label"]
    ))
    elems.append(Paragraph("Oluyole Modern Market Is for Someone Like You", styles["section_title"]))
    elems.append(Paragraph(GOAL_PARAGRAPHS.get(goal, GOAL_PARAGRAPHS["invest"]), styles["body"]))
    return elems


def make_location_section(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph(
        f"{full_title.upper()}, LET US TALK ABOUT THE LOCATION", styles["section_label"]
    ))
    elems.append(Paragraph("New Garage Is Not Just Another Address", styles["section_title"]))

    body = (
        "New Garage is one of those intersections in Ibadan that functions less like a location and more like a system, "
        "where four major arteries (Akala Expressway, Podo Road, Challenge, and the Lagos-Ibadan Expressway) "
        "converge and create a commercial vortex that has been active for decades before this market was conceived. "
        "The daily footfall here is not manufactured by marketing or driven by a single anchor tenant. "
        "It is the organic consequence of geography and industrial density, with Oluyole hosting nearly 50% of "
        "all industries in Oyo State, including multinationals like Pepsi, Procter & Gamble, British American Tobacco, "
        "and 7Up, whose thousands of workers, suppliers, and vendors pass through this corridor every single day."
    )
    elems.append(Paragraph(body, styles["body"]))

    body2 = (
        "What makes this particularly compelling is that infrastructure is already following the commercial gravity: "
        "the Akala road dualization is underway, the New Garage terminal is in proximity, and the government has "
        "formalized the market upgrade through a public-private partnership with Land Republic, meaning the structural "
        "conditions that drive long-term commercial real estate value appreciation are already in motion."
    )
    elems.append(Paragraph(body2, styles["body"]))

    loc_data = [
        ["Location", "New Garage Axis, Oluyole LGA, Ibadan, Oyo State"],
        ["Road Access", "Akala Expressway, Podo Road, Challenge, Lagos-Ibadan Expressway"],
        ["Industrial Proximity", "Adjacent to Oluyole Industrial Estate (largest in Ibadan)"],
        ["Daily Footfall", "50,000+ commuters and vendors within a 5km radius"],
        ["Government Backing", "Partnership with Oluyole Local Government, Oyo State"],
        ["Infrastructure", "Akala dualization underway, New Garage terminal nearby"],
    ]
    tbl = Table(loc_data, colWidths=[50 * mm, W - 50 * mm - 50 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [colors.HexColor("#FAF6F0"), WHITE]),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR", (0, 0), (0, -1), BLUE),
        ("TEXTCOLOR", (1, 0), (1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#D0D8E8")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#B0C0D8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(tbl)
    return elems


def make_commercial_context(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph(
        f"{full_title.upper()}, HERE IS THE COMMERCIAL REAL ESTATE CASE", styles["section_label"]
    ))
    elems.append(Paragraph("Income-Generating Assets in a High-Density Corridor", styles["section_title"]))

    body = (
        "Commercial real estate in a proven trade corridor behaves differently from residential property. "
        "It does not depend on sentiment, it does not stall because of interest rate anxiety, and it does not "
        "sit idle while the owner waits for appreciation. It generates income from the first day a tenant occupies "
        "it, and in a location like New Garage, finding that tenant is not a challenge because the demand for "
        "structured commercial space here already exceeds supply. Over 3,000 informal traders are currently "
        "operating without secure, formal shop spaces in this axis and actively seeking to transition into "
        "structured environments. That is not a projection. That is an existing, documented demand pool."
    )
    elems.append(Paragraph(body, styles["body"]))

    body2 = (
        "When you own a unit at Oluyole Modern Market, you are managing a cashflow position, not just a property. "
        "The shop sits on government-allocated land with a 20 to 25-year lease, rental income starts from "
        "N500,000 to N1.2 million per unit annually with projected reviews every two years, and capital recovery "
        "is modeled at 8 years or less, leaving the remaining 12 to 17 years of the lease as net-positive yield."
    )
    elems.append(Paragraph(body2, styles["body"]))
    return elems


def make_size_table(styles):
    elems = []
    elems.append(Spacer(1, 10))
    elems.append(Paragraph("SHOP SIZE REFERENCE", styles["section_label"]))
    elems.append(Paragraph("Understanding What Your Space Looks Like", styles["section_title"]))

    cw = (W - 50 * mm) / 3
    size_data = [
        [
            Paragraph("STANDARD UNIT", styles["table_head"]),
            Paragraph("CLASSIC UNIT", styles["table_head"]),
            Paragraph("EXECUTIVE UNIT", styles["table_head"]),
        ],
        [
            Paragraph("10ft x 10.5ft\n(3m x 3.2m)", ParagraphStyle("sz",
                fontName="Helvetica-Bold", fontSize=12, textColor=BLUE,
                alignment=TA_CENTER, leading=16)),
            Paragraph("12ft x 13ft\n(3.5m x 3.8m)", ParagraphStyle("sz",
                fontName="Helvetica-Bold", fontSize=12, textColor=RED,
                alignment=TA_CENTER, leading=16)),
            Paragraph("18ft x 21ft\n(5.5m x 6.4m)", ParagraphStyle("sz",
                fontName="Helvetica-Bold", fontSize=12, textColor=NAVY,
                alignment=TA_CENTER, leading=16)),
        ],
        [
            Paragraph("Boutique, phone accessories, provisions, pharmacy kiosk, financial services agent",
                ParagraphStyle("sz2", fontName="Helvetica", fontSize=7.5,
                    textColor=colors.HexColor("#444444"), alignment=TA_CENTER, leading=11)),
            Paragraph("Clothing, electronics, hardware, foodstuff, beauty supply, professional office",
                ParagraphStyle("sz2", fontName="Helvetica", fontSize=7.5,
                    textColor=colors.HexColor("#444444"), alignment=TA_CENTER, leading=11)),
            Paragraph("Supermarket, showroom, stockroom-enabled trade, corporate anchor tenant",
                ParagraphStyle("sz2", fontName="Helvetica", fontSize=7.5,
                    textColor=colors.HexColor("#444444"), alignment=TA_CENTER, leading=11)),
        ],
        [
            Paragraph("Lease: 20 Years", styles["small_label"]),
            Paragraph("Lease: 25 Years", styles["small_label"]),
            Paragraph("Lease: 25 Years", styles["small_label"]),
        ],
    ]
    tbl = Table(size_data, colWidths=[cw, cw, cw])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), BLUE),
        ("BACKGROUND", (1, 0), (1, 0), RED),
        ("BACKGROUND", (2, 0), (2, 0), NAVY),
        ("BACKGROUND", (0, 1), (0, 1), LIGHT_BLUE),
        ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#FDECEA")),
        ("BACKGROUND", (2, 1), (2, 1), colors.HexColor("#E8EEF8")),
        ("BACKGROUND", (0, 2), (-1, 2), CREAM),
        ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#E8EEF8")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.HexColor("#C0C8D8")),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#C0C8D8")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#8899BB")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(tbl)
    return elems


def make_pricing_table(styles, category, title, first_name):
    full_title = f"{title} {first_name}"
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph(
        f"{full_title.upper()}, HERE ARE THE SHOP CATEGORIES AND PRICING", styles["section_label"]
    ))
    elems.append(Paragraph("Your Investment Entry Points", styles["section_title"]))

    all_cats = {
        "standard": {
            "name": "Standard", "upstairs": "N6,450,000", "downstairs": "N7,525,000",
            "deposit": "N1,000,000", "lease": "20 Years", "size": "10ft x 10.5ft",
        },
        "classic": {
            "name": "Classic", "upstairs": "N8,600,000", "downstairs": "N9,675,000",
            "deposit": "N2,000,000", "lease": "25 Years", "size": "12ft x 13ft",
        },
        "executive": {
            "name": "Executive", "upstairs": "N16,125,000", "downstairs": "N17,200,000",
            "deposit": "N2,000,000", "lease": "25 Years", "size": "18ft x 21ft",
        },
    }

    show = ["standard", "classic", "executive"] if category == "all" else [category]

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

    cw_total = W - 50 * mm
    col_ws = [
        cw_total * 0.14, cw_total * 0.18, cw_total * 0.18,
        cw_total * 0.16, cw_total * 0.13, cw_total * 0.21
    ]
    tbl = Table(rows, colWidths=col_ws)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#3A5080")),
        ("BOX", (0, 0), (-1, -1), 1, BLUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        bg = BLUE if i % 2 == 1 else MID_BLUE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    tbl.setStyle(TableStyle(style_cmds))
    elems.append(tbl)

    # Payment note
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
            Paragraph("LAND REPUBLIC-OLUYOLE MARKET\nProvidus Bank: 1307642762",
                ParagraphStyle("nv", fontName="Helvetica", fontSize=7.5, textColor=WHITE,
                    alignment=TA_CENTER, leading=11)),
        ],
    ]
    cw2 = cw_total / 4
    tbl2 = Table(notes_data, colWidths=[cw2] * 4)
    tbl2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0D2040")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.HexColor("#2A4070")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, GOLD),
        ("BOX", (0, 0), (-1, -1), 1, BLUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(tbl2)
    return elems


def make_why_it_works(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph(
        f"{full_title.upper()}, AT A QUICK GLANCE, HERE IS WHY THIS GENERALLY WORKS",
        styles["section_label"]
    ))
    elems.append(Paragraph("Four Reasons This Investment Makes Sense", styles["section_title"]))

    reasons = [
        ("01", "Structural Demand, Not Manufactured Interest",
         "3,000+ informal traders are actively being displaced from unstructured setups in this corridor, "
         "creating a captive tenant pool that was formed by market forces, not marketing."),
        ("02", "Government-Backed Title Security",
         "A public-private partnership with Oluyole Local Government means your lease is protected "
         "by institutional authority, not an individual's goodwill, regardless of any future administrative changes."),
        ("03", "8-Year Capital Recovery on a 25-Year Asset",
         "Your purchase price is recovered in 8 years or less through rental income, leaving up to 17 years "
         "of net yield from a fully paid-for asset. That is the mathematics of compounding commercial real estate."),
        ("04", "Infrastructure Appreciation Already in Motion",
         "Akala road dualization is underway, the New Garage terminal is nearby, and the market upgrade is "
         "formalized. These are present conditions accelerating value, not future promises."),
    ]

    for num, title_r, desc in reasons:
        row = [
            [Paragraph(num, ParagraphStyle("rn", fontName="Times-Bold", fontSize=22,
                textColor=GOLD, alignment=TA_CENTER, leading=28))],
            [
                Paragraph(title_r, ParagraphStyle("rt", fontName="Helvetica-Bold", fontSize=9.5,
                    textColor=NAVY, leading=13, spaceAfter=4)),
                Paragraph(desc, ParagraphStyle("rd", fontName="Helvetica", fontSize=8.5,
                    textColor=colors.HexColor("#333333"), leading=13)),
            ]
        ]
        tbl = Table([row[0:1] + [row[1]]], colWidths=[18 * mm, W - 50 * mm - 18 * mm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), LIGHT_BLUE),
            ("BACKGROUND", (1, 0), (1, 0), CREAM),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (0, 0), 4),
            ("LEFTPADDING", (1, 0), (1, 0), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8D4E8")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 3))
    return elems


def make_comparison_table(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = []
    elems.append(Spacer(1, 14))
    elems.append(Paragraph(
        f"{full_title.upper()}, LET US ALSO DO A QUICK MARKET COMPARISON", styles["section_label"]
    ))
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
    col_ws = [(W - 50 * mm) * f for f in [0.28, 0.28, 0.24, 0.20]]
    tbl = Table(rows, colWidths=col_ws)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), NAVY),
        ("TEXTCOLOR", (1, 1), (1, -1), BLUE),
        ("TEXTCOLOR", (2, 1), (-1, -1), colors.HexColor("#555555")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#D0D8E8")),
        ("BOX", (0, 0), (-1, -1), 1, BLUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        bg = CREAM if i % 2 == 0 else WHITE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
        style_cmds.append(("BACKGROUND", (1, i), (1, i), colors.HexColor("#EEF4FF")))
    tbl.setStyle(TableStyle(style_cmds))
    elems.append(tbl)
    return elems


def make_cta(styles, agent_name, agent_phone, agent_email, property_url, agent_social, agent_tagline, title, first_name):
    full_title = f"{title} {first_name}"
    elems = []
    elems.append(Spacer(1, 16))

    inner = [
        Paragraph("NEXT STEP", ParagraphStyle("ct0", fontName="Helvetica-Bold",
            fontSize=8, textColor=colors.HexColor("#B0C4DE"), alignment=TA_CENTER, spaceAfter=6)),
        Paragraph(
            f"Your Unit at Oluyole Modern Market Is Waiting, {full_title}",
            styles["cta_main"]
        ),
        Spacer(1, 6),
        Paragraph(
            "Units are allocated on a first-come, first-served basis, and with the infrastructure upgrade already "
            "underway in this corridor, the price advantage available at the pre-delivery stage is time-bound. "
            "Let us have a conversation or a consultation call so we can talk about your preferred category, "
            "payment structure, and any questions you might have. We can also arrange a site inspection and "
            "secure your position in this commercial space.",
            ParagraphStyle("ctab", fontName="Helvetica", fontSize=9, textColor=WHITE,
                alignment=TA_CENTER, leading=14, spaceAfter=12)
        ),
        Spacer(1, 8),
    ]

    contact_row = [
        Paragraph(agent_name, ParagraphStyle("ci", fontName="Helvetica-Bold",
            fontSize=9, textColor=GOLD, alignment=TA_CENTER)),
        Paragraph(agent_phone, ParagraphStyle("ci", fontName="Helvetica-Bold",
            fontSize=9, textColor=GOLD, alignment=TA_CENTER)),
    ]
    if agent_email:
        contact_row.append(
            Paragraph(agent_email, ParagraphStyle("ci", fontName="Helvetica",
                fontSize=8.5, textColor=WHITE, alignment=TA_CENTER))
        )

    cw = (W - 50 * mm) / len(contact_row)
    ctbl = Table([contact_row], colWidths=[cw] * len(contact_row))
    ctbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0A1628")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.HexColor("#3A5278")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    inner.append(ctbl)

    if property_url:
        inner.append(Spacer(1, 6))
        inner.append(Paragraph(
            property_url.replace("https://", "").replace("http://", "").rstrip("/"),
            ParagraphStyle("url", fontName="Helvetica-Oblique", fontSize=8.5,
                textColor=colors.HexColor("#8BA4C8"), alignment=TA_CENTER)
        ))

    inner.append(Spacer(1, 8))
    inner.append(Paragraph(
        "Account Name: LAND REPUBLIC-OLUYOLE MARKET  |  Providus Bank  |  1307642762",
        ParagraphStyle("acct", fontName="Helvetica", fontSize=8,
            textColor=colors.HexColor("#B0C4DE"), alignment=TA_CENTER)
    ))
    inner.append(Spacer(1, 8))
    inner.append(Paragraph(
        f"Prepared by {agent_name}" + (f"  |  {agent_social}" if agent_social else "") + (f"  |  {agent_tagline}" if agent_tagline else ""),
        ParagraphStyle("sig", fontName="Helvetica-Oblique", fontSize=8,
            textColor=colors.HexColor("#8BA4C8"), alignment=TA_CENTER)
    ))

    tbl = Table([[inner]], colWidths=[W - 50 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("LINEABOVE", (0, 0), (-1, 0), 3, GOLD),
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
    agent_name = form.get("agent_name", "Israel Toluwalope OLALEYE")
    agent_phone = form.get("agent_phone", "+2349033499271")
    agent_email = form.get("agent_email", "")
    property_url = form.get("property_url", "landrepublic.co/properties/oluyole-modern-market")
    agent_social  = form.get("agent_social", "")
    agent_tagline = form.get("agent_tagline", "")

    goal_label = GOAL_LABELS.get(goal, "Invest")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=25 * mm, rightMargin=25 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=f"OMM Pitch - {title} {first_name}"
    )

    styles = build_styles()
    story = []

    story += make_hero(styles, title, first_name, occupation, goal_label)
    story += make_stats_bar(styles)
    story += make_investment_brief(styles, title, first_name, goal, goal_label, profile)
    story += make_location_section(styles, title, first_name)
    story += make_commercial_context(styles, title, first_name)
    story += make_size_table(styles)
    story += make_pricing_table(styles, category, title, first_name)
    story += make_why_it_works(styles, title, first_name)
    story += make_comparison_table(styles, title, first_name)
    story += make_cta(styles, agent_name, agent_phone, agent_email, property_url, agent_social, agent_tagline, title, first_name)

    doc.build(story)
    buf.seek(0)
    return buf


@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        HTML, preview=False, full_title="", hero_sub="",
        goal_para="", show_standard=True, show_classic=True, show_executive=True,
        agent_name="", agent_phone="", agent_email="", property_url="",
        agent_social="", agent_tagline=""
    )


@app.route("/generate", methods=["POST"])
def generate():
    form = request.form
    action = form.get("action", "pdf")

    title = form.get("title", "Mr.")
    first_name = form.get("first_name", "Valued Investor")
    occupation = form.get("occupation", "Professional")
    goal = form.get("goal", "invest")
    profile = form.get("profile", "nigeria")
    category = form.get("category", "all")
    agent_name = form.get("agent_name", "Israel Toluwalope OLALEYE")
    agent_phone = form.get("agent_phone", "+2349033499271")
    agent_email = form.get("agent_email", "")
    property_url = form.get("property_url", "")
    agent_social  = form.get("agent_social", "")
    agent_tagline = form.get("agent_tagline", "")

    goal_label = GOAL_LABELS.get(goal, "Invest")
    full_title = f"{title} {first_name}"
    hero_sub = f"Oluyole Modern Market is for someone like you, a {occupation} whose primary focus is to {goal_label.lower()}"

    show_standard = category in ("all", "standard")
    show_classic = category in ("all", "classic")
    show_executive = category in ("all", "executive")

    if action == "preview":
        return render_template_string(
            HTML, preview=True,
            full_title=full_title,
            hero_sub=hero_sub,
            goal_para=GOAL_PARAGRAPHS.get(goal, GOAL_PARAGRAPHS["invest"]),
            show_standard=show_standard,
            show_classic=show_classic,
            show_executive=show_executive,
            agent_name=agent_name,
            agent_phone=agent_phone,
            agent_email=agent_email,
            property_url=property_url,
            agent_social=agent_social,
            agent_tagline=agent_tagline,
        )

    pdf_buf = build_pdf(form)
    fn_clean = first_name.replace(" ", "_")
    filename = f"OMM_Pitch_{fn_clean}.pdf"
    return send_file(pdf_buf, as_attachment=True, download_name=filename, mimetype="application/pdf")


if __name__ == "__main__":
    print("\n" + "=" * 54)
    print("  OLUYOLE MODERN MARKET PITCH GENERATOR")
    print("=" * 54)
    print("  Open on THIS device:  http://localhost:5001")
    print("=" * 54)
    print("  Press Ctrl+C to stop\n")
    app.run(debug=False, port=5001)
