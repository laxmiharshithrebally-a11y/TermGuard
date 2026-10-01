"use client";

import React, { useState } from "react";
import { PlusCircle, Calendar, ShieldCheck, X, FileText, CheckCircle2 } from "lucide-react";

interface CreateAgreementModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export default function CreateAgreementModal({
  isOpen,
  onClose,
  onCreated,
}: CreateAgreementModalProps) {
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("INSURANCE");
  const [deadlineDate, setDeadlineDate] = useState(() => {
    // Default to 30 days from now
    const d = new Date();
    d.setDate(d.getDate() + 30);
    return d.toISOString().split("T")[0];
  });
  const [deadlineTime, setDeadlineTime] = useState("18:00");
  const [moneyAtRisk, setMoneyAtRisk] = useState<number | "">("");
  const [clauseTerms, setClauseTerms] = useState("");
  const [noticeDraft, setNoticeDraft] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  if (!isOpen) return null;

  // Auto-generate notice draft when title changes if user hasn't typed a custom one
  const handleTitleChange = (val: string) => {
    setTitle(val);
    if (!noticeDraft || noticeDraft.startsWith("To Support / Management,")) {
      setNoticeDraft(
        `To Support / Management Team,\n\nSubject: Formal Notice of Cancellation / Non-Renewal for ${val || "[Agreement Name]"}\n\nPlease accept this formal written notice that I will NOT be renewing this agreement upon expiration. Please ensure no automatic debit or renewal charges are billed to my account/card.\n\nPlease confirm receipt of this notice in writing.\n\nThank you,\nHarshith R.`
      );
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setErrorMsg("Please enter an agreement title or topic name.");
      return;
    }
    if (!deadlineDate) {
      setErrorMsg("Please select a cutoff deadline date.");
      return;
    }

    setIsSubmitting(true);
    setErrorMsg("");

    const isoDueAt = new Date(`${deadlineDate}T${deadlineTime || "18:00"}:00`).toISOString();
    const numericMoney = typeof moneyAtRisk === "number" ? moneyAtRisk : parseInt(String(moneyAtRisk) || "0", 10) || 0;

    try {
      // 1. Create Reminder
      const reminderRes = await fetch("/api/reminders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: `Notice Deadline: ${title}`,
          dueAt: isoDueAt,
          sourceClauseQuote: clauseTerms.trim() || `Must deliver written notice before ${deadlineDate} to cancel without penalty.`,
          sourceSection: "Notice & Cancellation Terms",
          financialImpactUsd: numericMoney,
          documentTitle: title,
          cancellationNoticeDraft: noticeDraft.trim(),
        }),
      });

      // 2. Also register in documents list so it appears in Contract Radar
      await fetch("/api/documents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: title,
          category: category,
          content: `${title.toUpperCase()}\nCATEGORY: ${category}\nDEADLINE: ${deadlineDate} ${deadlineTime}\nMONEY AT RISK: ₹${numericMoney.toLocaleString("en-IN")} INR\nTERMS: ${clauseTerms || "Notice required prior to cutoff to avoid auto-debit."}`,
        }),
      });

      if (reminderRes.ok) {
        onCreated();
        onClose();
        // Reset form
        setTitle("");
        setMoneyAtRisk("");
        setClauseTerms("");
        setNoticeDraft("");
      } else {
        const data = await reminderRes.json();
        setErrorMsg(data.error || "Failed to create agreement.");
      }
    } catch (err: any) {
      setErrorMsg(err.message || "An unexpected error occurred.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-[#0f172a] border border-slate-700 w-full max-w-xl rounded-2xl shadow-2xl flex flex-col overflow-hidden max-h-[92vh] text-slate-100">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
              <PlusCircle className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white">
                Add Agreement or Alert Topic
              </h2>
              <p className="text-xs text-slate-400">
                Monitor deadlines, track ₹ INR at risk, and send automated 3-stage alerts
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center justify-center transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 overflow-y-auto space-y-4 text-xs">
          {errorMsg && (
            <div className="p-3 rounded-xl bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
              {errorMsg}
            </div>
          )}

          {/* Agreement / Topic Title */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1.5">
              Agreement Title / Topic Name <span className="text-rose-400">*</span>
            </label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => handleTitleChange(e.target.value)}
              placeholder="e.g. Car Insurance Renewal, Airtel Broadband, Health Policy, Gym Pass"
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-medium text-xs transition-all"
            />
          </div>

          {/* Category & Amount in INR */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold text-slate-300 mb-1.5">
                Agreement Type
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-indigo-500 font-medium text-xs"
              >
                <option value="INSURANCE" className="bg-slate-900 text-white">Insurance (Car, Health, Life)</option>
                <option value="LEASE" className="bg-slate-900 text-white">Rental Flat / Office Lease</option>
                <option value="SUBSCRIPTION" className="bg-slate-900 text-white">Gym / SaaS / Streaming</option>
                <option value="TELECOM" className="bg-slate-900 text-white">Broadband / Mobile Connection</option>
                <option value="BANKING" className="bg-slate-900 text-white">Credit Card / Loan Obligation</option>
                <option value="EMPLOYMENT" className="bg-slate-900 text-white">Employment / Contract Notice</option>
                <option value="OTHER" className="bg-slate-900 text-white">Other Custom Topic</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-300 mb-1.5">
                Money at Risk (in ₹ INR)
              </label>
              <div className="relative">
                <span className="absolute left-3.5 top-2.5 font-bold text-slate-400 text-xs">
                  ₹
                </span>
                <input
                  type="number"
                  min="0"
                  step="100"
                  value={moneyAtRisk}
                  onChange={(e) => setMoneyAtRisk(e.target.value === "" ? "" : Number(e.target.value))}
                  placeholder="e.g. 15000"
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl pl-8 pr-3.5 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-medium text-xs transition-all"
                />
              </div>
            </div>
          </div>

          {/* Last Date / Cutoff Deadline Date & Time */}
          <div className="p-3.5 rounded-xl bg-indigo-950/40 border border-indigo-500/40 space-y-2.5">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block font-bold text-white mb-1.5 flex items-center gap-1.5 text-xs">
                  <Calendar className="w-4 h-4 text-indigo-400" />
                  <span>Last Date / Cutoff Date <span className="text-rose-400">*</span></span>
                </label>
                <input
                  type="date"
                  required
                  value={deadlineDate}
                  onChange={(e) => setDeadlineDate(e.target.value)}
                  className="w-full bg-slate-900 border border-indigo-500/60 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-indigo-400 font-bold text-xs"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-300 mb-1.5 text-xs">
                  Cutoff Time
                </label>
                <input
                  type="time"
                  value={deadlineTime}
                  onChange={(e) => setDeadlineTime(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-white focus:outline-none focus:border-indigo-500 font-medium text-xs"
                />
              </div>
            </div>

            <p className="text-[11px] text-indigo-200 leading-relaxed bg-slate-900/80 p-2.5 rounded-lg border border-indigo-900/60 font-medium">
              📅 <strong>Notice Schedule:</strong> If the <strong>25th</strong> is your last date, pick 25. TermGuard will automatically send you alerts <strong>1 week before</strong>, <strong>1 day before</strong>, and on the <strong>final cutoff date itself</strong>, and will automatically delete the reminder after the date passes.
            </p>
          </div>

          {/* Key Clause / Terms Description */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1.5">
              Notice Clause / Terms (Optional)
            </label>
            <textarea
              rows={2}
              value={clauseTerms}
              onChange={(e) => setClauseTerms(e.target.value)}
              placeholder="e.g. Must give 30 days prior written notice before policy expiry to avoid auto-debit."
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-xs transition-all"
            />
          </div>

          {/* Pre-written Formal Notice Draft */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1.5 flex items-center justify-between">
              <span>Pre-Written Cancellation Letter / Notice</span>
              <span className="text-[10px] text-slate-400 font-normal">Auto-formatted</span>
            </label>
            <textarea
              rows={4}
              value={noticeDraft}
              onChange={(e) => setNoticeDraft(e.target.value)}
              placeholder="Notice draft will appear here..."
              className="w-full bg-[#0a0f1d] border border-slate-700 rounded-xl p-3 font-mono text-[11px] text-slate-200 focus:outline-none focus:border-indigo-500 transition-all leading-relaxed"
            />
          </div>

          {/* Actions */}
          <div className="pt-3 border-t border-slate-800 flex items-center justify-end gap-2.5">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-sm transition-all disabled:opacity-50"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>{isSubmitting ? "Adding Agreement..." : "Save & Track Agreement"}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
