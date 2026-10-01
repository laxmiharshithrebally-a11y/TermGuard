"use client";

import React, { useState, useEffect } from "react";
import { Mail, ShieldCheck, ExternalLink, RefreshCw, Send, X } from "lucide-react";
import { EmailDispatchLog } from "@/lib/types";

interface EmailInspectorModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function EmailInspectorModal({ isOpen, onClose }: EmailInspectorModalProps) {
  const [logs, setLogs] = useState<EmailDispatchLog[]>([]);
  const [selectedLog, setSelectedLog] = useState<EmailDispatchLog | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchOutbox = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/email");
      const data = await res.json();
      if (data.success && data.emailLogs) {
        setLogs(data.emailLogs);
        if (data.emailLogs.length > 0 && !selectedLog) {
          setSelectedLog(data.emailLogs[0]);
        }
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchOutbox();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-3 sm:p-6">
      <div className="bg-[#0f172a] border border-slate-700 w-full max-w-5xl h-[85vh] rounded-2xl flex flex-col overflow-hidden shadow-2xl text-slate-100">
        {/* Modal Header */}
        <div className="p-4 border-b border-slate-800 bg-slate-900/90 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
              <Mail className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                TermGuard Live Email Outbox & Delivery Inspector
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-semibold font-mono">
                  Live Dispatch Active
                </span>
              </h2>
              <p className="text-xs text-slate-400">
                Inspect authentic emails dispatched to user inboxes with verified clauses.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchOutbox}
              className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
              title="Refresh Outbox"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin text-indigo-400" : ""}`} />
            </button>
            <button
              onClick={onClose}
              className="w-8 h-8 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center justify-center transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Body Split */}
        <div className="flex-1 grid grid-cols-1 md:grid-cols-12 overflow-hidden">
          {/* Left Column: Log List (4 cols) */}
          <div className="md:col-span-4 border-r border-slate-800 bg-[#090d16] overflow-y-auto divide-y divide-slate-800/80">
            {logs.map((log) => {
              const isSelected = selectedLog?.id === log.id;
              return (
                <div
                  key={log.id}
                  onClick={() => setSelectedLog(log)}
                  className={`p-3.5 cursor-pointer transition-all ${
                    isSelected
                      ? "bg-indigo-600/20 border-l-4 border-indigo-400 text-white"
                      : "hover:bg-slate-800/40 text-slate-300"
                  }`}
                >
                  <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1 font-mono">
                    <span
                      className={`px-1.5 py-0.5 rounded font-bold ${
                        log.status === "SENT"
                          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                          : log.status === "SIMULATED"
                          ? "bg-blue-500/20 text-blue-300 border border-blue-500/30"
                          : "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                      }`}
                    >
                      {log.status}
                    </span>
                    <span>{new Date(log.timestamp).toLocaleTimeString("en-IN")}</span>
                  </div>
                  <h4 className="text-xs font-bold truncate text-white">{log.subject}</h4>
                  <p className="text-[11px] text-slate-400 truncate mt-0.5">
                    To: {log.recipient}
                  </p>
                </div>
              );
            })}

            {logs.length === 0 && (
              <div className="p-8 text-center text-xs text-slate-400">
                No emails dispatched yet. Click "Send Alert" on any deadline in the Deadlines tab!
              </div>
            )}
          </div>

          {/* Right Column: Email Preview & Headers (8 cols) */}
          <div className="md:col-span-8 flex flex-col bg-[#0b1120] overflow-hidden">
            {selectedLog ? (
              <div className="flex-1 flex flex-col overflow-hidden">
                {/* Email Metadata Bar */}
                <div className="p-4 border-b border-slate-800 bg-slate-900/90 space-y-1.5 text-xs font-mono">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Recipient:</span>
                    <span className="text-indigo-300 font-bold">{selectedLog.recipient}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Subject:</span>
                    <span className="text-white font-semibold truncate max-w-md">
                      {selectedLog.subject}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Resend Message ID:</span>
                    <span className="text-slate-400 text-[11px]">{selectedLog.messageId}</span>
                  </div>
                </div>

                {/* Rendered HTML Sandbox */}
                <div className="flex-1 p-4 overflow-y-auto bg-slate-950">
                  <div className="rounded-xl overflow-hidden shadow-lg border border-slate-800">
                    <iframe
                      srcDoc={selectedLog.htmlContent}
                      title="Email Preview"
                      className="w-full h-[520px] bg-white border-0"
                      sandbox="allow-same-origin"
                    />
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex items-center justify-center p-8 text-slate-400 text-xs">
                Select an email from the left outbox list to inspect headers and delivery markup.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
