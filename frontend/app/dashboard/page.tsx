"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { AppShell } from "@/components/layout/app-shell";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DashboardPage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      router.replace("/login");
    }
  }, [router]);

  return (
    <AppShell>
      <div className="mx-auto max-w-5xl">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold tracking-tight">
            Welcome back
          </h2>

          <p className="mt-1 text-muted-foreground">
            Upload documents and start asking questions.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Documents</CardTitle>
              <CardDescription>
                Your indexed PDF library.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <p className="text-3xl font-semibold">
                —
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Chats</CardTitle>
              <CardDescription>
                Your saved conversations.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <p className="text-3xl font-semibold">
                —
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>RAG Status</CardTitle>
              <CardDescription>
                Retrieval system availability.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <p className="font-medium text-foreground">
                Ready
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}