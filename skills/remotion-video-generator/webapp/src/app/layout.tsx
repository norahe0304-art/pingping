/**
 * [INPUT]: Depends on Next.js App Router runtime and local global stylesheet.
 * [OUTPUT]: Exposes the root HTML shell for all webapp routes.
 * [POS]: webapp/src/app bootstrap layout; imports globals and defines document scaffold.
 * [PROTOCOL]: 变更时更新此头部，然后检查 AGENTS.md
 */
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Remotion Video Generator",
  description: "Gamma-like editor for production-ready video workflows.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
