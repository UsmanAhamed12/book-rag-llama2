import { Plus } from "lucide-react";
import Link from "next/link";

import { Brand } from "@/components/layout/brand";
import { Navigation } from "@/components/layout/navigation";

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 flex-col border-r border-border/80 bg-sidebar/95 px-4 backdrop-blur md:flex">
      <div className="flex h-20 items-center px-2">
        <Brand />
      </div>

      <div className="pb-5 pt-1">
        <Link
          href="/dashboard/chat"
          className="flex h-10 w-full items-center justify-center gap-2 rounded-xl bg-primary px-4 text-sm font-medium text-primary-foreground shadow-sm transition hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <Plus className="size-4" />
          <span>Start a conversation</span>
        </Link>
      </div>

      <div className="flex-1">
        <Navigation />
      </div>

      <div className="mb-4 rounded-xl border border-border/70 bg-muted/40 p-3">
        <p className="text-xs font-medium">Evidence-first answers</p>
        <p className="mt-1 text-[11px] leading-4 text-muted-foreground">
          Every response stays grounded in your selected library.
        </p>
      </div>
    </aside>
  );
}
