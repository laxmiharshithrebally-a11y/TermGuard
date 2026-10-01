import { NextResponse } from "next/server";
import { getEmailLogs, getReminders, updateReminder } from "@/lib/storage";
import { dispatchReminderEmail } from "@/lib/resend";

export async function GET() {
  try {
    const logs = getEmailLogs();
    return NextResponse.json({ success: true, emailLogs: logs });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { reminderId, emailOverride } = body;

    const reminders = getReminders();
    const targetReminder = reminders.find((r) => r.id === reminderId);

    if (!targetReminder) {
      return NextResponse.json({ success: false, error: "Reminder not found" }, { status: 404 });
    }

    const result = await dispatchReminderEmail(targetReminder, emailOverride);

    updateReminder(targetReminder.id, {
      status: "TRIGGERED",
      notifiedAt: new Date().toISOString(),
      notificationEmail: emailOverride || targetReminder.notificationEmail,
      resendMessageId: result.messageId,
    });

    return NextResponse.json({ success: true, result });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
