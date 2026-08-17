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
    <div className="min-h-screen bg-muted/20">
      <Sidebar />
      <Header />

      <main className="min-h-screen pt-16 md:pl-64">
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  );
}