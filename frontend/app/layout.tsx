import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navigation } from "@/components/Navigation";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "NutriTrack",
  description: "Modern Calorie Tracker",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-slate-50 text-slate-900 pb-20 pt-16`}>
        <Navigation />
        <main className="max-w-screen-md mx-auto pt-8 px-4">
          {children}
        </main>
      </body>
    </html>
  );
}
