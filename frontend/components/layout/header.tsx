"use client";

import { LogOut, User } from "lucide-react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";

export function Header() {
  const router = useRouter();

  function handleLogout() {
    localStorage.removeItem("access_token");
    router.replace("/login");
  }

  return (
    <header className="fixed left-0 right-0 top-0 z-30 flex h-16 items-center justify-between border-b bg-background/95 px-6 backdrop-blur md:left-64">
      <div>
        <h1 className="font-semibold">
          Book RAG Assistant
        </h1>
        <p className="text-xs text-muted-foreground">
          Chat with your documents
        </p>
      </div>

      <div className="flex items-center gap-2">
        <div className="hidden items-center gap-2 text-sm text-muted-foreground sm:flex">
          <User className="size-4" />
          Account
        </div>

        <Button
          variant="ghost"
          size="icon"
          onClick={handleLogout}
          aria-label="Logout"
        >
          <LogOut className="size-4" />
        </Button>
      </div>
    </header>
  );
}