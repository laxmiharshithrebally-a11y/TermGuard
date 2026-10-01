import { NextResponse } from "next/server";
import { processAgentChat, AgentChatMessage } from "@/lib/gemini";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { messages, documentContext } = body as {
      messages: AgentChatMessage[];
      documentContext?: string;
    };

    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return NextResponse.json(
        { success: false, error: "Messages array is required." },
        { status: 400 }
      );
    }

    const response = await processAgentChat(messages, documentContext);
    return NextResponse.json({ success: true, message: response });
  } catch (err: any) {
    return NextResponse.json({ success: false, error: err.message }, { status: 500 });
  }
}
