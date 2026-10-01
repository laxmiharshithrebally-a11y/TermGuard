"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ShieldAlert,
  ArrowRight,
  Zap,
  Mail,
  FileText,
  Clock,
  CheckCircle2,
  IndianRupee,
  AlertTriangle,
  Sparkles,
  Lock,
  Phone,
  RotateCcw,
  Bell,
  Trash2,
} from "lucide-react";
import { SAMPLE_CONTRACTS } from "@/lib/sampleContracts";
import SplashIntro from "@/components/SplashIntro";

export default function LandingPage() {
  const [selectedSampleIndex, setSelectedSampleIndex] = useState(0);
  const [showSplash, setShowSplash] = useState(true);
  const activeContract = SAMPLE_CONTRACTS[selectedSampleIndex];

  return (
    <>
      {/* 1.8-Second Animated TermGuard Intro Splash Screen */}
      {showSplash && <SplashIntro onComplete={() => setShowSplash(false)} />}

      <div className="min-h-screen bg-[#eef2f6] text-slate-900 flex flex-col selection:bg-indigo-600/15 selection:text-indigo-900">
        {/* Navbar */}
        <header className="sticky top-0 z-40 bg-white/95 border-b border-slate-300/70 px-6 lg:px-12 py-3.5 backdrop-blur-md shadow-xs">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#0f172a] border border-slate-700 flex items-center justify-center text-indigo-400 shadow-md">
                <ShieldAlert className="w-5 h-5 text-indigo-400" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-extrabold text-xl tracking-tight text-[#0f172a]">
                    Term<span className="text-indigo-600">Guard</span>
                  </span>
                  <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-[#0f172a] text-indigo-300 border border-slate-700 hidden sm:inline-block">
                    Contract Defense
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowSplash(true)}
                title="Replay TermGuard Intro Animation"
                className="px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-200/60 transition-all flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Intro Animation</span>
              </button>

              <Link
                href="/dashboard"
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#0f172a] hover:bg-[#1e293b] text-white font-semibold text-xs sm:text-sm shadow-md transition-all hover:scale-[1.02] border border-slate-700"
              >
                <span>Launch Console</span>
                <ArrowRight className="w-4 h-4 text-indigo-400" />
              </Link>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="relative px-6 lg:px-12 pt-16 pb-16 max-w-7xl mx-auto text-center space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-slate-300 text-indigo-700 text-xs font-bold shadow-xs">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>Autonomous Contract & Notice Deadline Guardian</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-black tracking-tight max-w-4xl mx-auto text-[#0f172a] leading-[1.12]">
            Never let hidden clauses & expired dates{" "}
            <span className="bg-gradient-to-r from-indigo-600 via-indigo-700 to-indigo-900 bg-clip-text text-transparent">
              trap your hard-earned money.
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed font-medium">
            TermGuard autonomously parses your rental agreements, gym memberships, insurance, and SaaS contracts to flag predatory traps, enforce 3-stage automated notice alerts, and auto-delete expired deadlines.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 pt-2">
            <Link
              href="/dashboard"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-[#0f172a] hover:bg-[#1e293b] text-white font-bold text-sm sm:text-base shadow-lg transition-all hover:scale-[1.02] flex items-center justify-center gap-2.5 border border-slate-700"
            >
              <span>Open TermGuard Console</span>
              <ArrowRight className="w-5 h-5 text-indigo-400" />
            </Link>
            <a
              href="#try-demo"
              className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 text-sm font-semibold transition-all shadow-xs"
            >
              Explore Live Contracts Below ↓
            </a>
          </div>

          {/* 4 Executive Metric Badges */}
          <div className="pt-10 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
            <div className="exec-dark-card p-4">
              <div className="text-2xl font-extrabold text-indigo-400 font-mono">3-Stage</div>
              <div className="text-xs text-slate-300 mt-1 font-medium">7D, 24H & Final Alerts</div>
            </div>
            <div className="exec-dark-card p-4">
              <div className="text-2xl font-extrabold text-amber-400 font-mono">₹1,50,000</div>
              <div className="text-xs text-slate-300 mt-1 font-medium">Protected in Presets</div>
            </div>
            <div className="exec-dark-card p-4">
              <div className="text-2xl font-extrabold text-emerald-400 font-mono">Email & SMS</div>
              <div className="text-xs text-slate-300 mt-1 font-medium">Real Cellular Towers</div>
            </div>
            <div className="exec-dark-card p-4">
              <div className="text-2xl font-extrabold text-cyan-400 font-mono">Auto-Clean</div>
              <div className="text-xs text-slate-300 mt-1 font-medium">Deletes Expired Notice</div>
            </div>
          </div>
        </section>

        {/* Interactive Try-It Sandbox Section */}
        <section id="try-demo" className="px-6 lg:px-12 py-12 max-w-7xl mx-auto w-full">
          <div className="bg-white rounded-3xl border border-slate-300/80 p-6 sm:p-10 shadow-lg relative overflow-hidden">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6 mb-6">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full bg-[#0f172a] text-indigo-300 text-[11px] font-bold uppercase tracking-wider border border-slate-700">
                    Interactive Contract Radar
                  </span>
                  <span className="text-xs text-slate-500 font-medium">Live Trap Extraction</span>
                </div>
                <h2 className="text-2xl font-bold text-[#0f172a] mt-1">
                  See TermGuard Defense in Action on Real Agreements
                </h2>
              </div>

              {/* Contract Switcher Tabs */}
              <div className="flex items-center gap-2 flex-wrap">
                {SAMPLE_CONTRACTS.map((doc, idx) => (
                  <button
                    key={doc.id}
                    onClick={() => setSelectedSampleIndex(idx)}
                    className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                      selectedSampleIndex === idx
                        ? "bg-[#0f172a] text-white shadow-sm border border-slate-700 font-bold"
                        : "bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200"
                    }`}
                  >
                    {idx === 0 ? "🏋️ Cult.fit Gym Pass" : idx === 1 ? "🏠 Bangalore Rental Flat" : "💻 Cloud Software SaaS"}
                  </button>
                ))}
              </div>
            </div>

            {/* Interactive Split View */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left: Raw Fine Print Preview */}
              <div className="lg:col-span-6 bg-[#0f172a] p-5 rounded-2xl border border-slate-800 font-mono text-xs text-slate-300 space-y-3 max-h-[380px] overflow-y-auto shadow-inner">
                <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider pb-2 border-b border-slate-800 flex items-center justify-between">
                  <span>AGREEMENT EXCERPT</span>
                  <span className="text-indigo-400 font-semibold">{activeContract.category}</span>
                </div>
                <p className="whitespace-pre-wrap leading-relaxed text-slate-200">
                  {activeContract.rawContent}
                </p>
              </div>

              {/* Right: AI Analysis & Trap Detection */}
              <div className="lg:col-span-6 space-y-4">
                <div className="exec-dark-card p-4 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-amber-400 tracking-wider">
                      Contract Hazard Score
                    </span>
                    <div className="text-xl font-extrabold text-white mt-0.5">
                      {activeContract.riskScore}/100 • Critical Trap Clauses
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] uppercase font-bold text-amber-400 tracking-wider">
                      Total At Risk
                    </span>
                    <div className="text-xl font-extrabold text-amber-400 mt-0.5">
                      ₹{activeContract.totalFinancialExposure.toLocaleString("en-IN")}
                    </div>
                  </div>
                </div>

                {/* Extracted Clauses in Dark Executive Style */}
                <div className="space-y-3">
                  {activeContract.clauses.map((clause) => (
                    <div
                      key={clause.id}
                      className="exec-dark-card p-4 space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                          {clause.riskLevel}
                        </span>
                        <span className="text-xs font-mono font-bold text-indigo-400">
                          Cutoff: {clause.deadlineDate}
                        </span>
                      </div>

                      <h4 className="text-sm font-bold text-white">
                        {clause.clauseTitle}
                      </h4>

                      <div className="p-2.5 rounded-lg bg-[#080d1a] font-mono text-[11px] text-slate-300 border border-slate-800">
                        "{clause.quotedText.slice(0, 140)}..."
                      </div>

                      <p className="text-xs text-slate-300 leading-relaxed">
                        <strong className="text-indigo-400">TermGuard Shield:</strong> {clause.explanation}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="pt-2">
                  <Link
                    href="/dashboard"
                    className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs sm:text-sm flex items-center justify-center gap-2 shadow-sm transition-all"
                  >
                    <span>Enforce in Command Console →</span>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 3-Stage Auto-Alert Schedule Showcase */}
        <section className="px-6 lg:px-12 py-12 max-w-7xl mx-auto w-full space-y-8">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <h2 className="text-3xl font-extrabold text-[#0f172a]">
              Automated 3-Stage Notice Lifecycle
            </h2>
            <p className="text-sm text-slate-600 font-medium">
              You never have to remember when to notify. TermGuard fires at the exact key dates and automatically cleans up afterwards.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
            <div className="exec-dark-card p-5 space-y-2.5">
              <div className="w-9 h-9 rounded-xl bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400">
                <Bell className="w-4.5 h-4.5" />
              </div>
              <div className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Stage 1: T - 7 Days</div>
              <h3 className="text-base font-bold text-white">1 Week Early Warning</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Sends an advance heads-up via Email and SMS so you can review notice clauses and draft termination letters with zero rush.
              </p>
            </div>

            <div className="exec-dark-card p-5 space-y-2.5">
              <div className="w-9 h-9 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
                <Clock className="w-4.5 h-4.5" />
              </div>
              <div className="text-xs font-bold text-amber-400 uppercase tracking-wider">Stage 2: T - 24 Hours</div>
              <h3 className="text-base font-bold text-white">24-Hour Urgent Alert</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Urgent notification delivered to your mobile phone and inbox alerting you that tomorrow is the cutoff deadline.
              </p>
            </div>

            <div className="exec-dark-card p-5 space-y-2.5">
              <div className="w-9 h-9 rounded-xl bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-rose-400">
                <AlertTriangle className="w-4.5 h-4.5" />
              </div>
              <div className="text-xs font-bold text-rose-400 uppercase tracking-wider">Stage 3: Deadline Day</div>
              <h3 className="text-base font-bold text-white">Final Cutoff Notice</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Fires on the exact deadline date to prevent auto-renewal lock-in, non-refundable debits, or security deposit forfeiture.
              </p>
            </div>

            <div className="exec-dark-card p-5 space-y-2.5">
              <div className="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
                <Trash2 className="w-4.5 h-4.5" />
              </div>
              <div className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Stage 4: Post-Expiry</div>
              <h3 className="text-base font-bold text-white">Auto-Delete & Archive</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                Once the cutoff date has passed, TermGuard logs a completed audit record and auto-deletes the reminder so your schedule stays clean.
              </p>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-auto border-t border-slate-300/80 py-8 px-6 text-center text-xs text-slate-500 bg-white">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-indigo-600" />
              <span className="font-bold text-[#0f172a]">TermGuard</span>
              <span>• Autonomous Contract & Deadline Defense</span>
            </div>
            <div>
              Built with Next.js 14, Google Gemini 2.5 Flash, Resend API & Twilio Cellular SMS.
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
