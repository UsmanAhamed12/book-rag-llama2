import type { Metadata } from "next";
import { ThemeProvider } from "@/components/theme-provider";
import { Toaster } from "@/components/ui/sonner";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000",
  ),
  title: {
    default: "Book RAG — Grounded answers from your documents",
    template: "%s · Book RAG",
  },
  description:
    "Upload PDF books, ask natural-language questions, and get evidence-backed answers with page-level citations.",
  openGraph: {
    title: "Book RAG — Grounded answers from your documents",
    description: "Grounded answers. Page-level proof.",
    images: [{ url: "/og.png", width: 1200, height: 630, alt: "Book RAG" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Book RAG — Grounded answers from your documents",
    description: "Grounded answers. Page-level proof.",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
      suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col">
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster richColors position="top-right" />
        </ThemeProvider>
      </body>
    </html>
  );
}
