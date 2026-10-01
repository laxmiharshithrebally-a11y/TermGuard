import { DocumentRecord } from "./types";

export const SAMPLE_CONTRACTS: DocumentRecord[] = [
  {
    id: "doc-gym-001",
    title: "Cult.fit & Gold's Gym — Annual Fitness Pass Agreement",
    category: "SUBSCRIPTION",
    uploadedAt: new Date(Date.now() - 86400000 * 2).toISOString(),
    riskScore: 85,
    totalFinancialExposure: 29990,
    status: "ANALYZED",
    rawContent: `CULT.FIT & GOLD'S FITNESS CLUB — ANNUAL MEMBERSHIP AGREEMENT
MEMBER NAME: Harshith R.
CITY: Bangalore / Hyderabad, India
MEMBERSHIP TYPE: All-Access Elite Annual Pass
START DATE: October 15, 2025

SECTION 1: ANNUAL MEMBERSHIP & FEES
1.1 The Member agrees to an annual 12-month membership for a total fee of ₹29,990 INR (inclusive of 18% GST).
1.2 Monthly installment equivalent equals ₹2,499 INR per month.

SECTION 4: AUTOMATIC CARD RENEWAL (IMPORTANT TRAP)
4.1 On October 14, 2026, this annual pass shall automatically renew for another full 12 months at the standard rate of ₹32,000 INR.
4.2 Auto-debit will be charged directly to your saved UPI / credit card without sending any separate OTP or warning message.
4.3 TO CANCEL AUTO-RENEWAL: You must submit a written cancellation request at least 30 days before renewal (DEADLINE: SEPTEMBER 14, 2026). Late cancellations will not be refunded.

SECTION 7: REFUND & CANCELLATION RESTRICTIONS
7.1 Membership fees once debited are strictly non-refundable under any circumstance.
7.2 If cancellation is not submitted before September 14, 2026, the full ₹32,000 INR will be debited for the next year.`,
    clauses: [
      {
        id: "clause-gym-1",
        clauseTitle: "30-Day Prior Cancellation Cutoff (Auto-Debit Trap)",
        sourceSection: "Section 4.3 & Section 7.2",
        quotedText:
          "TO CANCEL AUTO-RENEWAL: You must submit a written cancellation request at least 30 days before renewal (DEADLINE: SEPTEMBER 14, 2026). Late cancellations will not be refunded.",
        deadlineDate: "2026-09-14",
        deadlineTime: "18:00",
        riskLevel: "CRITICAL",
        financialImpactUsd: 32000,
        explanation:
          "If you do not cancel before September 14, they will automatically charge ₹32,000 to your credit card / UPI for another full year with zero refund.",
        actionRequired: "Submit cancellation request to gym support before September 14, 2026.",
      },
      {
        id: "clause-gym-2",
        clauseTitle: "Price Increase Upon Renewal (+₹2,010)",
        sourceSection: "Section 4.1",
        quotedText:
          "this annual pass shall automatically renew for another full 12 months at the standard rate of ₹32,000 INR.",
        deadlineDate: "2026-10-14",
        deadlineTime: "23:59",
        riskLevel: "WARNING",
        financialImpactUsd: 2010,
        explanation:
          "The annual fee silently jumps from ₹29,990 to ₹32,000 when it renews automatically.",
        actionRequired: "Review your membership plan before initial term ends.",
      },
    ],
  },
  {
    id: "doc-lease-002",
    title: "2BHK Apartment Rental Agreement (Flat 402, Green Glen Layout, Bangalore)",
    category: "LEASE",
    uploadedAt: new Date(Date.now() - 86400000 * 5).toISOString(),
    riskScore: 78,
    totalFinancialExposure: 70000,
    status: "ANALYZED",
    rawContent: `HOUSE RENT AGREEMENT (RESIDENTIAL LEASE)
PREMISES: Flat No. 402, 4th Floor, Green Glen Layout, Bellandur, Bangalore - 560103
LANDLORD: V. Narayana Rao
TENANT: Harshith R.
MONTHLY RENT: ₹35,000 INR per month
SECURITY DEPOSIT: ₹1,50,000 INR (Rupees One Lakh Fifty Thousand)
LEASE PERIOD: July 1, 2025 to June 30, 2026

SECTION 3: SECURITY DEPOSIT & FORFEITURE PENALTY
3.1 The Tenant has paid a refundable interest-free security deposit of ₹1,50,000 INR to the Landlord.
3.2 MANDATORY 2-MONTH NOTICE PERIOD: Either party must give two (2) full months written notice before vacating the flat (DEADLINE: APRIL 30, 2026).
3.3 PENALTY CLAUSE: If the Tenant fails to give full 2 months notice in writing before vacating, Landlord will forfeit two months of rent (₹70,000 INR) directly from the security deposit.

SECTION 6: PAINTING & CLEANING CHARGES
6.1 A fixed deduction of one month rent (₹35,000 INR) will be deducted from deposit towards repainting and deep cleaning upon handover.`,
    clauses: [
      {
        id: "clause-lease-1",
        clauseTitle: "2-Month Move-Out Notice (₹70,000 Deposit Forfeiture Trap)",
        sourceSection: "Section 3.2 & Section 3.3",
        quotedText:
          "Either party must give two (2) full months written notice before vacating the flat (DEADLINE: APRIL 30, 2026)... Landlord will forfeit two months of rent (₹70,000 INR) directly from the security deposit.",
        deadlineDate: "2026-04-30",
        deadlineTime: "18:00",
        riskLevel: "CRITICAL",
        financialImpactUsd: 70000,
        explanation:
          "If you do not give written notice to the landlord by April 30, the landlord will legally cut ₹70,000 from your security deposit.",
        actionRequired: "Send official written move-out notice to landlord on WhatsApp & Email before April 30, 2026.",
      },
      {
        id: "clause-lease-2",
        clauseTitle: "Fixed Painting & Cleaning Deduction (₹35,000)",
        sourceSection: "Section 6.1",
        quotedText:
          "A fixed deduction of one month rent (₹35,000 INR) will be deducted from deposit towards repainting and deep cleaning upon handover.",
        deadlineDate: "2026-06-15",
        deadlineTime: "12:00",
        riskLevel: "WARNING",
        financialImpactUsd: 35000,
        explanation:
          "Landlord will automatically deduct ₹35,000 from your deposit unless inspected and agreed upon in advance.",
        actionRequired: "Schedule a flat inspection with landlord 15 days before leaving.",
      },
    ],
  },
  {
    id: "doc-saas-003",
    title: "Zoho / AWS Cloud Services India — Annual Business Plan",
    category: "SUBSCRIPTION",
    uploadedAt: new Date(Date.now() - 86400000 * 10).toISOString(),
    riskScore: 65,
    totalFinancialExposure: 48000,
    status: "ANALYZED",
    rawContent: `BUSINESS CLOUD SOFTWARE & HOSTING SERVICES AGREEMENT
CUSTOMER: TechVentures India Pvt Ltd
SERVICE: Business Enterprise Suite
ANNUAL COST: ₹48,000 INR per year (billed annually)
EXPIRY DATE: November 30, 2026

SECTION 5: AUTO-RENEWAL & NOTICE PERIOD
5.1 This business subscription will automatically renew on December 1, 2026 for another full 12-month period at ₹48,000 INR.
5.2 To stop auto-renewal, the customer must submit an opt-out cancellation ticket at least 30 days in advance (DEADLINE: OCTOBER 31, 2026).
5.3 Any cancellation submitted after October 31 will be rejected, and the full ₹48,000 INR will be debited.`,
    clauses: [
      {
        id: "clause-saas-1",
        clauseTitle: "30-Day Prior Opt-Out Window (₹48,000 Lock-in)",
        sourceSection: "Section 5.2 & Section 5.3",
        quotedText:
          "To stop auto-renewal, the customer must submit an opt-out cancellation ticket at least 30 days in advance (DEADLINE: OCTOBER 31, 2026). Any cancellation submitted after October 31 will be rejected, and the full ₹48,000 INR will be debited.",
        deadlineDate: "2026-10-31",
        deadlineTime: "23:59",
        riskLevel: "CRITICAL",
        financialImpactUsd: 48000,
        explanation:
          "If you miss October 31 by even 1 day, you will be locked into paying ₹48,000 for another whole year.",
        actionRequired: "Submit opt-out ticket to support before October 31, 2026.",
      },
    ],
  },
];
