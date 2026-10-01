import { NextResponse } from "next/server";
import { getAuditLogs } from "@/lib/storage";

export async function GET() {
  try {
    const logs = getAuditLogs();
    return NextResponse.json({ success: true, auditLogs: logs });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
