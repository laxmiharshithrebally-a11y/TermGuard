import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Academic Formal Palette
    C_BG = RGBColor(0xF8, 0xFA, 0xFC)          # Clean light slate
    C_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)     # Pure white container
    C_BORDER = RGBColor(0xCB, 0xD5, 0xE1)      # Subtle soft border
    C_NAVY = RGBColor(0x1E, 0x3A, 0x8A)        # Formal deep navy
    C_BLUE = RGBColor(0x25, 0x63, 0xEB)        # Academic royal blue
    C_DARK = RGBColor(0x0F, 0x17, 0x2A)        # High contrast slate
    C_MUTED = RGBColor(0x64, 0x74, 0x8B)       # Secondary slate

    diag_dir = r"D:\TERMGUARD\TERMGUARD\diagrams"
    img_dir = r"D:\TERMGUARD\TERMGUARD\diagrams\slides_img"

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, section_tag=""):
        # Top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.52), Inches(11.733), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p_tag = tf.paragraphs[0]
        p_tag.text = f"TERMGUARD | MINI PROJECT PRESENTATION | {section_tag}".upper()
        p_tag.font.name = "Calibri"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

    def add_card(slide, statements):
        # Full width clean container card - strictly NO bullet points
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.58), Inches(11.733), Inches(5.35))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(10.933), Inches(4.85))
        tf = tb.text_frame
        tf.word_wrap = True

        for idx, (label, text) in enumerate(statements):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(20)
            p.font.name = "Calibri"
            p.font.size = Pt(15.5)
            p.font.color.rgb = C_DARK

            # Bold keyword label in royal blue
            r_label = p.add_run()
            r_label.text = label + "  —  "
            r_label.font.bold = True
            r_label.font.color.rgb = C_BLUE

            # Clear simple English explanation
            r_text = p.add_run()
            r_text.text = text
            r_text.font.bold = False

    # =========================================================================
    # SLIDE 1: TITLE (Item 1)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_CARD_BG
    card1.line.color.rgb = C_BLUE
    card1.line.width = Pt(2.5)

    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.35), Inches(10.333), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "MINI PROJECT PRESENTATION"
    p0.font.name = "Calibri"
    p0.font.size = Pt(14)
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
    p2.text = "Autonomous Contract Analysis & Multi-Channel Deadline Defense System"
    p2.font.name = "Calibri"
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_MUTED
    p2.space_after = Pt(26)

    p3 = tf1.add_paragraph()
    p3.text = "PRESENTED BY:\n1. REBALLY LAXMI HARSHITH  (Roll No: 201224539090)\n2. SHUBHAM PRADHAN"
    p3.font.name = "Calibri"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = C_DARK
    p3.space_after = Pt(14)

    p4 = tf1.add_paragraph()
    p4.text = "Department of Computer Science & Engineering | Academic Year 2025–2026\nLive Application: https://termguard.onrender.com"
    p4.font.name = "Calibri"
    p4.font.size = Pt(11)
    p4.font.color.rgb = C_BLUE

    # =========================================================================
    # SLIDE 2: ABSTRACT (Item 2)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Abstract", "Item 2")
    add_card(s2, [
        ("Project Purpose", "TermGuard is an automated contract intelligence system created to protect consumers from hidden fees, unfair lock-in clauses, and missed renewal dates."),
        ("Working Principle", "The system analyzes digital contracts, calculates exact cancellation deadlines, and tracks them continuously in the background without manual effort."),
        ("Automated Defense", "When a deadline approaches, TermGuard sends timely email reminders with ready-made dispute letters so users can cancel agreements quickly and effortlessly."),
        ("Consumer Value", "It bridges the gap between ordinary consumers and complex legal fine print, preventing unwanted bank deductions and saving hard-earned money.")
    ])

    # =========================================================================
    # SLIDE 3: INTRODUCTION (Item 3)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Introduction", "Item 3")
    add_card(s3, [
        ("Current Scenario", "Everyday users sign lengthy digital agreements for gym passes, software subscriptions, rental leases, and streaming services without reading the terms."),
        ("The Fine Print Dilemma", "These contracts frequently contain strict notice periods and automatic renewal clauses that trap users into unwanted recurring payments."),
        ("The TermGuard Solution", "TermGuard acts as a 24/7 personal contract assistant that reads agreements, extracts vital dates, and alerts consumers before money is debited."),
        ("Practical Utility", "It simplifies complicated legal wording into plain language so that anyone can understand their rights without paying for legal advice.")
    ])

    # =========================================================================
    # SLIDE 4: MODULES, LIBRARIES & PACKAGES (Item 3.1, 3.2, 3.3)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Introduction  —  Modules, Libraries & Packages", "Item 3.1, 3.2, 3.3")
    add_card(s4, [
        ("System Modules", "Document Upload & Parser Module, AI Risk Scoring Engine, Scheduled Alert Notification Engine, and One-Click Dispute Letter Generator."),
        ("Frontend Libraries", "Next.js 14 App Router, React 18, Tailwind CSS for clean responsive user interfaces, and Lucide React Icons for visual indicators."),
        ("Backend Packages", "Node-cron for autonomous background scheduling, Resend API for email delivery, and PDF-Parse for reading document files."),
        ("Architecture Integration", "The modern stack ensures fast server-side rendering, secure API routes, and reliable daily execution on production cloud servers.")
    ])

    # =========================================================================
    # SLIDE 5: SYSTEM ANALYSIS — LIMITATIONS & MOTIVATION (Item 4)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "System Analysis  —  Limitations & Motivation", "Item 4")
    add_card(s5, [
        ("Limitations of Manual Ways", "Consumers rarely read 20-page legal documents, and standard calendar reminders require tedious manual date entry and calculation."),
        ("Forgotten Notice Windows", "Most subscription contracts require a 15 to 30 day cancellation notice prior to renewal, which consumers easily miss."),
        ("High Cost of Legal Help", "Hiring a lawyer to review ordinary consumer subscriptions or draft formal cancellation letters is impractical and expensive."),
        ("Project Motivation", "To build a free, autonomous software tool that levels the legal playing field for ordinary consumers and prevents accidental financial losses.")
    ])

    # =========================================================================
    # SLIDE 6: SYSTEM ANALYSIS — EXISTING & PROPOSED SYSTEMS (Item 4)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "System Analysis  —  Existing & Proposed Systems", "Item 4")
    add_card(s6, [
        ("Existing System", "Completely manual process where users must read dense contracts, calculate notice dates in their head, and compose dispute letters from scratch."),
        ("Existing System Weakness", "Prone to human forgetfulness, lack of legal understanding, and missed deadlines leading to non-refundable account charges."),
        ("Proposed System", "An automated web solution that analyzes contract text, scores contract risk from 0 to 100, monitors notice dates, and dispatches automated alerts."),
        ("Key Innovation", "Provides ready-to-send formal legal dispute letters directly inside the reminder email, allowing immediate action with zero legal expertise.")
    ])

    # =========================================================================
    # SLIDE 7: SYSTEM REQUIREMENT SPECIFICATION (Item 5)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "System Requirement Specification", "Item 5")
    add_card(s7, [
        ("Hardware Requirements", "Intel or AMD Dual-Core Processor (2.0 GHz or higher), 4 GB RAM minimum (8 GB recommended), and 10 GB free hard disk storage."),
        ("Software Environment", "Node.js runtime environment (version 18 or above), npm package manager, and Git version control system."),
        ("Operating System Support", "Platform independent architecture that runs smoothly across Windows 10/11, Linux distributions, and macOS."),
        ("Client Browser Support", "Accessible on any modern web browser including Google Chrome, Microsoft Edge, Mozilla Firefox, and Safari on mobile or desktop.")
    ])

    # =========================================================================
    # SLIDE 8: SYSTEM DESIGN — ARCHITECTURE (Item 6)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "System Design  —  Architecture", "Item 6")

    # Left text card
    card_arch = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.58), Inches(5.6), Inches(5.35))
    card_arch.fill.solid()
    card_arch.fill.fore_color.rgb = C_CARD_BG
    card_arch.line.color.rgb = C_BORDER
    card_arch.line.width = Pt(1.5)

    tb_arch = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.9))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    arch_points = [
        ("Presentation Layer", "Next.js dashboard with responsive user interface for viewing active contracts, countdown timers, and risk scores."),
        ("Application Layer", "API route handlers that manage contract parsing, risk evaluation algorithms, and dispute letter formatting."),
        ("Automation Layer", "Autonomous Node-cron background service running 24/7 to calculate notice days remaining."),
        ("Delivery Layer", "Resend API integration that delivers automated warning emails directly into user inboxes.")
    ]
    for idx, (lbl, txt) in enumerate(arch_points):
        p = tf_arch.paragraphs[0] if idx == 0 else tf_arch.add_paragraph()
        p.space_after = Pt(14)
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.color.rgb = C_DARK

        r_l = p.add_run()
        r_l.text = lbl + "  —  "
        r_l.font.bold = True
        r_l.font.color.rgb = C_BLUE

        r_t = p.add_run()
        r_t.text = txt

    # Right side: Architecture diagram image
    arch_img_path = os.path.join(diag_dir, "architecture_diagram.png")
    if os.path.exists(arch_img_path):
        s8.shapes.add_picture(arch_img_path, Inches(6.6), Inches(1.58), Inches(5.933), Inches(5.35))

    # =========================================================================
    # SLIDE 9: SYSTEM DESIGN — UML DIAGRAMS (Item 6.1)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "System Design  —  UML Diagrams", "Item 6.1")

    # Left text card
    card_uml = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.58), Inches(5.6), Inches(5.35))
    card_uml.fill.solid()
    card_uml.fill.fore_color.rgb = C_CARD_BG
    card_uml.line.color.rgb = C_BORDER
    card_uml.line.width = Pt(1.5)

    tb_uml = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.9))
    tf_uml = tb_uml.text_frame
    tf_uml.word_wrap = True

    uml_points = [
        ("Use Case Model", "Represents consumer interactions such as uploading agreements, inspecting risk levels, receiving email alerts, and downloading dispute notices."),
        ("Sequence Execution", "Illustrates step-by-step communication between the frontend client, Next.js server actions, cron timers, and the email gateway."),
        ("Class Structure", "Defines the core data entities including Agreement records, Deadline calculation entities, Risk Score models, and Alert payloads.")
    ]
    for idx, (lbl, txt) in enumerate(uml_points):
        p = tf_uml.paragraphs[0] if idx == 0 else tf_uml.add_paragraph()
        p.space_after = Pt(20)
        p.font.name = "Calibri"
        p.font.size = Pt(14.5)
        p.font.color.rgb = C_DARK

        r_l = p.add_run()
        r_l.text = lbl + "  —  "
        r_l.font.bold = True
        r_l.font.color.rgb = C_BLUE

        r_t = p.add_run()
        r_t.text = txt

    # Right side: UML Use Case Diagram
    uml_img_path = os.path.join(diag_dir, "uml_use_case_diagram.png")
    if os.path.exists(uml_img_path):
        s9.shapes.add_picture(uml_img_path, Inches(6.6), Inches(1.58), Inches(5.933), Inches(5.35))

    # =========================================================================
    # SLIDE 10: SYSTEM DESIGN — FLOW-CHART (Item 6.2)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "System Design  —  Flow-chart", "Item 6.2")

    # Left text card
    card_flow = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.58), Inches(5.6), Inches(5.35))
    card_flow.fill.solid()
    card_flow.fill.fore_color.rgb = C_CARD_BG
    card_flow.line.color.rgb = C_BORDER
    card_flow.line.width = Pt(1.5)

    tb_flow = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.9))
    tf_flow = tb_flow.text_frame
    tf_flow.word_wrap = True

    flow_points = [
        ("Step 1: Document Input", "User submits agreement text or uploads a contract document into the web interface."),
        ("Step 2: Risk & Date Extraction", "System parses the text to identify renewal dates, notice windows, and hidden trap clauses."),
        ("Step 3: Background Tracking", "The Node-cron background service checks remaining notice days every 24 hours."),
        ("Step 4: Proactive Alert Dispatch", "Dispatches automated emails at 3 days, 1 day, and on deadline day with ready-to-use dispute letters.")
    ]
    for idx, (lbl, txt) in enumerate(flow_points):
        p = tf_flow.paragraphs[0] if idx == 0 else tf_flow.add_paragraph()
        p.space_after = Pt(16)
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.color.rgb = C_DARK

        r_l = p.add_run()
        r_l.text = lbl + "  —  "
        r_l.font.bold = True
        r_l.font.color.rgb = C_BLUE

        r_t = p.add_run()
        r_t.text = txt

    # Right side: Flowchart diagram image
    flow_img_path = os.path.join(diag_dir, "flowchart_lifecycle.png")
    if os.path.exists(flow_img_path):
        s10.shapes.add_picture(flow_img_path, Inches(6.6), Inches(1.58), Inches(5.933), Inches(5.35))

    # =========================================================================
    # SLIDE 11: SYSTEM IMPLEMENTATION (Item 7)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "System Implementation", "Item 7")
    add_card(s11, [
        ("Interactive Web Dashboard", "Constructed using Next.js 14 and React 18, providing a clean user interface to manage contracts, review countdowns, and inspect risk metrics."),
        ("Risk Scoring Implementation", "Evaluates contracts against consumer protection rules to compute an objective risk score from 0 to 100 based on clause severity."),
        ("Autonomous Background Engine", "Implemented with Node-cron to execute midnight checks, compare calendar dates, and verify active cancellation windows."),
        ("Automated Dispute Generation", "Dynamically generates formal cancellation notices populated with user details, agreement name, and relevant consumer law citations.")
    ])

    # =========================================================================
    # SLIDE 12: TESTING (Item 8)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "Testing", "Item 8")
    add_card(s12, [
        ("Unit Testing", "Tested individual modules including date difference logic, risk calculation formulas, and document text extraction using sample contracts."),
        ("Integration Testing", "Verified reliable communication between Next.js server actions, backend data storage, and external email delivery services."),
        ("Functional Verification", "Validated that background cron jobs run accurately and trigger alerts at the exact scheduled notice intervals without fail."),
        ("Email Delivery Validation", "Tested email alerts across multiple email providers to ensure clean formatting and accurate dispute letter attachments.")
    ])

    # =========================================================================
    # SLIDE 13: OUTPUT SCREENS (GUI SCREEN SHOTS) (Item 9)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_header(s13, "Output Screens (GUI Screen Shots)", "Item 9")

    # 3 screenshot cards side-by-side
    screens = [
        ("screen_1.png", "1. Active Dashboard", "Shows active agreements, countdown timers, and risk ratings."),
        ("screen_2.png", "2. Add Agreement Modal", "Simple input interface for submitting contract text and renewal dates."),
        ("screen_3.png", "3. Delivered Email Alert", "Real Gmail notification containing the ready-to-send dispute letter.")
    ]

    card_w = Inches(3.75)
    card_h = Inches(5.35)
    gap = Inches(0.24)
    start_x = Inches(0.8)

    for i, (fn, stitle, sdesc) in enumerate(screens):
        x = start_x + i * (card_w + gap)

        # Container card
        scard = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.58), card_w, card_h)
        scard.fill.solid()
        scard.fill.fore_color.rgb = C_CARD_BG
        scard.line.color.rgb = C_BORDER
        scard.line.width = Pt(1.5)

        # Image
        img_p = os.path.join(img_dir, fn)
        if os.path.exists(img_p):
            s13.shapes.add_picture(img_p, x + Inches(0.15), Inches(1.75), card_w - Inches(0.3), Inches(3.2))

        # Description text below screenshot
        stb = s13.shapes.add_textbox(x + Inches(0.15), Inches(5.1), card_w - Inches(0.3), Inches(1.6))
        stf = stb.text_frame
        stf.word_wrap = True

        sp1 = stf.paragraphs[0]
        sp1.text = stitle
        sp1.font.name = "Calibri"
        sp1.font.size = Pt(14)
        sp1.font.bold = True
        sp1.font.color.rgb = C_NAVY
        sp1.space_after = Pt(4)

        sp2 = stf.add_paragraph()
        sp2.text = sdesc
        sp2.font.name = "Calibri"
        sp2.font.size = Pt(12)
        sp2.font.color.rgb = C_DARK

    # =========================================================================
    # SLIDE 14: CONCLUSION (Item 10)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_bg(s14)
    add_header(s14, "Conclusion", "Item 10")
    add_card(s14, [
        ("Project Summary", "TermGuard successfully delivers an autonomous contract defense system that protects everyday consumers from fine print traps and surprise renewal fees."),
        ("Key Accomplishment", "Developed and deployed a full-stack web application combining document scanning, deadline monitoring, and automated legal dispute drafting."),
        ("Practical Impact", "Eliminates financial losses caused by forgotten notice periods, providing peace of mind to users without requiring expensive legal consultations."),
        ("Future Enhancements", "Planned additions include instant WhatsApp alert integration and a dedicated browser extension for scanning terms during online checkout.")
    ])

    out_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Mini_Project_Presentation.pptx"
    prs.save(out_path)
    print(f"SUCCESS: Saved presentation to {out_path}")
    print(f"Total slides: {len(prs.slides)}")

if __name__ == "__main__":
    build_presentation()
