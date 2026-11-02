import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_super_simple_ppt():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Clean, simple theme colors (Off-white background, deep navy headers, pure white cards)
    C_BG = RGBColor(0xF8, 0xFA, 0xFC)
    C_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)
    C_BORDER = RGBColor(0xE2, 0xE8, 0xF0)
    C_NAVY = RGBColor(0x1E, 0x3A, 0x8A)
    C_BLUE = RGBColor(0x25, 0x63, 0xEB)
    C_DARK = RGBColor(0x0F, 0x17, 0x2A)
    C_MUTED = RGBColor(0x47, 0x55, 0x69)

    diag_dir = r"D:\TERMGUARD\TERMGUARD\diagrams"
    img_dir = r"D:\TERMGUARD\TERMGUARD\diagrams\slides_img"

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, slide_badge=""):
        # Top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_cat = tf.paragraphs[0]
        p_cat.text = f"TERMGUARD • MINI PROJECT REVIEW {slide_badge}".upper()
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

    def add_card(slide, left, top, width, height, title, items):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.28), top + Inches(0.22), width - Inches(0.56), height - Inches(0.44))
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
            p.space_after = Pt(6)
            p.font.name = "Calibri"
            p.font.size = Pt(11.5)
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
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_CARD_BG
    card1.line.color.rgb = C_BLUE
    card1.line.width = Pt(2.5)

    tb1 = s1.shapes.add_textbox(Inches(1.8), Inches(1.35), Inches(9.733), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "A MINI PROJECT PRESENTATION ON"
    p0.font.name = "Calibri"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "TERMGUARD"
    p1.font.name = "Calibri"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY

    p2 = tf1.add_paragraph()
    p2.text = "Smart Contract Reader & Automated Deadline Alert System"
    p2.font.name = "Calibri"
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_MUTED
    p2.space_after = Pt(22)

    p3 = tf1.add_paragraph()
    p3.text = "SUBMITTED BY:\n1. REBALLY LAXMI HARSHITH  (Roll No: 201224539090)\n2. SHUBHAM PRADHAN"
    p3.font.name = "Calibri"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = C_DARK
    p3.space_after = Pt(12)

    p4 = tf1.add_paragraph()
    p4.text = "Department of Computer Science & Engineering | Academic Year 2025–2026\nLive Website: https://termguard.onrender.com"
    p4.font.name = "Calibri"
    p4.font.size = Pt(11)
    p4.font.color.rgb = C_BLUE

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "1. Introduction to TermGuard", "[Slide 2/12]")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "The Everyday Situation",
             [
                 ("Long Agreements", "Every time we join a gym, rent a flat, or buy software, we are asked to agree to long legal terms."),
                 ("Nobody Reads Them", "Agreements have 20 to 30 pages. 99% of people simply click 'I Agree' without reading."),
                 ("Hidden Rules", "Companies hide strict rules inside: auto-debiting fees, strict cancellation dates, and non-refundable deposits."),
                 ("People Lose Money", "Because people forget the dates, they end up paying for services they no longer use."),
             ])

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "What is TermGuard?",
             [
                 ("Smart Contract Reader", "TermGuard is a simple web tool that reads contracts for you in seconds."),
                 ("Finds Hidden Traps", "It uses Google Gemini AI to find secret rules and shows you the exact money at risk in Rupees (₹)."),
                 ("Sends Phone Warnings", "It automatically sends SMS to your mobile phone and emails to your inbox before the last date."),
                 ("Writes the Letter", "It even prepares ready-made cancellation letters so you can easily stop the payment."),
             ])

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "2. Problem Statement", "[Slide 3/12]")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Tricks Used by Companies",
             [
                 ("Silent Auto-Renewals", "Gym passes and software plans silently charge your card again for another full year (e.g., ₹32,000 auto-debit)."),
                 ("Tricky 30-Day Rules", "Companies say: 'You must cancel at least 30 days before renewal, otherwise no refund!'"),
                 ("Lost Rent Deposits", "Landlords keep entire ₹70,000 security deposits if tenants forget to give a 2-month advance move-out notice."),
                 ("Price Hikes", "Companies quietly increase your monthly fee without asking you first."),
             ])

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Why Regular Calendars Fail",
             [
                 ("Calendars Cannot Read", "Phone calendars (like Google Calendar) cannot read PDF contracts or understand legal terms."),
                 ("Only Reminds on Last Day", "Calendars remind you on the last day—by then, the 30-day notice window is already gone and your money is lost!"),
                 ("Zero Letter Help", "Normal calendars cannot write a formal legal letter for you."),
                 ("Huge Money Lost", "An average person loses ₹15,000 to ₹50,000 every year to forgotten subscriptions and penalties."),
             ])

    # =========================================================================
    # SLIDE 4: OBJECTIVES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "3. Project Objectives", "[Slide 4/12]")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Main Goals of TermGuard",
             [
                 ("Read Contracts with AI", "Use Google Gemini AI to scan agreements in under 2 seconds and find sneaky clauses."),
                 ("Show Money at Risk", "Clearly calculate and show how much money is at risk in Indian Rupees (₹ INR)."),
                 ("Find Real Cutoff Dates", "Calculate the true last date to cancel by subtracting notice periods backwards from renewal."),
                 ("Write Cancellation Drafts", "Auto-generate formal letters ready to send to gym managers, landlords, or support."),
             ])

    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Alert & Security Goals",
             [
                 ("3-Stage Alert System", "Send reminders at 3 key times: 1 week before, 24 hours before, and on the last day."),
                 ("Direct Phone Delivery", "Send real SMS text messages to mobile phones and emails directly to Gmail inboxes."),
                 ("Auto-Clean Expired Dates", "Automatically remove old dates 24 hours after they pass to keep the screen clean."),
                 ("Safe History Log", "Keep a safe, timestamped log of all alerts sent for future proof."),
             ])

    # =========================================================================
    # SLIDE 5: EXISTING SYSTEM VS PROPOSED SYSTEM
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "4. Existing System vs. Proposed System", "[Slide 5/12]")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Existing System (Manual / Phone Calendar)",
             [
                 ("Manual Reading", "Reading 20 pages of hard English is tiring and easy to misunderstand."),
                 ("Late Reminders", "Calendar only alerts on the final day, after the notice cutoff has already passed."),
                 ("Normal Chatbots (ChatGPT)", "Completely passive; once you close the chat, it forgets your contract."),
                 ("No Cancellation Help", "Users have to figure out how to write formal legal letters themselves."),
                 ("Easy to Forget", "No automated SMS alerts sent directly to your phone SIM card."),
             ])

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Proposed System (TermGuard)",
             [
                 ("Fast AI Reading", "Gemini AI reads the full agreement and finds hidden traps in 2 seconds."),
                 ("Early 3-Stage Alerts", "Alerts you 7 days before, 1 day before, and on the cutoff day so you have time."),
                 ("Runs 24/7 in Cloud", "Monitors dates automatically in the cloud even when your laptop is turned off."),
                 ("Pre-Written Letters", "Writes cancellation letters citing exact contract sections (e.g., Section 4.3)."),
                 ("Real SMS & Email", "Sends real SMS to your phone number and clean emails to your Gmail inbox."),
             ])

    # =========================================================================
    # SLIDE 6: TECHNOLOGIES USED
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "5. Technologies & Tools Used (Simple & Clear)", "[Slide 6/12]")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Frontend (Website Design)",
             [
                 ("Next.js 14", "Modern web framework that runs both the website and the backend API together."),
                 ("React 18", "Builds fast, interactive buttons, cards, and countdown timers."),
                 ("Tailwind CSS", "Gives the website a clean, professional dark-mode style."),
                 ("TypeScript", "Stops coding errors before they happen, making the website reliable."),
             ])

    add_card(s6, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "AI & Backend",
             [
                 ("Google Gemini 1.5 Flash", "Smart Google AI that reads contracts and finds dates in under 2 seconds."),
                 ("Node.js", "Server software that runs our backend code and calculations."),
                 ("JSON Database (db.json)", "Saves contracts and dates locally in a file with zero extra server costs."),
                 ("Render Cloud", "Hosts our live website online at termguard.onrender.com."),
             ])

    add_card(s6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Alerts & Communication",
             [
                 ("Twilio SMS API", "Sends real text messages directly to mobile phones over cellular towers."),
                 ("Fast2SMS Gateway", "Indian SMS service used as an automatic backup for Indian phone numbers."),
                 ("Resend Email API", "Sends clean, verified alert emails directly to Gmail primary inboxes."),
                 ("Activity Log", "Safely records every scan and alert sent."),
             ])

    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "6. System Architecture (How Everything Connects)", "[Slide 7/12]")

    arch_img = os.path.join(diag_dir, "architecture_diagram.png")
    if os.path.exists(arch_img):
        s7.shapes.add_picture(arch_img, Inches(0.8), Inches(1.5), width=Inches(7.2))

    add_card(s7, Inches(8.3), Inches(1.5), Inches(4.2), Inches(5.4),
             "How the System Works",
             [
                 ("1. User Screen", "The user opens the website and uploads a contract or picks a sample agreement."),
                 ("2. Backend API", "The server cleans the text and passes it to Google Gemini AI."),
                 ("3. Gemini AI", "The AI reads the text, finds the traps, and calculates the cutoff date."),
                 ("4. Safe Storage", "Details are saved in db.json with a live countdown timer."),
                 ("5. Automated Alerts", "When the date is near, the system sends SMS to phone and HTML email to inbox."),
             ])

    # =========================================================================
    # SLIDE 8: MODULES DESCRIPTION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "7. System Modules (Main Parts of the App)", "[Slide 8/12]")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Screen Modules",
             [
                 ("Dashboard Top HUD", "Shows big cards with Total Money Saved (₹1,48,440) and active countdown timers."),
                 ("Document Studio", "Where you paste contracts or choose sample agreements (Gym, Rent Flat, SaaS)."),
                 ("AI Assistant Chat", "A helpful chatbot where you can ask simple questions like 'When should I cancel?'"),
             ])

    add_card(s8, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Core Processing Modules",
             [
                 ("Deadlines Center", "Shows active reminder cards with live countdown timers in days, hours, and minutes."),
                 ("Auto-Alert Timer (Cron)", "Runs automatically in the background to check which dates are arriving today."),
                 ("Add Agreement Modal", "A simple popup to add any new contract, cutoff date, and money at risk."),
             ])

    add_card(s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.3),
             "Messaging & History Modules",
             [
                 ("SMS Dispatcher", "Formats phone numbers (+91) and sends text alerts via Twilio and Fast2SMS."),
                 ("Email Dispatcher", "Sends clean, dark-themed emails with ready-to-copy cancellation letters."),
                 ("Activity Trust Log", "A clear table showing timestamps and delivery IDs for every alert sent."),
             ])

    # =========================================================================
    # SLIDE 9: METHODOLOGY & 3-STAGE WORKING
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "8. Methodology: How the 3-Stage Alert Works", "[Slide 9/12]")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5),
             "1. Contract Scan & Risk Score",
             [
                 ("Contract Scan", "Gemini AI finds the exact clauses and cutoff dates in 2 seconds."),
                 ("Risk Score (0-100)", "Higher risk points for auto-debits (30 pts) and price hikes (15 pts)."),
                 ("Money at Risk", "Clearly displays the exact Rupees at stake (e.g., ₹32,000 at risk)."),
             ])

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.5),
             "2. Stage 1: 1-Week Warning (7 Days Left)",
             [
                 ("Timing", "Triggers automatically 7 days before the cutoff deadline."),
                 ("Purpose", "Gives you a calm early warning so you have plenty of time to prepare."),
                 ("Channels", "Sends an early SMS to mobile and notification to email inbox."),
             ])

    add_card(s9, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.5),
             "3. Stage 2 & 3: Urgent & Final Call",
             [
                 ("Stage 2 (24 Hours Left)", "Sends an urgent alert warning that tomorrow is your last day!"),
                 ("Stage 3 (Final Day)", "Final call alert on the exact day with pre-written cancellation letter."),
                 ("No Repeat Spam", "Smart flags ensure you get the alert only once per stage."),
             ])

    add_card(s9, Inches(6.8), Inches(4.4), Inches(5.7), Inches(2.5),
             "4. Stage 4: Auto-Delete (After 24h)",
             [
                 ("Timing", "Triggers 24 hours after the deadline has completely passed."),
                 ("Action", "Automatically cleans up the expired reminder from the main screen."),
                 ("Clean Dashboard", "Keeps your dashboard clean while saving a copy in the history log."),
             ])

    # =========================================================================
    # SLIDE 10: OUTPUT SCREENS (WITH REAL SCREENSHOTS)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "9. Output Screens (Live System in Action)", "[Slide 10/12]")

    # Card 1: Dashboard Screenshot
    card_w = Inches(3.7)
    card_h = Inches(5.3)

    # 1. Dashboard
    c1 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), card_w, card_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_CARD_BG
    c1.line.color.rgb = C_BORDER
    tb_c1 = s10.shapes.add_textbox(Inches(0.95), Inches(1.75), Inches(3.4), Inches(0.8))
    tb_c1.text_frame.word_wrap = True
    p = tb_c1.text_frame.paragraphs[0]
    p.text = "1. Executive Dashboard"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p_sub = tb_c1.text_frame.add_paragraph()
    p_sub.text = "Shows ₹1,48,440 saved and active countdown timers."
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = C_MUTED

    img1 = os.path.join(img_dir, "screen_1.png")
    if os.path.exists(img1):
        s10.shapes.add_picture(img1, Inches(0.95), Inches(2.65), width=Inches(3.4))

    # 2. Add Modal
    c2 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.6), card_w, card_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_CARD_BG
    c2.line.color.rgb = C_BORDER
    tb_c2 = s10.shapes.add_textbox(Inches(4.95), Inches(1.75), Inches(3.4), Inches(0.8))
    tb_c2.text_frame.word_wrap = True
    p = tb_c2.text_frame.paragraphs[0]
    p.text = "2. Add Agreement Modal"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p_sub = tb_c2.text_frame.add_paragraph()
    p_sub.text = "Popup to add new agreements, dates, and money in ₹ INR."
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = C_MUTED

    img2 = os.path.join(img_dir, "screen_2.png")
    if os.path.exists(img2):
        s10.shapes.add_picture(img2, Inches(4.95), Inches(2.65), width=Inches(3.4))

    # 3. Email Inbox
    c3 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.6), card_w, card_h)
    c3.fill.solid()
    c3.fill.fore_color.rgb = C_CARD_BG
    c3.line.color.rgb = C_BORDER
    tb_c3 = s10.shapes.add_textbox(Inches(8.95), Inches(1.75), Inches(3.4), Inches(0.8))
    tb_c3.text_frame.word_wrap = True
    p = tb_c3.text_frame.paragraphs[0]
    p.text = "3. Live Gmail Delivery"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p_sub = tb_c3.text_frame.add_paragraph()
    p_sub.text = "Real email received citing Section 4.3 with letter ready."
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = C_MUTED

    img3 = os.path.join(img_dir, "screen_3.png")
    if os.path.exists(img3):
        s10.shapes.add_picture(img3, Inches(8.95), Inches(2.65), width=Inches(3.4))

    # =========================================================================
    # SLIDE 11: ADVANTAGES & LIMITATIONS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "10. Advantages & Limitations (Simple & Honest)", "[Slide 11/12]")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Key Advantages",
             [
                 ("Works 24/7 Automatically", "Monitors your cutoff dates continuously in the cloud without needing you to remember."),
                 ("Super Fast AI Reading", "Reads long 20-page agreements in under 2 seconds using Google Gemini AI."),
                 ("Real Phone SMS & Email", "Sends real text alerts to your mobile phone SIM card and emails to your Gmail inbox."),
                 ("Pre-Written Legal Letters", "Automatically writes cancellation letters citing exact contract sections so you don't have to."),
                 ("Zero Database Hosting Cost", "Uses lightweight local JSON storage, making it completely free to run and deploy."),
             ])

    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Current Limitations",
             [
                 ("Text Input Only", "Currently accepts pasted text or presets (camera photo scanning can be added next)."),
                 ("English Language Focus", "Best optimized for English contracts (Indian regional languages coming in next phase)."),
                 ("Cloud Free-Tier Wakeup", "On free cloud hosting, the server takes a few seconds to wake up if inactive."),
                 ("Cannot Force Companies", "TermGuard warns you in time, but the user still needs to click and send the cancellation email."),
             ])

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, "11. Conclusion & Future Enhancements", "[Slide 12/12]")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Project Conclusion",
             [
                 ("Protects Consumer Money", "TermGuard stops companies from taking your hard-earned money through sneaky fine print."),
                 ("Active vs Passive", "Replaces useless calendar reminders with automated 3-stage phone and email alerts."),
                 ("Saves Real Money", "Successfully protects users from gym auto-debits (₹32,000) and lost rental deposits (₹70,000)."),
                 ("Live on the Internet", "Fully built, tested, and running live at https://termguard.onrender.com."),
             ])

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3),
             "Future Scope (What We Can Add Next)",
             [
                 ("Chrome Browser Extension", "Automatically scan Terms of Service on shopping websites before you click 'Buy'."),
                 ("WhatsApp Chatbot", "Receive alerts on WhatsApp and reply 'Cancel' to send the cancellation letter instantly."),
                 ("Indian Regional Languages", "Add support for contracts in Hindi, Telugu, Tamil, and Kannada."),
                 ("Camera OCR Scan", "Allow users to take a photo of a paper contract using their phone camera."),
             ])

    output_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Simple_English_Presentation.pptx"
    prs.save(output_path)
    print("Simple English 12-slide presentation created successfully at:", output_path)

if __name__ == '__main__':
    create_super_simple_ppt()
