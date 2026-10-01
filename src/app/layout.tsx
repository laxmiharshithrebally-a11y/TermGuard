import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TermGuard — Autonomous Contract & Deadline Defense",
  description:
    "Protect your commitments from predatory fine print, hidden auto-renewals, 30-day notice traps, and deposit forfeitures with automated 3-stage notice alerts and real SMS delivery.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased selection:bg-indigo-500/20 selection:text-indigo-900">
        {children}
      </body>
    </html>
  );
}
