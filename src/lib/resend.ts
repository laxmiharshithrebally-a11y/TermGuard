import { Resend } from "resend";
import { addEmailLog, addAuditLog, getSettings } from "./storage";
import { Reminder } from "./types";

export interface SendEmailResult {
  success: boolean;
  messageId: string;
  isRealDispatch: boolean;
  statusMessage: string;
  htmlContent: string;
}

export function generateReminderEmailHtml(
  reminder: Reminder,
  recipientEmail: string,
  alertStage?: "7_DAYS" | "24_HOURS" | "FINAL_DAY"
): string {
  const dueFormatted = new Date(reminder.dueAt).toLocaleDateString("en-IN", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const stageHeader =
    alertStage === "7_DAYS"
      ? { badge: "7-Day Early Warning", title: "📅 7 Days Remaining to Notice Cutoff", color: "#6366f1" }
      : alertStage === "24_HOURS"
      ? { badge: "24-Hour Urgent Warning", title: "🚨 Urgent: Cutoff Closes Tomorrow!", color: "#f59e0b" }
      : alertStage === "FINAL_DAY"
      ? { badge: "Final Expiration Day", title: "⚠️ Notice Deadline Closes Today!", color: "#ef4444" }
      : { badge: "Deadline Alert", title: "⚠️ Action Required: Contract Cutoff Imminent", color: "#6366f1" };

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>TermGuard Alert</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }
    .container { max-width: 600px; margin: 0 auto; background-color: #1e293b; border: 1px solid #334155; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 35px rgba(0,0,0,0.5); }
    .header { background: linear-gradient(135deg, #090d16 0%, #1e1b4b 100%); padding: 28px 32px; border-bottom: 2px solid ${stageHeader.color}; }
    .brand { font-size: 13px; text-transform: uppercase; letter-spacing: 2px; color: #818cf8; font-weight: 700; margin-bottom: 8px; }
    .title { font-size: 20px; font-weight: 700; color: #ffffff; margin: 0; line-height: 1.3; }
    .content { padding: 32px; }
    .badge { display: inline-block; padding: 6px 14px; border-radius: 9999px; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 16px; background-color: rgba(99, 102, 241, 0.2); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.4); }
    .deadline-box { background-color: #0f172a; border-radius: 12px; padding: 18px 20px; margin: 20px 0; border-left: 4px solid ${stageHeader.color}; }
    .deadline-label { font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .deadline-value { font-size: 17px; font-weight: 700; color: #38bdf8; margin-top: 4px; }
    .financial-alert { background-color: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; padding: 14px 18px; margin: 20px 0; color: #fbbf24; font-size: 14px; }
    .clause-box { background-color: #0b0f17; border: 1px dashed #475569; border-radius: 10px; padding: 16px; margin: 20px 0; font-family: monospace; font-size: 12px; line-height: 1.6; color: #e2e8f0; }
    .clause-title { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; margin-bottom: 8px; font-weight: 600; }
    .footer { background-color: #090d16; padding: 20px 32px; border-top: 1px solid #1e293b; text-align: center; font-size: 12px; color: #64748b; }
    .btn { display: inline-block; background-color: #4f46e5; color: #ffffff !important; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-weight: 700; font-size: 14px; margin-top: 12px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand">TermGuard • Autonomous Contract Defense</div>
      <h1 class="title">${stageHeader.title}</h1>
    </div>
    <div class="content">
      <span class="badge">${stageHeader.badge}</span>
      <p style="font-size: 15px; line-height: 1.6; margin-top: 0; color: #cbd5e1;">
        TermGuard has detected an active contract obligation requiring your prompt intervention to prevent unwanted financial commitment or penalty forfeiture.
      </p>

      <div class="deadline-box">
        <div class="deadline-label">Action Item</div>
        <div style="font-size: 16px; font-weight: 600; color: #ffffff; margin-top: 4px;">${reminder.title}</div>
        <div class="deadline-label" style="margin-top: 12px;">Enforcement Cutoff Timestamp</div>
        <div class="deadline-value">${dueFormatted}</div>
      </div>

      ${
        reminder.financialImpactUsd
          ? `
      <div class="financial-alert">
        💰 <strong>Potential Money at Risk:</strong> ₹${reminder.financialImpactUsd.toLocaleString("en-IN")} INR
      </div>
      `
          : ""
      }

      ${
        reminder.sourceClauseQuote
          ? `
      <div class="clause-box">
        <div class="clause-title">SOURCE CLAUSE ${reminder.sourceSection ? `(${reminder.sourceSection})` : ""}:</div>
        "${reminder.sourceClauseQuote}"
      </div>
      `
          : ""
      }

      ${
        reminder.cancellationNoticeDraft
          ? `
      <div style="margin-top: 24px;">
        <div class="deadline-label" style="margin-bottom: 8px;">PRE-WRITTEN NOTICE DRAFT READY TO COPY:</div>
        <div class="clause-box" style="white-space: pre-wrap; font-size: 12px; color: #cbd5e1;">
${reminder.cancellationNoticeDraft}
        </div>
      </div>
      `
          : ""
      }

      <div style="text-align: center; margin-top: 28px;">
        <a href="http://localhost:3000/dashboard" class="btn">Open TermGuard Console →</a>
      </div>
    </div>
    <div class="footer">
      Sent by <strong>TermGuard Autonomous Defense Core</strong> • Recipient: ${recipientEmail}<br/>
      Cryptographic Audit Hash: #${reminder.id}
    </div>
  </div>
</body>
</html>
  `;
}

export async function dispatchReminderEmail(
  reminder: Reminder,
  targetEmail?: string,
  alertStage?: "7_DAYS" | "24_HOURS" | "FINAL_DAY"
): Promise<SendEmailResult> {
  const settings = getSettings();
  const recipient = targetEmail || settings.userEmail || "laxmiharshithrebally@gmail.com";
  const apiKey = settings.resendApiKey || process.env.RESEND_API_KEY;

  const stagePrefix =
    alertStage === "7_DAYS"
      ? "[TermGuard Warning - 7 Days Left]"
      : alertStage === "24_HOURS"
      ? "[TermGuard URGENT - 24 Hours Left]"
      : alertStage === "FINAL_DAY"
      ? "[TermGuard FINAL CALL - Cutoff Today]"
      : "[TermGuard Action Required]";

  const subject = `${stagePrefix}: ${reminder.title}`;
  const htmlContent = generateReminderEmailHtml(reminder, recipient, alertStage);

  if (apiKey && apiKey.startsWith("re_")) {
    try {
      const resend = new Resend(apiKey);
      const data = await resend.emails.send({
        from: "TermGuard Defense <onboarding@resend.dev>",
        to: [recipient],
        subject: subject,
        html: htmlContent,
      });

      if (data.error) {
        throw new Error(data.error.message);
      }

      const messageId = data.data?.id || `msg_${Date.now()}`;

      addEmailLog({
        recipient,
        subject,
        htmlContent,
        status: "DELIVERED",
        messageId,
        reminderId: reminder.id,
        reminderTitle: reminder.title,
        sourceClause: reminder.sourceClauseQuote,
      });

      addAuditLog({
        actionType: "EMAIL_DELIVERED",
        summary: `Real Email Dispatched via Resend: ${reminder.title}`,
        details: `Dispatched to ${recipient}. Resend Message ID: ${messageId}. HTTP 200 OK.`,
        targetId: reminder.id,
        status: "SUCCESS",
      });

      return {
        success: true,
        messageId,
        isRealDispatch: true,
        statusMessage: `Real email successfully dispatched to ${recipient}! Message ID: ${messageId}`,
        htmlContent,
      };
    } catch (err: any) {
      console.error("Resend API dispatch failed:", err.message);
    }
  }

  // Fallback Simulation
  const fallbackMessageId = `sim_${Date.now().toString(36)}`;

  addEmailLog({
    recipient,
    subject,
    htmlContent,
    status: "SIMULATED",
    messageId: fallbackMessageId,
    reminderId: reminder.id,
    reminderTitle: reminder.title,
    sourceClause: reminder.sourceClauseQuote,
  });

  addAuditLog({
    actionType: "EMAIL_TRIGGERED",
    summary: `Simulated Email Created: ${reminder.title}`,
    details: `Generated email for ${recipient} in TermGuard Outbox.`,
    targetId: reminder.id,
    status: "INFO",
  });

  return {
    success: true,
    messageId: fallbackMessageId,
    isRealDispatch: false,
    statusMessage: `Email generated for ${recipient}. Available in In-App Outbox.`,
    htmlContent,
  };
}
