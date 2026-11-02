import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_formal_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Formal, Premium Academic Palette
    C_BG = RGBColor(0xF8, 0xFA, 0xFC)          # Crisp light slate background
    C_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)     # Pure white container card
    C_BORDER = RGBColor(0xCB, 0xD5, 0xE1)      # Subtle formal border
    C_NAVY = RGBColor(0x1E, 0x3A, 0x8A)        # Formal deep navy blue
    C_BLUE = RGBColor(0x25, 0x63, 0xEB)        # Academic royal blue
    C_DARK = RGBColor(0x0F, 0x17, 0x2A)        # High-contrast slate dark text
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
        # Formal top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.52), Inches(11.733), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_cat = tf.paragraphs[0]
        p_cat.text = f"TERMGUARD • ACADEMIC DEFENSE REVIEW {slide_tag}".upper()
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

    def add_formal_card(slide, statements):
        # FORMAL LAYOUT - NO BULLET POINTS!
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.4))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.933), Inches(4.9))
        tf = tb.text_frame
        tf.word_wrap = True

        for idx, (label, text) in enumerate(statements):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(16)
            p.font.name = "Calibri"
            p.font.size = Pt(15.5)
            p.font.color.rgb = C_DARK

            # Bold formal keyword label with blue highlight
            r_label = p.add_run()
            r_label.text = label + "  —  "
            r_label.font.bold = True
            r_label.font.color.rgb = C_BLUE

            # Clean formal statement text
            r_text = p.add_run()
            r_text.text = text
            r_text.font.bold = False

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Formal Academic Title)
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
    p2.text = "Autonomous Contract Analysis & Multi-Channel Deadline Defense System"
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
    p4.text = "Department of Computer Science & Engineering | Academic Year 2025–2026\nLive Application: https://termguard.onrender.com"
    p4.font.name = "Calibri"
    p4.font.size = Pt(11)
    p4.font.color.rgb = C_BLUE

    # =========================================================================
    # SLIDE 2: INTRODUCTION (Formal, No Bullets)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "1. Introduction to TermGuard", "[Slide 2/12]")

    add_formal_card(s2, [
        ("Digital Contracting Context", "Modern consumer agreements for gym passes, rental flats, and subscriptions routinely exceed twenty pages of dense legal terms."),
        ("Consumer Vulnerability", "More than ninety-nine percent of consumers accept agreements without reading, entering into obligations they never fully understood."),
        ("System Definition", "TermGuard is an autonomous legal intelligence system that parses and analyzes contracts in under two seconds using Google Gemini AI."),
        ("Core Functionality", "The platform extracts hidden financial obligations and dispatches timely notifications directly to consumer mobile phones and email accounts."),
    ])

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT (Formal, No Bullets)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "2. Problem Statement", "[Slide 3/12]")

    add_formal_card(s3, [
        ("Silent Automatic Renewals", "Service providers automatically debit recurring fees from consumer accounts without requiring explicit confirmation."),
        ("Restrictive Cancellation Rules", "Agreements mandate advance written notice thirty days before renewal, otherwise all refund rights are forfeited."),
        ("Security Deposit Forfeiture", "Residential leases enforce severe penalties and deposit deductions if move-out notices are not served months in advance."),
        ("Calendar Tool Limitations", "Standard smartphone calendars only notify users on the event date, after the required legal notice window has already closed."),
        ("Measurable Financial Impact", "Average consumers lose between fifteen thousand and fifty thousand rupees annually to uncancelled subscriptions and penalties."),
    ])

    # =========================================================================
    # SLIDE 4: OBJECTIVES (Formal, No Bullets)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "3. Project Objectives", "[Slide 4/12]")

    add_formal_card(s4, [
        ("Automated Contract Analysis", "Deploy Google Gemini 1.5 Flash AI to scan agreements and isolate critical clauses in under two seconds."),
        ("Financial Risk Quantification", "Accurately compute total monetary liability and exposure at stake in Indian Rupees (INR)."),
        ("Backward Cutoff Calculation", "Automatically compute mandatory cancellation deadlines by subtracting required notice periods from renewal dates."),
        ("Three-Stage Notification Engine", "Enforce staged alerts dispatched at seven days, twenty-four hours, and on the cutoff date via Cellular SMS and Email."),
        ("Automated Dispute Generation", "Generate legally structured cancellation notices ready for submission, formally revoking auto-debit authorizations."),
    ])

    # =========================================================================
    # SLIDE 5: EXISTING VS PROPOSED (Formal, No Bullets)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "4. Existing System vs. Proposed System", "[Slide 5/12]")

    add_formal_card(s5, [
        ("Document Examination", "Manual review requires extensive time and legal expertise, whereas TermGuard extracts critical clauses in two seconds."),
        ("Alert Timing Mechanism", "Calendar applications notify on the final day when notice is already lost, while TermGuard provides advance staged warnings."),
        ("Legal Notice Drafting", "Consumers must draft cancellation letters independently, whereas TermGuard automatically generates section-specific notices."),
        ("Notification Delivery", "Application notifications are easily overlooked, while TermGuard dispatches direct cellular SMS to mobile phone SIM cards."),
        ("Operational Persistence", "Standard chatbots forget contracts once closed, whereas TermGuard maintains continuous twenty-four-seven cloud monitoring."),
    ])

    # =========================================================================
    # SLIDE 6: TECHNOLOGIES USED (Formal, No Bullets)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "5. Technologies & Tools Used", "[Slide 6/12]")

    add_formal_card(s6, [
        ("Full-Stack Framework", "Next.js 14 and React 18 power the responsive dashboard interface, server-side actions, and backend API routing."),
        ("Artificial Intelligence Core", "Google Gemini 1.5 Flash executes rapid semantic analysis, clause classification, and date extraction in under two seconds."),
        ("Telecommunications Gateway", "Twilio REST API and Fast2SMS deliver authenticated cellular text alerts directly to registered mobile devices."),
        ("Transactional Email Service", "Resend API compiles and transmits verified, responsive HTML notification templates directly to user Gmail inboxes."),
        ("Local Persistence Storage", "An atomic file-based JSON database engine ensures rapid local execution with zero third-party database hosting overhead."),
        ("Cloud Production Hosting", "Render Cloud Platform hosts the live web service with automated continuous deployment linked to our GitHub repository."),
    ])

    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE (Diagram + Clean Text)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "6. System Architecture & Execution Flow", "[Slide 7/12]")

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
    p0.text = "Operational Architecture:"
    p0.font.name = "Calibri"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = C_NAVY
    p0.space_after = Pt(14)

    steps = [
        ("Presentation Layer", "Client interface collects agreement text and displays dashboard metrics."),
        ("API Gateway Layer", "Next.js server routes sanitize text and structure prompt payloads."),
        ("Cognitive AI Engine", "Google Gemini isolates clauses, risk severity, and cutoff timestamps."),
        ("Persistence Layer", "Atomic JSON storage indexes active deadlines and countdown timers."),
        ("Telephony Dispatch", "Twilio and Resend transmit multi-channel alerts upon threshold maturity."),
    ]
    for lbl, desc in steps:
        p = tf7.add_paragraph()
        p.space_after = Pt(12)
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        r_lbl = p.add_run()
        r_lbl.text = lbl + ":  "
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = C_BLUE
        r_desc = p.add_run()
        r_desc.text = desc

    # =========================================================================
    # SLIDE 8: SYSTEM MODULES (Formal, No Bullets)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "7. System Modules Description", "[Slide 8/12]")

    add_formal_card(s8, [
        ("Executive Heads-Up Display", "Presents real-time aggregate capital protected alongside active agreement and deadline counters."),
        ("Document Intake Studio", "Processes contract text and manages pre-verified presets across gym, rental, and software categories."),
        ("Deadlines & Alerts Center", "Coordinates scheduled reminders with live countdown timers, snooze options, and manual trigger controls."),
        ("Interactive Assistant Agent", "Enables conversational contract exploration, answering specific legal inquiries in accessible language."),
        ("Telecommunications Engine", "Normalizes international phone numbers and delivers multi-channel SMS and HTML email notifications."),
        ("Activity Trust Log", "Maintains an immutable, timestamped audit trail recording all document analyses and message dispatch IDs."),
    ])

    # =========================================================================
    # SLIDE 9: METHODOLOGY & 3-STAGE WORKING (Formal, No Bullets)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "8. Methodology: Three-Stage Alert Lifecycle", "[Slide 9/12]")

    add_formal_card(s9, [
        ("Contract Ingestion & Analysis", "Gemini AI extracts predatory clauses, cutoff deadlines, and monetary liability in under two seconds."),
        ("Stage One: Seven-Day Warning", "Dispatches an advance alert seven days prior to the cutoff date to provide sufficient preparation time."),
        ("Stage Two: Twenty-Four Hour Alert", "Transmits an urgent priority notification warning that the final notice window closes tomorrow."),
        ("Stage Three: Cutoff Day Notice", "Fires on the final day, attaching an auto-formatted legal cancellation notice citing specific contract sections."),
        ("Stage Four: Post-Expiry Cleanup", "Automatically purges reminders twenty-four hours after expiration while preserving historical audit records."),
    ])

    # =========================================================================
    # SLIDE 10: OUTPUT SCREENS (Screenshots With Formal Captions)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "9. Output Screens & Verification", "[Slide 10/12]")

    card10 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.733), Inches(5.4))
    card10.fill.solid()
    card10.fill.fore_color.rgb = C_CARD_BG
    card10.line.color.rgb = C_BORDER
    card10.line.width = Pt(1.5)

    box_w = Inches(3.6)
    spacing = Inches(0.35)
    start_x = Inches(1.1)

    screen_data = [
        ("Executive Command Dashboard", "Displays aggregate protected capital and live countdown timers.", "screen_1.png"),
        ("Agreement Registration Modal", "Captures agreement terms, cutoff timestamps, and monetary risk.", "screen_2.png"),
        ("Live Inbox Email Delivery", "Verified transactional HTML alert citing Section 4.3 with legal notice.", "screen_3.png"),
    ]

    for i, (title, desc, filename) in enumerate(screen_data):
        curr_x = start_x + i * (box_w + spacing)

        tb = s10.shapes.add_textbox(curr_x, Inches(1.75), box_w, Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_MUTED

        img_path = os.path.join(img_dir, filename)
        if os.path.exists(img_path):
            s10.shapes.add_picture(img_path, curr_x, Inches(2.7), width=box_w)

    # =========================================================================
    # SLIDE 11: ADVANTAGES & LIMITATIONS (Formal, No Bullets)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "10. Advantages & Limitations", "[Slide 11/12]")

    add_formal_card(s11, [
        ("Autonomous Cloud Execution", "Monitors agreement deadlines continuously in the cloud without requiring manual user initiation."),
        ("High-Performance Analysis", "Evaluates multi-page contracts in under two seconds through Google Gemini 1.5 Flash foundation model."),
        ("Multi-Channel Telephony", "Ensures delivery through real cellular SMS and cryptographically authenticated HTML emails."),
        ("Actionable Legal Generation", "Synthesizes formal cancellation letters citing exact contract sections to protect consumer legal rights."),
        ("Zero Database Maintenance", "Employs an atomic file-based persistence model that eliminates external database hosting expenditure."),
        ("Current System Boundary", "Operates primarily on text input and English agreements, with camera OCR scanning planned for future expansion."),
    ])

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE SCOPE (Formal, No Bullets)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "11. Conclusion & Future Enhancements", "[Slide 12/12]")

    add_formal_card(s12, [
        ("Restoring Consumer Balance", "TermGuard protects consumer finances by transforming passive legal text into an automated active defense system."),
        ("Proactive Capital Protection", "Effectively prevents monetary loss arising from hidden automatic renewals and strict notice period forfeiture."),
        ("Production System Status", "The system is fully developed, tested, and operational in production at https://termguard.onrender.com."),
        ("Browser Extension Integration", "Future development includes a browser extension to intercept and analyze terms at online checkout."),
        ("Interactive Messaging Bots", "Expansion into WhatsApp Business interfaces will allow consumers to approve cancellation notices with a single reply."),
        ("Multilingual Regional Expansion", "Future releases will support legal clause extraction across major Indian regional languages."),
    ])

    output_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Formal_Presentation.pptx"
    prs.save(output_path)
    print("Formal 12-slide presentation created successfully at:", output_path)

if __name__ == '__main__':
    create_formal_presentation()
