import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_callout(doc, title, text, bg_hex="F1F5F9", border_color="2563EB"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(title)
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(11)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor.from_string(border_color)

    p2 = cell.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(2)
    run_b = p2.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    # empty paragraph after table for spacing
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(6)

def add_qa(doc, q_num, question, answer, examiner_tip=None):
    # Question
    p_q = doc.add_paragraph()
    p_q.paragraph_format.space_before = Pt(10)
    p_q.paragraph_format.space_after = Pt(3)
    p_q.paragraph_format.keep_with_next = True

    r_num = p_q.add_run(f"Q{q_num}: ")
    r_num.font.name = "Calibri"
    r_num.font.size = Pt(11)
    r_num.font.bold = True
    r_num.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A) # Deep Navy

    r_q = p_q.add_run(question)
    r_q.font.name = "Calibri"
    r_q.font.size = Pt(11)
    r_q.font.bold = True
    r_q.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Dark Slate

    # Answer
    p_a = doc.add_paragraph()
    p_a.paragraph_format.space_before = Pt(0)
    p_a.paragraph_format.space_after = Pt(4)
    r_ans_lbl = p_a.add_run("Answer: ")
    r_ans_lbl.font.name = "Calibri"
    r_ans_lbl.font.size = Pt(10.5)
    r_ans_lbl.font.bold = True
    r_ans_lbl.font.color.rgb = RGBColor(0x25, 0x63, 0xEB) # Royal Blue

    r_ans = p_a.add_run(answer)
    r_ans.font.name = "Calibri"
    r_ans.font.size = Pt(10.5)
    r_ans.font.color.rgb = RGBColor(0x33, 0x41, 0x55) # Muted Dark

    if examiner_tip:
        add_callout(doc, "EXAMINER INSIGHT & DEFENSE TIP", examiner_tip, bg_hex="F0FDF4", border_color="16A34A")

