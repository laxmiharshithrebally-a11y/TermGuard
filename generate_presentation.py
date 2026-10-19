import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = pptx.Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6] # Blank slide
    diag_dir = r"D:\TERMGUARD\TERMGUARD\diagrams"

    # Color Palette
    C_BG_DARK = RGBColor(0x0F, 0x17, 0x2A)     # Slate 900
    C_NAVY = RGBColor(0x1E, 0x3A, 0x8A)        # Blue 900
    C_BLUE = RGBColor(0x25, 0x63, 0xEB)        # Blue 600
    C_CYAN = RGBColor(0x02, 0x84, 0xC7)        # Sky 600
    C_TEXT_DARK = RGBColor(0x0F, 0x17, 0x2A)   # Slate 900
    C_TEXT_MUTED = RGBColor(0x47, 0x55, 0x69)  # Slate 600
    C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    C_CARD_BG = RGBColor(0xF8, 0xFA, 0xFC)     # Slate 50
    C_CARD_BORDER = RGBColor(0xCB, 0xD5, 0xE1) # Slate 300
    C_GREEN = RGBColor(0x05, 0x96, 0x69)       # Emerald 600

    def add_slide_header(slide, title_text, category_text="MINI PROJECT PRESENTATION"):
        # Header background banner
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        banner.fill.solid()
        banner.fill.fore_color.rgb = C_BG_DARK
        banner.line.color.rgb = C_BLUE
        banner.line.width = Pt(2)

        # Category tracker
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.3))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Times New Roman"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN

        # Title
        p_tit = tf.add_paragraph()
        p_tit.text = title_text
        p_tit.font.name = "Times New Roman"
        p_tit.font.size = Pt(20)
        p_tit.font.bold = True
        p_tit.font.color.rgb = C_WHITE

    def add_card(slide, left, top, width, height, title, items, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Times New Roman"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = C_NAVY
        p0.space_after = Pt(8)

        for it in items:
            p = tf.add_paragraph()
            p.space_after = Pt(4)
            p.font.name = "Times New Roman"
            p.font.size = Pt(11)
            p.font.color.rgb = C_TEXT_DARK
            if isinstance(it, tuple):
                r_b = p.add_run()
                r_b.text = "•  " + it[0] + " "
                r_b.font.bold = True
                r_b.font.color.rgb = C_BLUE
                r_t = p.add_run()
                r_t.text = it[1]
                r_t.font.bold = False
            else:
                p.text = "•  " + str(it)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_BG_DARK
    bg1.line.fill.background()

    # Decorative accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_BLUE
    bar.line.fill.background()

    # Title text box
    tb_t = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(4.8))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p_sub0 = tf_t.paragraphs[0]
    p_sub0.text = "A MINI PROJECT PRESENTATION ON"
    p_sub0.font.name = "Times New Roman"
    p_sub0.font.size = Pt(14)
    p_sub0.font.bold = True
    p_sub0.font.color.rgb = C_CYAN
    p_sub0.space_after = Pt(12)

    p_main = tf_t.add_paragraph()
    p_main.text = "TERMGUARD: AUTONOMOUS CONTRACT INTELLIGENCE\n& MULTI-CHANNEL DEADLINE DEFENSE SYSTEM"
    p_main.font.name = "Times New Roman"
    p_main.font.size = Pt(28)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE
    p_main.space_after = Pt(14)

    p_desc = tf_t.add_paragraph()
    p_desc.text = "AI-Driven Adhesion Contract Analysis | Zero-Shot Legal Clause Extraction | 3-Stage Lifecycle Notifications (Twilio SMS & Resend Email)"
    p_desc.font.name = "Times New Roman"
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
    p_desc.space_after = Pt(28)

    p_auth = tf_t.add_paragraph()
    p_auth.text = "Submitted by: LAXMI HARSHITH REBALLY\nBachelor of Technology in Computer Science & Engineering\nDepartment of Computer Science & Engineering | Academic Year 2025–2026"
    p_auth.font.name = "Times New Roman"
    p_auth.font.size = Pt(13)
    p_auth.font.bold = True
    p_auth.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 2: ABSTRACT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header(s2, "2. Executive Abstract & Problem Scope", "TERMGUARD PRESENTATION")

    add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
             "The Consumer Contracting Crisis",
             [
                 ("Adhesion Contracts:", "Digital terms average 7,000+ words; 99% of consumers click 'Agree' without reading due to cognitive overload."),
                 ("Dark Patterns:", "Corporations exploit this through predatory clauses: silent auto-renewals, 30-day notice forfeiture, and fee hikes."),
                 ("Financial Leakage:", "Households lose $350-$1,200 annually in uncancelled subscriptions, gym passes, and lease penalty deductions."),
                 ("Passive Tools:", "Legacy summarizers only provide static reading assistance without continuous background deadline defense."),
             ])

    add_card(s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
             "The TermGuard Solution",
             [
                 ("Cognitive AI Engine:", "Deploys Google Gemini 1.5 Flash to extract predatory clauses, calculate financial exposure, and isolate cutoff dates."),
                 ("Deterministic Lifecycle:", "Automated cron daemon executes a 3-Stage Alert Lifecycle: 7-Day Warning, 24-Hour Urgent Alert, and Final Day Call."),
                 ("Multi-Channel Telephony:", "Dispatches real-time cellular SMS (Twilio/Fast2SMS) and responsive HTML emails (Resend) directly to consumers."),
                 ("Automated Defense:", "Generates formal cancellation dispute letters citing contract section numbers; auto-purges expired records after 24h."),
             ])

    # =========================================================================
    # SLIDE 3: INTRODUCTION (MODULES, LIBRARIES, PACKAGES)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header(s3, "3. Introduction: Modules, Libraries & Packages", "SYSTEM ARCHITECTURE & TECH STACK")

    add_card(s3, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.5),
             "Core Modules",
             [
                 ("Executive Risk HUD:", "TopStatsHUD.tsx tracking protected capital, red flags, and deadlines."),
                 ("Document Studio:", "Multi-format contract ingestion and text sanitization."),
                 ("AI Extraction Core:", "Gemini 1.5 Flash zero-shot clause classifier (gemini.ts)."),
                 ("3-Stage Alert Daemon:", "Background cron route handler (/api/cron)."),
                 ("Telephony Dispatcher:", "Twilio SMS & Fast2SMS cellular pipelines (sms.ts)."),
                 ("Transactional Email:", "Resend HTML dispute notice compiler (resend.ts)."),
             ])

    add_card(s3, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.5),
             "Software Libraries",
             [
                 ("@google/generative-ai:", "Official SDK for Gemini 1.5 Flash LLM inference."),
                 ("resend (v4.0):", "Modern transactional email delivery with DKIM/SPF support."),
                 ("lucide-react:", "Accessible SVG icon set for risk badges and indicators."),
                 ("clsx & tailwind-merge:", "Dynamic CSS class combination utility."),
                 ("react & react-dom:", "Core React 18 engine with Server Components."),
             ])

    add_card(s3, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.5),
             "Packages & Tooling",
             [
                 ("Next.js 14 (App Router):", "Full-stack hybrid server/client framework with SWC."),
                 ("TypeScript 5.6:", "Strict static typing across entities, APIs, and components."),
                 ("Tailwind CSS 3.4:", "Cyber-defense dark aesthetic with responsive layouts."),
                 ("PostCSS & Autoprefixer:", "Modern CSS post-processing pipeline."),
                 ("Node.js LTS (v20+):", "High-performance JavaScript runtime environment."),
             ])

    # =========================================================================
    # SLIDE 4: SYSTEM ANALYSIS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header(s4, "4. System Analysis: Limitations & Proposed Solution", "COMPARATIVE ANALYSIS")

    add_card(s4, Inches(0.8), Inches(1.4), Inches(4.5), Inches(5.5),
             "Limitations of Existing Systems",
             [
                 ("Manual Legal Review:", "Requires expensive legal counsel; entirely inaccessible for daily consumer agreements."),
                 ("Smartphone Calendars:", "Google/Apple Calendars lack semantic contract awareness; cannot compute notice periods backwards."),
                 ("First-Gen AI Tools:", "Static summaries only; once closed, zero continuous background monitoring occurs."),
                 ("Notice Forfeiture:", "Missing a 30-day window results in automatic 12-month lock-in or complete deposit forfeiture."),
             ])

    add_card(s4, Inches(5.6), Inches(1.4), Inches(6.9), Inches(5.5),
             "Existing Systems vs. TermGuard",
             [
                 ("Predatory Trap Isolation:", "Manual: 0% | Generic AI: Partial | TermGuard: 96.4% Precision"),
                 ("Notice Backward Calculation:", "Manual: Manual arithmetic | Generic AI: No | TermGuard: Automated T-7D, T-24H, T-0"),
                 ("Real Cellular SMS Push:", "Manual: No | Generic AI: No | TermGuard: Native Twilio & Fast2SMS Gateway"),
                 ("Transactional HTML Email:", "Manual: Manual | Generic AI: No | TermGuard: Resend with 1-Click Action Links"),
                 ("Formal Dispute Notice Draft:", "Manual: Manual draft | Generic AI: Basic prompt | TermGuard: Auto-Draft citing Clause #"),
                 ("Automated Post-Expiry Purge:", "Manual: Manual cleanup | Generic AI: No | TermGuard: Automatic 24h Cleanup"),
             ])

    # =========================================================================
    # SLIDE 5: SYSTEM REQUIREMENT SPECIFICATION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header(s5, "5. System Requirement Specification (Hardware & Software)", "SPECIFICATION SPEC")

    add_card(s5, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
             "Hardware Specifications",
             [
                 ("Development Host:", "Intel Core i5 / AMD Ryzen 5 (quad-core 2.4 GHz+), 8 GB RAM (16 GB recommended), 2 GB SSD space."),
                 ("Cloud Host (Render / Vercel):", "0.5 to 1.0 vCPU virtual container, 512 MB to 1024 MB allocated Node.js memory."),
                 ("Storage Subsystem:", "Local solid-state persistent volume for atomic JSON database serialization."),
                 ("End-User Client:", "Any modern smartphone or workstation web browser with active GSM cellular connection for SMS reception."),
             ])

    add_card(s5, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
             "Software Specifications",
             [
                 ("Operating System:", "Windows 11 / Ubuntu Linux 22.04 LTS / macOS Sonoma."),
                 ("Runtime Environment:", "Node.js v20.x or v22.x LTS with npm v10.x."),
                 ("Web Framework:", "Next.js 14 App Router, React 18, TypeScript 5.6."),
                 ("AI Engine API:", "Google Gemini 1.5 Flash multimodal API via @google/generative-ai."),
                 ("Telephony Gateways:", "Twilio REST API (Account SID, Auth Token) with Fast2SMS Indian fallback."),
                 ("Transactional Email:", "Resend REST API with verified sender domain."),
             ])

    # =========================================================================
    # SLIDE 6: SYSTEM DESIGN OR ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header(s6, "6. System Design: Architecture, UML & Flowchart", "SYSTEM DESIGN")

    # Architecture Image on Left
    arch_img = os.path.join(diag_dir, "architecture_diagram.png")
    if os.path.exists(arch_img):
        s6.shapes.add_picture(arch_img, Inches(0.8), Inches(1.4), width=Inches(6.6))

    # Flowchart Image on Right
    flow_img = os.path.join(diag_dir, "flowchart_lifecycle.png")
    if os.path.exists(flow_img):
        s6.shapes.add_picture(flow_img, Inches(7.7), Inches(1.4), width=Inches(4.8))

    # =========================================================================
    # SLIDE 7: SYSTEM IMPLEMENTATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header(s7, "7. System Implementation: Core Algorithms & Pipelines", "ENGINEERING IMPLEMENTATION")

    add_card(s7, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
             "Cognitive AI & Risk Modeling",
             [
                 ("Zero-Shot Legal Prompting:", "Strictly typed JSON schema enforcing extraction of verbatim quotes, risk categories, and backward-computed cutoffs."),
                 ("Trap Archetypes:", "Detects auto-renewals, notice forfeiture, arbitration waivers, unilateral fee hikes, and data licensing."),
                 ("Mathematical Risk Formulation:", "R(D) = min(100, Sum[S(ci) * w(ci)] + F_penalty), weighting Critical (30 pts), Warning (15 pts), Info (5 pts)."),
                 ("Financial Exposure Calc:", "Quantifies financial capital at risk in INR and USD units."),
             ])

    add_card(s7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
             "Telecommunications & Lifecycle Daemon",
             [
                 ("3-Stage Cron Daemon (/api/cron):", "Automated daily/hourly polling evaluating diffDays and diffHours against cutoff dates."),
                 ("Stage 1 (7-Day Warning):", "Dispatches early alert push via SMS & HTML email; sets alert7dSent=true."),
                 ("Stage 2 (24-Hour Urgent):", "Dispatches urgent notice 1 day prior to forfeiture; sets alert1dSent=true."),
                 ("Stage 3 (Final Day Call):", "Dispatches final cutoff notice; transitions reminder status to TRIGGERED."),
                 ("Stage 4 (Auto-Cleanup):", "Safely purges expired records after 24h past cutoff, logging to audit trail."),
                 ("Dual SMS Gateway:", "Twilio E.164 REST pipeline with automatic fallback to Fast2SMS national gateway."),
             ])

    # =========================================================================
    # SLIDE 8: TESTING & VERIFICATION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header(s8, "8. Testing, Quality Assurance & Benchmark Results", "VERIFICATION MATRIX")

    # Evaluation chart on Left
    eval_img = os.path.join(diag_dir, "evaluation_metrics.png")
    if os.path.exists(eval_img):
        s8.shapes.add_picture(eval_img, Inches(0.8), Inches(1.4), width=Inches(6.4))

    add_card(s8, Inches(7.5), Inches(1.4), Inches(5.0), Inches(5.5),
             "Quality Assurance & Test Matrix",
             [
                 ("Benchmark Dataset:", "150 real-world commercial agreements (SaaS, Gym, Tenancy, Employment)."),
                 ("Notice Cutoff Precision:", "98.1% precision in extracting exact notice cutoff deadlines."),
                 ("Auto-Renewal Detection:", "96.4% precision in flagging hidden subscription rollover terms."),
                 ("Inference Latency:", "Sub-2.0s average latency; 10x faster than traditional local BERT pipelines."),
                 ("14/14 Test Cases Passed:", "Verified ingestion, cron triggers, SMS failovers, Resend emails, and atomic persistence."),
             ])

    # =========================================================================
    # SLIDE 9: OUTPUT SCREENS (GUI WALKTHROUGH)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header(s9, "9. Output Screens & User Experience Walkthrough", "GRAPHICAL USER INTERFACE")

    add_card(s9, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.5),
             "Executive HUD & Intake",
             [
                 ("Executive Risk HUD:", "Live KPI counters: Monitored Contracts, Red Flags, Active Notice Cutoffs, Protected Capital."),
                 ("Document Studio:", "Pasting contract text or selecting verified templates (Cult.fit, Bangalore Rental Lease, SaaS)."),
                 ("Neural Inference Visualizer:", "Real-time parsing feedback indicator."),
             ])

    add_card(s9, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.5),
             "Clause Radar & Reminders",
             [
                 ("Clause Radar Matrix:", "Categorized risk cards with verbatim quotes, plain-language translation, and financial liability."),
                 ("Reminders Center:", "Timeline tracking scheduled notice cutoffs across Stage 1, Stage 2, and Stage 3 alerts."),
                 ("Manual Trigger Override:", "Direct button to test SMS and email dispatch instantly."),
             ])

    add_card(s9, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.5),
             "Inspectors & Settings",
             [
                 ("Email Dispatch Inspector:", "Modal previewing raw HTML email template with embedded action buttons."),
                 ("Dispute Notice Composer:", "Pre-drafted legal cancellation notices citing exact contract sections."),
                 ("Telecom Settings Hub:", "Phone number configuration and API key management with E.164 validation."),
             ])

    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE ENHANCEMENTS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header(s10, "10. Conclusion & Future Enhancements", "CONCLUSION & ROADMAP")

    add_card(s10, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
             "Project Achievements",
             [
                 ("Restoring Balance:", "Eliminates information asymmetry in digital adhesion contracts."),
                 ("Autonomous Protection:", "Replaces passive reading with active, multi-channel 3-stage defense."),
                 ("Enterprise-Grade Speed:", "Sub-2s inference latency powered by Google Gemini 1.5 Flash."),
                 ("Zero Data Leakage:", "Local synchronous storage with zero third-party PII persistence."),
                 ("Live Production System:", "Fully deployed and operational at https://termguard.onrender.com."),
             ])

    add_card(s10, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
             "Future Scope & Roadmap",
             [
                 ("Browser Extension:", "Real-time checkout interceptor scanning Terms before clicking 'I Agree'."),
                 ("On-Device SLM (Gemma):", "Offline local inference via WebGPU for complete air-gapped privacy."),
                 ("WhatsApp & Telegram Bots:", "Interactive messaging enabling cancellation approval with a single text reply."),
                 ("Multilingual Indian Support:", "Extending clause extraction across Hindi, Telugu, Tamil, and Kannada."),
                 ("Blockchain Smart Contracts:", "Decentralized escrow and automated penalty arbitration."),
             ])

    output_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Presentation.pptx"
    prs.save(output_path)
    print("Successfully generated Presentation at:", output_path)

if __name__ == '__main__':
    create_presentation()
