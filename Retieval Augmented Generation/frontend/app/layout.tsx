import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Image Retrieval RAG - Advanced AI-Powered Image Search",
  description: "Retrieval Augmented Generation system for intelligent image search with AI-powered captions and narratives",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-gray-950 min-h-screen">
        {children}
      </body>
    </html>
  );
}
