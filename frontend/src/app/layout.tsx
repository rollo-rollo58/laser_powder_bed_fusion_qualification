import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LPBF | Build Qualification Workbench",
  description: "Research-only powder-bed fusion process diagnostics and qualification",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen font-sans antialiased">{children}</body>
    </html>
  );
}
