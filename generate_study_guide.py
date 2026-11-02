import os
import docx
from docx.shared import Cm, Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_study_guide():
    doc = docx.Document()

    # Base styling - clean, readable, friendly format for personal study
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(11)
    normal_font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Margins
    for sec in doc.sections:
        sec.left_margin = Cm(2.0)
        sec.right_margin = Cm(2.0)
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(2.0)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(18)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)
        return p

    def add_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        rt = p.add_run(text)
        rt.font.italic = italic
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_after = Pt(3)
        b_dot = p.add_run("👉  ")
        b_dot.font.bold = True
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        p.add_run(text)
        return p

    def add_qa(q, a, tip=""):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(10)
        p_q.paragraph_format.space_after = Pt(2)
        rq = p_q.add_run("❓ " + q)
        rq.font.bold = True
        rq.font.size = Pt(11.5)
        rq.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.left_indent = Inches(0.25)
        p_a.paragraph_format.space_after = Pt(4)
        ra_label = p_a.add_run("💡 How to Answer: ")
        ra_label.font.bold = True
        ra_label.font.color.rgb = RGBColor(0x04, 0x78, 0x57)
        p_a.add_run(a)

        if tip:
            p_tip = doc.add_paragraph()
            p_tip.paragraph_format.left_indent = Inches(0.25)
            p_tip.paragraph_format.space_after = Pt(4)
            rt_label = p_tip.add_run("🔥 Faculty Insider Tip: ")
            rt_label.font.bold = True
            rt_label.font.color.rgb = RGBColor(0xD9, 0x77, 0x06)
            p_tip.add_run(tip)

    # -------------------------------------------------------------------------
    # DOCUMENT HEADER
    # -------------------------------------------------------------------------
    add_title("TERMGUARD: COMPLETE SELF-STUDY & VIVA MASTER PREP GUIDE")
    add_subtitle("Informal, Plain-English Project Learning Guide | For Personal Exam & Viva Preparation | Author: Laxmi Harshith Rebally")

    # -------------------------------------------------------------------------
    # SECTION 1: THE BIG PICTURE IN 2 MINUTES
    # -------------------------------------------------------------------------
    add_h1("SECTION 1: THE BIG PICTURE (UNDERSTAND YOUR PROJECT IN 2 MINUTES)")
    add_p("What is TermGuard, really?", bold_prefix="The Concept: ")
    add_p("Think of TermGuard as a digital lawyer and an alarm clock combined into one website. When you sign up for a gym, rent an apartment in Bangalore, or buy software subscriptions, companies bury sneaky rules in 20-page legal contracts. They know nobody reads them. These rules say: 'If you don't cancel 30 days before renewal, we will quietly take ₹32,000 from your bank account.'")
    add_p("TermGuard reads that contract using Google Gemini AI, spots the trap, calculates how much money you could lose, and automatically sends SMS and Email warnings to your phone 1 week before, 1 day before, and on the cutoff day. It even writes the cancellation letter for you so you can just copy-paste and send it!")

    add_p("The 3 Real Contracts We Built Inside the Website:", bold_prefix="Real Examples to Tell Faculty: ")
    add_bullet("Annual gym pass that silently auto-debits ₹32,000 unless cancelled 30 days in advance.", "1. Cult.fit & Gold's Gym (₹32,000 Trap): ")
    add_bullet("Lease agreement where landlord keeps the entire ₹70,000 security deposit if a 2-month written move-out notice is missed.", "2. Bangalore Flat 402 Rental Lease (₹70,000 Trap): ")
    add_bullet("Enterprise business software plan that locks you into a ₹48,000 annual contract unless you submit an opt-out ticket.", "3. Cloud SaaS / AWS-Zoho Business (₹48,000 Trap): ")

    # -------------------------------------------------------------------------
    # SECTION 2: EVERY SINGLE TOOL EXPLAINED IN PLAIN ENGLISH
    # -------------------------------------------------------------------------
    add_h1("SECTION 2: ALL TOOLS & PACKAGES EXPLAINED (WHAT IS IT, WHY WE USED IT, WHAT IF WE DELETE IT)")
    add_p("Faculty love asking: 'Why did you use this specific package? What would happen if we removed it?' Here is the exact answer for every tool:")

    tools = [
        ("Next.js 14 (App Router)", 
         "The full-stack web framework built by Vercel that runs both our frontend website and our backend server.",
         "Before Next.js, developers had to build two separate projects: a React frontend and an Express.js backend. Next.js combines both into one folder. Our pages are in src/app/page.tsx and our backend APIs are in src/app/api/*/route.ts.",
         "The entire website would collapse. We would have to rewrite separate Express backend servers and configure CORS headers."),
        
        ("React 18", 
         "A library for building interactive visual user interfaces using reusable building blocks called 'Components'.",
         "When an alert is sent or countdown timer ticks down, React updates only that specific card on the screen without reloading or flickering the whole webpage.",
         "The webpage would become completely static like an old HTML page from 1995."),
        
        ("TypeScript", 
         "JavaScript with strict type checking built by Microsoft.",
         "Legal data is sensitive. If a reminder object doesn't have a deadlineDate or title, TypeScript catches the error while coding instead of the website crashing in front of your professor.",
         "Nothing visually changes, but the code would be prone to random 'undefined is not a function' crashes during runtime."),
        
        ("Google Gemini 1.5 Flash (@google/generative-ai)", 
         "Google's state-of-the-art Artificial Intelligence model (Large Language Model).",
         "It acts as our AI lawyer. It reads long contracts, understands the legal jargon, extracts the exact clause quotes, calculates money in ₹ INR, and finds the cutoff date in under 2 seconds.",
         "The website wouldn't be able to analyze contracts automatically. Users would have to manually read and type everything themselves."),
        
        ("Twilio REST API", 
         "A global cloud telecommunications platform that sends SMS to physical phones.",
         "When a deadline is near, it delivers real cellular SMS to your phone SIM card over mobile towers.",
         "We wouldn't be able to send real cellular text messages to mobile phones."),
        
        ("Fast2SMS Gateway", 
         "An Indian national bulk and transactional SMS provider.",
         "Acts as an automatic backup. If Twilio faces international carrier delays in India, TermGuard seamlessly reroutes the alert through Fast2SMS.",
         "If Twilio has an issue in India, the user would not get the SMS."),
        
        ("Resend API (resend package)", 
         "A modern email delivery service for developers.",
         "It compiles our dark-themed HTML email and delivers it straight to the user's Gmail primary inbox with zero spam folder risk (uses DKIM/SPF domain verification).",
         "Emails would either bounce or end up in the user's Spam/Junk folder."),
        
        ("Tailwind CSS", 
         "A utility-first CSS styling tool.",
         "It gives our website the modern, dark cyber-defense look (soft titanium background, dark obsidian cards, amber warning pills).",
         "The website would lose all its colors, buttons, and layout styling."),
        
        ("Lucide React", 
         "A library of modern vector SVG icons.",
         "Renders the icons you see on screen: Shield, Clock, Phone, Mail, Trash, Checkmark.",
         "Icons would show up as broken squares or missing graphics."),
        
        ("clsx & tailwind-merge", 
         "Helper tools for combining CSS classes dynamically.",
         "When a risk level changes to CRITICAL, clsx dynamically changes the card border to Red; tailwind-merge ensures no two CSS rules fight each other.",
         "Buttons and badges might show wrong colors or conflicting styles."),
        
        ("Local JSON Database (data/db.json using Node 'fs')", 
         "A lightweight file-based database that stores agreements, reminders, settings, and logs.",
         "It costs ₹0 to host, starts up in 1 millisecond on cloud servers, and lets anyone run the project offline without installing MongoDB or MySQL.",
         "The app wouldn't be able to save newly added agreements or reminders."),
        
        ("Render Cloud Platform", 
         "A cloud platform that hosts our website online at https://termguard.onrender.com.",
         "Whenever we push code to GitHub, Render automatically builds and deploys it live on the internet with a free SSL HTTPS certificate.",
         "The website would only run on your local laptop (localhost:3000) instead of being live on the internet."),
    ]

    for name, what, why, rem in tools:
        add_h2(name)
        add_p(what, bold_prefix="What it is: ")
        add_p(why, bold_prefix="Why we used it in TermGuard: ")
        add_p(rem, bold_prefix="What happens if we remove it: ")

    # ---------------------------------------------------------
    # SECTION 3: WHAT IS ON THE WEBSITE & WHAT FACULTY WILL ASK
    # ---------------------------------------------------------
    add_h1("SECTION 3: SCREEN-BY-SCREEN GUIDE (WHAT YOU SEE & WHAT FACULTY WILL ASK)")

    screens = [
        ("Screen 1: Landing Page (https://termguard.onrender.com)",
         "Shows the animated shield intro, the main headline, and 3 live interactive contracts.",
         "Why did you build a separate landing page instead of just opening the dashboard?",
         "Because in real-world products, non-technical consumers need to understand the problem (adhesion contracts and dark patterns) before they trust the software with their legal agreements."),
        
        ("Screen 2: Executive HUD (Top 4 Metric Cards on Dashboard)",
         "Shows Total Money Protected (₹1,48,440), Active Cutoffs (3), Monitored Agreements (4), and Live SMS/Email status.",
         "How is 'Total Money Protected' calculated? Is it hardcoded?",
         "No, it is dynamically computed! It sums the financialImpactUsd values of all active reminders currently stored in the database. When a new contract is added, this number automatically updates."),
        
        ("Screen 3: Monitored Deadlines & 3-Stage Alert Center",
         "Shows active reminder cards with countdown timers and 'Send Alert' buttons.",
         "Explain your 3-Stage Alert Lifecycle. Why not just send one reminder?",
         "Because legal contracts require prior notice! If an agreement says '30-day prior written notice required', an alert on the last day is useless—your money is already lost! Our 3 stages give users time: Stage 1 (7 days before), Stage 2 (24 hours before), and Stage 3 (Final day)."),
        
        ("Screen 4: Add Agreement Modal (+ Add Agreement / Topic)",
         "A popup form allowing users to enter custom agreements, cutoff dates, and money at risk.",
         "What happens when I pick a cutoff date in this modal?",
         "The form submits to our storage API. TermGuard calculates the 7-day and 24-hour warning thresholds backwards from that cutoff date and generates a pre-formatted legal cancellation draft."),
        
        ("Screen 5: The Pre-Written Legal Notice Draft",
         "A formal letter template ready to copy and send to gym managers, landlords, or support.",
         "Where did this cancellation letter come from?",
         "TermGuard auto-formats it using the extracted clause information. It formally cites the exact section number (e.g., Section 4.3) and revokes auto-debit consent, giving the consumer strong legal standing."),
        
        ("Screen 6: The Trust Log (Audit Ledger Tab)",
         "A detailed table recording timestamps, action types, status codes, and message IDs.",
         "What is the importance of this Trust Log?",
         "In legal and financial applications, non-repudiation is essential. If a user disputes an auto-debit with their bank, this audit log provides proof of when the document was parsed and when notice reminders were triggered."),
        
        ("Screen 7: Live Gmail Inbox (The Received Email)",
         "The actual email received in Gmail with dark styling, ₹32,000 risk callout, and button.",
         "Is this a real email or a screenshot simulation?",
         "It is a 100% real transactional email delivered via Resend API! It is cryptographically signed with DKIM and SPF headers and delivered directly to the user's registered inbox."),
    ]

    for title, what_see, q, a in screens:
        add_h2(title)
        add_p(what_see, bold_prefix="What is on this screen: ")
        add_qa(q, a)

    # ---------------------------------------------------------
    # SECTION 4: 20 TOUGH VIVA QUESTIONS WITH CONFIDENT ANSWERS
    # ---------------------------------------------------------
    add_h1("SECTION 4: TOP 20 TOUGH VIVA QUESTIONS & HOW TO ANSWER CONFIDENTLY")
    add_p("These are the exact tricky questions examiners ask to test whether you really understand your project or just copied it. Study these answers carefully:")

    viva_list = [
        ("What is the difference between an Adhesion Contract and a Regular Contract?",
         "In a regular contract, both parties negotiate terms. In an Adhesion Contract, one party (usually a big company) writes the contract and forces the consumer to accept it on a 'take-it-or-leave-it' basis (like software terms or gym agreements). Consumers have zero bargaining power.",
         "Mention the term 'Cognitive Overload'—contracts average 7,000+ words, so 99% of people click 'Agree' without reading."),
        
        ("Why did you use Gemini 1.5 Flash instead of GPT-4 or training a local Python model?",
         "Three reasons: (1) Latency: Gemini Flash answers in 1.5 seconds. (2) Context Window: It can read up to 1 million tokens, meaning entire 50-page contracts fit easily. (3) Structured JSON: It guarantees valid JSON without hallucinating. Training our own model from scratch would require massive GPU power and thousands of labeled legal contracts.",
         "Faculty will appreciate that you considered latency and cost efficiency."),
        
        ("What is 'Zero-Shot Learning' and where is it used in your project?",
         "Zero-shot learning means giving the AI model an instruction and an unseen contract without retraining the model's weights. In gemini.ts, we use zero-shot system prompts with a strict JSON schema to isolate clauses and compute financial exposure on new contracts.",
         "This proves you understand modern AI vs traditional machine learning."),
        
        ("Why did you use a JSON file database (db.json) instead of MongoDB or MySQL?",
         "For three practical architectural reasons: (1) Zero hosting costs on Render, (2) 100% offline portability—anyone can clone the project and run it with zero database setup, (3) Instant cold-start time (0ms connection latency). Furthermore, our code is decoupled using repository functions (getReminders, saveReminders), meaning we can swap it for PostgreSQL in 10 minutes if needed.",
         "This shows architectural maturity—you chose the simplest tool that solved the problem cleanly."),
        
        ("How does the background cron job work if your laptop is closed?",
         "The project is deployed on Render Cloud (https://termguard.onrender.com). The cron endpoint (/api/cron) is a serverless REST route. External cloud uptime monitors (or Render cron workers) send an HTTP POST request to /api/cron periodically. It executes in the cloud independent of my laptop.",
         "Explain that cron is server-side, not client-side in the browser."),
        
        ("What is 'Idempotency' and how did you implement it in your alerts?",
         "Idempotency means that running an operation multiple times produces the same result without duplicate side-effects. In our reminders, we store three boolean flags: alert7dSent, alert1dSent, and alertFinalSent. Even if the cron runs every 5 minutes, it checks if the flag is true. If true, it skips dispatching, preventing the user from receiving 50 duplicate SMS messages.",
         "Examiners LOVE the word 'Idempotent'. It shows senior engineering knowledge."),
        
        ("What is Stage 4 Auto-Cleanup?",
         "24 hours after a cutoff date has passed, TermGuard automatically removes the reminder from the active dashboard view and logs a completed audit record. This prevents the user's interface from becoming cluttered with expired contracts while maintaining a clean historical ledger.",
         "Relate this to GDPR's 'Data Minimization' principle."),
        
        ("How do you prevent SMS spam or high Twilio API bills?",
         "We implement three safeguards: (1) Strict phone number validation with international E.164 formatting, (2) The idempotent alert flags that ensure a message can only fire once per stage, and (3) A Local Simulation Fallback mode during development so no SMS fees are incurred during testing.",
         "Shows practical budget and security awareness."),
        
        ("How is the Risk Score (0-100) calculated?",
         "We use a deterministic mathematical formula: Critical clauses (like auto-debits and arbitration waivers) add 30 points. Warning clauses (like price increases) add 15 points. Info clauses add 5 points. If the total money at risk exceeds ₹25,000, an additional exposure penalty is added, capped at a maximum of 100.",
         "If there is a whiteboard, offer to write down R(D) = min(100, Sum[S(c_i) * w(c_i)] + F_penalty)."),
        
        ("What is E.164 phone formatting?",
         "E.164 is the international telecommunication numbering standard. It formats numbers with a plus sign, country code, and national number with zero spaces or dashes (e.g., +919246972662 for India). Twilio requires this format to route messages across global carrier networks.",
         "Shows deep networking and telephony knowledge."),
        
        ("What is DKIM and SPF in email delivery?",
         "SPF (Sender Policy Framework) lists the authorized IP addresses allowed to send email for a domain. DKIM (DomainKeys Identified Mail) attaches a cryptographic digital signature to every email. Resend uses these so that recipient mail servers (like Gmail) know the alert is authentic and deliver it directly to the inbox instead of the spam folder.",
         "This explains why your emails landed cleanly in your Gmail inbox!"),
        
        ("What is the difference between Next.js Server Components and Client Components?",
         "Server Components render on the server and send pure HTML to the browser, making page loads faster with zero JavaScript overhead. Client Components (marked with 'use client') run in the user's browser to handle interactive features like button clicks, form inputs, and modal state.",
         "Mention that src/app/dashboard/page.tsx coordinates client components."),
        
        ("Can this system handle PDF files or only pasted text?",
         "In the current version, users paste the text or select pre-verified contract templates. The architecture is designed to support PDF parsing by piping file buffers through libraries like pdf-parse before sending the text payload to Gemini.",
         "Acknowledge current capability while explaining how easily it extends."),
        
        ("What happens if Gemini AI gives a wrong date or hallucinates?",
         "We implement two defense layers: (1) Strict JSON Schema prompting with few-shot legal examples, and (2) The Clause Radar interface displays the exact verbatim quote side-by-side with the date, allowing the user to inspect the source sentence with one click before activating the reminder.",
         "Explain 'Human-in-the-Loop' verification."),
        
        ("How do you ensure user privacy when reading personal contracts?",
         "First, contracts are processed ephemerally in memory during inference. Second, under Google Cloud's Enterprise API terms, data sent via API is NOT used to train Google's models. Third, our Stage 4 auto-cleanup safely deletes expired reminder data after 24 hours.",
         "Crucial for data protection and ethics questions."),
        
        ("What are the limitations of your project?",
         "Currently: (1) It requires text input or pre-set templates rather than direct image OCR scans, (2) It primarily supports English-language legal agreements, and (3) Cron scheduling relies on HTTP triggers. These are natural areas for future enhancement.",
         "Always be honest about limitations—professors respect self-awareness!"),
        
        ("What future enhancements do you plan to add?",
         "1. A Chrome browser extension that scans Terms of Service modals during online checkout before the user clicks 'I Agree'. 2. Local on-device Small Language Models (Google Gemma) using WebGPU for 100% offline privacy. 3. WhatsApp Business Bot integration allowing users to cancel subscriptions with a single WhatsApp reply.",
         "Shows you have a vision beyond the classroom."),
        
        ("How does clsx and tailwind-merge work together?",
         "clsx dynamically constructs CSS class strings based on JavaScript conditions (e.g., applying red borders for Critical risks). tailwind-merge takes that string and resolves conflicting Tailwind utility classes (e.g., if both p-2 and p-4 are passed, it keeps the latter cleanly).",
         "A great frontend-specific technical answer."),
        
        ("What is the role of Lucide React in this project?",
         "Lucide React provides pure inline vector SVG icons (Shield, Clock, AlertTriangle, Phone, Mail). Because they are inline SVGs, they render in 0 milliseconds with zero HTTP requests and look razor-sharp on 4K displays.",
         "Shows attention to UI performance and rendering efficiency."),
        
        ("If asked: 'Can you show me a live demo right now?'",
         "Open https://termguard.onrender.com/dashboard, click on the Cult.fit Gym card, click 'Send Alert (Email / SMS)' or 'Run Cron', show the success toast, and switch to the Trust Log tab to prove the event was recorded with a real timestamp and message ID!",
         "Always stay calm and do this demonstration step by step."),
    ]

    for q, a, tip in viva_list:
        add_qa(q, a, tip)

    # ---------------------------------------------------------
    # SECTION 5: TECHNICAL CHEAT SHEET
    # ---------------------------------------------------------
    add_h1("SECTION 5: FANCY TECHNICAL TERMS TO USE IN FRONT OF FACULTY")
    add_p("Sprinkle these terms naturally into your speech—examiners love hearing them:")
    add_bullet("A standard-form take-it-or-leave-it contract with zero room for consumer negotiation.", "Adhesion Contract: ")
    add_bullet("Deceptive user interface design tricks used by companies to manipulate users into recurring payments.", "Dark Patterns: ")
    add_bullet("An operation that can be applied multiple times without changing the result beyond the initial application (e.g., preventing duplicate SMS alerts).", "Idempotent Execution: ")
    add_bullet("AI reasoning where the model correctly completes a task without requiring task-specific fine-tuning or prior training examples.", "Zero-Shot Semantic Inference: ")
    add_bullet("The legal assurance that a user or system cannot deny the authenticity of their signature or sending a message (guaranteed by our Trust Log).", "Non-Repudiation: ")
    add_bullet("Cryptographic email authentication protocols guaranteeing that our alerts are delivered to primary inboxes rather than spam folders.", "DKIM / SPF Domain Signatures: ")
    add_bullet("React's internal algorithm for comparing the Virtual DOM with the real DOM to execute lightning-fast, flicker-free UI updates.", "Virtual DOM Reconciliation: ")

    # ---------------------------------------------------------
    # SECTION 6: THREE GOLDEN RULES FOR YOUR REVIEW
    # ---------------------------------------------------------
    add_h1("SECTION 6: THREE GOLDEN RULES FOR TOMORROW'S REVIEW")
    add_bullet("Don't start with code or technical jargon. Start with the real-life problem: 'Faculty, 99% of people agree to gym and rental contracts without reading them, losing thousands of rupees to auto-debit traps.' Once they relate to the problem, they will love your solution.", "1. Hook Them with the Story First: ")
    add_bullet("When showing the dashboard, click things slowly and explain what is happening: 'Here is the HUD calculating ₹1,48,440 saved... Here is the Cult.fit contract... When I click Send Alert, our server calls Twilio and Resend...'", "2. Guide Their Eyes on the Screen: ")
    add_bullet("If you don't know a random theoretical question, say: 'That is a great perspective, sir/ma'am. In our current architecture we solved this using X, but implementing your suggestion in our future roadmap would be an excellent enhancement.' Faculty appreciate humility and engineering mindset!", "3. Never Panic on Tough Questions: ")

    output_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Self_Study_and_Viva_Master_Prep.docx"
    doc.save(output_path)
    print("Self-study master prep guide created successfully at:", output_path)

if __name__ == '__main__':
    create_study_guide()
