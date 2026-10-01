import fs from "fs";
import path from "path";
import {
  DocumentRecord,
  Reminder,
  AuditLogEntry,
  EmailDispatchLog,
  AppSettings,
} from "./types";
import { SAMPLE_CONTRACTS } from "./sampleContracts";

const DATA_DIR = path.join(process.cwd(), "data");
const DB_PATH = path.join(DATA_DIR, "db.json");

interface DatabaseSchema {
  documents: DocumentRecord[];
  reminders: Reminder[];
  auditLogs: AuditLogEntry[];
  emailLogs: EmailDispatchLog[];
  settings: AppSettings;
}

const DEFAULT_SETTINGS: AppSettings = {
  userEmail: "laxmiharshithrebally@gmail.com",
  targetPhoneNumber: "9246972662",
  resendApiKey: process.env.RESEND_API_KEY || "",
  geminiApiKey: process.env.GEMINI_API_KEY || "",
  twilioAccountSid: process.env.TWILIO_ACCOUNT_SID || "",
  twilioAuthToken: process.env.TWILIO_AUTH_TOKEN || "",
  twilioPhoneNumber: process.env.TWILIO_PHONE_NUMBER || "",
  twilioMessagingServiceSid: process.env.TWILIO_MESSAGING_SERVICE_SID || "",
  fast2smsApiKey: process.env.FAST2SMS_API_KEY || "",
  cronIntervalMinutes: 5,
  autoSendEmails: true,
  autoSendSms: true,
};

function getInitialReminders(): Reminder[] {
  return [
    {
      id: "rem-gym-01",
      documentId: "doc-gym-001",
      documentTitle: "Cult.fit & Gold's Gym — Annual Fitness Pass",
      title: "Cancel Gym Auto-Renewal to prevent ₹32,000 auto-debit",
      dueAt: "2026-09-14T18:00:00.000Z",
      sourceSection: "Section 4.3 & 7.2",
      sourceClauseQuote:
        "TO CANCEL AUTO-RENEWAL: You must submit a written cancellation request at least 30 days before renewal (DEADLINE: SEPTEMBER 14, 2026). Late cancellations will not be refunded.",
      financialImpactUsd: 32000,
      status: "PENDING",
      createdAt: new Date(Date.now() - 86400000 * 2).toISOString(),
      cancellationNoticeDraft: `To Support / Membership Team,\n\nRE: Formal Notice of Cancellation for Annual Gym Membership\n\nAs per Section 4.3 of the Membership Terms, I am providing my 30-day written notice to cancel my annual membership pass. Please do not auto-debit my credit card / UPI for ₹32,000 for the upcoming renewal term.\n\nPlease confirm receipt of this cancellation notice in writing.\n\nThank you,\nHarshith R.`,
    },
    {
      id: "rem-lease-02",
      documentId: "doc-lease-002",
      documentTitle: "2BHK Apartment Rental Agreement (Flat 402, Bangalore)",
      title: "Deliver 2-Month Move-Out Notice to Landlord (Protect ₹70,000 Deposit)",
      dueAt: "2026-04-30T18:00:00.000Z",
      sourceSection: "Section 3.2 & 3.3",
      sourceClauseQuote:
        "Either party must give two (2) full months written notice before vacating the flat (DEADLINE: APRIL 30, 2026)... Landlord will forfeit two months of rent (₹70,000 INR) directly from the security deposit.",
      financialImpactUsd: 70000,
      status: "PENDING",
      createdAt: new Date(Date.now() - 86400000 * 4).toISOString(),
      cancellationNoticeDraft: `Dear Landlord (Mr. Narayana Rao),\n\nSubject: Formal 2-Month Notice to Vacate Flat 402 (Green Glen Layout, Bellandur)\n\nAs per Section 3.2 of our Rental Agreement, I am giving formal written notice that I will be vacating the flat on June 30, 2026. Please schedule the flat handover inspection and process the full return of my security deposit (₹1,50,000) minus standard painting deductions.\n\nRegards,\nHarshith R.`,
    },
    {
      id: "rem-saas-03",
      documentId: "doc-saas-003",
      documentTitle: "Zoho / AWS Cloud Services India — Annual Business Plan",
      title: "Submit 30-Day Opt-Out Ticket to prevent ₹48,000 renewal charge",
      dueAt: "2026-10-31T23:59:00.000Z",
      sourceSection: "Section 5.2",
      sourceClauseQuote:
        "To stop auto-renewal, the customer must submit an opt-out cancellation ticket at least 30 days in advance (DEADLINE: OCTOBER 31, 2026).",
      financialImpactUsd: 48000,
      status: "PENDING",
      createdAt: new Date(Date.now() - 86400000 * 7).toISOString(),
    },
  ];
}

