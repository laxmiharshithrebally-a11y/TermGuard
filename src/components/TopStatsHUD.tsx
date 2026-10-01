"use client";

import React, { useState } from "react";
import { ShieldCheck, IndianRupee, Clock, Activity, FileText, PlusCircle, HelpCircle, ChevronDown, ChevronUp, Bell } from "lucide-react";

interface TopStatsHUDProps {
  totalProtectedUsd: number;
  totalContracts: number;
  activeDeadlines: number;
  onSelectSample: (docId: string) => void;
  onOpenCreateModal?: () => void;
}

export default function TopStatsHUD({
  totalProtectedUsd,
  totalContracts,
  activeDeadlines,
  onSelectSample,
  onOpenCreateModal,
}: TopStatsHUDProps) {
  const [showExplanation, setShowExplanation] = useState(false);

  return (
    <div className="mb-6 space-y-4">
      {/* Friendly Explanation Banner */}
      <div className="p-3.5 rounded-xl bg-white border border-slate-300 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2.5 text-slate-800">
          <div className="w-6 h-6 rounded-lg bg-[#0f172a] text-indigo-400 flex items-center justify-center shrink-0">
            <HelpCircle className="w-4 h-4" />
          </div>
          <div>
            <span className="font-bold text-[#0f172a]">TermGuard Metric Dashboard:</span>{" "}
            <span className="text-slate-600 font-medium">
              Protecting liability in ₹ INR, enforcing 3-stage notice cutoff schedules, and guarding your contracts.
            </span>
          </div>
        </div>

        <button
          onClick={() => setShowExplanation(!showExplanation)}
          className="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1 self-start sm:self-auto shrink-0 transition-colors"
        >
          <span>{showExplanation ? "Hide Details" : "How TermGuard Works"}</span>
          {showExplanation ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>
      </div>

      {showExplanation && (
        <div className="p-4 rounded-xl bg-[#0f172a] border border-slate-700 text-xs text-slate-300 leading-relaxed space-y-2 animate-in fade-in duration-200 shadow-lg">
          <p className="font-bold text-indigo-300">
            🛡️ TermGuard Autonomous Defense System:
          </p>
          <ul className="list-disc list-inside space-y-1.5 text-slate-300 pl-1 font-medium">
            <li><strong>Total Money Protected:</strong> The sum of annual fees, rental deposit deductions, and penalties prevented by sending timely cancellation notice.</li>
            <li><strong>3-Stage Auto-Alerts:</strong> Alerts are dispatched <strong>7 days before</strong> (early warning), <strong>24 hours before</strong> (urgent), and on the <strong>final cutoff day</strong>.</li>
            <li><strong>Auto-Delete Cleanup:</strong> When a deadline passes, TermGuard automatically archives and removes it from active monitoring to prevent clutter.</li>
            <li><strong>Delivery:</strong> Connected to live Resend email and cellular Twilio SMS to your mobile phone.</li>
          </ul>
        </div>
      )}

      {/* 4 Executive Dark Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        {/* Card 1: Money Protected */}
        <div className="exec-dark-card p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-400 mb-1.5">
              <span>Total Money Protected</span>
              <div className="p-1 rounded-md bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                <IndianRupee className="w-3.5 h-3.5" />
              </div>
            </div>
            <div className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              ₹{totalProtectedUsd.toLocaleString("en-IN")}
            </div>
          </div>
          <p className="text-[11px] text-emerald-400 mt-2 font-medium">
            Saved from auto-renewals & penalty traps
          </p>
        </div>

        {/* Card 2: Active Notice Deadlines */}
        <div className="exec-dark-card p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-400 mb-1.5">
              <span>Active Deadlines Monitored</span>
              <div className="p-1 rounded-md bg-amber-500/15 text-amber-400 border border-amber-500/30">
                <Clock className="w-3.5 h-3.5" />
              </div>
            </div>
            <div className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              {activeDeadlines} <span className="text-sm font-semibold text-slate-400">Cutoffs</span>
            </div>
          </div>
          <p className="text-[11px] text-amber-400 mt-2 font-medium">
            3-Stage countdown alerts active
          </p>
        </div>

        {/* Card 3: Contracts Guarded */}
        <div className="exec-dark-card p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-400 mb-1.5">
              <span>Monitored Agreements</span>
              <div className="p-1 rounded-md bg-indigo-500/15 text-indigo-400 border border-indigo-500/30">
                <ShieldCheck className="w-3.5 h-3.5" />
              </div>
            </div>
            <div className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              {totalContracts} <span className="text-sm font-semibold text-slate-400">Agreements</span>
            </div>
          </div>
          <p className="text-[11px] text-indigo-400 mt-2 font-medium">
            Verified clause citations extracted
          </p>
        </div>

        {/* Card 4: Alert Delivery Status */}
        <div className="exec-dark-card p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-400 mb-1.5">
              <span>Cellular & Email Alert Core</span>
              <div className="p-1 rounded-md bg-cyan-500/15 text-cyan-400 border border-cyan-500/30">
                <Activity className="w-3.5 h-3.5" />
              </div>
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-xl font-bold text-white tracking-tight">
                SMS & Email Live
              </span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 mt-2 font-medium">
            Twilio Cellular & Resend Inboxes Active
          </p>
        </div>
      </div>

      {/* Preset Agreement Selector Banner in Executive Dark Style */}
      <div className="p-3.5 rounded-xl exec-dark-card flex flex-col lg:flex-row lg:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 text-slate-300 font-medium">
          <span className="px-2.5 py-1 rounded-lg bg-indigo-600/30 text-indigo-300 font-bold text-[11px] border border-indigo-500/30 shrink-0">
            Quick Radar
          </span>
          <span>Switch agreement to inspect traps & obligations:</span>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => onSelectSample("doc-gym-001")}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium transition-all"
          >
            <FileText className="w-3.5 h-3.5 text-indigo-400" />
            <span>Cult.fit Gym (₹32,000)</span>
          </button>
          <button
            onClick={() => onSelectSample("doc-lease-002")}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium transition-all"
          >
            <FileText className="w-3.5 h-3.5 text-amber-400" />
            <span>Bangalore Flat (₹70,000)</span>
          </button>
          <button
            onClick={() => onSelectSample("doc-saas-003")}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium transition-all"
          >
            <FileText className="w-3.5 h-3.5 text-blue-400" />
            <span>Cloud SaaS (₹48,000)</span>
          </button>

          {/* Prominent Add Custom Agreement Button */}
          {onOpenCreateModal && (
            <button
              onClick={onOpenCreateModal}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold shadow-sm transition-all ml-auto sm:ml-0"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span>+ Add Any Agreement / Topic</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
