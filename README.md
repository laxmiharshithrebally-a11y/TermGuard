# FinePrint AI — Autonomous Contract & Deadline Defense Agent

> **Tagline:** Stop letting fine print quietly drain your wallet.  
> **Location:** `D:\project\fineprint`  
> **Live Local URL:** [http://localhost:3000](http://localhost:3000)

---

## 🌟 What FinePrint AI Does

Companies count on consumers ignoring 20 pages of fine print. **FinePrint AI** is an autonomous contract intelligence and deadline enforcement agent that:
1. **Reads Complex Agreements**: Ingests Gym Contracts, Apartment Leases, SaaS Agreements, Warranties, and Job Offers.
2. **Flags Predatory Clauses & Traps**: Identifies sneaky auto-renewals, 45-day certified postal mail cancellation traps, and security deposit forfeitures with exact quoted source clauses.
3. **Calculates Financial Liability**: Displays the exact dollars at stake (e.g. *$1,740 locked-in fees*).
4. **Enforces Deadlines via Real Email**: Dispatches real emails to your personal inbox via **Resend** before the cancellation cutoff window closes.
5. **Zero-Hallucination Side-by-Side Clause Visualizer**: Clicking any extracted trap highlights and scrolls to the exact contract sentence.
6. **1-Click Pre-Written Dispute & Cancellation Notices**: Auto-generates formal legal cancellation letters citing the exact section codes.
7. **The Trust Layer**: Immutable audit ledger recording every document parse, scheduled date, and Resend message ID.

---

## 🚀 Quick Start Guide

### 1. Launch the Application
The server is currently running at:
👉 **[http://localhost:3000](http://localhost:3000)** (or [http://localhost:3000/dashboard](http://localhost:3000/dashboard))

To launch anytime from your terminal:
```bash
cd D:\project\fineprint
npm start
```
Or double-click `run.bat` in File Explorer.

---

## 🎯 1-Minute Live Demo / Viva Walkthrough

When presenting or showcasing **FinePrint AI**:

1. **The Pitch (Landing Page)**:
   * Open `http://localhost:3000`.
   * Show the headline: *"Stop letting fine print quietly drain your wallet."*
   * Click **"Gym Membership"** in the **Interactive Sandbox** to show instant clause extraction on the public page without signing in.
   * Click **"Launch Dashboard →"**.

2. **The Executive Command Center (`/dashboard`)**:
   * Point to the Top Stats HUD: **3 Contracts Guarded**, **$11,840 Protected Liability**, **Active Deadlines**, and **Agent Nervous System: Active**.

3. **Screen 1: AI Agent Command Hub (Chat)**:
   * Type: *"Remind me next Friday at 6pm to cancel my gym membership"*
   * Show the agent's **Thought Process Badge** (*"Extracting temporal parameters..."*).
   * Show the generated **Interactive Action Card** with the $145 risk calculation.
   * Click **"Approve & Schedule Reminder"** $\rightarrow$ committed to the database in real time!

4. **Screen 2: Document Studio & Clause Radar**:
   * Switch to the **Documents & Radar** tab.
   * Select the **Equinox Sports Club Agreement**.
   * Click the **"Mandatory 45-Day Prior Certified Mail Cutoff"** card on the right.
   * **Watch the left document pane smoothly scroll and glow amber on Section 4.2 & 7.2!** This proves zero hallucination.

5. **Screen 3: Deadlines & Execution Center**:
   * Switch to the **Deadlines** tab.
   * Show the live countdown clock (*"Renews in 339d 21h 14m 33s"*).
   * Click **"📄 Legal Notice"** to reveal the pre-written cancellation letter citing the contract section.
   * Click **"⚡ Send Real Email Now"** $\rightarrow$ shows immediate delivery toast!
   * Click **"⚡ Run Cron Check Now"** to demonstrate how background workers trigger alerts automatically.

6. **Screen 4: The Trust Layer (Activity Log) & Outbox Inspector**:
   * Click **"Trust Log"** in the navbar to show the cryptographic-style audit ledger with timestamps.
   * Click **"Outbox"** in the top bar to inspect the authentic rendered HTML email that arrived in the user's inbox!

---

## ⚙️ Configuration & Real Email Setup

Click the **⚙️ Settings** icon in the top navigation bar to configure:
* **Target Notification Email**: Enter your real personal email (e.g., `yourname@gmail.com`).
* **Resend API Key**: Enter your key from [resend.com](https://resend.com) (`re_...`).  
  *(If no key is entered, FinePrint AI safely renders and logs the authentic email in the In-App Outbox Inspector).*
* **Google Gemini API Key**: Enter your Gemini key (`AIza...`) for extended conversational reasoning.

---

## 🏗️ Architecture Stack

* **Frontend & Backend**: Next.js 14 (App Router) + React 18 + TypeScript + Tailwind CSS
* **Agent Brain**: Google Gemini 2.5 Flash + Conversational Heuristic Safeguard Engine
* **Delivery Nervous System**: Resend Email API + Vercel Cron Dispatch Worker
* **Storage & Ledger**: Persistent zero-dependency JSON database (`/data/db.json`)
* **Design Theme**: Cyber Obsidian (`#090D16`), Cyber Cyan (`#06B6D4`), and Amber Hazard Glow
