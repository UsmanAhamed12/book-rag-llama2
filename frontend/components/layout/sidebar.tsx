"use client";

import {
  BookOpen,
  FileText,
  MessageSquare,
  Plus,
  Settings,
} from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 border-r bg-background md:flex md:flex-col">
      <div className="flex h-16 items-center gap-3 px-6">
        <div className="flex size-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <BookOpen className="size-5" />
        </div>

        <div>
          <p className="font-semibold">Book RAG</p>
          <p className="text-xs text-muted-foreground">
            AI Assistant
          </p>
        </div>
      </div>

      <Separator />

      <div className="p-4">
        <Button className="w-full justify-start gap-2">
          <Plus className="size-4" />
          New Chat
        </Button>
      </div>

      <nav className="flex-1 space-y-1 px-3">
        <Link
            href="/dashboard/chat"
            className="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground transition hover:bg-muted hover:text-foreground"
            >
            <MessageSquare className="size-4" />
            Chats
        </Link>

        <Link
          href="/dashboard/documents"
          className="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground transition hover:bg-muted hover:text-foreground"
        >
          <FileText className="size-4" />
          Documents
        </Link>
      </nav>

      <div className="border-t p-3">
        <button className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground transition hover:bg-muted hover:text-foreground">
          <Settings className="size-4" />
          Settings
        </button>
      </div>
    </aside>
  );
}