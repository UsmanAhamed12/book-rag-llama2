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
    <div className="min-h-screen bg-background text-foreground">
      <Sidebar />
      <Header />

      <main className="min-h-screen pt-16 md:pl-64">
        <div className="mx-auto max-w-[90rem] p-4 sm:p-6 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
