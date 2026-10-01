"use client";

import React, { useState } from "react";
import {
  Mail,
  Phone,
  Send,
  CheckCircle2,
  AlertTriangle,
  User,
  Info,
  ExternalLink,
  MessageSquare,
  X,
  IndianRupee,
} from "lucide-react";
import { Reminder } from "@/lib/types";

interface SendAlertModalProps {
  isOpen: boolean;
  onClose: () => void;
  reminder: Reminder | null;
  defaultEmail: string;
  onSendEmail: (reminderId: string, email: string) => Promise<void>;
}

export default function SendAlertModal({
  isOpen,
  onClose,
  reminder,
  defaultEmail,
  onSendEmail,
}: SendAlertModalProps) {
  const [recipientName, setRecipientName] = useState("");
  const [recipientEmail, setRecipientEmail] = useState(defaultEmail || "laxmiharshithrebally@gmail.com");
  const [phoneNumber, setPhoneNumber] = useState("9246972662");
  const [sendingEmail, setSendingEmail] = useState(false);
  const [sendingSms, setSendingSms] = useState(false);
  const [statusMessage, setStatusMessage] = useState<{ text: string; type: "success" | "error" | "info" } | null>(null);

  if (!isOpen || !reminder) return null;

  const dueFormatted = new Date(reminder.dueAt).toLocaleDateString("en-IN", {
    weekday: "short",
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const rawPhoneDigits = phoneNumber.replace(/\D/g, "");
  const formattedIndianPhone = rawPhoneDigits.length === 10 ? `+91${rawPhoneDigits}` : rawPhoneDigits;

  const alertMessageBody = `[TermGuard Alert] Action required: ${reminder.title}. Cutoff: ${dueFormatted}.${reminder.financialImpactUsd ? ` At risk: ₹${reminder.financialImpactUsd.toLocaleString("en-IN")}.` : ""} Please check your TermGuard dashboard.`;

  // Direct Device SMS URI
  const directSmsUri = `sms:${rawPhoneDigits}?body=${encodeURIComponent(alertMessageBody)}`;

  // Handle Send Real Email
  const handleSendEmail = async () => {
    if (!recipientEmail || !recipientEmail.includes("@")) {
      setStatusMessage({ text: "Please enter a valid email address.", type: "error" });
      return;
    }
    setSendingEmail(true);
    setStatusMessage(null);
    try {
      await onSendEmail(reminder.id, recipientEmail);
      setStatusMessage({
        text: `Email alert successfully delivered to ${recipientEmail}! Check your Inbox or Spam folder.`,
        type: "success",
      });
    } catch (err: any) {
      setStatusMessage({ text: `Notice: ${err.message}`, type: "error" });
    } finally {
      setSendingEmail(false);
    }
  };

  // Handle Send Cellular SMS via Twilio / Server Gateway
  const handleSendSms = async () => {
    if (!rawPhoneDigits || rawPhoneDigits.length < 10) {
      setStatusMessage({
        text: "Please enter a valid 10-digit mobile number.",
        type: "error",
      });
      return;
    }
    setSendingSms(true);
    setStatusMessage(null);
    try {
      const res = await fetch("/api/sms", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          reminderId: reminder.id,
          phoneNumber: rawPhoneDigits,
          recipientName: recipientName.trim() || "Harshith",
        }),
      });
      const data = await res.json();
      if (data.success) {
        if (data.result.isRealDispatch) {
          setStatusMessage({
            text: `✅ ${data.result.statusMessage || `Real SMS dispatched to ${rawPhoneDigits} via Twilio!`}`,
            type: "success",
          });
        } else {
          setStatusMessage({
            text: data.result.statusMessage || `SMS generated for ${rawPhoneDigits}.`,
            type: "info",
          });
        }
      } else {
        setStatusMessage({ text: `SMS error: ${data.error}`, type: "error" });
      }
    } catch (err: any) {
      setStatusMessage({ text: `SMS error: ${err.message}`, type: "error" });
    } finally {
      setSendingSms(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-[#0f172a] border border-slate-700 w-full max-w-lg rounded-2xl p-6 space-y-5 shadow-2xl text-white">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h2 className="text-base font-bold text-white">TermGuard Alert Dispatcher</h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Send warning notifications via Verified Email or Cellular Mobile SMS
            </p>
          </div>
          <button
            onClick={onClose}
            className="w-7 h-7 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center justify-center transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Selected Reminder Summary */}
        <div className="p-3.5 rounded-xl bg-[#080d1a] border border-slate-800 space-y-1.5 text-xs">
          <div className="flex items-center justify-between">
            <span className="font-bold text-white truncate max-w-xs">
              {reminder.title}
            </span>
            {reminder.financialImpactUsd && (
              <span className="font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30">
                ₹{reminder.financialImpactUsd.toLocaleString("en-IN")} at risk
              </span>
            )}
          </div>
          <div className="text-slate-400 text-[11px]">
            Cutoff Date: <strong className="text-slate-200">{dueFormatted}</strong>
          </div>
        </div>

        {/* Contact Input Fields */}
        <div className="space-y-3.5 text-xs">
          {/* Recipient Name */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1">
              Recipient Name (Optional)
            </label>
            <input
              type="text"
              value={recipientName}
              onChange={(e) => setRecipientName(e.target.value)}
              placeholder="e.g. Harshith (or Landlord / Gym Support)"
              className="w-full bg-[#080d1a] border border-slate-700 rounded-xl px-3.5 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-xs"
            />
          </div>

          {/* Email Address */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1 flex items-center justify-between">
              <span>Email Address</span>
              <span className="text-[10px] text-emerald-400 font-semibold bg-emerald-500/15 px-2 py-0.5 rounded border border-emerald-500/30">
                ✓ Resend Verified
              </span>
            </label>
            <input
              type="email"
              value={recipientEmail}
              onChange={(e) => setRecipientEmail(e.target.value)}
              placeholder="laxmiharshithrebally@gmail.com"
              className="w-full bg-[#080d1a] border border-slate-700 rounded-xl px-3.5 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-xs font-mono"
            />
          </div>

          {/* Mobile Phone Number */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1 flex items-center justify-between">
              <span>Mobile Phone Number</span>
              <span className="text-[10px] text-indigo-400 font-semibold bg-indigo-500/15 px-2 py-0.5 rounded border border-indigo-500/30">
                Twilio Cellular SMS Active
              </span>
            </label>
            <div className="relative">
              <span className="absolute left-3.5 top-2 font-bold text-slate-400 text-xs">
                +91
              </span>
              <input
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="9246972662"
                className="w-full bg-[#080d1a] border border-slate-700 rounded-xl pl-11 pr-3.5 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-xs font-mono font-medium"
              />
            </div>
          </div>
        </div>

        {/* Action Buttons: Email, Cellular SMS, Direct Mobile SMS */}
        <div className="pt-2 border-t border-slate-800 space-y-2.5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {/* Send Real Email */}
            <button
              onClick={handleSendEmail}
              disabled={sendingEmail || !recipientEmail}
              className="flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-sm transition-all disabled:opacity-50"
            >
              <Mail className="w-4 h-4" />
              <span>{sendingEmail ? "Sending..." : "Send Email Alert"}</span>
            </button>

            {/* Send Cellular SMS via Twilio */}
            <button
              onClick={handleSendSms}
              disabled={sendingSms || !phoneNumber}
              className="flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition-all disabled:opacity-50 shadow-sm"
            >
              <Phone className="w-4 h-4" />
              <span>{sendingSms ? "Dispatching SMS..." : "Send Cellular SMS"}</span>
            </button>
          </div>

          {/* Direct Instant Device Link */}
          {rawPhoneDigits.length >= 10 && (
            <div className="p-2.5 rounded-xl bg-[#080d1a] border border-slate-800 flex items-center justify-between text-xs">
              <span className="text-slate-400">Alternative direct dispatch:</span>
              <a
                href={directSmsUri}
                target="_blank"
                rel="noreferrer"
                className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold text-[11px] flex items-center gap-1 transition-all"
              >
                <MessageSquare className="w-3 h-3 text-indigo-400" />
                <span>Open in Phone SMS App</span>
              </a>
            </div>
          )}

          {/* Status Alert Notification */}
          {statusMessage && (
            <div
              className={`p-3 rounded-xl border text-xs leading-relaxed ${
                statusMessage.type === "success"
                  ? "bg-emerald-500/15 border-emerald-500/30 text-emerald-300 font-medium"
                  : statusMessage.type === "info"
                  ? "bg-amber-500/15 border-amber-500/30 text-amber-300"
                  : "bg-rose-500/15 border-rose-500/30 text-rose-300"
              }`}
            >
              <p>{statusMessage.text}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
