import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_clean_short_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Clean, premium academic theme
    C_BG = RGBColor(0xF8, 0xFA, 0xFC)          # Soft light slate background
    C_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)     # Pure white container card
    C_BORDER = RGBColor(0xCB, 0xD5, 0xE1)      # Subtle border
    C_NAVY = RGBColor(0x1E, 0x3A, 0x8A)        # Main title navy
    C_BLUE = RGBColor(0x25, 0x63, 0xEB)        # Accent royal blue
    C_DARK = RGBColor(0x0F, 0x17, 0x2A)        # Deep readable text
    C_MUTED = RGBColor(0x64, 0x74, 0x8B)       # Subtitle slate

    diag_dir = r"D:\TERMGUARD\TERMGUARD\diagrams"
    img_dir = r"D:\TERMGUARD\TERMGUARD\diagrams\slides_img"

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, slide_tag=""):
        # Top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.52), Inches(11.733), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_cat = tf.paragraphs[0]
        p_cat.text = f"TERMGUARD • PROJECT REVIEW {slide_tag}".upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

    def add_single_wide_card(slide, points, title=""):
        # ONE SINGLE, WIDE, SPACIOUS CARD - NO CRAMPED SPLITS!
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.4))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.933), Inches(4.9))
        tf = tb.text_frame
        tf.word_wrap = True

        if title:
            p0 = tf.paragraphs[0]
            p0.text = title
            p0.font.name = "Calibri"
            p0.font.size = Pt(17)
            p0.font.bold = True
            p0.font.color.rgb = C_NAVY
            p0.space_after = Pt(14)
            start_idx = 1
        else:
            start_idx = 0

        for idx, pt in enumerate(points):
            if start_idx == 0 and idx == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()

            p.space_after = Pt(16)
            p.font.name = "Calibri"
            p.font.size = Pt(16)
            p.font.color.rgb = C_DARK

            if isinstance(pt, tuple):
                r_b = p.add_run()
                r_b.text = "👉  " + pt[0] + ":  "
                r_b.font.bold = True
                r_b.font.color.rgb = C_BLUE
                r_t = p.add_run()
                r_t.text = pt[1]
                r_t.font.bold = False
            else:
                r_b = p.add_run()
                r_b.text = "👉  "
                r_b.font.bold = True
                r_b.font.color.rgb = C_BLUE
                r_t = p.add_run()
                r_t.text = str(pt)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Clean, Big, Impactful)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_CARD_BG
    card1.line.color.rgb = C_BLUE
    card1.line.width = Pt(2.5)

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "A MINI PROJECT PRESENTATION ON"
    p0.font.name = "Calibri"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "TERMGUARD"
    p1.font.name = "Calibri"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p1.space_after = Pt(6)

    p2 = tf1.add_paragraph()
    p2.text = "Smart Contract Reader & Automated Deadline Defense System"
    p2.font.name = "Calibri"
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_MUTED
    p2.space_after = Pt(26)

    p3 = tf1.add_paragraph()
    p3.text = "SUBMITTED BY:\n1. REBALLY LAXMI HARSHITH  (Roll No: 201224539090)\n2. SHUBHAM PRADHAN"
    p3.font.name = "Calibri"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = C_DARK
    p3.space_after = Pt(14)

    p4 = tf1.add_paragraph()
    p4.text = "Department of Computer Science & Engineering | Academic Year 2025–2026\nLive Web App: https://termguard.onrender.com"
    p4.font.name = "Calibri"
    p4.font.size = Pt(11)
    p4.font.color.rgb = C_BLUE

    # =========================================================================
    # SLIDE 2: INTRODUCTION (Very short, 4 simple lines)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "1. Introduction to TermGuard", "[Slide 2/12]")

    add_single_wide_card(s2, [
        ("Long Agreements", "Every gym pass, rental flat, and software plan comes with a 20-page legal agreement."),
        ("Nobody Reads Them", "99% of people simply click 'I Agree' without reading because it takes over 45 minutes."),
        ("What TermGuard Is", "A smart web tool that reads contracts for you in 2 seconds using Google Gemini AI."),
        ("What It Does", "Spots hidden money traps and sends automatic SMS and Email alerts to your phone before you lose money."),
    ])

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT (Short & Clear)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "2. Problem Statement", "[Slide 3/12]")

    add_single_wide_card(s3, [
        ("Silent Auto-Debits", "Gyms silently charge your bank card ₹32,000 for another year without asking you."),
        ("Strict 30-Day Rules", "Contracts say: 'You must cancel 30 days before renewal, otherwise no refund!'"),
        ("Lost Rent Deposits", "Landlords keep ₹70,000 security deposits if you forget to give a 2-month written notice."),
        ("Phone Calendars Fail", "Regular calendars only remind you on the last day—when it is already too late!"),
        ("Real Money Lost", "Normal people lose ₹15,000 to ₹50,000 every year to forgotten subscriptions."),
    ])

    # =========================================================================
    # SLIDE 4: OBJECTIVES (Simple 4 Goals)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "3. Project Objectives", "[Slide 4/12]")

    add_single_wide_card(s4, [
        ("Fast AI Contract Reading", "Scan any legal contract in under 2 seconds using Google Gemini AI."),
        ("Show Money at Risk", "Clearly calculate how much money you could lose in Indian Rupees (₹ INR)."),
        ("Calculate Real Cutoff Dates", "Find the true last date to cancel by subtracting notice periods backwards."),
        ("3-Stage Phone Alerts", "Send warnings via SMS and Email at 3 times: 1 week before, 1 day before, and cutoff day."),
        ("Ready-to-Send Letters", "Automatically write formal cancellation letters so you can stop payments instantly."),
    ])

    # =========================================================================
    # SLIDE 5: EXISTING VS PROPOSED (Clean Comparison)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "4. Existing System vs. Proposed System", "[Slide 5/12]")

    add_single_wide_card(s5, [
        ("Reading Contracts", "Manual reading takes 45 minutes of hard English  ➔  TermGuard AI reads in 2 seconds."),
        ("Reminder Timing", "Phone calendar alerts on the last day (Too late!)  ➔  TermGuard alerts 7 days & 1 day before."),
        ("Writing Cancellation Letters", "You have to write legal letters yourself  ➔  TermGuard auto-writes the letter for you."),
        ("Alert Delivery", "Easy to miss calendar notifications  ➔  Real SMS sent directly to your mobile phone SIM card."),
        ("Continuous Monitoring", "Regular chatbots forget contracts once closed  ➔  TermGuard monitors 24/7 in the cloud."),
    ])

    # =========================================================================
    # SLIDE 6: TECHNOLOGIES USED (Simple & Clear)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "5. Technologies & Tools Used", "[Slide 6/12]")

    add_single_wide_card(s6, [
        ("Next.js 14 & React 18", "Modern full-stack framework for building our fast, interactive web dashboard."),
        ("Google Gemini 1.5 Flash AI", "Smart Google AI that understands legal contract text in under 2 seconds."),
        ("Twilio & Fast2SMS", "Telecom services that send real SMS text messages directly to mobile phones."),
        ("Resend Email API", "Email service that sends clean, verified alert emails directly to Gmail inboxes."),
        ("Local JSON Database (db.json)", "Saves contracts and reminders safely with zero extra server hosting costs."),
        ("Render Cloud Platform", "Hosts our live website online at https://termguard.onrender.com."),
    ])

    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE (Clean Diagram + 3 Simple Steps)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "6. System Architecture (How Everything Connects)", "[Slide 7/12]")

    card7 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.4))
    card7.fill.solid()
    card7.fill.fore_color.rgb = C_CARD_BG
    card7.line.color.rgb = C_BORDER
    card7.line.width = Pt(1.5)

    arch_img = os.path.join(diag_dir, "architecture_diagram.png")
    if os.path.exists(arch_img):
        s7.shapes.add_picture(arch_img, Inches(1.1), Inches(1.7), width=Inches(7.2))

    tb7 = s7.shapes.add_textbox(Inches(8.5), Inches(1.9), Inches(3.8), Inches(4.7))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    p0 = tf7.paragraphs[0]
    p0.text = "Simple 4-Step Flow:"
    p0.font.name = "Calibri"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = C_NAVY
    p0.space_after = Pt(14)

    steps = [
        ("1. Upload Contract", "User pastes contract text or picks a sample agreement."),
        ("2. Gemini AI Reads", "AI finds hidden traps and calculates the cutoff date."),
        ("3. Stored in DB", "Saved in db.json with a live countdown timer."),
        ("4. Real Alerts Sent", "Twilio sends SMS and Resend sends Email when date arrives."),
    ]
    for st, desc in steps:
        p = tf7.add_paragraph()
        p.space_after = Pt(12)
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        rb = p.add_run()
        rb.text = "• " + st + ":\n  "
        rb.font.bold = True
        rb.font.color.rgb = C_BLUE
        rt = p.add_run()
        rt.text = desc

    # =========================================================================
    # SLIDE 8: SYSTEM MODULES (5 Simple Modules)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "7. System Modules (Main Parts of the Website)", "[Slide 8/12]")

    add_single_wide_card(s8, [
        ("Executive Dashboard HUD", "Top cards showing Total Money Saved (₹1,48,440) and active countdown timers."),
        ("Document Studio", "Where you paste contracts or choose sample agreements (Gym, Rent Flat, SaaS)."),
        ("Deadlines & Alerts Center", "Shows active reminder cards with live countdown timers in days, hours, and minutes."),
        ("AI Assistant Chat", "A helpful chatbot where you can ask questions like 'When is my last date to cancel?'"),
        ("SMS & Email Dispatcher", "Sends real SMS to phone numbers (+91) and emails with ready-to-copy cancellation letters."),
        ("Activity Trust Log", "A clear table showing timestamps and message IDs for every alert sent."),
    ])

    # =========================================================================
    # SLIDE 9: 3-STAGE ALERT WORKING (Clear Steps)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "8. Methodology: How the 3-Stage Alert Works", "[Slide 9/12]")

    add_single_wide_card(s9, [
        ("Step 1: AI Contract Scan", "Gemini AI scans the agreement, finds the traps, and calculates cutoff dates in 2 seconds."),
        ("Step 2: Stage 1 (7 Days Left)", "Sends an early warning SMS & Email so you have plenty of time to prepare without rushing."),
        ("Step 3: Stage 2 (24 Hours Left)", "Sends an urgent alert warning that tomorrow is your final cutoff day!"),
        ("Step 4: Stage 3 (Final Day)", "Sends final call alert on the cutoff day with a pre-written cancellation letter citing Section 4.3."),
        ("Step 5: Stage 4 (Auto-Cleanup)", "Automatically deletes expired reminders after 24 hours to keep your dashboard clean."),
    ])

    # =========================================================================
    # SLIDE 10: OUTPUT SCREENS (3 Clean Thumbnails With Clear Labels)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "9. Output Screens (Live Website in Action)", "[Slide 10/12]")

    card10 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.4))
    card10.fill.solid()
    card10.fill.fore_color.rgb = C_CARD_BG
    card10.line.color.rgb = C_BORDER
    card10.line.width = Pt(1.5)

    # 3 screenshot boxes side by side
    box_w = Inches(3.6)
    spacing = Inches(0.35)
    start_x = Inches(1.1)

    screen_data = [
        ("1. Dashboard Screen", "Shows ₹1,48,440 saved & countdown timers.", "screen_1.png"),
        ("2. Add Agreement Modal", "Easy popup to add contracts & cutoff dates.", "screen_2.png"),
        ("3. Live Email in Gmail", "Real email received with cancellation letter.", "screen_3.png"),
    ]

    for i, (title, desc, filename) in enumerate(screen_data):
        curr_x = start_x + i * (box_w + spacing)

        # Title & desc box
        tb = s10.shapes.add_textbox(curr_x, Inches(1.75), box_w, Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_MUTED

        # Image
        img_path = os.path.join(img_dir, filename)
        if os.path.exists(img_path):
            s10.shapes.add_picture(img_path, curr_x, Inches(2.7), width=box_w)

    # =========================================================================
    # SLIDE 11: ADVANTAGES & LIMITATIONS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "10. Advantages & Limitations (Simple & Honest)", "[Slide 11/12]")

    add_single_wide_card(s11, [
        ("Works 24/7 in the Cloud", "Monitors your cutoff dates continuously even when your laptop is turned off."),
        ("Super Fast AI Reading", "Reads long 20-page agreements in under 2 seconds using Google Gemini AI."),
        ("Real Phone SMS & Email", "Sends real text alerts directly to your mobile phone SIM card and Gmail inbox."),
        ("Auto-Writes Cancellation Letters", "Prepares formal letters citing exact sections (e.g., Section 4.3) ready to send."),
        ("Zero Hosting Costs", "Uses lightweight local JSON storage, making it completely free to run and deploy."),
        ("Current Limitation", "Currently accepts text input or presets (phone camera scanning can be added next)."),
    ])

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "11. Conclusion & Future Enhancements", "[Slide 12/12]")

    add_single_wide_card(s12, [
        ("Conclusion: Money Saved", "TermGuard stops companies from taking your money through sneaky contract rules."),
        ("Conclusion: Active Defense", "Replaces useless calendar reminders with automated 3-stage phone and email warnings."),
        ("Conclusion: Live Production", "Fully built, tested, and running live on the internet at https://termguard.onrender.com."),
        ("Future Scope: Chrome Extension", "Automatically scan Terms of Service on shopping sites before clicking 'Buy'."),
        ("Future Scope: WhatsApp Chatbot", "Receive alerts on WhatsApp and reply 'Cancel' to send cancellation letters instantly."),
        ("Future Scope: Indian Languages", "Add support for contracts in Hindi, Telugu, Tamil, and Kannada."),
    ])

    output_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Clean_Short_Presentation.pptx"
    prs.save(output_path)
    print("Clean, short 12-slide presentation created successfully at:", output_path)

if __name__ == '__main__':
    create_clean_short_presentation()
