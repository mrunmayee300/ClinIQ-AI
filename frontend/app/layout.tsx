import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ClinIQ AI",
  description: "AI-assisted clinical reasoning and triage dashboard"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
