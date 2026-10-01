"use client";

import React, { useState, useEffect } from "react";
import {
  Clock,
  Mail,
  Zap,
  CheckCircle2,
  AlertCircle,
  FileText,
  IndianRupee,
  Trash2,
  Calendar,
  ChevronDown,
  ChevronUp,
  Send,
  Phone,
  PlusCircle,
  X,
  Copy,
  Bell,
  AlertTriangle,
} from "lucide-react";
import { Reminder } from "@/lib/types";
import SendAlertModal from "./SendAlertModal";

interface RemindersCenterProps {
  reminders: Reminder[];
  onTriggerEmail: (reminderId: string, emailOverride?: string) => Promise<void>;
  onUpdateStatus: (id: string, status: Reminder["status"]) => Promise<void>;
  onSnooze: (id: string) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
  onTriggerCron: () => void;
  isCronRunning?: boolean;
  defaultEmail?: string;
  hasResendKey?: boolean;
  onOpenSettings?: () => void;
  onOpenOutbox?: () => void;
  onOpenCreateModal?: () => void;
}

export default function RemindersCenter({
  reminders,
  onTriggerEmail,
  onUpdateStatus,
  onSnooze,
  onDelete,
  onTriggerCron,
  isCronRunning = false,
  defaultEmail = "laxmiharshithrebally@gmail.com",
  hasResendKey = true,
  onOpenSettings,
  onOpenOutbox,
  onOpenCreateModal,
}: RemindersCenterProps) {
  const [filter, setFilter] = useState<"ALL" | "PENDING" | "TRIGGERED" | "RESOLVED">("ALL");
  const [selectedNoticeReminder, setSelectedNoticeReminder] = useState<Reminder | null>(null);
  const [selectedAlertReminder, setSelectedAlertReminder] = useState<Reminder | null>(null);
  const [expandedQuotes, setExpandedQuotes] = useState<Record<string, boolean>>({});
  const [now, setNow] = useState(Date.now());

  // Countdown timer
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, []);

  const calculateCountdown = (dueAt: string) => {
    const diff = new Date(dueAt).getTime() - now;
    if (diff <= 0) return { expired: true, text: "Cutoff Passed / Due Now", daysLeft: 0, hoursLeft: 0 };

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / 1000 / 60) % 60);
    const seconds = Math.floor((diff / 1000) % 60);

    return {
      expired: false,
      text: `${days}d ${hours}h ${minutes}m ${seconds}s`,
      daysLeft: days,
      hoursLeft: days * 24 + hours,
    };
  };

  const filteredReminders = reminders.filter((r) => {
    if (filter === "ALL") return true;
    return r.status === filter;
  });

  const toggleQuote = (id: string) => {
    setExpandedQuotes((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="space-y-5">
      {/* Header & Filter Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-slate-300">
        <div>
          <h2 className="text-xl font-black text-[#0f172a] tracking-tight">
            Monitored Deadlines & 3-Stage Notice Alerts
          </h2>
          <p className="text-xs text-slate-600 mt-0.5 font-medium">
            Automated alerts at 1-week, 24-hours, and final cutoff day • Auto-deletes after expiry
          </p>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          {/* Add New Agreement / Topic Button */}
          {onOpenCreateModal && (
            <button
              onClick={onOpenCreateModal}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm transition-all"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span>+ Add Agreement / Topic</span>
            </button>
          )}

          {/* Status Tabs in Executive Dark Style */}
          <div className="flex items-center bg-[#0f172a] p-1 rounded-xl border border-slate-700">
            {(["ALL", "PENDING", "TRIGGERED", "RESOLVED"] as const).map((status) => (
              <button
                key={status}
                onClick={() => setFilter(status)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  filter === status
                    ? "bg-indigo-600 text-white shadow-sm font-bold"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                {status}
              </button>
            ))}
          </div>

          {/* Trigger Cron Button */}
          <button
            onClick={onTriggerCron}
            disabled={isCronRunning}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#0f172a] hover:bg-slate-800 text-slate-200 border border-slate-700 text-xs font-semibold transition-all shadow-sm"
          >
            <Zap className={`w-3.5 h-3.5 text-amber-400 ${isCronRunning ? "animate-spin" : ""}`} />
            <span>{isCronRunning ? "Scanning..." : "Run Cron"}</span>
          </button>
        </div>
      </div>

      {/* Modern Executive Dual-Tone Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredReminders.map((reminder) => {
          const countdown = calculateCountdown(reminder.dueAt);
          const isQuoteOpen = expandedQuotes[reminder.id];

          // Determine current stage for display
          const isUrgent24h = !countdown.expired && countdown.hoursLeft <= 24;
          const isWarning7d = !countdown.expired && countdown.daysLeft <= 7 && countdown.hoursLeft > 24;

          return (
            <div
              key={reminder.id}
              className="exec-dark-card p-5 flex flex-col justify-between space-y-4"
            >
              <div>
                {/* Status + Financial Risk */}
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-1.5">
                    <span
                      className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider ${
                        reminder.status === "TRIGGERED"
                          ? "bg-purple-500/20 text-purple-300 border border-purple-500/30"
                          : reminder.status === "RESOLVED"
                          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                          : "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                      }`}
                    >
                      {reminder.status}
                    </span>

                    {/* Stage Badge */}
                    {isUrgent24h ? (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3 text-amber-400" />
                        <span>24H Alert</span>
                      </span>
                    ) : isWarning7d ? (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 flex items-center gap-1">
                        <Bell className="w-3 h-3 text-indigo-400" />
                        <span>7D Warning</span>
                      </span>
                    ) : null}
                  </div>

                  {reminder.financialImpactUsd ? (
                    <span className="text-xs font-bold text-amber-400 bg-amber-500/10 px-2.5 py-0.5 rounded-md border border-amber-500/20 flex items-center gap-0.5">
                      <IndianRupee className="w-3 h-3" />
                      <span>{reminder.financialImpactUsd.toLocaleString("en-IN")} at risk</span>
                    </span>
                  ) : null}
                </div>

                {/* Reminder Title */}
                <h3 className="text-base font-bold text-white tracking-tight leading-snug">
                  {reminder.title}
                </h3>

                {reminder.documentTitle && (
                  <p className="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
                    <FileText className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                    <span className="truncate">{reminder.documentTitle}</span>
                  </p>
                )}

                {/* Live Countdown Box */}
                <div className="mt-3.5 p-3 rounded-xl bg-[#080d1a] border border-slate-800 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1.5 text-slate-400 font-medium">
                    <Clock className="w-3.5 h-3.5 text-indigo-400" />
                    <span>Notice Cutoff:</span>
                  </div>
                  <div className="font-mono font-bold text-white">
                    {countdown.text}
                  </div>
                </div>

                {/* Verified Source Clause */}
                {reminder.sourceClauseQuote && (
                  <div className="mt-3">
                    <button
                      onClick={() => toggleQuote(reminder.id)}
                      className="text-[11px] text-slate-400 hover:text-white flex items-center gap-1 font-medium transition-colors"
                    >
                      <span>
                        Verified Clause {reminder.sourceSection ? `(${reminder.sourceSection})` : ""}
                      </span>
                      {isQuoteOpen ? (
                        <ChevronUp className="w-3 h-3" />
                      ) : (
                        <ChevronDown className="w-3 h-3" />
                      )}
                    </button>
                    {isQuoteOpen && (
                      <div className="mt-1.5 p-2.5 rounded-lg bg-[#080d1a] border border-slate-800 font-mono text-[11px] text-slate-300 leading-relaxed">
                        "{reminder.sourceClauseQuote}"
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="pt-3 border-t border-slate-800 space-y-2">
                <div className="flex items-center gap-2">
                  {/* Send Alert Button */}
                  <button
                    onClick={() => setSelectedAlertReminder(reminder)}
                    className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow-sm"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>Send Alert (Email / SMS)</span>
                  </button>

                  {/* Pre-Written Notice */}
                  {reminder.cancellationNoticeDraft && (
                    <button
                      onClick={() => setSelectedNoticeReminder(reminder)}
                      className="py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-all shadow-xs"
                      title="View Formal Legal Cancellation Notice Letter"
                    >
                      Legal Notice
                    </button>
                  )}
                </div>

                {/* Snooze, Resolve, Delete */}
                <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
                  <div className="flex items-center gap-2 font-medium">
                    <button
                      onClick={() => onSnooze(reminder.id)}
                      className="hover:text-indigo-400 transition-colors"
                    >
                      + Snooze 24h
                    </button>
                    <span>•</span>
                    <button
                      onClick={() =>
                        onUpdateStatus(
                          reminder.id,
                          reminder.status === "RESOLVED" ? "PENDING" : "RESOLVED"
                        )
                      }
                      className="hover:text-emerald-400 transition-colors"
                    >
                      {reminder.status === "RESOLVED" ? "Re-Open" : "Mark Resolved"}
                    </button>
                  </div>

                  <button
                    onClick={() => onDelete(reminder.id)}
                    className="text-slate-500 hover:text-rose-400 p-1 transition-colors"
                    title="Delete Reminder"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {filteredReminders.length === 0 && (
        <div className="exec-dark-card p-12 text-center text-slate-400 text-xs space-y-3">
          <p>No deadlines found for this filter.</p>
          {onOpenCreateModal && (
            <button
              onClick={onOpenCreateModal}
              className="px-4 py-2 rounded-xl bg-indigo-600 text-white font-semibold text-xs shadow-xs hover:bg-indigo-500 transition-all"
            >
              + Add Your First Agreement or Topic
            </button>
          )}
        </div>
      )}

      {/* Send Alert Modal (Email / Normal SMS) */}
      <SendAlertModal
        isOpen={Boolean(selectedAlertReminder)}
        onClose={() => setSelectedAlertReminder(null)}
        reminder={selectedAlertReminder}
        defaultEmail={defaultEmail}
        onSendEmail={onTriggerEmail}
      />

      {/* Pre-Written Legal Notice Modal */}
      {selectedNoticeReminder && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#0f172a] border border-slate-700 w-full max-w-xl rounded-2xl p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white">
                Formal Cancellation / Non-Renewal Notice Letter
              </h3>
              <button
                onClick={() => setSelectedNoticeReminder(null)}
                className="w-7 h-7 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center justify-center"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-400">
              Pre-written termination letter citing verified contract clauses and notice terms.
            </p>

            <textarea
              readOnly
              rows={10}
              value={selectedNoticeReminder.cancellationNoticeDraft}
              className="w-full bg-[#080d1a] border border-slate-800 rounded-xl p-3.5 font-mono text-xs text-slate-200 focus:outline-none leading-relaxed"
            />

            <div className="flex items-center justify-between pt-2">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(
                    selectedNoticeReminder.cancellationNoticeDraft || ""
                  );
                  alert("Copied cancellation notice letter to clipboard!");
                }}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow-xs"
              >
                <Copy className="w-3.5 h-3.5" />
                <span>Copy Letter</span>
              </button>

              <button
                onClick={() => setSelectedNoticeReminder(null)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition-all"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
