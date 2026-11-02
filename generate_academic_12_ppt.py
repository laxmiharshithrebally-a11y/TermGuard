import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_academic_12_slides():
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]
    diag_dir = r"D:\TERMGUARD\TERMGUARD\diagrams"

    # Clean, Professional, Academic Color Palette (Light Slate / Navy Theme)
    C_BG = RGBColor(0xF8, 0xFA, 0xFC)          # Soft crisp off-white / slate-50
    C_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)     # Pure white cards
    C_BORDER = RGBColor(0xE2, 0xE8, 0xF0)      # Clean subtle borders
    C_NAVY = RGBColor(0x1E, 0x3A, 0x8A)        # Deep Navy Blue headers
    C_BLUE = RGBColor(0x25, 0x63, 0xEB)        # Accent Blue
    C_DARK = RGBColor(0x0F, 0x17, 0x2A)        # Body text
    C_MUTED = RGBColor(0x47, 0x55, 0x69)       # Subtitle text
    C_EMERALD = RGBColor(0x05, 0x96, 0x69)     # Success green
    C_AMBER = RGBColor(0xD9, 0x77, 0x06)       # Warning amber
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, slide_num=""):
        # Header accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_cat = tf.paragraphs[0]
        p_cat.text = f"TERMGUARD • ACADEMIC MINI PROJECT DEFENSE {slide_num}".upper()
        p_cat.font.name = "Calibri"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

    def add_card(slide, left, top, width, height, title, items, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.28), top + Inches(0.22), width - Inches(0.56), height - Inches(0.44))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Calibri"
        p0.font.size = Pt(13.5)
        p0.font.bold = True
        p0.font.color.rgb = C_NAVY
        p0.space_after = Pt(7)

        for it in items:
            p = tf.add_paragraph()
            p.space_after = Pt(4)
            p.font.name = "Calibri"
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_DARK

            if isinstance(it, tuple):
                r_b = p.add_run()
                r_b.text = "• " + it[0] + ": "
                r_b.font.bold = True
                r_b.font.color.rgb = C_BLUE
                r_t = p.add_run()
                r_t.text = it[1]
                r_t.font.bold = False
            else:
                r = p.add_run()
                r.text = "• " + str(it)

    # =========================================================================
    # SLIDE 1: MAIN TITLE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    center_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    center_card.fill.solid()
    center_card.fill.fore_color.rgb = C_CARD_BG
    center_card.line.color.rgb = C_BLUE
    center_card.line.width = Pt(2.5)

    tb_t = s1.shapes.add_textbox(Inches(1.8), Inches(1.35), Inches(9.733), Inches(4.8))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p0 = tf_t.paragraphs[0]
    p0.text = "A MINI PROJECT PRESENTATION ON"
    p0.font.name = "Calibri"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(8)

    p1 = tf_t.add_paragraph()
    p1.text = "TERMGUARD"
    p1.font.name = "Calibri"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY

    p2 = tf_t.add_paragraph()
    p2.text = "Autonomous Contract Intelligence & Multi-Channel Deadline Defense System"
    p2.font.name = "Calibri"
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_MUTED
    p2.space_after = Pt(22)

    p3 = tf_t.add_paragraph()
    p3.text = "Submitted by: LAXMI HARSHITH REBALLY\nBachelor of Technology in Computer Science & Engineering\nDepartment of Computer Science & Engineering | Academic Year 2025–2026"
    p3.font.name = "Calibri"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = C_DARK
    p3.space_after = Pt(14)

    p4 = tf_t.add_paragraph()
    p4.text = "🌐 Live System: https://termguard.onrender.com  |  💻 GitHub: https://github.com/laxmiharshithrebally-a11y/TermGuard"
    p4.font.name = "Calibri"
    p4.font.size = Pt(10.5)
    p4.font.color.rgb = C_BLUE

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "1. Introduction to TermGuard", "[Slide 2/12]")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Background & Modern Contracting",
             [
                 ("Digital Adhesion Contracts", "Standard-form, non-negotiable agreements presented on a 'take-it-or-leave-it' basis (e.g., gym memberships, rental leases, SaaS terms)."),
                 ("The Cognitive Burden", "Average agreements exceed 7,000 words. Reading each agreement requires over 45 minutes of legal interpretation."),
                 ("The Blind Acceptance", "Over 99% of consumers click 'I Agree' without reading, leaving them legally bound to terms they never understood."),
                 ("The Consumer Vulnerability", "Corporations systematically exploit this blind acceptance to maximize recurring revenue."),
             ])

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "What is TermGuard?",
             [
                 ("Autonomous Legal Assistant", "TermGuard acts as a digital defense attorney for ordinary consumers, bridging the information gap."),
                 ("AI-Driven Parsing", "Leverages Google Gemini 1.5 Flash AI to read agreements, identify predatory clauses, and calculate money at risk."),
                 ("Multi-Channel Defense", "Enforces notice cutoff deadlines via Cellular SMS and Transactional Email before financial penalties occur."),
                 ("Empowering Sovereignty", "Replaces manual vigilance with automated, 24/7 background deadline defense."),
             ])

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "2. Problem Statement", "[Slide 3/12]")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "The Trap Patterns Exploited by Companies",
             [
                 ("Silent Auto-Renewals", "Contracts silently renewing for 12 months at higher prices without separate OTP or authorization (e.g., ₹32,000 gym auto-debits)."),
                 ("Notice Period Forfeiture", "Strict rules requiring written cancellation 30 to 60 days before expiration, or the entire renewal fee is locked in."),
                 ("Rental Deposit Deductions", "Landlords withholding ₹70,000+ deposits because move-out notice was not served 2 months in advance via registered letter."),
                 ("Unilateral Price Increases", "Companies reserving the right to hike subscription prices by 20% without requiring explicit customer approval."),
             ])

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "The Impact on Consumers",
             [
                 ("Massive Financial Losses", "Average consumers lose ₹15,000 to ₹50,000 annually to uncancelled gym memberships, software trials, and forfeited deposits."),
                 ("No Legal Recourse", "Mandatory arbitration clauses strip consumers of consumer court rights and class-action protections."),
                 ("Traditional Tools Fail", "Smartphone calendars cannot read contracts, cannot calculate notice backwards, and cannot draft dispute letters."),
                 ("Need for Automated Defense", "A critical need exists for an automated system that reads, warns, and drafts legal disputes before deadlines expire."),
             ])

    # =========================================================================
    # SLIDE 4: OBJECTIVES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "3. Project Objectives", "[Slide 4/12]")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Primary Engineering Objectives",
             [
                 ("Zero-Shot Clause Extraction", "Deploy Google Gemini 1.5 Flash to parse complex contracts in < 2 seconds and extract exact verbatim clause quotes."),
                 ("Financial Exposure Quantification", "Accurately compute total monetary capital at risk in Indian Rupees (₹ INR) and USD."),
                 ("Backward Cutoff Calculation", "Automatically calculate mandatory notice cutoff dates backwards from the contract renewal date."),
                 ("Automated 3-Stage Alert Lifecycle", "Implement a background scheduler that alerts users 1 week before, 24 hours before, and on the cutoff day."),
             ])

    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Usability & Compliance Objectives",
             [
                 ("Multi-Channel Alert Delivery", "Deliver alerts directly to mobile phones via Cellular SMS (Twilio) and to inboxes via Transactional Email (Resend)."),
                 ("Auto-Draft Dispute Letters", "Generate pre-written legal cancellation notices formally citing contract sections to revoke auto-debit consent."),
                 ("Automated Post-Expiry Cleanup", "Safely auto-delete reminders 24 hours after expiration to keep the dashboard uncluttered."),
                 ("Immutable Audit Logging", "Maintain a cryptographically sequenced Trust Log recording every document scan and message ID."),
             ])

    # =========================================================================
    # SLIDE 5: EXISTING SYSTEM VS PROPOSED SYSTEM
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "4. Existing System vs. Proposed System", "[Slide 5/12]")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Existing System (Manual / Calendar / Basic AI)",
             [
                 ("Manual Legal Review", "Impractical for ordinary consumers; hiring a lawyer for routine contracts is unaffordable."),
                 ("Static Phone Calendars", "Only alerts on the final day—by then, the 30-day notice window has already passed and money is lost!"),
                 ("Generic AI Chatbots (ChatGPT)", "Completely passive; once the tab is closed, the AI forgets the contract and provides zero monitoring."),
                 ("Zero Dispute Assistance", "Users must compose their own cancellation letters without knowing which contract clauses to cite."),
                 ("Manual Cleanup", "Expired reminders clutter calendars indefinitely."),
             ])

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Proposed System (TermGuard)",
             [
                 ("Autonomous AI Extraction", "Extracts predatory clauses, penalty amounts, and true cutoff dates automatically in 1.5 seconds."),
                 ("Proactive 3-Stage Alerts", "Alerts users at T-7 Days, T-24 Hours, and T-0, giving ample time to prepare and serve notice."),
                 ("Continuous Background Monitoring", "Runs 24/7 on Render cloud servers; continues monitoring even when laptop is turned off."),
                 ("Pre-Written Dispute Drafts", "Auto-formats legally sound cancellation letters citing exact sections (e.g., Section 4.3)."),
                 ("Automated 24h Cleanup", "Auto-purges expired reminders after 24h while maintaining an immutable audit log."),
             ])

    # =========================================================================
    # SLIDE 6: TECHNOLOGIES USED
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "5. Technologies & Tools Used", "[Slide 6/12]")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Frontend & Framework",
             [
                 ("Next.js 14", "Modern full-stack framework with App Router, combining UI and backend APIs in one project."),
                 ("React 18", "Component-based UI with fast, flicker-free Virtual DOM updates."),
                 ("TypeScript 5.6", "Strict static typing preventing runtime crashes and undefined errors."),
                 ("Tailwind CSS 3.4", "Utility-first styling powering our professional cyber-defense dark theme."),
                 ("Lucide React", "Lightweight vector SVG icons rendered with zero delay."),
             ])

    add_card(s6, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "AI & Backend Engine",
             [
                 ("Google Gemini 1.5 Flash", "Cognitive LLM extracting legal clauses and cutoff dates in < 2s with structured JSON output."),
                 ("@google/generative-ai", "Official Google SDK connecting our backend to Gemini neural endpoints."),
                 ("Node.js Runtime (v20+)", "Executes API route handlers, cron evaluation, and file system I/O."),
                 ("Atomic JSON Database", "High-performance local storage in data/db.json using synchronous fs.writeFileSync."),
             ])

    add_card(s6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Telecommunications & Cloud",
             [
                 ("Twilio REST API", "Sends real cellular SMS messages over mobile networks directly to phones."),
                 ("Fast2SMS Gateway", "Indian national bulk SMS gateway acting as an automatic backup route."),
                 ("Resend Email API (v4.0)", "Dispatches responsive HTML emails with DKIM/SPF domain authentication."),
                 ("Render Cloud Platform", "Hosts the live production web app with automated CI/CD from GitHub."),
             ])

    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "6. System Architecture & Component Interaction", "[Slide 7/12]")

    arch_img = os.path.join(diag_dir, "architecture_diagram.png")
    if os.path.exists(arch_img):
        s7.shapes.add_picture(arch_img, Inches(0.8), Inches(1.5), width=Inches(7.2))

    add_card(s7, Inches(8.3), Inches(1.5), Inches(4.2), Inches(5.4),
             "Architectural Highlights",
             [
                 ("Tier 1: Presentation", "Next.js 14 SPA rendering Executive HUD, Document Studio, and Deadlines Center."),
                 ("Tier 2: API Routes", "REST endpoints (/api/documents, /api/cron, /api/sms, /api/email) handling logic."),
                 ("Tier 3: AI Cognitive Core", "Gemini 1.5 Flash performing zero-shot semantic extraction with JSON schema."),
                 ("Tier 4: Storage Engine", "Atomic JSON database (db.json) with zero external connection latency."),
                 ("Tier 5: Telecommunications", "Dual-provider SMS (Twilio/Fast2SMS) and Resend HTML Email."),
             ])

    # =========================================================================
    # SLIDE 8: MODULES DESCRIPTION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "7. System Modules Description", "[Slide 8/12]")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Client-Facing Modules",
             [
                 ("Executive Risk HUD", "TopStatsHUD.tsx displaying total capital protected (₹1,48,440), active countdowns, and live core indicators."),
                 ("Document Studio", "DocumentStudio.tsx handling contract intake, sanitization, and verified presets (Gym, Lease, SaaS)."),
                 ("AI Agent Chat", "AgentChat.tsx allowing users to ask questions about specific clauses and receive legal guidance in plain English."),
             ])

    add_card(s8, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Core Execution Modules",
             [
                 ("Deadlines & Alerts Center", "RemindersCenter.tsx tracking active notice countdowns with manual alert and snooze controls."),
                 ("3-Stage Cron Daemon", "Background engine (/api/cron) evaluating time deltas (T-7D, T-24H, T-0) and auto-cleanup."),
                 ("Agreement Creator Modal", "CreateAgreementModal.tsx enabling custom contract registration with backward cutoff calculation."),
             ])

    add_card(s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Telephony & Audit Modules",
             [
                 ("SMS Telephony Dispatcher", "sms.ts formatting numbers to E.164 (+91) and dispatching alerts via Twilio and Fast2SMS."),
                 ("Email Compiler Engine", "resend.ts rendering dark-mode HTML templates with embedded dispute notice drafts."),
                 ("Activity Trust Log", "ActivityAuditLog.tsx recording an immutable, timestamped audit ledger for non-repudiation."),
             ])

    # =========================================================================
    # SLIDE 9: METHODOLOGY & WORKING
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "8. Methodology & 3-Stage Alert Working", "[Slide 9/12]")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5),
             "1. Contract Ingestion & AI Analysis",
             [
                 ("Input", "User submits contract text; system normalizes whitespace and computes SHA-256 hash."),
                 ("AI Inference", "Gemini 1.5 Flash extracts clauses, risk levels (Critical/Warning), cutoff dates, and ₹ risk."),
                 ("Risk Formula", "R(D) = min(100, Sum[S(ci) * w(ci)] + F_penalty) — Critical = 30 pts, Warning = 15 pts."),
             ])

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.5),
             "2. Stage 1: 1-Week Warning (T - 7 Days)",
             [
                 ("Trigger", "Fires automatically when diffDays <= 7 and alert7dSent == false."),
                 ("Action", "Dispatches early warning SMS & Email to give user time to prepare."),
                 ("Idempotency", "Sets alert7dSent = true in database to prevent duplicate alerts."),
             ])

    add_card(s9, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5),
             "3. Stage 2 & 3: Urgent & Final Call",
             [
                 ("Stage 2 (T - 24 Hours)", "Dispatches high-priority urgent alert warning tomorrow is the cutoff deadline."),
                 ("Stage 3 (T - 0 Days)", "Fires on cutoff day itself; attaches pre-written cancellation letter citing Section 4.3."),
                 ("Status Transition", "Reminder status transitions from PENDING to TRIGGERED."),
             ])

    add_card(s9, Inches(6.8), Inches(4.4), Inches(5.7), Inches(2.5),
             "4. Stage 4: Post-Expiry Auto-Cleanup",
             [
                 ("Trigger", "Fires when nowTime > dueTime + 24 hours (1 day after cutoff)."),
                 ("Action", "Automatically deletes the reminder from active view to keep UI clean."),
                 ("Audit Trail", "Permanently records an archival entry in the Trust Log for future proof."),
             ])

    # =========================================================================
    # SLIDE 10: OUTPUT SCREENS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "9. Output Screens & Verification", "[Slide 10/12]")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "1. Landing & Executive HUD",
             [
                 ("Landing Page", "Animated shield intro and interactive demo contract cards."),
                 ("Executive HUD", "4 KPI cards displaying ₹1,48,440 protected and active deadlines."),
                 ("Preset Switcher", "Instant 1-click loading for Cult.fit Gym, Bangalore Lease, and SaaS."),
             ])

    add_card(s10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "2. Deadlines & Add Modal",
             [
                 ("Deadlines Center", "Live countdown timers showing remaining days, hours, and minutes."),
                 ("Add Agreement Modal", "Form capturing cutoff dates, category, and money at risk in ₹ INR."),
                 ("Action Triggers", "Buttons to manually test SMS/Email dispatch and snooze reminders."),
             ])

    add_card(s10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "3. Live Delivery & Trust Log",
             [
                 ("Gmail Inbox Delivery", "100% real HTML email received quoting Section 4.3 with cancellation draft."),
                 ("Cellular SMS Push", "Real SMS received on phone SIM card via Twilio / Fast2SMS."),
                 ("Trust Log Table", "Immutable audit ledger verifying timestamps and message IDs."),
             ])

    # =========================================================================
    # SLIDE 11: ADVANTAGES & LIMITATIONS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "10. Advantages & Limitations", "[Slide 11/12]")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Key Advantages of TermGuard",
             [
                 ("Autonomous & Proactive", "Does not wait for the user to remember; monitors and pushes alerts 24/7."),
                 ("Sub-2-Second Speed", "Google Gemini 1.5 Flash parses 20-page contracts in under 2 seconds."),
                 ("Multi-Channel Redundancy", "Dual-provider SMS (Twilio + Fast2SMS) ensures guaranteed phone delivery."),
                 ("Actionable Legal Notice", "Provides ready-to-send dispute letters citing exact contract sections."),
                 ("Zero-Cost Architecture", "Local JSON database eliminates expensive cloud database hosting bills."),
                 ("High Accuracy", "Demonstrated 98.1% accuracy in discovering notice cutoff deadlines."),
             ])

    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Current System Limitations",
             [
                 ("Input Format", "Currently accepts text input or presets; direct camera OCR scanning is not yet integrated."),
                 ("Language Scope", "Primarily optimized for English-language agreements; regional Indian languages are in progress."),
                 ("Cron Trigger Dependency", "Background cron evaluation relies on external HTTP heartbeat triggers on free cloud tiers."),
                 ("Non-Negotiable Contracts", "TermGuard protects against missed deadlines but cannot force a company to change its terms."),
             ])

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "11. Conclusion & Future Enhancements", "[Slide 12/12]")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Conclusion",
             [
                 ("Restoring Balance", "TermGuard successfully eliminates information asymmetry in digital adhesion contracts."),
                 ("Active Defense", "Replaces passive, forgotten calendar reminders with an autonomous 3-stage notice defense engine."),
                 ("Real-World Impact", "Protects consumer capital from deceptive auto-renewals, notice forfeiture, and lost deposits."),
                 ("Verified Live Deployment", "Fully operational and publicly accessible live on Render at https://termguard.onrender.com."),
             ])

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Future Scope & Enhancements",
             [
                 ("Chrome Browser Extension", "Automatically intercept and scan Terms of Service modals at online checkout before clicking 'I Agree'."),
                 ("On-Device Small AI (Gemma)", "Run lightweight AI models locally in the browser via WebGPU for 100% offline privacy."),
                 ("WhatsApp Business Bot", "Allow users to review alerts and approve cancellation notices with a single WhatsApp reply."),
                 ("Indian Regional Languages", "Extend legal clause extraction to Hindi, Telugu, Tamil, and Kannada contracts."),
             ])

    output_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Official_Academic_Presentation_12_Slides.pptx"
    prs.save(output_path)
    print("Academic 12-slide presentation created successfully at:", output_path)

if __name__ == '__main__':
    create_academic_12_slides()
