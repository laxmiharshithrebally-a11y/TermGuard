import { NextResponse } from "next/server";
import {
  getReminders,
  createReminder,
  updateReminder,
  deleteReminder,
  addAuditLog,
} from "@/lib/storage";
import { Reminder } from "@/lib/types";

export async function GET() {
  try {
    const reminders = getReminders();
    return NextResponse.json({ success: true, reminders });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const {
      title,
      dueAt,
      sourceClauseQuote,
      sourceSection,
      financialImpactUsd,
      documentId,
      documentTitle,
      cancellationNoticeDraft,
    } = body;

    if (!title || !dueAt) {
      return NextResponse.json(
        { success: false, error: "Title and dueAt are required" },
        { status: 400 }
      );
    }

    const newReminder: Reminder = {
      id: `rem-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      title,
      dueAt,
      sourceClauseQuote,
      sourceSection,
      financialImpactUsd: financialImpactUsd || 0,
      documentId,
      documentTitle,
      status: "PENDING",
      createdAt: new Date().toISOString(),
      cancellationNoticeDraft,
    };

    createReminder(newReminder);

    addAuditLog({
      actionType: "REMINDER_CREATED",
      summary: `Reminder Scheduled: ${title}`,
      details: `Enforcement set for ${new Date(dueAt).toLocaleString()}. Protected liability: $${financialImpactUsd || 0}.`,
      targetId: newReminder.id,
      status: "SUCCESS",
    });

    return NextResponse.json({ success: true, reminder: newReminder });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function PATCH(req: Request) {
  try {
    const body = await req.json();
    const { id, ...updates } = body;
    if (!id) {
      return NextResponse.json({ success: false, error: "Reminder ID required" }, { status: 400 });
    }

    const updated = updateReminder(id, updates);
    if (!updated) {
      return NextResponse.json({ success: false, error: "Reminder not found" }, { status: 404 });
    }

    addAuditLog({
      actionType: "REMINDER_UPDATED",
      summary: `Reminder Updated: ${updated.title}`,
      details: `Status set to ${updated.status}. Modified properties: ${Object.keys(updates).join(", ")}.`,
      targetId: id,
      status: "INFO",
    });

    return NextResponse.json({ success: true, reminder: updated });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function DELETE(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const id = searchParams.get("id");
    if (!id) {
      return NextResponse.json({ success: false, error: "Reminder ID required" }, { status: 400 });
    }

    deleteReminder(id);

    addAuditLog({
      actionType: "REMINDER_RESOLVED",
      summary: `Reminder Deleted: ${id}`,
      details: "Removed reminder obligation from active monitoring queue.",
      targetId: id,
      status: "INFO",
    });

    return NextResponse.json({ success: true });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
