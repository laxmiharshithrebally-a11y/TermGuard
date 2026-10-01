"use client";

import React, { useState, useRef } from "react";
import {
  FileText,
  AlertTriangle,
  ShieldCheck,
  Calendar,
  IndianRupee,
  Plus,
  Trash2,
  CheckCircle,
  Search,
  Sparkles,
  X,
} from "lucide-react";
import { DocumentRecord, ExtractedClause } from "@/lib/types";

interface DocumentStudioProps {
  documents: DocumentRecord[];
  selectedDocId: string;
  onSelectDoc: (id: string) => void;
  onUploadDoc: (doc: { title: string; content: string; category: any }) => void;
  onDeleteDoc: (id: string) => void;
  onAddReminderFromClause: (clause: ExtractedClause, doc: DocumentRecord) => void;
  onOpenCreateModal?: () => void;
}

export default function DocumentStudio({
  documents,
  selectedDocId,
  onSelectDoc,
  onUploadDoc,
  onDeleteDoc,
  onAddReminderFromClause,
  onOpenCreateModal,
}: DocumentStudioProps) {
  const [highlightedText, setHighlightedText] = useState<string | null>(null);
  const [activeClauseId, setActiveClauseId] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");
  const [newCategory, setNewCategory] = useState("SUBSCRIPTION");
  const [newDeadlineDate, setNewDeadlineDate] = useState(() => {
    const d = new Date();
    d.setDate(d.getDate() + 30);
    return d.toISOString().split("T")[0];
  });
  const [newMoneyAtRisk, setNewMoneyAtRisk] = useState<number | "">("");
  const [addedClauseIds, setAddedClauseIds] = useState<Record<string, boolean>>({});

  const documentViewerRef = useRef<HTMLDivElement>(null);

  const currentDoc =
    documents.find((d) => d.id === selectedDocId) || documents[0] || null;

  const handleClauseClick = (clause: ExtractedClause) => {
    setActiveClauseId(clause.id);
    setHighlightedText(clause.quotedText);

    if (documentViewerRef.current) {
      const viewer = documentViewerRef.current;
      const targetElement = viewer.querySelector(`[data-clause-id="${clause.id}"]`);
      if (targetElement) {
        targetElement.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  };

  const handleAddReminder = (clause: ExtractedClause) => {
    if (!currentDoc) return;
    setAddedClauseIds((prev) => ({ ...prev, [clause.id]: true }));
    onAddReminderFromClause(clause, currentDoc);
  };

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newContent.trim()) return;

    const numericMoney = typeof newMoneyAtRisk === "number" ? newMoneyAtRisk : parseInt(String(newMoneyAtRisk) || "0", 10) || 0;

    // 1. Ingest document
    onUploadDoc({
      title: newTitle,
      content: `${newTitle.toUpperCase()}\nCATEGORY: ${newCategory}\nLAST DATE: ${newDeadlineDate}\nMONEY AT RISK: ₹${numericMoney.toLocaleString("en-IN")}\nTERMS:\n${newContent}`,
      category: newCategory as any,
    });

    // 2. Also register reminder with the last date so 3-stage alerts and auto-deletion are active
    if (newDeadlineDate) {
      try {
        await fetch("/api/reminders", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            title: `Notice Deadline: ${newTitle}`,
            dueAt: new Date(`${newDeadlineDate}T18:00:00`).toISOString(),
            sourceClauseQuote: newContent.slice(0, 200),
            sourceSection: "Notice Terms",
            financialImpactUsd: numericMoney,
            documentTitle: newTitle,
            cancellationNoticeDraft: `To Support / Management,\n\nPlease accept this formal notice that I will not be renewing ${newTitle}. Please cancel before the cutoff on ${newDeadlineDate}.\n\nThank you,\nHarshith R.`,
          }),
        });
      } catch (err) {
        console.error(err);
      }
    }

    setNewTitle("");
    setNewContent("");
    setNewMoneyAtRisk("");
    setIsUploadModalOpen(false);
  };

  return (
    <div className="space-y-4">
      {/* Top Action Bar in Executive Dark Styling */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 p-4 exec-dark-card">
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shrink-0">
            <FileText className="w-4 h-4" />
          </div>
          <div className="flex flex-col flex-1 sm:flex-initial">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Active Agreement Workspace
            </label>
            <select
              value={currentDoc?.id || ""}
              onChange={(e) => onSelectDoc(e.target.value)}
              className="bg-slate-900 border border-slate-700 text-white font-semibold text-xs sm:text-sm rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500 w-full sm:w-88 mt-0.5"
            >
              {documents.map((doc) => (
                <option key={doc.id} value={doc.id} className="bg-slate-900 text-white">
                  {doc.title} (₹{doc.totalFinancialExposure.toLocaleString("en-IN")} at risk)
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
          <button
            onClick={() => onOpenCreateModal ? onOpenCreateModal() : setIsUploadModalOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow-sm"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>+ Add Agreement with Last Date</span>
          </button>
        </div>
      </div>

      {currentDoc ? (
        /* Dual-Pane Studio Layout */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 h-[720px]">
          {/* Left Pane (Raw Document) — 7 Columns in Executive Dark Style */}
          <div className="lg:col-span-7 exec-dark-card flex flex-col overflow-hidden">
            {/* Header */}
            <div className="p-3.5 border-b border-slate-800 bg-slate-900/90 flex items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="font-bold text-white tracking-wide">
                  {currentDoc.category} Agreement Reader
                </span>
              </div>

              {/* Quick Search */}
              <div className="relative">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search contract text..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="bg-slate-950 border border-slate-700 rounded-lg pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500 w-48"
                />
              </div>
            </div>

            {/* Document Content with Smooth Scroll & Highlighting */}
            <div
              ref={documentViewerRef}
              className="flex-1 overflow-y-auto p-5 font-mono text-xs leading-relaxed text-slate-200 space-y-3 bg-[#0a0f1d]"
            >
              {currentDoc.rawContent.split("\n\n").map((paragraph, pIdx) => {
                const isSelected =
                  highlightedText &&
                  paragraph.toLowerCase().includes(highlightedText.toLowerCase().slice(0, 30));

                return (
                  <div
                    key={pIdx}
                    data-clause-id={`para-${pIdx}`}
                    className={`p-3.5 rounded-xl transition-all ${
                      isSelected
                        ? "bg-amber-500/20 border-l-4 border-amber-400 text-amber-200 shadow-sm"
                        : searchTerm &&
                          paragraph.toLowerCase().includes(searchTerm.toLowerCase())
                        ? "bg-indigo-950/80 border-l-4 border-indigo-400 text-indigo-200 font-medium"
                        : "hover:bg-slate-900/50"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{paragraph}</p>
                  </div>
                );
              })}
            </div>

            <div className="p-3 border-t border-slate-800 bg-slate-900/90 text-[11px] text-slate-400 flex items-center justify-between">
              <span>Click any clause on the right to auto-highlight</span>
              <span className="font-semibold text-emerald-400 flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" /> Grounded in Verified Text
              </span>
            </div>
          </div>

          {/* Right Pane (Hazard Radar) — 5 Columns */}
          <div className="lg:col-span-5 exec-dark-card flex flex-col overflow-hidden">
            {/* Radar Header */}
            <div className="p-3.5 border-b border-slate-800 bg-slate-900/90 flex items-center justify-between">
              <div>
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                  Identified Clauses & Traps
                </h3>
                <p className="text-[11px] text-slate-400 mt-0.5">
                  {currentDoc.clauses.length} Fine-print rules detected
                </p>
              </div>

              <div className="text-right">
                <span className="text-[10px] text-slate-400 uppercase font-semibold">
                  Hazard Score
                </span>
                <div className="text-sm font-bold text-amber-400">
                  {currentDoc.riskScore}/100 Risk
                </div>
              </div>
            </div>

            {/* Clause Cards List */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-[#090d16]">
              {currentDoc.clauses.map((clause) => {
                const isActive = activeClauseId === clause.id;
                const isAdded = addedClauseIds[clause.id];

                return (
                  <div
                    key={clause.id}
                    onClick={() => handleClauseClick(clause)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all ${
                      isActive
                        ? "border-amber-400/80 bg-amber-500/10 shadow-md"
                        : "border-slate-800 bg-[#0f172a] hover:border-slate-700 hover:bg-[#131c31]"
                    }`}
                  >
                    {/* Header */}
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                          clause.riskLevel === "CRITICAL"
                            ? "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                            : clause.riskLevel === "WARNING"
                            ? "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                            : "bg-blue-500/20 text-blue-300 border border-blue-500/30"
                        }`}
                      >
                        {clause.riskLevel}
                      </span>
                      <span className="text-xs font-bold text-amber-300 flex items-center gap-0.5">
                        <IndianRupee className="w-3.5 h-3.5" />
                        <span>{clause.financialImpactUsd.toLocaleString("en-IN")} at risk</span>
                      </span>
                    </div>

                    <h4 className="text-sm font-bold text-white mb-1">
                      {clause.clauseTitle}
                    </h4>

                    <div className="text-[11px] font-mono text-indigo-400 mb-2 font-medium">
                      {clause.sourceSection}
                    </div>

                    {/* Quoted Snippet */}
                    <div className="p-2.5 rounded-lg bg-[#070b13] font-mono text-[11px] text-slate-300 mb-2.5 leading-relaxed border border-slate-800">
                      "{clause.quotedText.slice(0, 150)}..."
                    </div>

                    {/* Explanation */}
                    <p className="text-xs text-slate-400 mb-3 leading-relaxed">
                      {clause.explanation}
                    </p>

                    {/* Schedule Button */}
                    <div className="pt-2.5 border-t border-slate-800 flex items-center justify-between gap-2">
                      <div className="text-xs text-slate-400 font-mono">
                        Cutoff: <strong className="text-slate-200">{clause.deadlineDate}</strong>
                      </div>

                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleAddReminder(clause);
                        }}
                        disabled={isAdded}
                        className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                          isAdded
                            ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 cursor-default"
                            : "bg-indigo-600 hover:bg-indigo-500 text-white shadow-sm"
                        }`}
                      >
                        {isAdded ? "✓ Added to Deadlines" : "+ Track Deadline"}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      ) : (
        <div className="p-12 text-center text-slate-400 text-xs exec-dark-card">
          No documents available.
        </div>
      )}

      {/* Upload Contract Modal with Last Date Picker */}
      {isUploadModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#0f172a] border border-slate-700 w-full max-w-lg p-6 rounded-2xl space-y-4 shadow-2xl text-slate-100">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <FileText className="w-5 h-5 text-indigo-400" />
                Upload New Agreement
              </h3>
              <button
                onClick={() => setIsUploadModalOpen(false)}
                className="w-7 h-7 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center justify-center transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleUploadSubmit} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Agreement Name <span className="text-rose-400">*</span>
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Golds Gym Agreement or Apartment Lease"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Category
                </label>
                <select
                  value={newCategory}
                  onChange={(e) => setNewCategory(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white focus:outline-none focus:border-indigo-500"
                >
                  <option value="SUBSCRIPTION" className="bg-slate-900 text-white">Subscription / Membership</option>
                  <option value="LEASE" className="bg-slate-900 text-white">Lease / Rental Agreement</option>
                  <option value="EMPLOYMENT" className="bg-slate-900 text-white">Employment / Offer Letter</option>
                  <option value="WARRANTY" className="bg-slate-900 text-white">Warranty / Purchase Terms</option>
                  <option value="CUSTOM" className="bg-slate-900 text-white">Other Contract</option>
                </select>
              </div>

              {/* Prominent Last Date & Money at Risk */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-3 rounded-xl bg-indigo-950/40 border border-indigo-500/40">
                <div>
                  <label className="block font-bold text-white mb-1 flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5 text-indigo-400" />
                    <span>Last Date / Cutoff Date <span className="text-rose-400">*</span></span>
                  </label>
                  <input
                    type="date"
                    required
                    value={newDeadlineDate}
                    onChange={(e) => setNewDeadlineDate(e.target.value)}
                    className="w-full bg-slate-900 border border-indigo-500/60 rounded-xl p-2.5 text-white focus:outline-none focus:border-indigo-400 font-bold"
                  />
                  <span className="text-[10px] text-indigo-300 mt-1 block">
                    e.g. 25th for 1-week, 1-day, & final alerts
                  </span>
                </div>

                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Money at Risk (in ₹ INR)
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-2.5 font-bold text-slate-400 text-xs">
                      ₹
                    </span>
                    <input
                      type="number"
                      min="0"
                      placeholder="e.g. 15000"
                      value={newMoneyAtRisk}
                      onChange={(e) => setNewMoneyAtRisk(e.target.value === "" ? "" : Number(e.target.value))}
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl pl-7 pr-3 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Contract Text / Fine Print <span className="text-rose-400">*</span>
                </label>
                <textarea
                  rows={6}
                  required
                  placeholder="Paste contract text, clauses, or auto-renewal terms here..."
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  className="w-full bg-[#0a0f1d] border border-slate-700 rounded-xl p-2.5 font-mono text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsUploadModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold shadow-sm"
                >
                  Track Agreement & Schedule Alerts
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
