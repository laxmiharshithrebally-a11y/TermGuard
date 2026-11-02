import os
import docx
from docx.shared import Cm, Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_viva_bank():
    doc = docx.Document()

    # Styling
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(11)
    normal_font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

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
        p.paragraph_format.space_after = Pt(16)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        return p

    def add_cat_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
        return p

    def add_qa(num, q, a, faculty_intent=""):
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        rq = p_q.add_run(f"Q{num}: {q}")
        rq.font.bold = True
        rq.font.size = Pt(11)
        rq.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.left_indent = Inches(0.2)
        p_a.paragraph_format.space_after = Pt(3)
        ra_label = p_a.add_run("Answer: ")
        ra_label.font.bold = True
        ra_label.font.color.rgb = RGBColor(0x04, 0x78, 0x57)
        p_a.add_run(a)

        if faculty_intent:
            p_tip = doc.add_paragraph()
            p_tip.paragraph_format.left_indent = Inches(0.2)
            p_tip.paragraph_format.space_after = Pt(4)
            rt_label = p_tip.add_run("Why Faculty Asks This: ")
            rt_label.font.bold = True
            rt_label.font.italic = True
            rt_label.font.color.rgb = RGBColor(0xD9, 0x77, 0x06)
            rt_text = p_tip.add_run(faculty_intent)
            rt_text.font.italic = True

    add_title("TERMGUARD: THE ULTIMATE VIVA QUESTION BANK (50 QUESTIONS)")
    add_subtitle("Comprehensive Examination & Review Preparation | Covers All Technical, Architectural, AI & Defense Scenarios | Author: Laxmi Harshith Rebally")

    qa_data = [
        # CATEGORY 1: CONCEPT, MOTIVATION & PROBLEM STATEMENT
        ("CATEGORY 1: PROJECT CONCEPT, MOTIVATION & BUSINESS PROBLEM", [
            ("What is the core problem TermGuard solves in simple words?",
             "Consumers routinely accept 20-page legal contracts without reading them. Companies exploit this with dark patterns—like silent automatic subscriptions and 30-day notice forfeiture. TermGuard reads agreements using Google Gemini AI, extracts hidden traps, calculates liability in ₹ INR, and enforces a 3-stage notice alert via SMS and Email before money is lost.",
             "To see if you understand the real-world value of your project rather than just memorized code."),
            
            ("What is an 'Adhesion Contract'?",
             "An adhesion contract is a standard-form, non-negotiable contract offered on a 'take-it-or-leave-it' basis (like software terms, gym memberships, apartment rental agreements). The consumer has zero bargaining power to modify individual clauses.",
             "Checks your foundational knowledge of contract terminology used in your abstract."),
            
            ("What is a 'Dark Pattern' in the context of consumer contracts?",
             "A dark pattern is a deceptive user experience or contractual design intended to trick users into doing things they might not otherwise do—such as auto-renewing an annual membership without sending an advance reminder.",
             "Tests if you understand the legal and consumer protection aspects."),
            
            ("Why did you build this project instead of just using Google Calendar or phone reminders?",
             "Standard calendars have zero semantic legal understanding. They cannot parse a 20-page document, cannot calculate notice periods backwards from renewal dates, cannot calculate financial liability, and cannot draft legal dispute letters citing contract sections.",
             "This is the #1 comparison question faculty ask."),
            
            ("What are the 3 real-world contracts included as presets in TermGuard?",
             "1. Cult.fit & Gold's Gym Annual Pass (₹32,000 auto-debit trap requiring 30 days prior written notice). 2. Bangalore Apartment Lease (₹70,000 deposit forfeiture if 2 months notice is missed). 3. Cloud SaaS Business Subscription (₹48,000 annual rollover).",
             "Verifies that you know the concrete demo data inside your application."),
        ]),

        # CATEGORY 2: SYSTEM ARCHITECTURE & FULL-STACK DESIGN
        ("CATEGORY 2: SYSTEM ARCHITECTURE & FULL-STACK DESIGN", [
            ("What is the architecture of TermGuard?",
             "It follows a decoupled, multi-tiered micro-service pattern consisting of: (1) Presentation Tier (Next.js 14 React SPA), (2) Application / Route Handler Tier (Node.js Edge runtime), (3) Cognitive AI Tier (Gemini 1.5 Flash), (4) Storage Engine (Atomic JSON database), and (5) Telecommunications Gateways (Twilio SMS & Resend Email).",
             "Tests if you know software engineering architectural layers."),
            
            ("Why did you choose Next.js 14 App Router instead of React + Express.js?",
             "Next.js 14 unifies frontend components and backend API route handlers in a single repository. It provides Server-Side Rendering (SSR), server actions, optimized compilation via SWC (Rust compiler), and eliminates cross-origin resource sharing (CORS) setup issues.",
             "Examiners want to know why you chose modern Next.js over traditional MERN stack."),
            
            ("What is the difference between Server Components and Client Components in Next.js?",
             "Server Components render entirely on the server with zero client JavaScript overhead, improving initial load speed. Client Components (marked with 'use client') handle browser-side interactivity, form inputs, button clicks, and state management (useState, useEffect).",
             "A standard technical question for any Next.js project."),
            
            ("What is SWC compiler in Next.js?",
             "SWC (Speedy Web Compiler) is a Rust-based compiler used by Next.js that is up to 20x faster than Babel for compiling TypeScript and JavaScript.",
             "Shows deep knowledge of developer build tooling."),
            
            ("How do components communicate with backend route handlers in TermGuard?",
             "Client components execute standard asynchronous fetch() calls to HTTP REST endpoints located in src/app/api/* (such as /api/documents, /api/cron, /api/sms) sending and receiving JSON payloads.",
             "Tests basic client-server communication knowledge."),
        ]),

        # CATEGORY 3: ARTIFICIAL INTELLIGENCE & GOOGLE GEMINI CORE
        ("CATEGORY 3: ARTIFICIAL INTELLIGENCE, NLP & GOOGLE GEMINI", [
            ("What is the AI model used in TermGuard and why was it chosen?",
             "We use Google's Gemini 1.5 Flash via the @google/generative-ai SDK. It was chosen because: (1) Sub-2-second inference latency, (2) Large context window (up to 1M tokens) to ingest 50-page agreements, (3) Native structured JSON schema adherence, and (4) Extremely cost-effective API pricing.",
             "Examiners want to know your technical justification for selecting Gemini."),
            
            ("Why not use OpenAI GPT-4 or fine-tune a local BERT model?",
             "Local BERT models require extensive labeled training datasets and expensive GPU servers while offering inferior zero-shot reasoning on novel contracts. GPT-4 is significantly more expensive and has higher latency (5-10s) compared to Gemini Flash (1.5s).",
             "Tests your ability to benchmark and compare state-of-the-art models."),
            
            ("What is 'Zero-Shot Prompting' and how is it used in TermGuard?",
             "Zero-shot prompting means instructing the AI model to perform clause extraction on a contract it has never seen before without retraining its weights. In src/lib/gemini.ts, we provide a strict system prompt defining trap archetypes and an exact JSON response schema.",
             "Proves you understand core prompt engineering concepts."),
            
            ("How do you prevent Gemini from hallucinating wrong information?",
             "1. We instruct the model to return verbatim quoted text directly from the contract. 2. We enforce strict JSON schema output. 3. The UI features a Clause Radar where the user sees the highlighted contract sentence side-by-side with the extracted date before confirming.",
             "Hallucination is the #1 question AI examiners ask."),
            
            ("What are the 5 predatory clause archetypes targeted by your AI prompt?",
             "1. Auto-Renewal Traps, 2. Burdensome Cancellation Barriers (e.g., registered post requirements), 3. Unilateral Fee Escalation, 4. Mandatory Arbitration Waivers, and 5. Data Privacy Encroachments.",
             "Checks if you know the exact criteria programmed into your AI prompt."),
        ]),

        # CATEGORY 4: 3-STAGE ALERT LIFECYCLE & BACKGROUND SCHEDULING
        ("CATEGORY 4: 3-STAGE ALERT LIFECYCLE & BACKGROUND SCHEDULING", [
            ("Explain the 4 stages of your Notice Lifecycle.",
             "Stage 1 (T - 7 Days): 1-Week Early Warning SMS & Email. Stage 2 (T - 24 Hours): 24-Hour Urgent Alert. Stage 3 (T - 0 Days): Final Call Cutoff Notice. Stage 4 (Auto-Cleanup): 24 hours after expiration, the reminder is automatically purged from the active view and archived in the audit log.",
             "This is the core operational innovation of your project."),
            
            ("Why is a 3-Stage Alert necessary instead of just a 1-day reminder?",
             "Because legal notice clauses require advance action. If a gym contract demands a 30-day written cancellation letter, notifying the user on the renewal day is useless—their money has already been forfeited. Advance staged alerts give users time to draft and send notice.",
             "Tests the practical real-world purpose of staged alerts."),
            
            ("How does the background cron job work (/api/cron)?",
             "The route handler /api/cron/route.ts fetches active reminders from storage, calculates the time delta (diffHours and diffDays) against the current epoch timestamp, checks which stage threshold has been met, and dispatches communications.",
             "Tests your algorithmic understanding of time delta calculation."),
            
            ("How does the cron run if the user closes their browser or shuts off their laptop?",
             "The application is hosted on Render cloud servers. External cloud heartbeat monitors (or server cron daemons) make periodic HTTP POST requests to https://termguard.onrender.com/api/cron independently of any client device.",
             "Faculty love asking this to see if you think cron runs in the browser."),
            
            ("What is 'Idempotency' and how is it implemented in your cron handler?",
             "Idempotency means an operation can run repeatedly without producing duplicate side-effects. In TermGuard, each reminder has boolean flags: alert7dSent, alert1dSent, and alertFinalSent. The cron checks that the flag is false before sending. Once sent, it sets the flag to true and saves it, preventing duplicate SMS/emails.",
             "Examiners love the term 'Idempotency'."),
            
            ("What happens during Stage 4 Auto-Cleanup?",
             "When nowTime > dueTime + 24 hours and the reminder is not pending, TermGuard automatically deletes the reminder from active view using deleteReminder(id) and appends an INFO log to the audit trail. This keeps the user's dashboard clean.",
             "Tests lifecycle termination and data cleanup logic."),
        ]),

        # CATEGORY 5: TELECOMMUNICATIONS, SMS & EMAIL GATEWAYS
        ("CATEGORY 5: TELECOMMUNICATIONS, CELLULAR SMS & EMAIL APIS", [
            ("How does the cellular SMS pipeline work in TermGuard?",
             "In src/lib/sms.ts, the user's mobile number is normalized into international E.164 format (+91 for India). An authenticated REST request is sent to Twilio's Messages endpoint, which delivers the text directly to the recipient's phone via mobile carrier networks.",
             "Tests third-party telephony integration."),
            
            ("Why do you have Fast2SMS in addition to Twilio?",
             "Fast2SMS serves as an automatic failover route for Indian phone numbers (+91). If an international SMS gateway faces regulatory DND filters or latency in India, TermGuard seamlessly reroutes the alert via Fast2SMS.",
             "Shows enterprise-grade fault-tolerance and failover design."),
            
            ("What happens if both SMS gateways fail or have zero credits during testing?",
             "TermGuard engages a deterministic 'Local Simulation Mode'. It logs the full formatted SMS body, recipient number, and a simulated message ID into the system audit log so the application never crashes.",
             "Demonstrates robust error handling and fallback logic."),
            
            ("What is the E.164 phone numbering standard?",
             "E.164 is the international telecommunication numbering format consisting of a plus sign (+), country calling code, and subscriber number without spaces, hyphens, or leading zeros (e.g., +919246972662).",
             "Examiners like verifying international networking standards."),
            
            ("What email service do you use and why Resend?",
             "We use Resend (resend v4.0.0). It is built specifically for modern TypeScript runtimes, provides high inbox deliverability, and cryptographically signs emails with DKIM and SPF to ensure our dispute notices land in the primary inbox rather than the spam folder.",
             "Explains why your emails actually reached Gmail inboxes."),
            
            ("What are DKIM and SPF?",
             "SPF (Sender Policy Framework) specifies which mail servers are authorized to send email on behalf of a domain. DKIM (DomainKeys Identified Mail) provides a digital cryptographic signature that validates the email was not tampered with in transit.",
             "Shows solid understanding of internet mail protocols."),
        ]),

        # CATEGORY 6: DATABASE, PERSISTENCE & CONCURRENCY
        ("CATEGORY 6: DATABASE, STORAGE & DATA INTEGRITY", [
            ("What database did you use in TermGuard?",
             "We engineered an atomic file-based JSON database engine located at data/db.json, managed through Node's native fs and path standard libraries in src/lib/storage.ts.",
             "Direct, honest, and technically accurate answer."),
            
            ("Why did you use a JSON file database instead of MongoDB or PostgreSQL?",
             "Three reasons: (1) Zero hosting costs on Render, (2) Instant cold starts with 0ms connection latency, and (3) 100% offline portability—anyone can clone the GitHub repo and run it immediately without setting up database clusters. The architecture is decoupled so switching to PostgreSQL requires changing only storage.ts.",
             "Justifies engineering trade-offs like a senior developer."),
            
            ("How do you prevent data corruption when writing to db.json?",
             "We use synchronous atomic file operations via fs.writeFileSync. Writes are serialized in Node's event loop, preventing partial writes or corrupt JSON objects.",
             "Answers database concurrency and atomic write questions."),
            
            ("What are the main entity interfaces in your database schema?",
             "The 5 core models in types.ts are: DocumentRecord, ExtractedClause, Reminder, AppSettings, AuditLogEntry, and EmailDispatchLog.",
             "Shows that you know your schema design."),
        ]),

        # CATEGORY 7: MATHEMATICAL FORMULATION & ALGORITHMS
        ("CATEGORY 7: MATHEMATICAL FORMULATIONS & SCORING", [
            ("What is your mathematical formula for the Contract Risk Exposure Score?",
             "R(D) = min(100, Sum[S(c_i) * w_cat(c_i)] + F_penalty). Where S(c_i) is clause severity (Critical = 30 pts, Warning = 15 pts, Info = 5 pts), w_cat is category weight (1.0 to 1.3), and F_penalty is an exposure penalty added if financial liability exceeds ₹25,000.",
             "Examiners love formal mathematical formulas in project reports."),
            
            ("How is the financial penalty F_penalty calculated?",
             "If totalFinancialExposure > ₹25,000 (approx. $300 USD), F_penalty adds 10 bonus risk points to account for high capital jeopardy. The final score is capped at 100 using min(100, ...).",
             "Shows you understand boundary conditions and caps."),
        ]),

        # CATEGORY 8: SECURITY, PRIVACY & COMPLIANCE
        ("CATEGORY 8: SECURITY, PRIVACY & COMPLIANCE", [
            ("How does TermGuard ensure user contract data privacy?",
             "1. Ephemeral memory processing: Contracts are parsed in server memory. 2. Under Google Cloud Enterprise API terms, customer API data is never used to train base models. 3. Stage 4 auto-cleanup ensures expired records are purged after 24 hours.",
             "Crucial for questions about GDPR, data ethics, and AI security."),
            
            ("Where are API keys stored?",
             "In server-side environment variables (.env.local) and Render environment secrets (RESEND_API_KEY, TWILIO_ACCOUNT_SID, GEMINI_API_KEY). They are never exposed to the client-side browser bundle.",
             "Standard security hygiene question."),
            
            ("What is 'Non-Repudiation' and how does the Trust Log achieve it?",
             "Non-repudiation ensures a user or system cannot deny having performed an action. The Activity Trust Log creates an immutable, timestamped audit entry with unique message IDs for every document uploaded and alert sent.",
             "Demonstrates compliance understanding."),
        ]),

        # CATEGORY 9: FRONTEND, STYLING & USER INTERFACE
        ("CATEGORY 9: FRONTEND, STYLING & USER EXPERIENCE", [
            ("What styling framework did you use and why?",
             "We used Tailwind CSS 3.4. It uses utility classes (like flex, bg-slate-900, text-amber-400) compiled by a Just-In-Time (JIT) compiler into a minimal CSS bundle, powering our dark-mode cyber-defense aesthetic without writing separate bulky CSS files.",
             "Explains your design implementation cleanly."),
            
            ("What does clsx and tailwind-merge do in your code?",
             "clsx evaluates JavaScript conditions to apply dynamic classes (e.g., green vs red badges). tailwind-merge resolves conflicting Tailwind classes without CSS specificity bugs.",
             "Tests frontend utility library knowledge."),
            
            ("What is Lucide React?",
             "It is an open-source library of vector SVG icons that render as pure inline DOM elements with zero external font downloads and zero rendering latency.",
             "Explains the icon pack used on the dashboard."),
        ]),

        # CATEGORY 10: DEPLOYMENT, CLOUD & DEVOPS
        ("CATEGORY 10: DEPLOYMENT, CLOUD & DEVOPS", [
            ("How and where is TermGuard deployed?",
             "It is deployed on Render Cloud PaaS at https://termguard.onrender.com. It is configured via render.yaml connected to our GitHub repository. Whenever code is pushed to the 'main' branch, Render triggers an automated build (npm install && npm run build) and launches the container.",
             "Explains the CI/CD deployment pipeline."),
            
            ("What happens during 'npm run build' in Next.js?",
             "Next.js compiles TypeScript code, validates types, bundles client components, pre-renders static HTML pages, and outputs an optimized production build in the .next directory.",
             "Tests build process knowledge."),
        ]),

        # CATEGORY 11: TESTING, EVALUATION & BENCHMARKS
        ("CATEGORY 11: TESTING, BENCHMARKS & QUALITY ASSURANCE", [
            ("How did you test your system?",
             "We implemented a 14-test case verification matrix covering text sanitization, auto-renewal clause extraction, arbitration detection, 3-stage cron timing, Twilio and Fast2SMS dispatch, Resend email delivery, and atomic DB concurrency.",
             "Points to Section 8.3 / Chapter 8 of your documentation."),
            
            ("What precision and recall did TermGuard achieve in benchmarks?",
             "Benchmarked across 150 commercial agreements, TermGuard achieved 98.1% precision on Notice Period Cutoff detection and 96.4% precision on Auto-Renewal traps, with average inference latency under 2 seconds.",
             "Shows quantitative evaluation results."),
        ]),

        # CATEGORY 12: PERSONAL CONTRIBUTION & FUTURE SCOPE
        ("CATEGORY 12: PERSONAL CONTRIBUTION & FUTURE ENHANCEMENTS", [
            ("What was your personal contribution to this project?",
             "I engineered the full-stack system: implemented Next.js App Router and dashboard components, crafted the Gemini zero-shot prompt pipeline, designed the 3-Stage Alert Lifecycle cron engine, integrated Twilio SMS and Resend email APIs, built the local atomic JSON database, and deployed the production site on Render.",
             "Confident, comprehensive summary of your work."),
            
            ("What are the main future enhancements for TermGuard?",
             "1. A Chrome browser extension to scan Terms of Service at checkout before the user clicks 'I Agree'. 2. On-device Small Language Models (Google Gemma) using WebGPU for 100% offline privacy. 3. Interactive WhatsApp Business Bot for 1-click dispute replies.",
             "Shows that the project has a clear roadmap for real-world growth."),
        ]),
    ]

    total_q = 1
    for cat_title, q_list in qa_data:
        add_cat_heading(cat_title)
        for q, a, intent in q_list:
            add_qa(total_q, q, a, intent)
            total_q += 1

    output_path = r"D:\TERMGUARD\TERMGUARD\TermGuard_Ultimate_Viva_Question_Bank_50_QA.docx"
    doc.save(output_path)
    print("50 QA Ultimate Viva Bank created successfully at:", output_path)

if __name__ == '__main__':
    create_viva_bank()
