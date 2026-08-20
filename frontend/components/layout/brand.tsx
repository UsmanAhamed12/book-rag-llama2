import { BookOpenText } from "lucide-react";
import Link from "next/link";

type BrandProps = {
  compact?: boolean;
};

export function Brand({ compact = false }: BrandProps) {
  return (
    <Link
      href="/dashboard"
      className="group inline-flex items-center gap-3 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      aria-label="Book RAG dashboard"
    >
      <span className="flex size-9 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-sm transition-transform group-hover:-rotate-3">
        <BookOpenText className="size-4.5" />
      </span>
      {!compact ? (
        <span className="min-w-0">
          <span className="block text-sm font-semibold tracking-tight">Book RAG</span>
          <span className="block text-[11px] text-muted-foreground">
            Grounded knowledge
          </span>
        </span>
      ) : null}
    </Link>
  );
}
