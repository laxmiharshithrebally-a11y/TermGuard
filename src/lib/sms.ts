import { addAuditLog, getSettings } from "./storage";
import { Reminder } from "./types";

export interface SendSmsResult {
  success: boolean;
  messageId: string;
  isRealDispatch: boolean;
  statusMessage: string;
  smsBody: string;
  recipientPhone: string;
}

export function formatReminderSmsText(
  reminder: Reminder,
  recipientName?: string,
  alertStage?: "7_DAYS" | "24_HOURS" | "FINAL_DAY"
): string {
  const dateFormatted = new Date(reminder.dueAt).toLocaleDateString("en-IN", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  const moneyStr = reminder.financialImpactUsd
    ? ` Protect ₹${reminder.financialImpactUsd.toLocaleString("en-IN")}.`
    : "";

  if (alertStage === "7_DAYS") {
    return `[TermGuard Warning] 7-Day Notice: Cutoff for "${reminder.title}" is in 1 week (${dateFormatted}).${moneyStr} Prepare cancellation notice in TermGuard.`;
  }

  if (alertStage === "24_HOURS") {
    return `[TermGuard URGENT] 24-Hour Alert: Tomorrow is the final notice cutoff for "${reminder.title}"!${moneyStr} Take action immediately.`;
  }

  if (alertStage === "FINAL_DAY") {
    return `[TermGuard FINAL CALL] Cutoff expires TODAY for "${reminder.title}".${moneyStr} Window closes today.`;
  }

  return `[TermGuard Alert] Hi ${recipientName || "there"}, action required: ${reminder.title}. Cutoff: ${dateFormatted}.${moneyStr} Check your TermGuard dashboard.`;
}

export async function dispatchReminderSms(
  reminder: Reminder,
  targetPhone: string,
  recipientName?: string,
  alertStage?: "7_DAYS" | "24_HOURS" | "FINAL_DAY"
): Promise<SendSmsResult> {
  const settings = getSettings();
  const digitsOnly = targetPhone.replace(/\D/g, "");
  const cleanPhone = targetPhone.trim();
  const smsBody = formatReminderSmsText(reminder, recipientName, alertStage);

  // 1. Check for Fast2SMS API Key (Popular instant SMS gateway in India)
  const fast2smsKey = settings.fast2smsApiKey || process.env.FAST2SMS_API_KEY;
  if (fast2smsKey && digitsOnly.length >= 10) {
    const indian10Digit = digitsOnly.slice(-10);
    try {
      const response = await fetch("https://www.fast2sms.com/dev/bulkV2", {
        method: "POST",
        headers: {
          authorization: fast2smsKey,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          route: "q",
          message: smsBody,
          language: "english",
          flash: 0,
          numbers: indian10Digit,
        }),
      });

      const data = await response.json();
      if (data.return) {
        const messageId = data.request_id || `fast2sms_${Date.now()}`;
        addAuditLog({
          actionType: "EMAIL_DELIVERED",
          summary: `Cellular SMS Dispatched via Fast2SMS: ${indian10Digit}`,
          details: `Delivered SMS to Indian phone ${indian10Digit} over cellular network. Request ID: ${messageId}.`,
          targetId: reminder.id,
          status: "SUCCESS",
        });

        return {
          success: true,
          messageId,
          isRealDispatch: true,
          statusMessage: `Real SMS successfully delivered to ${indian10Digit} over cellular network via Fast2SMS!`,
          smsBody,
          recipientPhone: indian10Digit,
        };
      }
    } catch (err: any) {
      console.error("Fast2SMS dispatch error:", err.message);
    }
  }

  // 2. Twilio Credentials (with automatic fallback to configured environment credentials)
  const accountSid =
    process.env.TWILIO_ACCOUNT_SID ||
    settings.twilioAccountSid ||
    "";
  const authToken =
    process.env.TWILIO_AUTH_TOKEN ||
    settings.twilioAuthToken ||
    "";
  const fromNumber =
    process.env.TWILIO_PHONE_NUMBER ||
    settings.twilioPhoneNumber ||
    "";
  const messagingServiceSid =
    process.env.TWILIO_MESSAGING_SERVICE_SID ||
    settings.twilioMessagingServiceSid ||
    "";

  if (accountSid && authToken && cleanPhone) {
    try {
      // Normalize to E.164 (+91 for 10-digit Indian numbers)
      let formattedPhone = cleanPhone;
      if (!formattedPhone.startsWith("+")) {
        if (digitsOnly.length === 10) {
          formattedPhone = `+91${digitsOnly}`;
        } else {
          formattedPhone = `+${digitsOnly}`;
        }
      }

      const authHeader = "Basic " + Buffer.from(`${accountSid}:${authToken}`).toString("base64");
      const url = `https://api.twilio.com/2010-04-01/Accounts/${accountSid}/Messages.json`;

      const params = new URLSearchParams();
      params.append("To", formattedPhone);
      if (fromNumber) {
        params.append("From", fromNumber);
      } else if (messagingServiceSid) {
        params.append("MessagingServiceSid", messagingServiceSid);
      }
      params.append("Body", smsBody);

      const response = await fetch(url, {
        method: "POST",
        headers: {
          Authorization: authHeader,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: params.toString(),
      });

      const data = await response.json();

      if (!response.ok) {
        // If fromNumber failed, attempt with MessagingServiceSid
        if (messagingServiceSid && fromNumber) {
          const fallbackParams = new URLSearchParams();
          fallbackParams.append("To", formattedPhone);
          fallbackParams.append("MessagingServiceSid", messagingServiceSid);
          fallbackParams.append("Body", smsBody);

          const fallbackRes = await fetch(url, {
            method: "POST",
            headers: {
              Authorization: authHeader,
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: fallbackParams.toString(),
          });
          const fallbackData = await fallbackRes.json();
          if (fallbackRes.ok) {
            const messageId = fallbackData.sid || `twilio_${Date.now()}`;
            addAuditLog({
              actionType: "EMAIL_DELIVERED",
              summary: `Cellular SMS Dispatched via Twilio: ${formattedPhone}`,
              details: `Dispatched SMS to ${formattedPhone}. Twilio SID: ${messageId}. Status: ${fallbackData.status || "queued"}.`,
              targetId: reminder.id,
              status: "SUCCESS",
            });
            return {
              success: true,
              messageId,
              isRealDispatch: true,
              statusMessage: `Real SMS successfully delivered directly to ${formattedPhone} via Twilio! (SID: ${messageId})`,
              smsBody,
              recipientPhone: formattedPhone,
            };
          }
        }
        throw new Error(data.message || "Twilio SMS dispatch failed");
      }

      const messageId = data.sid || `twilio_${Date.now()}`;

      addAuditLog({
        actionType: "EMAIL_DELIVERED",
        summary: `Cellular SMS Dispatched via Twilio: ${formattedPhone}`,
        details: `Dispatched SMS to ${formattedPhone}. Twilio SID: ${messageId}. Status: ${data.status || "queued"}.`,
        targetId: reminder.id,
        status: "SUCCESS",
      });

      return {
        success: true,
        messageId,
        isRealDispatch: true,
        statusMessage: `Real SMS delivered directly to ${formattedPhone} via Twilio! (SID: ${messageId})`,
        smsBody,
        recipientPhone: formattedPhone,
      };
    } catch (err: any) {
      console.error("Twilio SMS dispatch error:", err.message);
    }
  }

  // 3. Simulated Fallback
  const simMessageId = `sms_sim_${Date.now().toString(36)}`;

  addAuditLog({
    actionType: "EMAIL_TRIGGERED",
    summary: `SMS Alert Generated: ${cleanPhone}`,
    details: `Alert text prepared for ${cleanPhone}: "${smsBody}".`,
    targetId: reminder.id,
    status: "INFO",
  });

  return {
    success: true,
    messageId: simMessageId,
    isRealDispatch: false,
    statusMessage: `SMS alert generated for ${cleanPhone}. (Tap 'Open in Phone SMS App' below to send immediately from your phone!)`,
    smsBody,
    recipientPhone: cleanPhone,
  };
}
