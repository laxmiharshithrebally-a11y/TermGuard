import { NextResponse } from "next/server";
import { getReminders } from "@/lib/storage";
import { dispatchReminderSms } from "@/lib/sms";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { reminderId, phoneNumber, recipientName } = body;

    if (!reminderId || !phoneNumber) {
      return NextResponse.json(
        { success: false, error: "Reminder ID and Phone Number are required" },
        { status: 400 }
      );
    }

    const reminders = getReminders();
    const targetReminder = reminders.find((r) => r.id === reminderId);

    if (!targetReminder) {
      return NextResponse.json(
        { success: false, error: "Reminder not found" },
        { status: 404 }
      );
    }

    const result = await dispatchReminderSms(targetReminder, phoneNumber, recipientName);
    return NextResponse.json({ success: true, result });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
