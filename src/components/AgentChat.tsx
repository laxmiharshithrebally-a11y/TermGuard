"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Send,
  Bot,
  User,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Calendar,
  AlertTriangle,
  CheckCircle2,
  FileUp,
  Paperclip,
  IndianRupee,
  ShieldCheck,
} from "lucide-react";
import { AgentChatMessage, AgentActionCard } from "@/lib/gemini";
import { Reminder } from "@/lib/types";

interface AgentChatProps {
  onReminderCreated: (reminder: Reminder) => void;
  selectedDocumentContext?: string;
  onNavigateToTab: (tab: string) => void;
}

export default function AgentChat({
  onReminderCreated,
  selectedDocumentContext,
  onNavigateToTab,
}: AgentChatProps) {
  const [messages, setMessages] = useState<AgentChatMessage[]>([
    {
      role: "assistant",
      content: `Hello! I am **TermGuard AI**, your autonomous contract and notice deadline guardian.\n\nI can read your agreements to catch hidden traps, or you can simply type a natural reminder like:\n👉 *"Remind me on September 14 to cancel my Cult.fit gym pass before ₹32,000 auto-debit."*\n\nHow can I protect your commitments today?`,
      thoughtProcess: [
        "TermGuard Agent Core Initialized: Google Gemini 2.5 Flash Engine online.",
        "Twilio Cellular SMS Gateway: Ready (+919246972662).",
        "Resend Email Dispatcher: Active (laxmiharshithrebally@gmail.com).",
        "3-Stage Notice Radar: Monitoring T-7D, T-24H, and T-0 cutoffs with auto-cleanup.",
      ],
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [expandedThoughts, setExpandedThoughts] = useState<Record<number, boolean>>({ 0: false });
  const [confirmedCardIds, setConfirmedCardIds] = useState<Record<string, boolean>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend?: string) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const newMessages: AgentChatMessage[] = [
      ...messages,
      { role: "user", content: query },
    ];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/agent/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: newMessages,
          documentContext: selectedDocumentContext,
        }),
      });

      const data = await res.json();
      if (data.success && data.message) {
        setMessages((prev) => [...prev, data.message]);
        setExpandedThoughts((prev) => ({
          ...prev,
          [newMessages.length]: true,
        }));
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: `I processed your request, but encountered a notice: ${data.error || "Unable to reach neural core"}.`,
          },
        ]);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error communicating with TermGuard Core: ${err.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmCard = async (card: AgentActionCard) => {
    if (confirmedCardIds[card.id]) return;

    try {
      const res = await fetch("/api/reminders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: card.title,
          dueAt: card.deadlineDate || new Date(Date.now() + 86400000 * 7).toISOString(),
          sourceClauseQuote: card.quotedText,
          sourceSection: card.sourceSection,
          financialImpactUsd: card.financialImpactUsd,
          cancellationNoticeDraft: card.preWrittenDraft,
        }),
      });

      const data = await res.json();
      if (data.success) {
        setConfirmedCardIds((prev) => ({ ...prev, [card.id]: true }));
        onReminderCreated(data.reminder);

        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: `✅ **Committed to Schedule!** I've scheduled **"${card.title}"** for **${new Date(card.deadlineDate || "").toLocaleString("en-IN")}**.\n\nTermGuard will dispatch 3-stage alerts (1 week before, 24 hours before, and cutoff day) via Email & Cellular SMS. Once expired, it will auto-delete.`,
          },
        ]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const toggleThought = (index: number) => {
    setExpandedThoughts((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const promptSuggestions = [
    "Remind me on September 14 to cancel Cult.fit pass",
    "Check Bangalore flat lease for security deposit forfeiture traps",
    "Remind me next Friday at 6pm to cancel my broadband",
    "Draft a formal move-out notice letter to my landlord",
  ];

  return (
    <div className="exec-dark-card flex flex-col h-[700px] overflow-hidden shadow-xl">
      {/* Chat Header */}
      <div className="p-4 border-b border-slate-800 bg-[#0b0f19] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              TermGuard AI Agent Core
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 font-semibold">
                Gemini 2.5 Flash Online
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              {selectedDocumentContext
                ? "Active Context: Agreement Loaded"
                : "Natural Language & 3-Stage Deadline Parsing Engine"}
            </p>
          </div>
        </div>

        {selectedDocumentContext && (
          <button
            onClick={() => onNavigateToTab("documents")}
            className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold underline"
          >
            View Active Agreement →
          </button>
        )}
      </div>

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5 bg-[#090d16]">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-3 max-w-3xl ${
              msg.role === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
            }`}
          >
            {/* Avatar */}
            <div
              className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                msg.role === "user"
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "bg-slate-800 text-indigo-400 border border-slate-700 shadow-sm"
              }`}
            >
              {msg.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            {/* Content Bubble */}
            <div className="space-y-3 max-w-[85%] sm:max-w-[75%]">
              {/* Agent Thought Badge */}
              {msg.thoughtProcess && msg.thoughtProcess.length > 0 && (
                <div className="bg-[#0b0f19] border border-indigo-900/40 rounded-lg overflow-hidden text-xs shadow-sm">
                  <button
                    onClick={() => toggleThought(idx)}
                    className="w-full px-3 py-2 flex items-center justify-between text-indigo-400 hover:bg-indigo-950/30 font-mono transition-colors"
                  >
                    <span className="flex items-center gap-1.5 font-semibold text-[11px]">
                      <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                      TermGuard Reasoning ({msg.thoughtProcess.length} steps)
                    </span>
                    {expandedThoughts[idx] ? (
                      <ChevronUp className="w-3.5 h-3.5" />
                    ) : (
                      <ChevronDown className="w-3.5 h-3.5" />
                    )}
                  </button>

                  {expandedThoughts[idx] && (
                    <div className="px-3 py-2.5 border-t border-indigo-950/60 bg-[#070b13] space-y-1.5 font-mono text-[11px] text-slate-400">
                      {msg.thoughtProcess.map((step, sIdx) => (
                        <div key={sIdx} className="flex items-start gap-2">
                          <span className="text-indigo-400 font-bold">{sIdx + 1}.</span>
                          <span>{step}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Message Text */}
              <div
                className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-indigo-600 text-white rounded-tr-none shadow-md"
                    : "bg-[#0f172a] text-slate-200 border border-slate-800 rounded-tl-none whitespace-pre-wrap shadow-md"
                }`}
              >
                {msg.content}
              </div>

              {/* Interactive Action Cards */}
              {msg.actionCards && msg.actionCards.length > 0 && (
                <div className="space-y-3 pt-1">
                  {msg.actionCards.map((card) => {
                    const isConfirmed = confirmedCardIds[card.id];
                    return (
                      <div
                        key={card.id}
                        className="p-4 rounded-xl border border-indigo-500/30 bg-[#0d1424] space-y-3 shadow-lg"
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <span className="text-[10px] font-bold tracking-wider uppercase px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                              Proposed Action Item
                            </span>
                            <h4 className="text-sm font-bold text-white mt-1.5">
                              {card.title}
                            </h4>
                          </div>
                          {card.financialImpactUsd && (
                            <span className="text-xs font-bold text-amber-400 px-2 py-1 rounded bg-amber-500/15 border border-amber-500/30 flex items-center gap-0.5">
                              <IndianRupee className="w-3 h-3" />
                              <span>{card.financialImpactUsd.toLocaleString("en-IN")} at risk</span>
                            </span>
                          )}
                        </div>

                        {card.deadlineDate && (
                          <div className="flex items-center gap-2 text-xs text-slate-300 font-medium">
                            <Calendar className="w-3.5 h-3.5 text-indigo-400" />
                            <span>
                              Cutoff Date:{" "}
                              <strong className="text-white">
                                {new Date(card.deadlineDate).toLocaleString("en-IN")}
                              </strong>
                            </span>
                          </div>
                        )}

                        {card.quotedText && (
                          <div className="p-2.5 rounded-lg bg-[#070b13] border border-slate-800 font-mono text-[11px] text-slate-300">
                            <span className="text-indigo-400 font-bold block mb-1">
                              Grounding Source ({card.sourceSection || "Clause"}):
                            </span>
                            "{card.quotedText}"
                          </div>
                        )}

                        <div className="flex items-center gap-2 pt-1">
                          <button
                            onClick={() => handleConfirmCard(card)}
                            disabled={isConfirmed}
                            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm ${
                              isConfirmed
                                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 cursor-default"
                                : "bg-indigo-600 hover:bg-indigo-500 text-white"
                            }`}
                          >
                            <CheckCircle2 className="w-4 h-4" />
                            <span>
                              {isConfirmed ? "Committed to Schedule" : "Approve & Schedule Notice Alert"}
                            </span>
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 max-w-xl mr-auto">
            <div className="w-8 h-8 rounded-lg bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-[#0f172a] p-4 rounded-2xl rounded-tl-none border border-slate-800 text-xs sm:text-sm text-slate-300 flex items-center gap-2 shadow-sm">
              <Sparkles className="w-4 h-4 text-indigo-400 animate-spin" />
              <span>Analyzing fine-print clauses and temporal constraints...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompt Chips */}
      <div className="px-4 py-2 bg-[#0b0f19] border-t border-slate-800 flex items-center gap-2 overflow-x-auto text-xs no-scrollbar">
        <span className="text-[11px] uppercase font-bold text-slate-500 shrink-0">
          Try:
        </span>
        {promptSuggestions.map((prompt, pIdx) => (
          <button
            key={pIdx}
            onClick={() => handleSend(prompt)}
            className="shrink-0 px-2.5 py-1 rounded-full bg-slate-800/80 hover:bg-indigo-950/60 text-slate-300 hover:text-indigo-300 border border-slate-700 text-[11px] font-medium transition-all"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Input Box */}
      <div className="p-3 sm:p-4 border-t border-slate-800 bg-[#0f172a]">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <button
            type="button"
            onClick={() => onNavigateToTab("documents")}
            title="Attach or Inspect Agreement"
            className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-indigo-400 border border-slate-700 transition-colors"
          >
            <Paperclip className="w-4 h-4" />
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a reminder (e.g. 'Remind me on Sept 14 to cancel gym') or ask a contract question..."
            className="flex-1 bg-[#0b0f19] border border-slate-700 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all font-medium"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="p-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold disabled:opacity-40 transition-all shadow-sm"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
