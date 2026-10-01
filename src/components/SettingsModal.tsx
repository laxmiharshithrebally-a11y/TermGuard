"use client";

import React, { useState, useEffect } from "react";
import { Settings, Key, Mail, CheckCircle2, Save, HelpCircle, Phone, X, ShieldCheck } from "lucide-react";
import { AppSettings } from "@/lib/types";

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSettingsUpdated: (settings: AppSettings) => void;
}

export default function SettingsModal({
  isOpen,
  onClose,
  onSettingsUpdated,
}: SettingsModalProps) {
  const [settings, setSettings] = useState<AppSettings>({
    userEmail: "laxmiharshithrebally@gmail.com",
    resendApiKey: "",
    geminiApiKey: "",
    twilioAccountSid: "",
    twilioAuthToken: "",
    twilioPhoneNumber: "",
    fast2smsApiKey: "",
    cronIntervalMinutes: 5,
    autoSendEmails: true,
    autoSendSms: true,
  });
  const [loading, setLoading] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetch("/api/settings")
        .then((res) => res.json())
        .then((data) => {
          if (data.success && data.settings) {
            setSettings(data.settings);
          }
        })
        .catch(console.error);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
      });
      const data = await res.json();
      if (data.success) {
        onSettingsUpdated(data.settings);
        setSavedSuccess(true);
        setTimeout(() => setSavedSuccess(false), 2500);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-[#0f172a] border border-slate-700 w-full max-w-xl rounded-2xl shadow-2xl flex flex-col overflow-hidden max-h-[92vh] text-slate-100">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/90">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
              <Settings className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">TermGuard Dispatch & Gateways</h3>
              <p className="text-xs text-slate-400">Configure email delivery & mobile cellular SMS gateways</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 flex items-center justify-center transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 overflow-y-auto space-y-4 text-xs">
          {/* Target Notification Email */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-indigo-400" />
              <span>Target Notification Email Address</span>
            </label>
            <input
              type="email"
              required
              value={settings.userEmail}
              onChange={(e) => setSettings({ ...settings, userEmail: e.target.value })}
              placeholder="e.g. laxmiharshithrebally@gmail.com"
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 font-medium"
            />
            <p className="text-[11px] text-slate-400 mt-1">
              All 3-stage notice alerts and cancellation letters are delivered to this inbox.
            </p>
          </div>

          {/* Resend API Key */}
          <div>
            <label className="block font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
              <Key className="w-3.5 h-3.5 text-indigo-400" />
              <span>Resend API Key (for Live Inboxes)</span>
            </label>
            <input
              type="password"
              value={settings.resendApiKey}
              onChange={(e) => setSettings({ ...settings, resendApiKey: e.target.value })}
              placeholder="re_..."
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs font-mono text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
            <p className="text-[10px] text-emerald-400 mt-1 flex items-center gap-1">
              <ShieldCheck className="w-3 h-3" /> Resend configured with live key in .env.local
            </p>
          </div>

          {/* Cellular SMS Gateway Section */}
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-emerald-400" />
                <h4 className="text-xs font-bold text-white">
                  Cellular SMS Delivery Gateway
                </h4>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-semibold font-mono">
                Twilio Active
              </span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Delivers real SMS to Indian phones over cellular network to target: <strong className="text-slate-200">+91 9246972662</strong>.
            </p>

            {/* Twilio Credentials */}
            <div className="space-y-2.5 pt-1">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                <div>
                  <label className="block text-[11px] font-medium text-slate-300 mb-1">
                    Twilio Account SID
                  </label>
                  <input
                    type="text"
                    value={settings.twilioAccountSid || ""}
                    onChange={(e) => setSettings({ ...settings, twilioAccountSid: e.target.value })}
                    placeholder="AC..."
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-slate-300 mb-1">
                    Twilio Auth Token
                  </label>
                  <input
                    type="password"
                    value={settings.twilioAuthToken || ""}
                    onChange={(e) => setSettings({ ...settings, twilioAuthToken: e.target.value })}
                    placeholder="Auth Token..."
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-[11px] font-medium text-slate-300 mb-1">
                  Twilio Provisioned Sender Number
                </label>
                <input
                  type="text"
                  value={settings.twilioPhoneNumber || ""}
                  onChange={(e) => setSettings({ ...settings, twilioPhoneNumber: e.target.value })}
                  placeholder="+19789515824"
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>

            {/* Fast2SMS Key Optional */}
            <div className="pt-2 border-t border-slate-800">
              <label className="block font-semibold text-slate-400 mb-1 text-[11px]">
                Fast2SMS API Key (Optional Alternative)
              </label>
              <input
                type="password"
                value={settings.fast2smsApiKey || ""}
                onChange={(e) => setSettings({ ...settings, fast2smsApiKey: e.target.value })}
                placeholder="Paste Fast2SMS authorization key (optional)..."
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          {/* Auto Send Toggle */}
          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-900 border border-slate-800">
            <div>
              <span className="text-xs font-bold text-white block">
                Automated 3-Stage Background Dispatch
              </span>
              <span className="text-[11px] text-slate-400">
                Automatically fire email & SMS at 1-week, 24-hours, and final day cutoffs.
              </span>
            </div>
            <input
              type="checkbox"
              checked={settings.autoSendEmails}
              onChange={(e) =>
                setSettings({ ...settings, autoSendEmails: e.target.checked })
              }
              className="w-4 h-4 rounded text-indigo-600 bg-slate-800 border-slate-600 focus:ring-indigo-500"
            />
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between pt-3 border-t border-slate-800">
            {savedSuccess ? (
              <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                Settings Saved!
              </span>
            ) : (
              <span />
            )}

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
              >
                Close
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex items-center gap-1.5 px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-sm transition-all disabled:opacity-50"
              >
                <Save className="w-3.5 h-3.5" />
                <span>{loading ? "Saving..." : "Save Settings"}</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
