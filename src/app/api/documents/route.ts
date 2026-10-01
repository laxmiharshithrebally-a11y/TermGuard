import { NextResponse } from "next/server";
import { getDocuments, saveDocument, deleteDocument, addAuditLog } from "@/lib/storage";
import { parseContractTextHeuristic } from "@/lib/gemini";
import { DocumentRecord } from "@/lib/types";

export async function GET() {
  try {
    const docs = getDocuments();
    return NextResponse.json({ success: true, documents: docs });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { title, content, category } = body;

    if (!title || !content) {
      return NextResponse.json(
        { success: false, error: "Title and content are required." },
        { status: 400 }
      );
    }

    const clauses = parseContractTextHeuristic(content, title);
    const totalExposure = clauses.reduce((acc, c) => acc + (c.financialImpactUsd || 0), 0);
    const riskScore = Math.min(95, 40 + clauses.length * 15);

    const newDoc: DocumentRecord = {
      id: `doc-${Date.now()}`,
      title,
      category: category || "CUSTOM",
      uploadedAt: new Date().toISOString(),
      rawContent: content,
      riskScore,
      totalFinancialExposure: totalExposure,
      clauses,
      status: "ANALYZED",
    };

    saveDocument(newDoc);

    addAuditLog({
      actionType: "DOC_PARSED",
      summary: `Document Ingested: ${title}`,
      details: `Analyzed ${content.length} characters. Extracted ${clauses.length} clauses. Total financial exposure: $${totalExposure}.`,
      targetId: newDoc.id,
      status: "SUCCESS",
    });

    return NextResponse.json({ success: true, document: newDoc });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}

export async function DELETE(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const id = searchParams.get("id");
    if (!id) {
      return NextResponse.json({ success: false, error: "Document ID required" }, { status: 400 });
    }
    deleteDocument(id);
    addAuditLog({
      actionType: "DOC_UPLOADED",
      summary: `Document Removed: ${id}`,
      details: "Purged document record and associated unsaved clauses.",
      targetId: id,
      status: "INFO",
    });
    return NextResponse.json({ success: true });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
