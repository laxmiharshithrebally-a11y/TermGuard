export type RiskLevel = "CRITICAL" | "WARNING" | "INFO";

export type ReminderStatus = "PENDING" | "DUE_SOON" | "TRIGGERED" | "RESOLVED" | "DISMISSED" | "EXPIRED";

export interface ExtractedClause {
  id: string;
  clauseTitle: string;
  sourceSection: string;
  quotedText: string;
  deadlineDate: string; // ISO string or YYYY-MM-DD
  deadlineTime?: string; // e.g. "17:00"
  riskLevel: RiskLevel;
  financialImpactUsd: number;
  explanation: string;
  actionRequired: string;
}

export interface DocumentRecord {
  id: string;
  title: string;
  category: "SUBSCRIPTION" | "LEASE" | "EMPLOYMENT" | "WARRANTY" | "CUSTOM" | "INSURANCE" | "TELECOM" | "BANKING" | "OTHER";
  uploadedAt: string;
  rawContent: string;
  riskScore: number; // 0 - 100
  totalFinancialExposure: number; // in INR
  clauses: ExtractedClause[];
  status: "ANALYZED" | "PROCESSING" | "ERROR";
}

export interface Reminder {
  id: string;
  documentId?: string;
  documentTitle?: string;
  title: string;
  dueAt: string; // ISO date-time string
  sourceClauseQuote?: string;
  sourceSection?: string;
  financialImpactUsd?: number;
  status: ReminderStatus;
  notifiedAt?: string;
  notificationEmail?: string;
  resendMessageId?: string;
  createdAt: string;
  cancellationNoticeDraft?: string;
  alert7dSent?: boolean;
  alert1dSent?: boolean;
  alertFinalSent?: boolean;
  autoDeleteAfterExpiry?: boolean;
}

export interface AuditLogEntry {
  id: string;
  timestamp: string;
  actionType:
    | "DOC_UPLOADED"
    | "DOC_PARSED"
    | "CLAUSE_EXTRACTED"
    | "REMINDER_CREATED"
    | "REMINDER_UPDATED"
    | "REMINDER_RESOLVED"
    | "CRON_HEARTBEAT"
    | "EMAIL_TRIGGERED"
    | "EMAIL_DELIVERED"
    | "DISPUTE_DRAFTED";
  summary: string;
  details: string;
  targetId?: string;
  metadata?: Record<string, any>;
  status: "SUCCESS" | "WARNING" | "INFO" | "ERROR";
}

export interface EmailDispatchLog {
  id: string;
  timestamp: string;
  recipient: string;
  subject: string;
  htmlContent: string;
  status: "SENT" | "DELIVERED" | "SIMULATED" | "FAILED";
  messageId: string;
  reminderId?: string;
  reminderTitle?: string;
  sourceClause?: string;
}

export interface AppSettings {
  userEmail: string;
  targetPhoneNumber?: string;
  resendApiKey: string;
  geminiApiKey: string;
  twilioAccountSid?: string;
  twilioAuthToken?: string;
  twilioPhoneNumber?: string;
  twilioMessagingServiceSid?: string;
  fast2smsApiKey?: string;
  cronIntervalMinutes: number;
  autoSendEmails: boolean;
  autoSendSms: boolean;
}
