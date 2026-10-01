"use client";

import React, { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import TopStatsHUD from "@/components/TopStatsHUD";
import AgentChat from "@/components/AgentChat";
import DocumentStudio from "@/components/DocumentStudio";
import RemindersCenter from "@/components/RemindersCenter";
import ActivityAuditLog from "@/components/ActivityAuditLog";
import EmailInspectorModal from "@/components/EmailInspectorModal";
import SettingsModal from "@/components/SettingsModal";
import CreateAgreementModal from "@/components/CreateAgreementModal";
import {
  DocumentRecord,
  Reminder,
  AuditLogEntry,
  AppSettings,
  ExtractedClause,
} from "@/lib/types";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<string>("reminders");
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLogEntry[]>([]);
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [selectedDocId, setSelectedDocId] = useState<string>("");
  const [isCronRunning, setIsCronRunning] = useState<boolean>(false);
  const [isOutboxOpen, setIsOutboxOpen] = useState<boolean>(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState<boolean>(false);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4000);
  };

  const refreshAllData = async () => {
    try {
      const [docsRes, remsRes, auditRes, settingsRes] = await Promise.all([
        fetch("/api/documents").then((r) => r.json()),
        fetch("/api/reminders").then((r) => r.json()),
        fetch("/api/audit").then((r) => r.json()),
        fetch("/api/settings").then((r) => r.json()),
      ]);

      if (docsRes.success) {
        setDocuments(docsRes.documents);
        if (docsRes.documents.length > 0 && !selectedDocId) {
          setSelectedDocId(docsRes.documents[0].id);
        }
      }
      if (remsRes.success) setReminders(remsRes.reminders);
      if (auditRes.success) setAuditLogs(auditRes.auditLogs);
      if (settingsRes.success) setSettings(settingsRes.settings);
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    }
  };

  useEffect(() => {
    refreshAllData();
  }, []);

  // Total protected exposure in INR
  const totalProtectedUsd = documents.reduce(
    (acc, d) => acc + (d.totalFinancialExposure || 0),
    0
  );

  const activeDeadlines = reminders.filter((r) => r.status === "PENDING").length;

  const handleTriggerCron = async () => {
    setIsCronRunning(true);
    try {
      const res = await fetch("/api/cron", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        showToast(
          `⚡ Cron heartbeat executed: ${data.triggeredCount} reminder(s) checked.`
        );
        refreshAllData();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsCronRunning(false);
    }
  };

  const handleTriggerEmail = async (reminderId: string, emailOverride?: string) => {
    try {
      const res = await fetch("/api/email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reminderId, emailOverride }),
      });
      const data = await res.json();
      if (data.success) {
        showToast(`✉️ ${data.result.statusMessage}`);
        refreshAllData();
      } else {
        showToast(`⚠️ Notice: ${data.error}`);
      }
    } catch (err: any) {
      showToast(`Error: ${err.message}`);
    }
  };

  const handleUpdateReminderStatus = async (
    id: string,
    status: Reminder["status"]
  ) => {
    try {
      const res = await fetch("/api/reminders", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, status }),
      });
      if (res.ok) {
        showToast(`Reminder marked as ${status}`);
        refreshAllData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSnooze = async (id: string) => {
    const target = reminders.find((r) => r.id === id);
    if (!target) return;
    const newDueDate = new Date(
      new Date(target.dueAt).getTime() + 86400000
    ).toISOString();

    try {
      const res = await fetch("/api/reminders", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, dueAt: newDueDate }),
      });
      if (res.ok) {
        showToast("Snoozed deadline by +24 hours!");
        refreshAllData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteReminder = async (id: string) => {
    try {
      const res = await fetch(`/api/reminders?id=${id}`, { method: "DELETE" });
      if (res.ok) {
        showToast("Reminder deleted from active schedule.");
        refreshAllData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleUploadDoc = async (doc: {
    title: string;
    content: string;
    category: any;
  }) => {
    try {
      const res = await fetch("/api/documents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(doc),
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Ingested and analyzed "${doc.title}"!`);
        refreshAllData();
        setSelectedDocId(data.document.id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteDoc = async (id: string) => {
    try {
      const res = await fetch(`/api/documents?id=${id}`, { method: "DELETE" });
      if (res.ok) {
        showToast("Document removed.");
        refreshAllData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddReminderFromClause = async (
    clause: ExtractedClause,
    doc: DocumentRecord
  ) => {
    try {
      const res = await fetch("/api/reminders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: `${clause.actionRequired}`,
          dueAt: `${clause.deadlineDate}T${clause.deadlineTime || "17:00"}:00.000Z`,
          sourceClauseQuote: clause.quotedText,
          sourceSection: clause.sourceSection,
          financialImpactUsd: clause.financialImpactUsd,
          documentId: doc.id,
          documentTitle: doc.title,
        }),
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Scheduled reminder for ${clause.deadlineDate}!`);
        refreshAllData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleResetDemo = async () => {
    if (!confirm("Reset all documents, reminders, and activity logs to default demo presets?"))
      return;
    try {
      const res = await fetch("/api/settings?action=reset", { method: "POST" });
      if (res.ok) {
        showToast("State reset to official demo contracts!");
        refreshAllData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const currentSelectedDoc = documents.find((d) => d.id === selectedDocId);

  return (
    <div className="min-h-screen flex flex-col bg-[#eef2f6] text-slate-900 selection:bg-indigo-900 selection:text-indigo-100">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl border border-slate-700 bg-[#0f172a] text-xs font-semibold text-white shadow-2xl flex items-center gap-2.5">
          <span className="w-2 h-2 rounded-full bg-indigo-400 animate-ping" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Main Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onOpenOutbox={() => setIsOutboxOpen(true)}
        onResetDemo={handleResetDemo}
        onTriggerCron={handleTriggerCron}
        isCronRunning={isCronRunning}
        onOpenCreateModal={() => setIsCreateModalOpen(true)}
      />

      {/* Dashboard Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {/* Top Metric HUD */}
        <TopStatsHUD
          totalProtectedUsd={totalProtectedUsd}
          totalContracts={documents.length}
          activeDeadlines={activeDeadlines}
          onSelectSample={(docId) => {
            setSelectedDocId(docId);
            setActiveTab("documents");
          }}
          onOpenCreateModal={() => setIsCreateModalOpen(true)}
        />

        {/* Tab 1: AI Agent Command Hub (Chat) */}
        {activeTab === "chat" && (
          <AgentChat
            onReminderCreated={() => {
              showToast("Reminder created and scheduled!");
              refreshAllData();
            }}
            selectedDocumentContext={currentSelectedDoc?.rawContent}
            onNavigateToTab={(t) => setActiveTab(t)}
          />
        )}

        {/* Tab 2: Document Studio & Clause Radar */}
        {activeTab === "documents" && (
          <DocumentStudio
            documents={documents}
            selectedDocId={selectedDocId}
            onSelectDoc={(id) => setSelectedDocId(id)}
            onUploadDoc={handleUploadDoc}
            onDeleteDoc={handleDeleteDoc}
            onAddReminderFromClause={handleAddReminderFromClause}
            onOpenCreateModal={() => setIsCreateModalOpen(true)}
          />
        )}

        {/* Tab 3: Deadlines & Execution Command Center */}
        {activeTab === "reminders" && (
          <RemindersCenter
            reminders={reminders}
            onTriggerEmail={handleTriggerEmail}
            onUpdateStatus={handleUpdateReminderStatus}
            onSnooze={handleSnooze}
            onDelete={handleDeleteReminder}
            onTriggerCron={handleTriggerCron}
            isCronRunning={isCronRunning}
            defaultEmail={settings?.userEmail || "laxmiharshithrebally@gmail.com"}
            hasResendKey={Boolean(settings?.resendApiKey && settings.resendApiKey.startsWith("re_"))}
            onOpenSettings={() => setIsSettingsOpen(true)}
            onOpenOutbox={() => setIsOutboxOpen(true)}
            onOpenCreateModal={() => setIsCreateModalOpen(true)}
          />
        )}

        {/* Tab 4: Trust Layer & Audit Ledger */}
        {activeTab === "audit" && (
          <ActivityAuditLog auditLogs={auditLogs} />
        )}
      </main>

      {/* Add New Agreement / Custom Alert Modal */}
      <CreateAgreementModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onCreated={() => {
          showToast("🎉 New agreement added & scheduled for monitoring!");
          refreshAllData();
          setActiveTab("reminders");
        }}
      />

      {/* Outbox Inspector Modal */}
      <EmailInspectorModal
        isOpen={isOutboxOpen}
        onClose={() => setIsOutboxOpen(false)}
      />

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onSettingsUpdated={(updated) => {
          setSettings(updated);
          showToast("Settings updated successfully!");
        }}
      />
    </div>
  );
}
