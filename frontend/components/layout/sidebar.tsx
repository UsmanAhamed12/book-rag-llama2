"use client";

import {
  BookOpen,
  FileText,
  MessageSquare,
  Plus,
  Settings,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

export function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    {
      href: "/dashboard/chat",
      label: "Chats",
      icon: MessageSquare,
    },
    {
      href: "/dashboard/documents",
      label: "Documents",
      icon: FileText,
    },
  ];

  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 flex-col border-r border-border bg-sidebar md:flex">
      <div className="flex h-16 items-center gap-3 px-6">
        <div className="flex size-9 items-center justify-center rounded-xl bg-gradient-to-tr from-violet-600 to-indigo-600 text-white shadow-lg shadow-indigo-500/20">
          <BookOpen className="size-5 animate-pulse" />
        </div>

        <div>
          <p className="font-heading font-semibold text-sm tracking-tight bg-gradient-to-r from-white via-indigo-200 to-indigo-100 bg-clip-text text-transparent">
            Book RAG
          </p>
          <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
            AI Assistant
          </p>
        </div>
      </div>

      <Separator className="opacity-40" />

      <div className="p-4">
        <Link
          href="/dashboard/chat"
          className="flex h-9 w-full items-center justify-start gap-2 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 px-4 text-xs font-semibold text-white shadow-lg shadow-indigo-500/20 hover:from-violet-500 hover:to-indigo-500 hover:scale-[1.01] transition-all"
        >
          <Plus className="size-4" />
          <span>New Chat</span>
        </Link>
      </div>

      <nav className="flex-1 space-y-1 px-3">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={[
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all duration-200",
                isActive
                  ? "bg-primary/10 text-primary shadow-inner border-l-2 border-primary pl-[10px]"
                  : "text-muted-foreground hover:bg-muted/50 hover:text-foreground",
              ].join(" ")}
            >
              <Icon className={["size-4 transition-transform", isActive ? "scale-110 text-primary" : ""].join(" ")} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-border/40 p-3">
        <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground transition hover:bg-muted/50 hover:text-foreground">
          <Settings className="size-4" />
          Settings
        </button>
      </div>
    </aside>
  );
}