function getInitialAuditLogs(): AuditLogEntry[] {
  const now = Date.now();
  return [
    {
      id: "log-seed-1",
      timestamp: new Date(now - 86400000 * 2).toISOString(),
      actionType: "DOC_UPLOADED",
      summary: "Contract Scanned: Cult.fit Gym Membership",
      details: "Parsed 4 sections. Found auto-debit renewal trap. Financial liability at risk: ₹32,000 INR.",
      status: "SUCCESS",
    },
    {
      id: "log-seed-2",
      timestamp: new Date(now - 86400000 * 2 + 1000).toISOString(),
      actionType: "CLAUSE_EXTRACTED",
      summary: "Trap Detected: 30-Day Auto-Debit Cutoff",
      details: "Section 4.3 requires notice before Sept 14, 2026 to stop ₹32,000 debit.",
      status: "WARNING",
    },
    {
      id: "log-seed-3",
      timestamp: new Date(now - 86400000 * 2 + 2000).toISOString(),
      actionType: "REMINDER_CREATED",
      summary: "Deadline Alert Scheduled for Sept 14, 2026",
      details: "Scheduled to notify laxmiharshithrebally@gmail.com and phone before auto-debit triggers.",
      status: "SUCCESS",
    },
    {
      id: "log-seed-4",
      timestamp: new Date(now - 3600000 * 3).toISOString(),
      actionType: "CRON_HEARTBEAT",
      summary: "Background Cron Check Completed",
      details: "Monitored 3 active deadlines. Total liability protected: ₹1,50,000 INR.",
      status: "INFO",
    },
  ];
}

function ensureDb(): DatabaseSchema {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }

  if (!fs.existsSync(DB_PATH)) {
    const initialDb: DatabaseSchema = {
      documents: SAMPLE_CONTRACTS,
      reminders: getInitialReminders(),
      auditLogs: getInitialAuditLogs(),
      emailLogs: [],
      settings: DEFAULT_SETTINGS,
    };
    fs.writeFileSync(DB_PATH, JSON.stringify(initialDb, null, 2), "utf8");
    return initialDb;
  }

  try {
    const raw = fs.readFileSync(DB_PATH, "utf8");
    return JSON.parse(raw);
  } catch (err) {
    const fallbackDb: DatabaseSchema = {
      documents: SAMPLE_CONTRACTS,
      reminders: getInitialReminders(),
      auditLogs: getInitialAuditLogs(),
      emailLogs: [],
      settings: DEFAULT_SETTINGS,
    };
    fs.writeFileSync(DB_PATH, JSON.stringify(fallbackDb, null, 2), "utf8");
    return fallbackDb;
  }
}

function writeDb(data: DatabaseSchema): void {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2), "utf8");
}

export function getDocuments(): DocumentRecord[] {
  return ensureDb().documents;
}

export function saveDocument(doc: DocumentRecord): void {
  const db = ensureDb();
  const index = db.documents.findIndex((d) => d.id === doc.id);
  if (index >= 0) {
    db.documents[index] = doc;
  } else {
    db.documents.unshift(doc);
  }
  writeDb(db);
}

export function deleteDocument(id: string): void {
  const db = ensureDb();
  db.documents = db.documents.filter((d) => d.id !== id);
  db.reminders = db.reminders.filter((r) => r.documentId !== id);
  writeDb(db);
}

export function getReminders(): Reminder[] {
  return ensureDb().reminders;
}

export function createReminder(reminder: Reminder): void {
  const db = ensureDb();
  db.reminders.unshift(reminder);
  writeDb(db);
}

export function updateReminder(id: string, updates: Partial<Reminder>): Reminder | null {
  const db = ensureDb();
  const index = db.reminders.findIndex((r) => r.id === id);
  if (index >= 0) {
    db.reminders[index] = { ...db.reminders[index], ...updates };
    writeDb(db);
    return db.reminders[index];
  }
  return null;
}

export function deleteReminder(id: string): void {
  const db = ensureDb();
  db.reminders = db.reminders.filter((r) => r.id !== id);
  writeDb(db);
}

export function getAuditLogs(): AuditLogEntry[] {
  return ensureDb().auditLogs;
}

export function addAuditLog(entry: Omit<AuditLogEntry, "id" | "timestamp">): AuditLogEntry {
  const db = ensureDb();
  const newEntry: AuditLogEntry = {
    id: `log-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
    timestamp: new Date().toISOString(),
    ...entry,
  };
  db.auditLogs.unshift(newEntry);
  if (db.auditLogs.length > 200) {
    db.auditLogs = db.auditLogs.slice(0, 200);
  }
  writeDb(db);
  return newEntry;
}

export function getEmailLogs(): EmailDispatchLog[] {
  return ensureDb().emailLogs;
}

export function addEmailLog(log: Omit<EmailDispatchLog, "id" | "timestamp">): EmailDispatchLog {
  const db = ensureDb();
  const newLog: EmailDispatchLog = {
    id: `email-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
    timestamp: new Date().toISOString(),
    ...log,
  };
  db.emailLogs.unshift(newLog);
  writeDb(db);
  return newLog;
}

export function getSettings(): AppSettings {
  return ensureDb().settings;
}

export function updateSettings(settings: Partial<AppSettings>): AppSettings {
  const db = ensureDb();
  db.settings = { ...db.settings, ...settings };
  writeDb(db);
  return db.settings;
}

export function resetToDemo(): void {
  const db: DatabaseSchema = {
    documents: SAMPLE_CONTRACTS,
    reminders: getInitialReminders(),
    auditLogs: getInitialAuditLogs(),
    emailLogs: [],
    settings: DEFAULT_SETTINGS,
  };
  writeDb(db);
}