def build_encyclopedia():
    doc = docx.Document()

    # Set Margins to 1 inch
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Document Header / Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("TERMGUARD: MASTER VIVA & TECHNICAL DEFENSE ENCYCLOPEDIA")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Exhaustive Slide-by-Slide, Architectural, Source Code, and Cross-Examination Question Bank (75 In-Depth Q&A)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Metadata Table
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    tbl_meta.columns[0].width = Inches(2.2)
    tbl_meta.columns[1].width = Inches(4.3)

    meta_rows = [
        ("Project Title:", "TermGuard (Autonomous Contract Analysis & Multi-Channel Deadline Defense)"),
        ("Student Presenters:", "1. Rebally Laxmi Harshith (Roll No: 201224539090)\n2. Shubham Pradhan"),
        ("Department & College:", "Department of Computer Science & Engineering | Academic Year 2025-2026"),
        ("Live Web Deployment:", "https://termguard.onrender.com (GitHub: laxmiharshithrebally-a11y/TermGuard)")
    ]
    for idx, (lbl, val) in enumerate(meta_rows):
        c1, c2 = tbl_meta.cell(idx, 0), tbl_meta.cell(idx, 1)
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "FFFFFF")
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c2, top=60, bottom=60, left=100, right=100)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(lbl)
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

        p2 = c2.paragraphs[0]
        r2 = p2.add_run(val)
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Overview Callout
    add_callout(
        doc,
        "HOW TO USE THIS MASTER VIVA PREP MANUAL",
        "This document contains exactly 75 comprehensive, categorized questions covering every possible angle faculty or external examiners can ask: slide-by-slide questions matching the presentation, live website mechanics, codebase architecture, UML and algorithms, and high-pressure cross-examination trap questions. Review the bold answers and examiner defense tips before entering the defense hall.",
        bg_hex="EFF6FF",
        border_color="2563EB"
    )

    # =========================================================================
    # PART 1: SLIDE-BY-SLIDE VIVA QUESTIONS (Slides 1 to 14)
    # =========================================================================
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.space_before = Pt(18)
    p_sec1.paragraph_format.space_after = Pt(6)
    r_sec1 = p_sec1.add_run("PART 1: SLIDE-BY-SLIDE PRESENTATION VIVA QUESTIONS")
    r_sec1.font.name = "Calibri"
    r_sec1.font.size = Pt(16)
    r_sec1.font.bold = True
    r_sec1.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    # Slide 1 Questions
    doc.add_heading("Slide 1: Title Slide", level=2)
    add_qa(
        doc, 1,
        "What is TermGuard in one single sentence?",
        "TermGuard is an autonomous web application that reads legal consumer agreements, flags hidden traps, and dispatches multi-stage email alerts with pre-drafted legal dispute letters before cancellation deadlines expire.",
        "Keep your answer under 15 seconds. Emphasize 'autonomous' and 'pre-drafted dispute letters'—that is the unique differentiator."
    )
    add_qa(
        doc, 2,
        "Why did you choose the name 'TermGuard'?",
        "The name represents its dual purpose: 'Term' refers to contractual terms, notice windows, and conditions; 'Guard' signifies an autonomous 24/7 watchdog protecting consumer rights and bank accounts against sneaky auto-renewals.",
        None
    )
    add_qa(
        doc, 3,
        "How did Rebally Laxmi Harshith and Shubham Pradhan divide the project responsibilities?",
        "Harshith focused on backend architecture, API route handlers, Node-cron background scheduling, and the Resend email dispatch engine. Shubham worked on frontend responsive design, Next.js dashboard UI, contract modal forms, testing, and documentation.",
        "Examiners frequently ask project partners who did what to test if both students actually contributed."
    )

    # Slide 2 Questions
    doc.add_heading("Slide 2: Abstract", level=2)
    add_qa(
        doc, 4,
        "What is the core problem identified in your abstract, and what is your novel solution?",
        "The problem is the consumer fine-print dilemma: over 99% of people agree to digital contracts without reading them, falling victim to strict 30-day notice periods and non-refundable auto-renewals. Our novel solution is an end-to-end autonomous defense system that extracts deadlines, calculates notice windows, monitors them daily via background workers, and provides instant dispute letters inside the alert email.",
        None
    )
    add_qa(
        doc, 5,
        "Why is TermGuard called an 'Autonomous' system?",
        "Because once a user inputs or uploads an agreement, the system operates completely independently in the background. It does not require the user to open the app, check calendars, or set reminders. The background cron worker runs daily, monitors date differences, and dispatches alerts automatically.",
        "Highlight that 'autonomous' means zero ongoing manual effort from the user."
    )

    # Slide 3 Questions
    doc.add_heading("Slide 3: Introduction", level=2)
    add_qa(
        doc, 6,
        "What are 'contracts of adhesion' and why are everyday consumers vulnerable to them?",
        "Contracts of adhesion are 'take-it-or-leave-it' agreements where one party (the company) drafts all terms, and the weaker party (the consumer) has no power to negotiate. Consumers are vulnerable because terms are deliberately made 20+ pages long with dense legalese to discourage reading, burying costly auto-renewal clauses.",
        "Using legal terms like 'contracts of adhesion' shows academic maturity and impresses faculty."
    )
    add_qa(
        doc, 7,
        "What everyday digital services cause the most financial traps for consumers?",
        "Annual fitness passes (gyms like Cult.fit and Gold's Gym), software-as-a-service subscriptions (Adobe, LinkedIn Premium, cloud storage), rental apartment lease agreements, and telecommunication contracts with lock-in periods.",
        None
    )

    # Slide 4 Questions
    doc.add_heading("Slide 4: Modules, Libraries and Packages", level=2)
    add_qa(
        doc, 8,
        "Explain the four main functional modules of TermGuard.",
        "1. Document Upload and Parsing Module: Accepts raw contract text or PDF uploads and extracts raw legal clauses.\n2. Risk Scoring Engine: Evaluates extracted terms against unfair trade practice rules to generate an objective 0 to 100 risk rating.\n3. Scheduled Alert Notification Engine: Autonomous cron scheduler that calculates remaining notice days and fires multi-stage alerts.\n4. Dispute Notice Generator: Populates formal legal cancellation letters with user names, contract clauses, and consumer protection rights.",
        None
    )
    add_qa(
        doc, 9,
        "Why did you choose Next.js 14 App Router instead of traditional Create React App?",
        "Next.js 14 App Router provides full-stack capabilities in a single unified project: React Server Components for fast initial page load, built-in API route handlers (`/api/cron`, `/api/email`) eliminating the need for a separate Express server, and seamless server-side environment variable security.",
        "Examiners love asking 'Why Next.js?' Stress that it unifies frontend UI and backend API routes in one codebase."
    )
    add_qa(
        doc, 10,
        "What is Node-cron and how does it fit into your package architecture?",
        "Node-cron is a pure JavaScript task scheduler for Node.js based on standard crontab syntax. It executes scheduled functions at specified intervals (such as every midnight `0 0 * * *`) without manual intervention, enabling TermGuard to evaluate contract deadlines 24/7.",
        None
    )
    add_qa(
        doc, 11,
        "Why did you use Resend API instead of traditional Nodemailer with SMTP?",
        "Traditional SMTP connections with Nodemailer frequently experience port blocks (ports 25, 465, 587) on modern serverless and cloud hosting providers like Render and Vercel. Resend operates over standard HTTPS REST API calls, guaranteeing 99.9% inbox deliverability, instant dispatch speeds, and built-in tracking without SMTP timeout errors.",
        "This is an outstanding technical answer that demonstrates real-world hosting experience."
    )
    add_qa(
        doc, 12,
        "What is `pdf-parse` and how does it handle binary PDF uploads?",
        "`pdf-parse` is a Node.js library that reads the binary buffer stream of an uploaded PDF file, decodes the PostScript font glyphs and streams, extracts plain text content, and returns it as a string so our regex and AI models can parse the contract terms.",
        None
    )
    add_qa(
        doc, 13,
        "What is `lucide-react` and `canvas-confetti` in your frontend package list?",
        "`lucide-react` provides light, tree-shakable SVG icons (clock, shield, alert, check) that give the dashboard a clean modern look without bloat. `canvas-confetti` is an interactive micro-animation library used to trigger a celebration burst when a user successfully cancels an agreement or resolves a dispute, reinforcing positive financial behavior.",
        None
    )

    # Slide 5 Questions
    doc.add_heading("Slide 5: System Analysis — Limitations & Motivation", level=2)
    add_qa(
        doc, 14,
        "Why are standard calendar tools (Google Calendar, Outlook) insufficient for contract tracking?",
        "Standard calendars are completely dumb and passive: they require the user to manually read the contract, manually find the renewal date, manually calculate the 30-day prior notice cutoff date, and manually type in an alarm. Furthermore, when the alarm rings, Google Calendar gives no legal advice, no risk score, and no dispute letter. TermGuard does all of this automatically.",
        None
    )
    add_qa(
        doc, 15,
        "What is a 'Notice Window' and why do users constantly miss it?",
        "A notice window is the mandatory time period specified in a contract (typically 15 to 30 days before renewal) during which a user must officially notify the company of cancellation. If a user tries to cancel on renewal day, it is already too late—the notice window has passed, and they are legally locked in for another year.",
        "Emphasize the difference between 'Renewal Date' and 'Cancellation Notice Cutoff Date'."
    )
    add_qa(
        doc, 16,
        "What is the social motivation behind building TermGuard?",
        "To democratize legal defense for everyday consumers. Large corporations employ legal departments to design fine-print traps. TermGuard acts as an autonomous digital lawyer for ordinary people, ensuring they never lose money to unfair terms.",
        None
    )

    # Slide 6 Questions
    doc.add_heading("Slide 6: System Analysis — Existing vs Proposed Systems", level=2)
    add_qa(
        doc, 17,
        "Tabulate the differences between the Existing System and the Proposed TermGuard System.",
        "1. Analysis: Existing is manual reading (takes hours); Proposed is automated clause parsing (takes seconds).\n2. Date Calculation: Existing requires manual calendar math; Proposed automatically computes notice cutoffs.\n3. Risk Awareness: Existing provides zero risk indicators; Proposed gives a 0-100 visual risk score with critical badges.\n4. Dispute Action: Existing requires hiring a lawyer or writing emails from scratch; Proposed provides instant pre-drafted formal legal cancellation notices inside the alert email.",
        None
    )
    add_qa(
        doc, 18,
        "What is the single biggest innovation of TermGuard over generic reminder apps?",
        "The integration of the ready-to-send legal dispute letter directly inside the alert notification. When the alert arrives in the user's Gmail inbox, they do not just get a reminder—they get a complete, legally cited cancellation notice ready to copy-paste or forward to customer support in one click.",
        None
    )

    # Slide 7 Questions
    doc.add_heading("Slide 7: System Requirement Specification (SRS)", level=2)
    add_qa(
        doc, 19,
        "What are the Hardware and Software Requirements for deploying and running TermGuard?",
        "Hardware: Dual-Core CPU (Intel/AMD 2.0 GHz+), 4 GB RAM minimum (8 GB recommended for concurrent builds), 10 GB disk storage, and stable broadband internet.\nSoftware: Node.js (version 18 or higher), npm package manager, modern web browser (Chrome, Edge, Firefox), and Git version control.\nOperating System: Cross-platform (Windows 10/11, Ubuntu Linux, macOS).",
        None
    )
    add_qa(
        doc, 20,
        "What is the difference between Functional and Non-Functional Requirements in your SRS?",
        "Functional Requirements define what the system does: uploading contracts, parsing notice dates, computing risk scores, sending emails, and generating dispute letters.\nNon-Functional Requirements define how the system performs: page load time under 1.5 seconds, 99.9% uptime on cloud hosting, mobile responsive viewport scaling, and zero storage of credit card details for strict security compliance.",
        "Examiners love testing the distinction between functional and non-functional requirements."
    )
    add_qa(
        doc, 21,
        "Why is Node.js version 18 or higher strictly required?",
        "Node.js 18 introduced native global `fetch` API support, modern ECMAScript module features, and improved crypto performance required by Next.js 14 App Router and Resend SDK.",
        None
    )

    # Slide 8 Questions
    doc.add_heading("Slide 8: System Design — Architecture", level=2)
    add_qa(
        doc, 22,
        "Walk me through the four layers of the TermGuard System Architecture.",
        "1. Presentation Layer: Client-side dashboard built with React 18 and Tailwind CSS showing active contracts, live countdown clocks, and risk metrics.\n2. Application Layer: Next.js API route handlers (`/api/documents`, `/api/cron`, `/api/email`) managing business logic, text parsing, and scoring algorithms.\n3. Background Service Layer: Node-cron scheduler running continuous 24-hour evaluation cycles to detect contracts entering notice cutoff windows.\n4. Delivery Layer: Resend Email Gateway transmitting structured transactional alerts with HTML dispute notices to consumer inboxes.",
        "Refer directly to the Architecture Diagram embedded on Slide 8 of your presentation."
    )
    add_qa(
        doc, 23,
        "How is data persisted in the architecture?",
        "In the current prototype, data is managed via a transactional JSON storage engine (`data/db.json`) abstracted behind `storage.ts`, providing fast reads, thread-safe atomic writes, and zero external database overhead. For production enterprise scaling, `storage.ts` can be swapped for PostgreSQL or MongoDB with Prisma ORM.",
        None
    )
    add_qa(
        doc, 24,
        "What architectural pattern does your application follow?",
        "It follows a Layered Service-Oriented Architecture (SOA) combined with the Repository Pattern in `src/lib/storage.ts`. Business logic is decoupled from persistence, and the presentation layer interacts strictly through typed API endpoints.",
        None
    )

    # Slide 9 Questions
    doc.add_heading("Slide 9: System Design — UML Diagrams", level=2)
    add_qa(
        doc, 25,
        "Who are the actors in your UML Use Case Diagram?",
        "The primary actor is the 'Consumer / Registered User'. The secondary actors are the 'Automated Cron Scheduler' and the 'External Email Gateway (Resend)'.",
        None
    )
    add_qa(
        doc, 26,
        "What are the key use cases supported by the system?",
        "Key use cases include: 1. Submit Contract Text / Document, 2. View Risk Analysis and Clause Breakdown, 3. Monitor Active Countdown Timers, 4. Trigger / Receive Multi-Stage Alert Notifications, 5. Generate and Download Formal Dispute Letters, and 6. Inspect Immutable Activity Audit Logs.",
        None
    )
    add_qa(
        doc, 27,
        "Describe the Sequence Diagram flow for the alert lifecycle.",
        "1. Consumer uploads contract -> Frontend POSTs to `/api/documents`.\n2. Server parses dates, computes risk score, saves to storage, and adds an audit log.\n3. Cron Worker triggers `/api/cron` daily at midnight.\n4. Cron queries active reminders, calculates `diffDays = (dueTime - nowTime) / 86400000`.\n5. If `diffDays <= 3` and alert not sent, Cron invokes `dispatchReminderEmail()`.\n6. Resend API returns Message ID -> Cron updates reminder status to `TRIGGERED` and notifies user.",
        "This demonstrates that you understand the exact chronological interaction between components."
    )
    add_qa(
        doc, 28,
        "What is the multiplicity between DocumentRecord and ExtractedClause in your UML Class Diagram?",
        "The relationship is One-to-Many (`1 : *`). A single uploaded agreement (`DocumentRecord`) can contain zero, one, or multiple extracted fine-print clauses (`ExtractedClause`), each with its own deadline date, risk level, and financial impact.",
        None
    )

    # Slide 10 Questions
    doc.add_heading("Slide 10: System Design — Flow-chart", level=2)
    add_qa(
        doc, 29,
        "Explain the decision nodes in your process lifecycle flowchart.",
        "The main decision nodes are:\n1. 'Is valid agreement text or PDF provided?': If no, prompt user with validation error; if yes, proceed to clause extraction.\n2. 'Are cancellation notice clauses present?': If yes, extract deadline and compute notice window; if no, set standard renewal date.\n3. 'Has the 3-day notice window arrived?': If yes, check if alert sent; if not, dispatch Stage 1 alert.\n4. 'Has final cutoff passed by >24 hours?': If yes, automatically archive and clean up the notice from the active monitoring dashboard.",
        None
    )
    add_qa(
        doc, 30,
        "What happens if a contract specifies a past date that has already expired?",
        "The system calculates `diffDays = (dueTime - nowTime) / 86400000`. If `diffDays < 0`, the system flags the agreement with status `EXPIRED`, logs an audit warning, and informs the user that the cutoff has already lapsed, suggesting immediate retroactive dispute action.",
        None
    )

    # Slide 11 Questions
    doc.add_heading("Slide 11: System Implementation", level=2)
    add_qa(
        doc, 31,
        "How is the Risk Score (0 to 100) mathematically calculated?",
        "The risk score starts from a baseline of 0 and adds weighted risk points based on detected predatory clauses:\n- Strict Auto-Renewal without notice: +35 points\n- Short Cancellation Window (<15 days): +25 points\n- Non-Refundable Upfront Clause: +20 points\n- Unilateral Price Increase Clause: +15 points\n- Hidden Termination Penalties: +15 points\nA score of 0-30 is categorized as Low Risk (Green), 31-70 as Moderate Warning (Amber), and 71-100 as Critical Risk (Red).",
        "Faculty love seeing concrete mathematical point-weighting systems."
    )
    add_qa(
        doc, 32,
        "How is the legal cancellation dispute letter generated dynamically?",
        "The system uses a templating engine in `storage.ts` that merges dynamic fields: user name, company name, agreement title, date of contract commencement, specific clause numbers cited from the contract, and relevant statutory consumer protection law citations (e.g., Consumer Protection Act 2019 / unfair contract terms provisions).",
        None
    )
    add_qa(
        doc, 33,
        "What is the 3-Stage Alert Notification strategy implemented in `src/app/api/cron/route.ts`?",
        "Stage 1 (7 Days Remaining): Early Warning alert advising the user to decide whether to continue or cancel.\nStage 2 (1 Day Remaining): Urgent Countdown alert warning that tomorrow is the final day to submit notice.\nStage 3 (Final Cutoff Day): Critical Deadline alert providing the complete pre-drafted dispute letter and emergency instructions.\nStage 4 (Expired +24 Hours): Automatic cleanup archiving the notice from active view to keep the dashboard clutter-free.",
        "Explaining all 4 stages proves deep familiarity with the background cron code."
    )

    # Slide 12 Questions
    doc.add_heading("Slide 12: Testing", level=2)
    add_qa(
        doc, 34,
        "What types of software testing were performed on TermGuard?",
        "1. Unit Testing: Tested date difference math (`diffDays`), clause regex extractors, and risk scoring functions using mock contract text.\n2. Integration Testing: Validated end-to-end communication between frontend modal forms, Next.js server actions, local storage, and the Resend API.\n3. Functional Testing: Tested cron job execution, manual force trigger buttons, and auto-cleanup logic for expired notices.\n4. User Acceptance & Cross-Browser Testing: Verified responsive layouts across Google Chrome, Edge, and mobile Safari.",
        None
    )
    add_qa(
        doc, 35,
        "How did you verify that the email alerts actually reach the user's inbox?",
        "We tested live dispatches using real Gmail accounts (`harshithlaxmi2003@gmail.com`). We confirmed email receipt within 2.4 seconds, checked SPF and DKIM authentication headers via Resend, and verified that HTML formatting and dispute letters rendered cleanly on desktop and mobile Gmail clients without going to Spam.",
        "Mentioning real tested email accounts proves you performed genuine live testing."
    )
    add_qa(
        doc, 36,
        "Did you encounter any bugs during testing, and how did you resolve them?",
        "Yes. During initial testing, we observed a timezone mismatch bug: the server runs in UTC while Indian users operate in IST (UTC+5:30). If a user entered a deadline for midnight on September 14, the server evaluated it at 18:30 UTC on September 13, causing alerts to trigger 5.5 hours early. We resolved this by normalizing all calendar dates to UTC ISO strings and evaluating calendar days using `Math.floor(diffHours / 24)`.",
        "Sharing a real bug and fix shows authenticity and high problem-solving capability."
    )

    # Slide 13 Questions
    doc.add_heading("Slide 13: Output Screens (GUI Screenshots)", level=2)
    add_qa(
        doc, 37,
        "Walk the examiner through the three screenshots shown on Slide 13.",
        "Screenshot 1 (Active Dashboard): Shows the main HUD with active agreements, total money defended (e.g., ₹61,990), active countdown clocks, and color-coded risk badges.\nScreenshot 2 (Add Agreement Modal): Shows the streamlined modal form where users enter contract names, paste legal clauses, or upload files with immediate parsing.\nScreenshot 3 (Delivered Email Alert): Displays a real Gmail screenshot showing the received alert subject, warning banner, countdown details, and pre-written cancellation dispute notice.",
        None
    )
    add_qa(
        doc, 38,
        "What do the colors on the dashboard cards represent?",
        "- Red Badge / Crimson Card: Critical Risk (>70 score) — Contract has strict auto-renewal and zero-refund clauses.\n- Amber / Orange Badge: Moderate Warning (31-70 score) — Contract has notice period requirements or price escalator clauses.\n- Green Badge / Emerald: Safe / Low Risk (0-30 score) — Transparent contract with fair cancellation terms.\n- Blue Badge: Pending active monitoring timer.",
        None
    )

    # Slide 14 Questions
    doc.add_heading("Slide 14: Conclusion & Future Enhancements", level=2)
    add_qa(
        doc, 39,
        "What are the main conclusions of the TermGuard project?",
        "TermGuard proves that everyday consumers can be effectively protected from predatory digital fine print using accessible web technologies. By combining automated document parsing, proactive background tracking, and instant dispute generation, it turns passive consumers into active defenders of their financial rights.",
        None
    )
    add_qa(
        doc, 40,
        "What are the future enhancements planned for Version 2.0?",
        "1. WhatsApp Business API & SMS integration for instant mobile push alerts.\n2. A Chrome/Firefox browser extension that automatically parses terms-of-service before users click 'Agree' on checkout pages.\n3. Virtual Card Auto-Pause integration via banking APIs to freeze recurring subscription charges automatically when a dispute is lodged.",
        "Future scope questions show vision beyond the basic syllabus requirements."
    )

    # =========================================================================
    # PART 2: WEBSITE & LIVE DEMO VIVA QUESTIONS
    # =========================================================================
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.space_before = Pt(18)
    p_sec2.paragraph_format.space_after = Pt(6)
    r_sec2 = p_sec2.add_run("PART 2: WEBSITE & LIVE DEMO WALKTHROUGH QUESTIONS")
    r_sec2.font.name = "Calibri"
    r_sec2.font.size = Pt(16)
    r_sec2.font.bold = True
    r_sec2.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_qa(
        doc, 41,
        "If the examiner says: 'Open the website and add a new contract right now', what will you do?",
        "1. Open https://termguard.onrender.com.\n2. Click the blue '+ Add Agreement' button on the top right.\n3. Select a preset sample (e.g., Cult.fit / Gold's Gym Membership) or paste contract text.\n4. Notice how the system immediately extracts the agreement title, renewal date (Oct 14, 2026), 30-day notice cutoff (Sept 14, 2026), and financial exposure (₹32,000).\n5. Click 'Save & Monitor Agreement' -> The dashboard immediately displays the new card with live countdown.",
        "Practice this sequence once so you can perform it smoothly in 10 seconds during the demo."
    )
    add_qa(
        doc, 42,
        "What happens when you click the 'Simulate Midnight Cron Check' or 'Send Alert Now' button?",
        "The frontend sends an asynchronous POST request to `/api/cron` with `forceTriggerId`. The server calculates remaining days, discovers that the notice cutoff is active, calls `dispatchReminderEmail()`, and returns HTTP 200. The dashboard updates the badge from 'PENDING' to 'TRIGGERED' and appends a new audit record to the Activity Audit Log.",
        None
    )
    add_qa(
        doc, 43,
        "What information is displayed on the Top Stats HUD?",
        "1. Active Defenses: Number of contracts currently monitored (e.g., 2 Active).\n2. Critical Traps: Contracts flagged with High Risk (>70 risk score).\n3. Approaching Cutoffs: Agreements with notice windows due within 30 days.\n4. Total Money Defended: Cumulative INR value of recurring auto-debits being tracked and protected (e.g., ₹61,990).",
        None
    )
    add_qa(
        doc, 44,
        "What is the purpose of the Activity Audit Log component at the bottom of the dashboard?",
        "It provides an immutable audit trail of every system event: document uploads, clause extractions, scheduled cron evaluations, email dispatches, and auto-cleanup of expired notices. This gives the user total transparency into when the watchdog evaluated their contracts.",
        None
    )
    add_qa(
        doc, 45,
        "What is the 'FinePrint AI Legal Assistant' chat feature on the website?",
        "It is an interactive conversational agent powered by Google Gemini API (`gemini-1.5-flash`). Users can ask natural language questions like 'What happens if I cancel my gym membership 10 days before renewal?' and the AI analyzes the contract context to explain their legal obligations and draft custom dispute letters.",
        "Mention that it has a robust fallback engine so it works smoothly even if the external AI API quota is exhausted."
    )
    add_qa(
        doc, 46,
        "Can a user preview what the email looks like before it is dispatched?",
        "Yes. In the Reminders Center or active card, clicking 'Email Preview' opens the `EmailInspectorModal` component. It renders the exact HTML email markup, subject line, warning banners, and attached cancellation notice draft exactly as the recipient will see it in Gmail.",
        None
    )
    add_qa(
        doc, 47,
        "What happens when a user clicks 'Mark as Resolved' or 'Dismiss'?",
        "The system updates the status of the reminder to `RESOLVED` in `data/db.json`, logs an audit entry, stops further cron countdown alerts for that contract, and triggers a celebratory canvas-confetti animation on screen.",
        None
    )

    # =========================================================================
    # PART 3: DEEP TECHNICAL & CODE ARCHITECTURE QUESTIONS
    # =========================================================================
    p_sec3 = doc.add_paragraph()
    p_sec3.paragraph_format.space_before = Pt(18)
    p_sec3.paragraph_format.space_after = Pt(6)
    r_sec3 = p_sec3.add_run("PART 3: DEEP TECHNICAL & CODE ARCHITECTURE QUESTIONS")
    r_sec3.font.name = "Calibri"
    r_sec3.font.size = Pt(16)
    r_sec3.font.bold = True
    r_sec3.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_qa(
        doc, 48,
        "Explain the directory structure of the TermGuard Next.js project.",
        "- `src/app`: Next.js 14 App Router containing page components (`page.tsx`, `layout.tsx`) and API route handlers (`/api/cron`, `/api/email`, `/api/documents`, `/api/agent/chat`).\n- `src/components`: Modular React client components (`CreateAgreementModal`, `TopStatsHUD`, `DocumentStudio`, `ActivityAuditLog`).\n- `src/lib`: Core utility modules (`resend.ts` for email, `gemini.ts` for AI, `storage.ts` for data persistence, `types.ts` for TypeScript interfaces).\n- `data/db.json`: Local JSON database storing agreements, reminders, audit logs, and settings.",
        None
    )
    add_qa(
        doc, 49,
        "What is the difference between Client Components and Server Components in your codebase?",
        "Server Components (default in Next.js 14) render on the server, keeping server secrets and heavy dependencies off the client bundle. Client Components (marked with `'use client'` at the top of files like `page.tsx` and `CreateAgreementModal.tsx`) handle interactive state (`useState`, `useEffect`), form submissions, modal open/close toggles, and live countdown timers.",
        "Faculty love modern React questions. Pointing out the `'use client'` directive proves you wrote modern Next.js 14 code."
    )
    add_qa(
        doc, 50,
        "How does `src/app/api/cron/route.ts` prevent duplicate alerts from being sent every day?",
        "The reminder entity stores boolean flags: `alert7dSent`, `alert1dSent`, and `alertFinalSent`. When the cron job fires a notification, it immediately updates the flag in `storage.ts` (`updateReminder(reminder.id, { alertFinalSent: true })`). On the next execution, the condition `!reminder.alertFinalSent` evaluates to false, preventing duplicate email dispatches.",
        "This is an important system design question about idempotency."
    )
    add_qa(
        doc, 51,
        "How is the live countdown timer implemented in React?",
        "Using a `useEffect` hook combined with a `setInterval` timer that runs every 1,000 milliseconds (1 second). It computes `const diff = new Date(dueAt).getTime() - Date.now()`, and converts the milliseconds into days, hours, minutes, and seconds. When the component unmounts, `clearInterval` is called in the cleanup function to prevent memory leaks.",
        "Mentioning `clearInterval` cleanup demonstrates solid React fundamentals."
    )
    add_qa(
        doc, 52,
        "How are environment variables managed securely in the project?",
        "Sensitive credentials (such as `RESEND_API_KEY` and `GEMINI_API_KEY`) are stored in `.env.local` on the development server and as encrypted Environment Variables on Render in production. They are never committed to GitHub (`.gitignore` protects them) and are only accessible inside server-side route handlers.",
        None
    )
    add_qa(
        doc, 53,
        "What is TypeScript's role in the project and how does `types.ts` enhance code reliability?",
        "`types.ts` defines strict interfaces (`DocumentRecord`, `ExtractedClause`, `Reminder`, `AuditLogEntry`, `RiskLevel`). TypeScript provides compile-time type verification, catching missing properties or incorrect types before deployment, eliminating common runtime JavaScript errors like `cannot read property of undefined`.",
        None
    )
    add_qa(
        doc, 54,
        "What HTTP status codes does your API return and how are errors handled?",
        "- `200 OK`: Successful data retrieval or email dispatch.\n- `201 Created`: New agreement or reminder successfully added.\n- `400 Bad Request`: Missing mandatory fields (e.g. empty title or invalid date).\n- `500 Internal Server Error`: Caught unexpected exceptions with clean JSON error messages wrapped in `try/catch` blocks.",
        None
    )

    # =========================================================================
    # PART 4: TOUGH EXAMINER TRAP QUESTIONS & DEFENSE STRATEGIES
    # =========================================================================
    p_sec4 = doc.add_paragraph()
    p_sec4.paragraph_format.space_before = Pt(18)
    p_sec4.paragraph_format.space_after = Pt(6)
    r_sec4 = p_sec4.add_run("PART 4: TOUGH EXAMINER TRAP QUESTIONS & COUNTER-ARGUMENTS")
    r_sec4.font.name = "Calibri"
    r_sec4.font.size = Pt(16)
    r_sec4.font.bold = True
    r_sec4.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_qa(
        doc, 55,
        "TRAP QUESTION: 'Render free tier spins down after 15 minutes of inactivity. How does your daily cron run if the server is asleep?'",
        "Excellent question, sir. In a production cloud deployment, relying solely on an internal node-cron process on a sleeping free-tier instance would miss midnight triggers. To solve this, TermGuard exposes a dedicated secure HTTP webhook endpoint at `POST /api/cron`. We use an external cron service (such as cron-job.org or GitHub Actions Scheduled Workflows) that pings this endpoint every 24 hours. The incoming HTTP request wakes up the Render container, executes the date evaluations, sends pending emails, and records audit logs.",
        "This is a masterstroke answer. Faculty will be thoroughly impressed by this cloud architectural awareness."
    )
    add_qa(
        doc, 56,
        "TRAP QUESTION: 'Why did you use a local JSON file (`db.json`) instead of a real relational database like PostgreSQL or MySQL?'",
        "For an academic prototype and demonstration environment, a structured JSON transactional database eliminates external connection latency, cloud database tier costs, and credential rotation overhead while maintaining full ACID-like transactional writes through atomic file updates. More importantly, the system is designed with a Repository Pattern in `src/lib/storage.ts`: all storage functions (`getReminders`, `saveAgreement`, `addAuditLog`) can be swapped to PostgreSQL with Prisma ORM in under 30 minutes without altering a single line of UI or API code.",
        "Emphasize the 'Repository Pattern' abstraction."
    )
    add_qa(
        doc, 57,
        "TRAP QUESTION: 'Why can't a user just use ChatGPT directly instead of your website?'",
        "ChatGPT is a stateless conversational text generator; it is not an autonomous monitoring system. ChatGPT cannot wake up at midnight on September 14, check calendar dates against system time, send an automated transactional email to your Gmail inbox, track status in a persistent database, or display a live visual countdown HUD. TermGuard is an integrated software system that uses AI only as one component inside an automated deadline tracking architecture.",
        "Examiners frequently test if your project is just a 'wrapper'. This answer cleanly destroys that misconception."
    )
    add_qa(
        doc, 58,
        "TRAP QUESTION: 'Is your pre-written dispute letter legally valid in an Indian consumer court?'",
        "Yes, sir. Under the Consumer Protection Act 2019, Section 2(47) defines 'unfair trade practices', and Section 2(46) defines 'unfair contracts'—specifically clauses imposing unreasonable conditions or penalties. A formal written notice sent to a service provider's registered email before the notice window expires constitutes admissible electronic evidence under Section 65B of the Indian Evidence Act.",
        "Citing real consumer law provisions demonstrates unmatched domain knowledge."
    )
    add_qa(
        doc, 59,
        "TRAP QUESTION: 'What happens if a contract contains multiple conflicting dates?'",
        "The parser evaluates all date occurrences and maps them to their respective clauses. If a contract specifies an initial agreement end date and a separate cancellation notice cutoff, the system prioritizes the earliest actionable deadline (the notice cutoff date), because missing that cutoff triggers the financial penalty.",
        None
    )
    add_qa(
        doc, 60,
        "TRAP QUESTION: 'What if the user uploads a contract that is 100 pages long?'",
        "In our current implementation, documents are chunked and streamed through regex filters that search specifically for cancellation keywords ('notice', 'auto-renew', 'terminate', 'debit', 'fee') so only relevant clauses are analyzed, preventing buffer overflow or memory spikes. For massive enterprise contracts, we can employ asynchronous queue workers with Redis BullMQ to process pages in parallel.",
        None
    )
    add_qa(
        doc, 61,
        "TRAP QUESTION: 'What prevents someone from spamming your `/api/email` endpoint to send thousands of emails?'",
        "In production, rate limiting is implemented via Next.js middleware and IP-based token buckets (e.g., Upstash Redis rate limiter), allowing a maximum of 5 email triggers per user per hour. Additionally, in our code, the email dispatch requires a valid reminder ID existing in the internal database.",
        None
    )

    # =========================================================================
    # PART 5: THEORETICAL & ACADEMIC VIVA QUESTIONS
    # =========================================================================
    p_sec5_theo = doc.add_paragraph()
    p_sec5_theo.paragraph_format.space_before = Pt(18)
    p_sec5_theo.paragraph_format.space_after = Pt(6)
    r_sec5_theo = p_sec5_theo.add_run("PART 5: ACADEMIC & SOFTWARE ENGINEERING METHODOLOGY QUESTIONS")
    r_sec5_theo.font.name = "Calibri"
    r_sec5_theo.font.size = Pt(16)
    r_sec5_theo.font.bold = True
    r_sec5_theo.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_qa(
        doc, 62,
        "What Software Development Life Cycle (SDLC) model was used to develop TermGuard?",
        "We followed the Agile Scrum methodology with 2-week sprint cycles. Sprint 1 focused on requirement analysis and UI wireframing; Sprint 2 focused on API route implementation and storage layer; Sprint 3 focused on Resend email integration and cron logic; and Sprint 4 focused on testing, live cloud deployment, and presentation preparation.",
        None
    )
    add_qa(
        doc, 63,
        "What is the difference between Verification and Validation in your testing phase?",
        "Verification answered 'Are we building the product right?' (checking code quality, TypeScript syntax, unit tests for date calculations). Validation answered 'Are we building the right product?' (testing whether an actual Gmail user receives a readable dispute notice before the cutoff and can cancel their membership successfully).",
        "A classic software engineering viva question that examiners love to ask."
    )
    add_qa(
        doc, 64,
        "What is White Box Testing and how did you apply it?",
        "White Box Testing involves examining internal code structures and execution paths. We applied it by tracing path coverage inside `src/app/api/cron/route.ts` to ensure all branches (Stage 1 7-day, Stage 2 1-day, Stage 3 Final cutoff, and Stage 4 auto-cleanup) execute correctly under various mock time inputs.",
        None
    )
    add_qa(
        doc, 65,
        "What is Black Box Testing and how did you apply it?",
        "Black Box Testing examines functionality without looking at internal code. We applied it by uploading various valid and malformed contracts through the frontend modal UI and verifying that expected countdown timers and risk scores were displayed without checking internal variables.",
        None
    )

    # 8 NEW HIGH-VALUE QUESTIONS (Total = 75 Q&A)
    doc.add_heading("Additional Technical & Architectural In-Depth Questions", level=2)
    add_qa(
        doc, 66,
        "How do you ensure cross-browser compatibility between Chrome, Safari, and mobile screens?",
        "We utilized Tailwind CSS with mobile-first viewport utility classes (`w-full md:w-1/2 lg:w-1/3`), CSS flexbox, and modern CSS grid. We also configured HTML5 viewport meta tags (`width=device-width, initial-scale=1.0`) and tested rendered UI across Chromium, WebKit (Safari), and Gecko (Firefox) rendering engines.",
        None
    )
    add_qa(
        doc, 67,
        "What is Server-Side Rendering (SSR) vs Static Site Generation (SSG), and which is used here?",
        "SSG builds HTML at compile time, whereas SSR generates fresh HTML on each client request. TermGuard uses hybrid rendering: the landing layout is statically pre-rendered for instant delivery, while dynamic agreement states, active countdown timers, and audit logs are re-hydrated dynamically via client components and API endpoints.",
        None
    )
    add_qa(
        doc, 68,
        "How does TermGuard protect user privacy if a contract contains credit card or Aadhaar numbers?",
        "The system has a zero-financial-credential policy: it does not store bank account or credit card numbers. Text parsing applies client-side regex masks that detect payment patterns and redact them prior to storage. Only agreement title, renewal dates, and extracted clause excerpts are retained.",
        "Privacy and data protection questions are very popular with examiners."
    )
    add_qa(
        doc, 69,
        "How does the Resend API authenticate emails to ensure they do not go into the Spam folder?",
        "Resend signs outgoing emails with DomainKeys Identified Mail (DKIM) and validates Sender Policy Framework (SPF) DNS records. Because emails are sent from authenticated domains with high reputation scores, email service providers (Gmail, Outlook) verify sender legitimacy and deliver directly to the primary inbox.",
        None
    )
    add_qa(
        doc, 70,
        "What is an ORM and why would you use Prisma ORM when migrating to PostgreSQL?",
        "An Object-Relational Mapper (ORM) maps database tables to TypeScript classes/types. Prisma ORM provides type-safe database queries, automated SQL migrations, and schema validation. By plugging Prisma into `src/lib/storage.ts`, we can switch from `db.json` to PostgreSQL without modifying our frontend or API routes.",
        None
    )
    add_qa(
        doc, 71,
        "Explain Synchronous vs Asynchronous execution in Node.js regarding your email dispatch.",
        "Node.js runs on a single-threaded non-blocking event loop. Calling `await dispatchReminderEmail()` dispatches the network request asynchronously using JavaScript promises. The thread is not blocked while waiting for the Resend server to respond; it continues processing other requests, resuming only when the promise resolves with the email message ID.",
        None
    )
    add_qa(
        doc, 72,
        "How did you and your partner use Git and GitHub during development?",
        "We maintained the repository at `github.com/laxmiharshithrebally-a11y/TermGuard`. We followed feature branching, committed atomic changes with descriptive commit messages, reviewed diffs before merging into `main`, and connected the `main` branch to Render for automated Continuous Deployment (CD).",
        "Demonstrates modern industry-standard DevOps collaboration."
    )
    add_qa(
        doc, 73,
        "How would TermGuard handle a company silently updating its Terms of Service midway through a plan?",
        "In our Version 2.0 roadmap, we have designed a Contract Diffing Engine using the Levenshtein Distance and Myers Diff algorithm. When a user uploads an amended agreement, TermGuard compares it against the original document, highlighting newly inserted arbitration clauses, price hikes, or shortened cancellation periods in red.",
        None
    )

    # =========================================================================
    # PART 6: EXAMINER PSYCHOLOGY & HIGH-SCORING DEFENSE TACTICS
    # =========================================================================
    p_sec6 = doc.add_paragraph()
    p_sec6.paragraph_format.space_before = Pt(18)
    p_sec6.paragraph_format.space_after = Pt(6)
    r_sec6 = p_sec6.add_run("PART 6: HIGH-SCORING DEFENSE STRATEGIES & VIVA TACTICS")
    r_sec6.font.name = "Calibri"
    r_sec6.font.size = Pt(16)
    r_sec6.font.bold = True
    r_sec6.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    add_qa(
        doc, 74,
        "What should you say if an examiner asks a technical question you don't know?",
        "'Sir, in our current implementation, we handled this using [explain what you currently have]. While we have not yet explored [the examiner's specific suggestion], that is a very valuable recommendation which we can incorporate into our Version 2.0 roadmap.' Never say 'I don't know' or stay silent.",
        "Pivot from what you know to future scope—examiners respect this professional attitude."
    )
    add_qa(
        doc, 75,
        "How should you respond if an examiner criticizes: 'This is just a simple CRUD application'?",
        "'Sir, while standard CRUD apps simply store and display records, TermGuard is an autonomous state-machine. Once data is submitted, the user never touches the app again. The autonomous cron worker wakes up every 24 hours, tracks dynamic time differentials, computes risk classifications, generates legal dispute citations, and dispatches multi-channel email alerts. It is an active consumer defense watchdog, not a passive data repository.'",
        "This completely disarms the 'simple CRUD' objection."
    )

    # =========================================================================
    # PART 7: 2-MINUTE SPOKEN DEFENSE SCRIPT FOR HARSHITH & SHUBHAM
    # =========================================================================
    p_sec7 = doc.add_paragraph()
    p_sec7.paragraph_format.space_before = Pt(18)
    p_sec7.paragraph_format.space_after = Pt(6)
    r_sec7 = p_sec7.add_run("PART 7: 2-MINUTE VIVA PRESENTATION OPENING & CLOSING SCRIPT")
    r_sec7.font.name = "Calibri"
    r_sec7.font.size = Pt(16)
    r_sec7.font.bold = True
    r_sec7.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    doc.add_heading("Opening Presentation Speech (Harshith Rebally)", level=3)
    p_h = doc.add_paragraph()
    p_h.add_run(
        "\"Good morning respected external examiner and faculty members. My name is Rebally Laxmi Harshith, and along with my teammate Shubham Pradhan, we are presenting our mini project titled 'TermGuard: Autonomous Contract Analysis and Multi-Channel Deadline Defense System'.\n\n"
        "Today, over 99% of consumers accept lengthy digital contracts for gym passes, subscriptions, and rental leases without reading them. Companies deliberately exploit this by hiding strict 30-day cancellation notice periods and non-refundable auto-renewals in the fine print. When users finally realize they want to cancel on renewal day, it is already too late—their bank account has been debited.\n\n"
        "TermGuard solves this by acting as an autonomous 24/7 contract watchdog. It scans agreements, flags unfair traps, tracks deadlines in the background, and dispatches timely email alerts containing ready-to-send legal dispute letters. Now, my teammate Shubham will walk you through the system architecture and implementation.\""
    )

    doc.add_heading("Technical Handover Speech (Shubham Pradhan)", level=3)
    p_s = doc.add_paragraph()
    p_s.add_run(
        "\"Thank you, Harshith. Respected faculty, the technical core of TermGuard is structured into four layers: Next.js 14 and React 18 on the presentation tier, serverless API route handlers on the application tier, an autonomous Node-cron scheduler running daily deadline evaluations, and the Resend API delivering transactional email alerts.\n\n"
        "We have deployed TermGuard live on Render at https://termguard.onrender.com. The system calculates an objective 0 to 100 risk score, maintains an immutable activity audit log, and has been verified with live Gmail alerts. We welcome you to review our live demonstration and we look forward to your questions.\""
    )

    out_file = r"D:\TERMGUARD\TERMGUARD\TermGuard_Exhaustive_Viva_Master_Encyclopedia.docx"
    doc.save(out_file)
    print(f"SUCCESS: Saved Master Viva Encyclopedia to {out_file}")

if __name__ == "__main__":
    build_encyclopedia()
