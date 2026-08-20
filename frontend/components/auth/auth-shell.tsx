import { BookOpenCheck, CheckCircle2, Quote } from "lucide-react";
import type { ReactNode } from "react";

type AuthShellProps = {
  eyebrow: string;
  title: string;
  description: string;
  children: ReactNode;
};

const benefits = [
  "Answers grounded only in your selected PDFs",
  "Page-level citations for every supported claim",
  "Private workspaces with saved conversations",
];

export function AuthShell({
  eyebrow,
  title,
  description,
  children,
}: AuthShellProps) {
  return (
    <main className="grid min-h-screen lg:grid-cols-[1.05fr_0.95fr]">
      <section className="relative hidden overflow-hidden border-r border-border bg-slate-950 p-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="auth-grid absolute inset-0 opacity-40" aria-hidden="true" />
        <div className="absolute -left-32 top-20 size-96 rounded-full bg-indigo-500/20 blur-3xl" />
        <div className="relative z-10 flex items-center gap-3">
          <span className="flex size-10 items-center justify-center rounded-xl bg-white text-slate-950">
            <BookOpenCheck className="size-5" />
          </span>
          <div>
            <p className="text-sm font-semibold">Book RAG</p>
            <p className="text-xs text-slate-400">Your books, made searchable</p>
          </div>
        </div>

        <div className="relative z-10 max-w-xl">
          <p className="mb-4 text-sm font-medium text-indigo-300">
            Evidence-first research
          </p>
          <h2 className="max-w-lg text-4xl font-semibold leading-tight tracking-tight xl:text-5xl">
            Turn dense documents into clear, cited answers.
          </h2>
          <ul className="mt-10 space-y-4">
            {benefits.map((benefit) => (
              <li key={benefit} className="flex items-center gap-3 text-sm text-slate-300">
                <CheckCircle2 className="size-4 text-indigo-300" />
                {benefit}
              </li>
            ))}
          </ul>
        </div>

        <blockquote className="relative z-10 max-w-lg rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur">
          <Quote className="mb-3 size-5 text-indigo-300" />
          <p className="text-sm leading-6 text-slate-300">
            Built for careful readers who want useful answers without losing the
            source behind them.
          </p>
        </blockquote>
      </section>

      <section className="flex min-h-screen items-center justify-center px-5 py-12 sm:px-10">
        <div className="w-full max-w-md">
          <div className="mb-8 lg:hidden">
            <div className="mb-6 flex items-center gap-3">
              <span className="flex size-10 items-center justify-center rounded-xl bg-primary text-primary-foreground">
                <BookOpenCheck className="size-5" />
              </span>
              <span className="font-semibold">Book RAG</span>
            </div>
          </div>
          <p className="text-sm font-medium text-primary">{eyebrow}</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">{title}</h1>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">
            {description}
          </p>
          <div className="mt-8">{children}</div>
        </div>
      </section>
    </main>
  );
}
