"use client";

import { LogOut, Menu, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useRouter, usePathname } from "next/navigation";
import { useState } from "react";

import { Brand } from "@/components/layout/brand";
import { Navigation } from "@/components/layout/navigation";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

export function Header() {
  const router = useRouter();
  const pathname = usePathname();
  const { resolvedTheme, setTheme } = useTheme();
  const [mobileOpen, setMobileOpen] = useState(false);

  function handleLogout() {
    localStorage.removeItem("access_token");
    router.replace("/login");
  }

  // Dynamic titles based on current route
  const getHeaderDetails = () => {
    if (pathname.includes("/dashboard/chat")) {
      return {
        title: "Ask your books",
        description: "Grounded answers with page-level citations",
      };
    }
    if (pathname.includes("/dashboard/documents")) {
      return {
        title: "Document library",
        description: "Upload and manage your searchable PDF collection",
      };
    }
    return {
      title: "Workspace overview",
      description: "Your library, conversations, and retrieval readiness",
    };
  };

  const { title, description } = getHeaderDetails();

  return (
    <header className="fixed left-0 right-0 top-0 z-30 flex h-16 items-center justify-between border-b border-border/70 bg-background/90 px-4 backdrop-blur-xl sm:px-6 md:left-64">
      <div className="flex items-center gap-3">
        <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
          <SheetTrigger
            render={
              <Button
                variant="ghost"
                size="icon"
                className="md:hidden"
                aria-label="Open navigation"
              />
            }
          >
            <Menu className="size-5" />
          </SheetTrigger>
          <SheetContent side="left" className="w-[19rem] p-5">
            <SheetHeader className="p-0">
              <SheetTitle className="sr-only">Workspace navigation</SheetTitle>
              <SheetDescription className="sr-only">
                Navigate between your dashboard, chat, and document library.
              </SheetDescription>
              <Brand />
            </SheetHeader>
            <div className="mt-6">
              <Navigation onNavigate={() => setMobileOpen(false)} />
            </div>
          </SheetContent>
        </Sheet>
        <div>
          <h1 className="text-sm font-semibold leading-none tracking-tight sm:text-base">
            {title}
          </h1>
          <p className="mt-1 hidden text-xs text-muted-foreground sm:block">
            {description}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
          aria-label={`Switch to ${resolvedTheme === "dark" ? "light" : "dark"} theme`}
        >
          {resolvedTheme === "dark" ? (
            <Sun className="size-4" />
          ) : (
            <Moon className="size-4" />
          )}
        </Button>

        <Button
          variant="ghost"
          size="icon"
          onClick={handleLogout}
          aria-label="Sign out"
          title="Sign out"
          className="hover:bg-destructive/10 hover:text-destructive"
        >
          <LogOut className="size-4" />
        </Button>
      </div>
    </header>
  );
}
