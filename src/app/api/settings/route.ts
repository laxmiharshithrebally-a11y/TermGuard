import { NextResponse } from "next/server";
import { getSettings, updateSettings, resetToDemo, addAuditLog } from "@/lib/storage";

export async function GET() {
  try {
    const settings = getSettings();
    return NextResponse.json({ success: true, settings });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function POST(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const action = searchParams.get("action");

    if (action === "reset") {
      resetToDemo();
      addAuditLog({
        actionType: "CRON_HEARTBEAT",
        summary: "System State Reset to Demo Presets",
        details: "Restored sample contracts, initial deadlines, and verified baseline state.",
        status: "INFO",
      });
      return NextResponse.json({ success: true, message: "Reset to demo successful" });
    }

    const updates = await req.json();
    const updated = updateSettings(updates);

    addAuditLog({
      actionType: "CRON_HEARTBEAT",
      summary: "System Settings Updated",
      details: `Updated user notification recipient to: ${updated.userEmail}.`,
      status: "INFO",
    });

    return NextResponse.json({ success: true, settings: updated });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
