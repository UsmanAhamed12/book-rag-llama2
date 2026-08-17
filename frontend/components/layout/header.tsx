"use client";

import { LogOut, User, Menu } from "lucide-react";
import { useRouter, usePathname } from "next/navigation";

import { Button } from "@/components/ui/button";

export function Header() {
  const router = useRouter();
  const pathname = usePathname();

  function handleLogout() {
    localStorage.removeItem("access_token");
    router.replace("/login");
  }

  // Dynamic titles based on current route
  const getHeaderDetails = () => {
    if (pathname.includes("/dashboard/chat")) {
      return {
        title: "RAG AI Chat",
        description: "Intelligent Q&A grounded in your custom documents",
      };
    }
    if (pathname.includes("/dashboard/documents")) {
      return {
        title: "Document Indexer",
        description: "Upload and manage indexed PDF source files",
      };
    }
    return {
      title: "Workspace Dashboard",
      description: "Overview of your files, chats, and indexing status",
    };
  };

  const { title, description } = getHeaderDetails();

  return (
    <header className="fixed left-0 right-0 top-0 z-30 flex h-16 items-center justify-between border-b border-border/40 bg-background/80 px-6 backdrop-blur-md md:left-64">
      <div className="flex items-center gap-3">
        {/* Mobile menu trigger can be implemented here if needed, keeping simple for now */}
        <div>
          <h1 className="font-heading font-semibold text-sm md:text-base leading-none tracking-tight">
            {title}
          </h1>
          <p className="mt-1 text-[10px] md:text-xs text-muted-foreground hidden sm:block">
            {description}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden items-center gap-2 rounded-full bg-muted/50 px-3 py-1.5 text-xs font-medium text-muted-foreground sm:flex border border-border/40">
          <User className="size-3.5 text-primary" />
          <span>Account</span>
        </div>

        <Button
          variant="ghost"
          size="icon"
          onClick={handleLogout}
          aria-label="Logout"
          className="size-8 rounded-lg hover:bg-destructive/10 hover:text-destructive transition-colors"
        >
          <LogOut className="size-4" />
        </Button>
      </div>
    </header>
  );
}