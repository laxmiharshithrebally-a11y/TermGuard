# 🛡️ TermGuard — Autonomous Contract & Notice Deadline Defense

> **Live Website:** [https://termguard.onrender.com](https://termguard.onrender.com)  
> **Command Dashboard:** [https://termguard.onrender.com/dashboard](https://termguard.onrender.com/dashboard)  
> **GitHub Repository:** [https://github.com/laxmiharshithrebally-a11y/TermGuard](https://github.com/laxmiharshithrebally-a11y/TermGuard)  

---

## 🌟 Overview

**TermGuard** is an autonomous contract intelligence and notice deadline defense system designed to stop fine print and predatory clauses from quietly draining your hard-earned money.

Companies rely on consumers missing cancellation windows buried in 20-page agreements. TermGuard parses agreements, flags traps, calculates liability at stake in **₹ INR**, enforces **3-stage automated alerts (via Cellular SMS & Email)**, and automatically deletes expired deadlines.

---

## 🚀 Key Features

### 1. 1.8-Second Animated Splash Intro
- Features an animated security shield with pulsing energy radar rings, initialization progress bar, and metallic brand reveal when the site opens.

### 2. Executive Dual-Tone Interface
- **Canvas:** Soft ambient titanium mist (`#EEF2F6`) with subtle radial illumination.
- **Option Cards & Controls:** Deep obsidian charcoal cards (`#0F172A`) with high-contrast typography, gold/amber ₹ INR indicators, and emerald status badges.

### 3. 3-Stage Automated Notice Lifecycle & Auto-Deletion
TermGuard autonomously monitors your contract cutoffs:
- 🔔 **Stage 1 (1 Week Before / T - 7 Days):** Automated early warning alert dispatched via Cellular SMS and Email to give you ample time to prepare.
- ⚠️ **Stage 2 (1 Day Before / T - 24 Hours):** Urgent action alert dispatched warning that tomorrow is the final notice cutoff.
- 🛑 **Stage 3 (On Final Cutoff Day):** Final call alert dispatched indicating the window closes today.
- 🗑️ **Stage 4 (Auto-Deletion After Expiration):** Once the cutoff date has passed, TermGuard automatically archives and removes the reminder from active view so your dashboard stays clean.

### 4. Real Cellular Mobile SMS & Email Dispatch
- **Cellular SMS:** Directly integrated with **Twilio** to deliver instant SMS notifications to verified mobile phones over the air (`[TermGuard Alert]`).
- **Live Email:** Dispatches verified notice reminders via **Resend** with pre-written formal cancellation letter drafts citing exact contract clauses.

### 5. Add Custom Agreements & Alert Topics
- Dedicated **Last Date / Cutoff Date** calendar picker with cutoff time and money at risk in ₹ INR.
- Pre-formats formal cancellation letters ready to copy and send to support or landlords.

### 6. Zero-Hallucination Document Studio & Hazard Radar
- Side-by-side agreement reader that automatically highlights and scrolls to the exact clause sentence in the contract text when clicked.

### 7. Immutable Trust Ledger
- Cryptographically verifiable audit trail recording every document parsed, trap extracted, scheduled deadline, and SMS/Email message ID.

---

## 🛠️ Tech Stack

- **Framework:** Next.js 14 (App Router, Server Actions, TypeScript)
- **Styling:** Tailwind CSS (Executive Dual-Tone Theme)
- **SMS Gateway:** Twilio Cellular SMS API
- **Email Gateway:** Resend API
- **AI Core:** Google Gemini Flash Engine (heuristic + generative clause analysis)
- **Hosting:** Render (`https://termguard.onrender.com`)

---

## 💻 Local Setup & Development

```bash
# 1. Clone repository
git clone https://github.com/laxmiharshithrebally-a11y/TermGuard.git
cd TermGuard

# 2. Install dependencies
npm install

# 3. Configure environment (.env.local)
RESEND_API_KEY="your_resend_key"
TWILIO_ACCOUNT_SID="your_twilio_sid"
TWILIO_AUTH_TOKEN="your_twilio_token"
TWILIO_PHONE_NUMBER="your_twilio_number"
TWILIO_MESSAGING_SERVICE_SID="your_messaging_service_sid"

# 4. Run development server
npm run dev

# 5. Open in browser
http://localhost:3000
```

---

## 🌐 Production Deployment

TermGuard is configured for 1-click deployment on Render via [`render.yaml`](render.yaml):
- **Live URL:** [https://termguard.onrender.com](https://termguard.onrender.com)
