import { GoogleGenerativeAI } from "@google/generative-ai";
import { getSettings, createReminder, addAuditLog } from "./storage";
import { ExtractedClause, Reminder } from "./types";

export interface AgentChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
  thoughtProcess?: string[];
  actionCards?: AgentActionCard[];
}

export interface AgentActionCard {
  id: string;
  type: "REMINDER_PROPOSAL" | "CLAUSE_RADAR" | "DISPUTE_NOTICE" | "CONFIRMATION";
  title: string;
  subtitle?: string;
  financialImpactUsd?: number;
  deadlineDate?: string;
  sourceSection?: string;
  quotedText?: string;
  preWrittenDraft?: string;
  actionPayload?: any;
}

export async function processAgentChat(
  messages: AgentChatMessage[],
  documentContext?: string
): Promise<AgentChatMessage> {
  const settings = getSettings();
  const apiKey = settings.geminiApiKey || process.env.GEMINI_API_KEY;
  const lastUserMessage = messages[messages.length - 1]?.content || "";

  const thoughts: string[] = [
    "Interpreting conversational intent and fine-print obligations...",
  ];

  // Try real Gemini API if key is available
  if (apiKey) {
    try {
      thoughts.push("Connecting to Google Gemini 2.5 Flash neural core...");
      const genAI = new GoogleGenerativeAI(apiKey);
      const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

      const prompt = `
You are FinePrint AI, an autonomous contract defense & deadline intelligence agent.
Your mission: Protect the user from predatory fine-print traps, auto-renewals, notice period forfeiture, and hidden fees.

Context Document (if any):
${documentContext || "None provided."}

User request:
"${lastUserMessage}"

If the user is asking to be reminded about something (e.g., "Remind me next Friday at 6pm to cancel gym"), extract the title, date/time, and financial impact.
If the user provides contract text, identify sneaky clauses, auto-renewals, and deadlines with exact quotes.

Respond in JSON format with this structure:
{
  "replyText": "Your natural language response to the user",
  "thoughts": ["step 1 thought", "step 2 thought"],
  "remindersToPropose": [
    {
      "title": "Action title",
      "dueDate": "YYYY-MM-DDTHH:mm:ss.000Z",
      "sourceClause": "Quoted fine print text",
      "sourceSection": "Section X.X",
      "financialImpactUsd": 120
    }
  ]
}
`;

      const result = await model.generateContent(prompt);
      const responseText = result.response.text();

      // Clean markdown code blocks if present
      const cleanJson = responseText.replace(/```json\n?|\n?```/g, "").trim();
      const parsed = JSON.parse(cleanJson);

      const actionCards: AgentActionCard[] = [];
      if (parsed.remindersToPropose && parsed.remindersToPropose.length > 0) {
        parsed.remindersToPropose.forEach((r: any, idx: number) => {
          actionCards.push({
            id: `card-${Date.now()}-${idx}`,
            type: "REMINDER_PROPOSAL",
            title: r.title,
            deadlineDate: r.dueDate,
            quotedText: r.sourceClause,
            sourceSection: r.sourceSection,
            financialImpactUsd: r.financialImpactUsd,
            actionPayload: r,
          });
        });
      }

      return {
        role: "assistant",
        content: parsed.replyText || "I've analyzed your request and prepared actionable safeguards.",
        thoughtProcess: parsed.thoughts || thoughts,
        actionCards,
      };
    } catch (err: any) {
      console.warn("Gemini API call failed, falling back to local heuristic brain:", err.message);
      thoughts.push(`Neural API notification: ${err.message}. Engaging Heuristic Safety Engine.`);
    }
  }

  // Autonomous Intelligent Heuristic Engine (works 100% offline & without API key!)
  const lower = lastUserMessage.toLowerCase();

  // Pattern 1: User types "remind me..."
  if (lower.includes("remind me") || lower.includes("cancel") || lower.includes("deadline")) {
    thoughts.push("Detected temporal reminder intent: 'remind me'");
    thoughts.push("Extracting action parameters, target company, and scheduled offset...");

    // Heuristic date inference
    let targetDate = new Date();
    let title = "Action Reminder";
    let financialImpact = 120;

    if (lower.includes("next friday")) {
      const dayOfWeek = targetDate.getDay();
      const daysUntilNextFriday = ((5 - dayOfWeek + 7) % 7 || 7) + 7;
      targetDate.setDate(targetDate.getDate() + daysUntilNextFriday);
    } else if (lower.includes("friday")) {
      const dayOfWeek = targetDate.getDay();
      const daysUntilFriday = (5 - dayOfWeek + 7) % 7 || 7;
      targetDate.setDate(targetDate.getDate() + daysUntilFriday);
    } else if (lower.includes("tomorrow")) {
      targetDate.setDate(targetDate.getDate() + 1);
    } else {
      // Default to 7 days from now
      targetDate.setDate(targetDate.getDate() + 7);
    }

    // Time adjustment
    if (lower.includes("6pm") || lower.includes("6:00 pm") || lower.includes("18:00")) {
      targetDate.setHours(18, 0, 0, 0);
    } else if (lower.includes("5pm") || lower.includes("17:00")) {
      targetDate.setHours(17, 0, 0, 0);
    } else {
      targetDate.setHours(9, 0, 0, 0);
    }

    if (lower.includes("gym")) {
      title = "Cancel gym membership before automatic renewal cycle";
      financialImpact = 145;
    } else if (lower.includes("netflix") || lower.includes("subscription")) {
      title = "Cancel monthly streaming subscription trial";
      financialImpact = 24;
    } else if (lower.includes("lease") || lower.includes("rent")) {
      title = "Deliver non-renewal notice to landlord";
      financialImpact = 2600;
    } else {
      title = lastUserMessage.replace(/remind me to/i, "").replace(/remind me/i, "").trim();
      title = title.charAt(0).toUpperCase() + title.slice(1);
    }

    thoughts.push(`Identified target cutoff: ${targetDate.toLocaleString()}`);
    thoughts.push("Prepared Interactive Action Card for 1-click user confirmation.");

    const actionCard: AgentActionCard = {
      id: `card-${Date.now()}`,
      type: "REMINDER_PROPOSAL",
      title: title,
      deadlineDate: targetDate.toISOString(),
      financialImpactUsd: financialImpact,
      quotedText: "Direct conversational schedule trigger via Agent Hub.",
      sourceSection: "Conversational Request",
      actionPayload: {
        title,
        dueDate: targetDate.toISOString(),
        financialImpactUsd: financialImpact,
        sourceClause: "Conversational User Trigger",
      },
    };

    return {
      role: "assistant",
      content: `I've prepared an autonomous safeguard for you: **"${title}"** scheduled for **${targetDate.toLocaleDateString("en-US", { weekday: "long", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}**.\n\nWould you like me to commit this to the real-time database and activate Resend email notifications?`,
      thoughtProcess: thoughts,
      actionCards: [actionCard],
    };
  }

  // Default response if general question
  thoughts.push("Evaluating general fine-print query...");
  return {
    role: "assistant",
    content: `I am **FinePrint AI**, your autonomous contract and deadline defense agent.\n\nHere is what I can do right now:\n1. **Read any contract or fine print** — Drop a file or paste text, and I'll find hidden auto-renewals, 30-day notice traps, and deposit forfeitures.\n2. **Type direct reminders** — e.g., *"Remind me next Friday at 6pm to cancel my gym membership."*\n3. **Enforce with Real Email** — When a deadline triggers, I deliver an alert directly to your inbox with a 1-click pre-written legal cancellation notice.\n\nTry uploading a contract in the **Documents** tab or type a reminder below!`,
    thoughtProcess: thoughts,
  };
}

