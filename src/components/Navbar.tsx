"use client";

import React from "react";
import Link from "next/link";
import { ShieldCheck, Zap, Settings, RefreshCw, Mail, PlusCircle, Bell } from "lucide-react";

interface NavbarProps {
  activeTab?: string;
  setActiveTab?: (tab: string) => void;
  onOpenSettings: () => void;
  onOpenOutbox: () => void;
  onResetDemo: () => void;
  onTriggerCron: () => void;
  isCronRunning?: boolean;
  onOpenCreateModal?: () => void;
}

export default function Navbar({
  activeTab = "chat",
  setActiveTab,
  onOpenSettings,
  onOpenOutbox,
  onResetDemo,
  onTriggerCron,
  isCronRunning = false,
  onOpenCreateModal,
}: NavbarProps) {
  return (
    <header className="sticky top-0 z-40 bg-[#0f172a] border-b border-slate-800 px-4 sm:px-8 py-3 text-white shadow-md">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-600/30">
            <ShieldCheck className="w-4.5 h-4.5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg text-white tracking-tight">
                Term<span className="text-indigo-400">Guard</span>
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-800 text-indigo-300 border border-slate-700 hidden sm:inline-block">
                Contract Defense
              </span>
            </div>
          </div>
        </Link>

        {/* Tab Switcher if on Dashboard */}
        {setActiveTab && (
          <nav className="hidden md:flex items-center gap-1 bg-[#0b0f19] p-1 rounded-xl border border-slate-800">
            {[
              { id: "chat", label: "AI Agent Chat" },
              { id: "documents", label: "Contract Radar" },
              { id: "reminders", label: "Deadlines & Alerts" },
              { id: "audit", label: "Trust Log" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === tab.id
                    ? "bg-indigo-600 text-white shadow-sm font-bold"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/60"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        )}

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {/* Quick Add Custom Agreement Button */}
          {onOpenCreateModal && (
            <button
              onClick={onOpenCreateModal}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm transition-all"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Add Agreement</span>
            </button>
          )}

          {/* Quick Cron Trigger */}
          <button
            onClick={onTriggerCron}
            disabled={isCronRunning}
            title="Force Run 3-Stage Background Check"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold transition-all shadow-xs"
          >
            <Zap className={`w-3.5 h-3.5 text-amber-400 ${isCronRunning ? "animate-spin" : ""}`} />
            <span className="hidden sm:inline">
              {isCronRunning ? "Checking..." : "Run Cron"}
            </span>
          </button>

          {/* Outbox Inspector */}
          <button
            onClick={onOpenOutbox}
            title="View Dispatched Email & SMS Outbox"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium transition-all shadow-xs"
          >
            <Mail className="w-3.5 h-3.5 text-indigo-400" />
            <span className="hidden sm:inline">Outbox</span>
          </button>

          {/* Reset Demo Presets */}
          <button
            onClick={onResetDemo}
            title="Reset to Demo State"
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors border border-slate-700 shadow-xs"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>

          {/* Settings */}
          <button
            onClick={onOpenSettings}
            title="System Settings"
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors border border-slate-700 shadow-xs"
          >
            <Settings className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </header>
  );
}
