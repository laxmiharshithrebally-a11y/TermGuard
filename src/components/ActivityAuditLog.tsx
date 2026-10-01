"use client";

import React, { useState } from "react";
import {
  FileText,
  Clock,
  Mail,
  Zap,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Info,
  Search,
} from "lucide-react";
import { AuditLogEntry } from "@/lib/types";

interface ActivityAuditLogProps {
  auditLogs: AuditLogEntry[];
}

export default function ActivityAuditLog({ auditLogs }: ActivityAuditLogProps) {
  const [filterType, setFilterType] = useState<string>("ALL");
  const [search, setSearch] = useState("");

  const filteredLogs = auditLogs.filter((log) => {
    if (filterType !== "ALL" && !log.actionType.includes(filterType)) {
      return false;
    }
    if (search.trim()) {
      const q = search.toLowerCase();
      return (
        log.summary.toLowerCase().includes(q) ||
        log.details.toLowerCase().includes(q) ||
        log.actionType.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const getActionIcon = (actionType: AuditLogEntry["actionType"]) => {
    switch (actionType) {
      case "DOC_UPLOADED":
      case "DOC_PARSED":
        return <FileText className="w-4 h-4 text-indigo-400" />;
      case "CLAUSE_EXTRACTED":
        return <AlertTriangle className="w-4 h-4 text-amber-400" />;
      case "REMINDER_CREATED":
      case "REMINDER_UPDATED":
      case "REMINDER_RESOLVED":
        return <Clock className="w-4 h-4 text-blue-400" />;
      case "EMAIL_TRIGGERED":
      case "EMAIL_DELIVERED":
        return <Mail className="w-4 h-4 text-emerald-400" />;
      case "CRON_HEARTBEAT":
        return <Zap className="w-4 h-4 text-purple-400" />;
      default:
        return <Info className="w-4 h-4 text-slate-400" />;
    }
  };

  const getStatusBadge = (status: AuditLogEntry["status"]) => {
    switch (status) {
      case "SUCCESS":
        return (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            200 OK
          </span>
        );
      case "WARNING":
        return (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
            FLAGGED
          </span>
        );
      case "ERROR":
        return (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
            ERROR
          </span>
        );
      default:
        return (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
            INFO
          </span>
        );
    }
  };

  return (
    <div className="space-y-4">
      {/* Header & Filter Controls */}
      <div className="p-4 rounded-2xl exec-dark-card flex flex-col sm:flex-row items-center justify-between gap-3">
        <div>
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
            TermGuard Trust Layer: Immutable Audit Ledger
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Every document scanned, trap extracted, and alert dispatched is timestamped and verifiable.
          </p>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          {/* Search */}
          <div className="relative flex-1 sm:flex-initial">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search audit trail..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500 w-full sm:w-48"
            />
          </div>

          {/* Type Filter */}
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-white font-semibold text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            <option value="ALL" className="bg-slate-900 text-white">All Events ({auditLogs.length})</option>
            <option value="DOC" className="bg-slate-900 text-white">Agreements</option>
            <option value="CLAUSE" className="bg-slate-900 text-white">Clauses</option>
            <option value="REMINDER" className="bg-slate-900 text-white">Deadlines</option>
            <option value="EMAIL" className="bg-slate-900 text-white">Emails / SMS</option>
            <option value="CRON" className="bg-slate-900 text-white">Cron Checks</option>
          </select>
        </div>
      </div>

      {/* Ledger Stream */}
      <div className="rounded-2xl overflow-hidden exec-dark-card">
        <div className="divide-y divide-slate-800 font-mono">
          {filteredLogs.map((log) => {
            const date = new Date(log.timestamp);
            const timeStr = date.toLocaleTimeString("en-IN", { hour12: false });
            const dateStr = date.toLocaleDateString("en-IN", { month: "short", day: "numeric" });

            return (
              <div
                key={log.id}
                className="p-4 hover:bg-slate-800/50 transition-colors flex flex-col sm:flex-row sm:items-start justify-between gap-3 text-xs"
              >
                <div className="flex items-start gap-3">
                  <div className="p-2 rounded-lg bg-slate-900 border border-slate-700 shrink-0 mt-0.5">
                    {getActionIcon(log.actionType)}
                  </div>

                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-bold text-white text-[13px]">
                        {log.summary}
                      </span>
                      {getStatusBadge(log.status)}
                    </div>
                    <p className="text-slate-300 font-sans text-xs leading-relaxed">
                      {log.details}
                    </p>
                    {log.targetId && (
                      <span className="text-[10px] text-slate-500 font-mono">
                        Target Ref: #{log.targetId}
                      </span>
                    )}
                  </div>
                </div>

                <div className="sm:text-right shrink-0 text-slate-400 text-[11px]">
                  <div className="font-semibold text-slate-200">{timeStr}</div>
                  <div className="text-slate-500 text-[10px]">{dateStr}</div>
                </div>
              </div>
            );
          })}

          {filteredLogs.length === 0 && (
            <div className="p-12 text-center text-slate-400">
              No audit log entries matching filter criteria.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