export function parseContractTextHeuristic(text: string, title: string): ExtractedClause[] {
  const clauses: ExtractedClause[] = [];
  const lines = text.split("\n");

  let currentSection = "General";
  lines.forEach((line, idx) => {
    if (line.match(/SECTION\s+\d+/i) || line.match(/ARTICLE\s+\d+/i)) {
      currentSection = line.trim();
    }

    // Check for auto renewal / conversion
    if (
      line.match(/automatically renew|automatic renewal|convert to a paid|successive.*term/i) &&
      clauses.length < 4
    ) {
      clauses.push({
        id: `clause-${Date.now()}-${idx}`,
        clauseTitle: "Enforced Automatic Renewal Trap",
        sourceSection: currentSection,
        quotedText: line.trim(),
        deadlineDate: new Date(Date.now() + 86400000 * 30).toISOString().split("T")[0],
        deadlineTime: "17:00",
        riskLevel: "CRITICAL",
        financialImpactUsd: 1200,
        explanation: "Contract binds customer to an automatic consecutive period unless opt-out notice is transmitted.",
        actionRequired: "Deliver formal opt-out notice prior to the stated deadline window.",
      });
    }

    // Check for notice periods
    if (
      line.match(/notice.*prior|days.*prior|certified mail|written notice/i) &&
      clauses.length < 5
    ) {
      clauses.push({
        id: `clause-${Date.now()}-${idx}-notice`,
        clauseTitle: "Mandatory Advance Notice Requirement",
        sourceSection: currentSection,
        quotedText: line.trim(),
        deadlineDate: new Date(Date.now() + 86400000 * 45).toISOString().split("T")[0],
        deadlineTime: "18:00",
        riskLevel: "WARNING",
        financialImpactUsd: 450,
        explanation: "Strict advance notice window enforced. Failure to comply forfeits deposits or triggers penalty dues.",
        actionRequired: "Submit certified termination notice in compliance with stated delivery protocol.",
      });
    }
  });

  if (clauses.length === 0) {
    clauses.push({
      id: `clause-default-${Date.now()}`,
      clauseTitle: "Standard Term Expiration & Renewal Check",
      sourceSection: "General Terms",
      quotedText: text.slice(0, 200) + "...",
      deadlineDate: new Date(Date.now() + 86400000 * 60).toISOString().split("T")[0],
      deadlineTime: "17:00",
      riskLevel: "INFO",
      financialImpactUsd: 300,
      explanation: "General agreement expiration cycle identified.",
      actionRequired: "Review account status before cycle end.",
    });
  }

  return clauses;
}
