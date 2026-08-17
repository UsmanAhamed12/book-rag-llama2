import type { ReactNode } from "react";

import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({
  children,
}: AppShellProps) {
  return (
    <div className="relative min-h-screen bg-background text-foreground overflow-hidden">
      {/* Decorative ambient lights */}
      <div className="absolute top-0 left-1/4 -z-10 size-96 rounded-full bg-violet-600/5 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-10 right-1/4 -z-10 size-96 rounded-full bg-indigo-500/5 blur-[120px] pointer-events-none" />
      
      <Sidebar />
      <Header />

      <main className="min-h-screen pt-16 md:pl-64 transition-all duration-300">
        <div className="p-4 md:p-6 max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-2 duration-300">
          {children}
        </div>
      </main>
    </div>
  );
}