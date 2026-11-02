import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_simple_clear_presentation():
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Clean, Professional, Academic Theme (Light & Elegant, NOT sci-fi AI)
    C_BG = RGBColor(0xF8, 0xFA, 0xFC)          # Soft crisp off-white / slate-50
    C_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)     # Pure white cards
    C_BORDER = RGBColor(0xE2, 0xE8, 0xF0)      # Subtle border
    C_NAVY = RGBColor(0x1E, 0x3A, 0x8A)        # Primary deep navy blue
    C_BLUE = RGBColor(0x25, 0x63, 0xEB)        # Accent blue
    C_DARK = RGBColor(0x0F, 0x17, 0x2A)        # Main text
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

    def add_header(slide, title_text, category="TERMGUARD • MINI PROJECT REVIEW"):
        # Header accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
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

    def add_card(slide, left, top, width, height, title, items, badge=""):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.25), width - Inches(0.6), height - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Calibri"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = C_NAVY
        p0.space_after = Pt(8)

        for it in items:
            p = tf.add_paragraph()
            p.space_after = Pt(5)
            p.font.name = "Calibri"
            p.font.size = Pt(11)
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
    # SLIDE 1: TITLE SLIDE (Clean, Professional Academic Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Center card container
    center_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    center_card.fill.solid()
    center_card.fill.fore_color.rgb = C_CARD_BG
    center_card.line.color.rgb = C_BLUE
    center_card.line.width = Pt(2.5)

    tb_t = s1.shapes.add_textbox(Inches(1.8), Inches(1.4), Inches(9.733), Inches(4.7))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p0 = tf_t.paragraphs[0]
    p0.text = "A MINI PROJECT PRESENTATION ON"
    p0.font.name = "Calibri"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(10)

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
    p2.space_after = Pt(24)

    p3 = tf_t.add_paragraph()
    p3.text = "Submitted by: LAXMI HARSHITH REBALLY\nBachelor of Technology in Computer Science & Engineering\nDepartment of Computer Science & Engineering | Academic Year 2025–2026"
    p3.font.name = "Calibri"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = C_DARK
    p3.space_after = Pt(14)

    p4 = tf_t.add_paragraph()
    p4.text = "🌐 Live Website: https://termguard.onrender.com  |  💻 GitHub: https://github.com/laxmiharshithrebally-a11y/TermGuard"
    p4.font.name = "Calibri"
    p4.font.size = Pt(10.5)
    p4.font.color.rgb = C_BLUE

    # =========================================================================
    # SLIDE 2: THE PROBLEM STATEMENT (Simple Real-World Context)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "1. The Problem: Hidden Contract Traps & Financial Loss")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "The Consumer Reality",
             [
                 ("Extremely Long Contracts", "Modern terms of service and leases average 7,000+ words (over 45 minutes of legal reading)."),
                 ("Nobody Reads Them", "Over 99% of users click 'I Agree' without reading due to cognitive overload."),
                 ("Asymmetric Power", "Companies use 'take-it-or-leave-it' contracts where consumers have zero negotiation power."),
                 ("Huge Financial Leakage", "Average households lose ₹15,000 to ₹50,000 annually to forgotten renewals, gym fees, and lost deposits."),
             ])

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Common Traps Used by Companies",
             [
                 ("Silent Auto-Renewals", "Recurring charges auto-debited without warning (e.g., annual gym pass silently charging ₹32,000)."),
                 ("Strict Notice Forfeiture", "Requiring written cancellation exactly 30 or 60 days before renewal, or else you are locked in for another year."),
                 ("Lost Rental Deposits", "Landlords keeping ₹70,000 deposits because a move-out notice was not sent 2 months in advance via registered letter."),
                 ("Calendar Apps Fail", "Standard smartphone calendars cannot read legal documents or calculate notice periods backwards."),
             ])

    # =========================================================================
    # SLIDE 3: EXISTING SYSTEM VS TERMGUARD
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "2. Existing Solutions vs. Proposed TermGuard Platform")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Limitations of Existing Methods",
             [
                 ("Manual Reading", "Requires legal expertise; completely impractical for ordinary consumers to read 20 pages."),
                 ("Smartphone Calendars", "Only alerts on the final day—by then, notice cutoff is already missed and money is lost!"),
                 ("Generic AI Chatbots", "Completely passive; once you close the chat tab, the AI forgets the contract and provides zero monitoring."),
                 ("Zero Legal Notice Help", "Users don't know how to legally draft formal cancellation letters citing exact clauses."),
             ])

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "The TermGuard Solution",
             [
                 ("Automatic AI Reading", "Google Gemini AI scans contracts in 2 seconds and extracts hidden traps and true cutoff dates."),
                 ("3-Stage Advance Alerts", "Alerts users at 7 Days, 24 Hours, and Final Day so you have time to act before cutoff."),
                 ("Real SMS & Email", "Delivers over-the-air Cellular SMS to phone and HTML emails directly to your Gmail inbox."),
                 ("Pre-Written Dispute Letters", "Auto-formats ready-to-send cancellation notices citing exact contract section numbers."),
             ])

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & TECH STACK (Simple & Clean)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "3. System Architecture & Technology Stack")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Frontend & Framework",
             [
                 ("Next.js 14", "Modern full-stack framework handling both UI and backend APIs in one repository."),
                 ("React 18", "Component-based UI with fast, flicker-free state updates."),
                 ("Tailwind CSS", "Clean, responsive styling with professional dark-theme aesthetic."),
                 ("TypeScript", "Strict static typing that prevents runtime crashes."),
             ])

    add_card(s4, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "AI & Backend APIs",
             [
                 ("Google Gemini 1.5 Flash", "AI model that reads contracts, finds traps, and extracts cutoff dates in < 2s."),
                 ("Node.js Runtime", "Executes server-side API routes and background processing."),
                 ("JSON Database", "Local atomic storage in data/db.json (zero cost, instant cold-starts)."),
                 ("Render Cloud", "Hosts the live production web app with automated CI/CD from GitHub."),
             ])

    add_card(s4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Telecommunications",
             [
                 ("Twilio REST API", "Sends real cellular SMS messages over mobile towers to user phones."),
                 ("Fast2SMS Gateway", "Indian national bulk SMS gateway serving as automatic backup route."),
                 ("Resend Email API", "Dispatches verified HTML emails with DKIM/SPF domain authentication."),
                 ("Audit Trust Log", "Immutable timestamped ledger recording all actions."),
             ])

    # =========================================================================
    # SLIDE 5: HOW TERMGUARD WORKS (Simple Step-by-Step Flow)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "4. Operational Workflow: From Upload to Alert")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.3),
             "Step 1: Ingestion",
             [
                 ("Contract Upload", "User pastes contract text or selects a verified preset (Gym, Lease, SaaS)."),
                 ("Sanitization", "System cleans text and generates SHA-256 fingerprint."),
                 ("Category Tagging", "Tags contract as Subscription, Lease, Insurance, etc."),
             ])

    add_card(s5, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.3),
             "Step 2: AI Analysis",
             [
                 ("Gemini AI Core", "Model scans text using zero-shot legal prompt."),
                 ("Trap Discovery", "Flags auto-debit rules, notice periods, and price hikes."),
                 ("Risk Scoring", "Computes 0-100 Risk Score and ₹ liability at stake."),
             ])

    add_card(s5, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.3),
             "Step 3: Staging",
             [
                 ("Cutoff Calculation", "Calculates exact notice deadline backwards from renewal."),
                 ("Save to Database", "Atomically stores reminder in data/db.json."),
                 ("Timer Activation", "Live countdown timer begins monitoring on dashboard."),
             ])

    add_card(s5, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.3),
             "Step 4: Dispatch",
             [
                 ("Cron Scheduler", "Background daemon checks active dates periodically."),
                 ("Multi-Channel Push", "Dispatches real Cellular SMS and HTML Email."),
                 ("Auto-Cleanup", "Automatically deletes reminder 24h after cutoff."),
             ])

    # =========================================================================
    # SLIDE 6: THE 3-STAGE ALERT LIFECYCLE (Core Feature)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "5. The 3-Stage Notice Alert Lifecycle & Auto-Cleanup")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5),
             "Stage 1: 1-Week Early Warning (T - 7 Days)",
             [
                 ("Trigger", "Fires automatically 7 days before the notice cutoff deadline."),
                 ("Purpose", "Gives the user ample time to prepare a cancellation notice without rushing."),
                 ("Channels", "Dispatches early alert via Cellular SMS and Transactional Email."),
             ])

    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.5),
             "Stage 2: 24-Hour Urgent Alert (T - 24 Hours)",
             [
                 ("Trigger", "Fires exactly 1 day before the forfeiture window closes."),
                 ("Purpose", "High-priority warning indicating tomorrow is the final day to act."),
                 ("Channels", "Urgent mobile SMS push + High-priority HTML inbox notification."),
             ])

    add_card(s6, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5),
             "Stage 3: Final Cutoff Notice (T - 0 Days)",
             [
                 ("Trigger", "Fires on the exact deadline date itself."),
                 ("Purpose", "Final call to prevent automatic credit card debit or deposit forfeiture."),
                 ("Action", "Provides a pre-written formal legal notice ready to send immediately."),
             ])

    add_card(s6, Inches(6.8), Inches(4.4), Inches(5.7), Inches(2.5),
             "Stage 4: Post-Expiry Auto-Cleanup (T + 24 Hours)",
             [
                 ("Trigger", "Fires 24 hours after the cutoff deadline has completely passed."),
                 ("Purpose", "Safely purges expired deadlines from the dashboard to keep the UI clean."),
                 ("Audit Trail", "Archives a permanent record in the Trust Log for future proof."),
             ])

    # =========================================================================
    # SLIDE 7: REAL-WORLD CONTRACTS IN TERMGUARD
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "6. Real-World Demonstrations Built into TermGuard")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Cult.fit & Gold's Gym",
             [
                 ("Contract Value", "₹29,990 annual fitness pass."),
                 ("Hidden Trap", "Section 4.1 & 4.3: Silently auto-renews at ₹32,000 with zero refund."),
                 ("Notice Rule", "Requires written notice at least 30 days before renewal (Sept 14)."),
                 ("TermGuard Action", "Alerts user in advance and saves ₹32,000 from unwanted debit."),
             ])

    add_card(s7, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Bangalore Apartment Lease",
             [
                 ("Contract Value", "₹70,000 security deposit on 2BHK flat."),
                 ("Hidden Trap", "Section 3.2: Forfeits entire ₹70,000 deposit if 2-month notice is missed."),
                 ("Notice Rule", "Requires written registered post notice 60 days before move-out."),
                 ("TermGuard Action", "Calculates 60-day backward cutoff and alerts tenant to protect deposit."),
             ])

    add_card(s7, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Cloud SaaS Subscription",
             [
                 ("Contract Value", "₹48,000 annual business software plan."),
                 ("Hidden Trap", "Section 5.2: Auto-rolls over for another 12 months with price increase."),
                 ("Notice Rule", "Requires support opt-out ticket submitted 30 days prior."),
                 ("TermGuard Action", "Flags unilateral price change and generates formal opt-out ticket text."),
             ])

    # =========================================================================
    # SLIDE 8: TELECOMMUNICATIONS & PRE-WRITTEN LEGAL NOTICE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "7. Live Alert Delivery & Pre-Written Dispute Letters")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Multi-Channel Telecommunications",
             [
                 ("Cellular SMS via Twilio", "Delivers over-the-air text messages directly to mobile phones using international E.164 (+91) format."),
                 ("Fast2SMS Indian Backup", "Automatic failover ensuring instant SMS delivery on Indian telecom carriers."),
                 ("HTML Email via Resend", "Delivers responsive dark-mode alert emails directly to Gmail inboxes with 100% deliverability (uses DKIM & SPF)."),
                 ("Immutable Trust Log", "Cryptographically timestamps every document upload and message ID for legal proof."),
             ])

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Pre-Written Legal Cancellation Notice",
             [
                 ("Auto-Generated", "TermGuard automatically drafts formal cancellation letters ready to copy and send."),
                 ("Clause Citation", "Directly cites the exact contract section (e.g., 'As per Section 4.3...')."),
                 ("Revokes Auto-Debit", "Formally revokes payment authorization, preventing banks from allowing recurring debits."),
                 ("Protects Consumer", "Provides concrete legal evidence in writing in case of future dispute."),
             ])

    # =========================================================================
    # SLIDE 9: TESTING & QUALITY ASSURANCE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "8. System Testing & Benchmark Verification")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Key Test Scenarios Executed",
             [
                 ("Contract Upload & Sanitization", "Tested with messy text, Unicode characters, and long leases. Result: PASS."),
                 ("Auto-Renewal Detection", "Tested with Section 4.3 30-day notice rule. Result: PASS (Extracted ₹32,000 risk)."),
                 ("3-Stage Alert Timing", "Tested T-7D, T-24H, and T-0 cron evaluation logic. Result: PASS."),
                 ("SMS & Email Dispatch", "Verified live delivery to real mobile phone and Gmail inbox. Result: PASS."),
                 ("Stage 4 Auto-Cleanup", "Verified 24h expired reminders are purged cleanly from UI. Result: PASS."),
             ])

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Evaluation Results & Highlights",
             [
                 ("14 / 14 Test Cases Passed", "All unit, integration, and end-to-end test cases passed without failure."),
                 ("98.1% Cutoff Accuracy", "Near-perfect precision in discovering exact notice deadlines in legal text."),
                 ("Sub-2-Second Speed", "Inference latency under 2 seconds powered by Google Gemini 1.5 Flash."),
                 ("Live Production System", "Fully deployed, verified, and operational at https://termguard.onrender.com."),
             ])

    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "9. Conclusion & Future Enhancements")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Project Conclusion",
             [
                 ("Empowering Consumers", "Eliminates unfair information asymmetry in 20-page adhesion contracts."),
                 ("Active vs Passive", "Replaces useless static calendar reminders with an automated 3-stage defense system."),
                 ("Verifiable Delivery", "Successfully bridges AI intelligence with real-world telecommunications (SMS & Email)."),
                 ("Zero-Cost Architecture", "High performance, zero external database costs, and fully open-source stack."),
             ])

    add_card(s10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Future Scope & Enhancements",
             [
                 ("Chrome Browser Extension", "Automatically scans Terms of Service modals during checkout before user clicks 'I Agree'."),
                 ("On-Device Small AI (Gemma)", "Running lightweight models locally in the browser using WebGPU for 100% offline privacy."),
                 ("WhatsApp Business Bot", "Enabling users to approve and send cancellation notices with a single WhatsApp reply."),
                 ("Indian Regional Languages", "Supporting legal contract extraction in Hindi, Telugu, Tamil, and Kannada."),
             ])

    output_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Simple_Clear_Presentation.pptx"
    prs.save(output_path)
    print("Simple, clear presentation created successfully at:", output_path)

if __name__ == '__main__':
    create_simple_clear_presentation()
