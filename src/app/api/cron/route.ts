import { NextResponse } from "next/server";
import {
  getReminders,
  updateReminder,
  deleteReminder,
  addAuditLog,
  getSettings,
} from "@/lib/storage";
import { dispatchReminderEmail } from "@/lib/resend";
import { dispatchReminderSms } from "@/lib/sms";

export async function POST(req: Request) {
  try {
    const { forceTriggerId } = (await req.json().catch(() => ({}))) as {
      forceTriggerId?: string;
    };
    const reminders = getReminders();
    const settings = getSettings();
    const now = new Date();
    const nowTime = now.getTime();

    let triggeredCount = 0;
    let cleanedCount = 0;
    const triggeredList: string[] = [];

    const targetPhone = settings.targetPhoneNumber || "9246972662";

    for (const reminder of reminders) {
      const dueTime = new Date(reminder.dueAt).getTime();
      const diffHours = (dueTime - nowTime) / (1000 * 3600);
      const diffDays = diffHours / 24;
      const isManualForce = forceTriggerId && reminder.id === forceTriggerId;

      // ─── STAGE 4: AUTO-CLEANUP AFTER EXPIRATION ────────────────────────────
      // If cutoff passed more than 24 hours ago, auto-delete/archive it from active view
      if (nowTime > dueTime + 24 * 3600 * 1000 && reminder.status !== "PENDING") {
        deleteReminder(reminder.id);
        cleanedCount++;
        addAuditLog({
          actionType: "REMINDER_RESOLVED",
          summary: `Auto-Cleanup: Expired Notice Archived: ${reminder.title}`,
          details: `Cutoff date (${new Date(reminder.dueAt).toLocaleDateString()}) has passed. Automatically cleaned up from active monitoring.`,
          targetId: reminder.id,
          status: "INFO",
        });
        continue;
      }

      // ─── STAGE 3: FINAL DAY / CUTOFF REACHED ─────────────────────────────
      if (
        (nowTime >= dueTime && !reminder.alertFinalSent && reminder.status === "PENDING") ||
        isManualForce
      ) {
        // Dispatch Email
        const emailRes = await dispatchReminderEmail(reminder, settings.userEmail, "FINAL_DAY");
        // Dispatch Cellular SMS
        await dispatchReminderSms(reminder, targetPhone, "Member", "FINAL_DAY");

        updateReminder(reminder.id, {
          status: "TRIGGERED",
          notifiedAt: new Date().toISOString(),
          notificationEmail: settings.userEmail,
          resendMessageId: emailRes.messageId,
          alertFinalSent: true,
        });

        triggeredCount++;
        triggeredList.push(`[Final Day] ${reminder.title}`);
        continue;
      }

      // ─── STAGE 2: 24-HOUR URGENT ALERT (1 DAY BEFORE) ────────────────────
      if (diffHours <= 24 && diffHours > 0 && !reminder.alert1dSent) {
        await dispatchReminderEmail(reminder, settings.userEmail, "24_HOURS");
        await dispatchReminderSms(reminder, targetPhone, "Member", "24_HOURS");

        updateReminder(reminder.id, {
          alert1dSent: true,
          notifiedAt: new Date().toISOString(),
        });

        triggeredCount++;
        triggeredList.push(`[24h Alert] ${reminder.title}`);
        continue;
      }

      // ─── STAGE 1: 7-DAY EARLY WARNING (1 WEEK BEFORE) ───────────────────
      if (diffDays <= 7 && diffDays > 1 && !reminder.alert7dSent) {
        await dispatchReminderEmail(reminder, settings.userEmail, "7_DAYS");
        await dispatchReminderSms(reminder, targetPhone, "Member", "7_DAYS");

        updateReminder(reminder.id, {
          alert7dSent: true,
          notifiedAt: new Date().toISOString(),
        });

        triggeredCount++;
        triggeredList.push(`[7-Day Warning] ${reminder.title}`);
      }
    }

    addAuditLog({
      actionType: "CRON_HEARTBEAT",
      summary: `TermGuard Cron Cycle: ${triggeredCount} Alerts Dispatched, ${cleanedCount} Expired Cleaned`,
      details:
        triggeredCount > 0
          ? `Dispatched multi-stage alerts for: ${triggeredList.join(", ")}.`
          : `Scanned active reminders. All temporal windows monitored. 0 immediate alerts due.`,
      status: triggeredCount > 0 ? "SUCCESS" : "INFO",
    });

    return NextResponse.json({
      success: true,
      scannedCount: reminders.length,
      triggeredCount,
      cleanedCount,
      triggeredList,
      timestamp: new Date().toISOString(),
    });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function GET() {
  try {
    const reminders = getReminders();
    const settings = getSettings();
    const now = new Date();
    const nowTime = now.getTime();
    let triggeredCount = 0;
    const targetPhone = settings.targetPhoneNumber || "9246972662";

    for (const reminder of reminders) {
      const dueTime = new Date(reminder.dueAt).getTime();
      const diffHours = (dueTime - nowTime) / (1000 * 3600);
      const diffDays = diffHours / 24;

      if (nowTime >= dueTime && !reminder.alertFinalSent && reminder.status === "PENDING") {
        await dispatchReminderEmail(reminder, settings.userEmail, "FINAL_DAY");
        await dispatchReminderSms(reminder, targetPhone, "Member", "FINAL_DAY");
        updateReminder(reminder.id, {
          status: "TRIGGERED",
          notifiedAt: new Date().toISOString(),
          alertFinalSent: true,
        });
        triggeredCount++;
      } else if (diffHours <= 24 && diffHours > 0 && !reminder.alert1dSent) {
        await dispatchReminderEmail(reminder, settings.userEmail, "24_HOURS");
        await dispatchReminderSms(reminder, targetPhone, "Member", "24_HOURS");
        updateReminder(reminder.id, { alert1dSent: true });
        triggeredCount++;
      } else if (diffDays <= 7 && diffDays > 1 && !reminder.alert7dSent) {
        await dispatchReminderEmail(reminder, settings.userEmail, "7_DAYS");
        await dispatchReminderSms(reminder, targetPhone, "Member", "7_DAYS");
        updateReminder(reminder.id, { alert7dSent: true });
        triggeredCount++;
      }
    }

    return NextResponse.json({ success: true, triggeredCount });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
