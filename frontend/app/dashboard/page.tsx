"use client";

import {
  FileText,
  Loader2,
  MessageSquare,
  Database,
  CheckCircle2,
  AlertCircle,
  Clock,
  ArrowRight,
  TrendingUp,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { AppShell } from "@/components/layout/app-shell";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { getChatSessions } from "@/lib/api/chat";
import { getDocuments } from "@/lib/api/documents";
import type { ChatSession } from "@/lib/types/chat";
import type { Document } from "@/lib/types/document";

export default function DashboardPage() {
  const router = useRouter();

  const [documents, setDocuments] = useState<Document[]>([]);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      router.replace("/login");
      return;
    }

    let cancelled = false;

    async function loadDashboard() {
      try {
        const [documentData, sessionData] = await Promise.all([
          getDocuments(),
          getChatSessions(),
        ]);

        if (cancelled) {
          return;
        }

        setDocuments(documentData);
        setSessions(sessionData);
      } catch {
        if (!cancelled) {
          setError("Unable to load dashboard data.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadDashboard();

    return () => {
      cancelled = true;
    };
  }, [router]);

  const totalChunks = useMemo(
    () => documents.reduce((total, doc) => total + doc.chunks, 0),
    [documents],
  );

  const completedDocuments = useMemo(
    () => documents.filter((doc) => doc.status === "completed").length,
    [documents],
  );

  const ragReady = documents.length > 0 && completedDocuments === documents.length;

  if (loading) {
    return (
      <AppShell>
        <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
          <Loader2 className="size-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground animate-pulse">Loading workspace metrics...</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-8">
        {/* Welcome Section */}
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="font-heading text-3xl font-extrabold tracking-tight text-foreground">
              Welcome back
            </h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Monitor your indexed knowledge bases, start Q&A sessions, and control vector ingestion.
            </p>
          </div>

          <div className="flex gap-2">
            <Link href="/dashboard/documents" passHref>
              <Button variant="outline" className="h-9 gap-2 border-border/40 hover:bg-muted/50 rounded-lg text-xs font-medium">
                <FileText className="size-4 text-violet-500" />
                Upload PDF
              </Button>
            </Link>
            <Link href="/dashboard/chat" passHref>
              <Button className="h-9 gap-2 bg-linear-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white border-0 shadow-lg shadow-indigo-500/20 rounded-lg text-xs font-medium">
                <MessageSquare className="size-4" />
                Start Chatting
              </Button>
            </Link>
          </div>
        </div>

        {error ? (
          <div className="rounded-xl border border-destructive/20 bg-destructive/10 p-4 text-sm text-destructive flex items-center gap-2">
            <AlertCircle className="size-5 shrink-0" />
            <span>{error}</span>
          </div>
        ) : null}

        {/* Stats Grid */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {/* Stat 1: Documents */}
          <Card className="aurora-glow-card glass-panel rounded-xl shadow-lg border border-white/5 relative overflow-hidden group">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Documents
              </span>
              <div className="flex size-8 items-center justify-center rounded-lg bg-violet-500/10 text-violet-400">
                <FileText className="size-4" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold font-heading">{documents.length}</div>
              <div className="mt-1 flex items-center gap-1.5 text-xs text-muted-foreground">
                <span className="inline-flex size-2 rounded-full bg-emerald-500 animate-pulse" />
                <span>{completedDocuments} fully indexed</span>
              </div>
            </CardContent>
          </Card>

          {/* Stat 2: Chats */}
          <Card className="aurora-glow-card glass-panel rounded-xl shadow-lg border border-white/5 relative overflow-hidden group">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Chats Saved
              </span>
              <div className="flex size-8 items-center justify-center rounded-lg bg-indigo-500/10 text-indigo-400">
                <MessageSquare className="size-4" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold font-heading">{sessions.length}</div>
              <div className="mt-1 text-xs text-muted-foreground flex items-center gap-1">
                <TrendingUp className="size-3 text-emerald-500" />
                <span>Saved sessions</span>
              </div>
            </CardContent>
          </Card>

          {/* Stat 3: Indexed Chunks */}
          <Card className="aurora-glow-card glass-panel rounded-xl shadow-lg border border-white/5 relative overflow-hidden group">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Indexed Chunks
              </span>
              <div className="flex size-8 items-center justify-center rounded-lg bg-cyan-500/10 text-cyan-400">
                <Database className="size-4" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold font-heading">
                {totalChunks.toLocaleString()}
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                Embeddings in Vector Database
              </p>
            </CardContent>
          </Card>

          {/* Stat 4: RAG Readiness */}
          <Card className="aurora-glow-card glass-panel rounded-xl shadow-lg border border-white/5 relative overflow-hidden group">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                RAG Engine
              </span>
              {ragReady ? (
                <div className="flex size-8 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400">
                  <CheckCircle2 className="size-4" />
                </div>
              ) : documents.length === 0 ? (
                <div className="flex size-8 items-center justify-center rounded-lg bg-amber-500/10 text-amber-400">
                  <AlertCircle className="size-4" />
                </div>
              ) : (
                <div className="flex size-8 items-center justify-center rounded-lg bg-violet-500/10 text-violet-400">
                  <Clock className="size-4 animate-spin" />
                </div>
              )}
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold font-heading flex items-center gap-2">
                {ragReady ? (
                  <>
                    <span className="inline-flex size-2.5 rounded-full bg-emerald-500 shadow-md shadow-emerald-500/40 animate-ping" />
                    <span>Engine Ready</span>
                  </>
                ) : documents.length === 0 ? (
                  <>
                    <span className="inline-flex size-2.5 rounded-full bg-amber-500" />
                    <span>No Documents</span>
                  </>
                ) : (
                  <>
                    <span className="inline-flex size-2.5 rounded-full bg-violet-500 animate-pulse" />
                    <span>Indexing Files...</span>
                  </>
                )}
              </div>
              <p className="mt-1.5 text-xs text-muted-foreground">
                {ragReady ? "Context retrieval active" : documents.length === 0 ? "Vector store empty" : "Building vector index"}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Sections */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Card: Recent Documents */}
          <Card className="glass-panel border-white/5 shadow-xl rounded-xl">
            <CardHeader className="border-b border-border/40 pb-4 flex flex-row items-center justify-between">
              <div>
                <CardTitle className="text-base font-semibold font-heading">Recent Documents</CardTitle>
                <CardDescription className="text-xs">Your latest vector-embedded source PDFs.</CardDescription>
              </div>
              <Link href="/dashboard/documents" className="text-xs text-primary font-semibold hover:underline flex items-center gap-1">
                <span>View all</span>
                <ArrowRight className="size-3" />
              </Link>
            </CardHeader>

            <CardContent className="pt-4">
              {documents.length === 0 ? (
                <div className="py-8 text-center">
                  <FileText className="mx-auto size-8 text-muted-foreground/40 mb-2" />
                  <p className="text-xs text-muted-foreground">No documents uploaded yet.</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {documents.slice(0, 5).map((doc) => (
                    <div
                      key={doc.id}
                      className="flex items-center justify-between gap-4 rounded-xl border border-border/40 bg-background/30 p-3 hover:bg-muted/30 transition duration-200"
                    >
                      <div className="min-w-0 flex items-center gap-3">
                        <div className="size-8 rounded-lg bg-violet-500/10 text-violet-400 flex items-center justify-center shrink-0">
                          <FileText className="size-4" />
                        </div>
                        <div className="min-w-0">
                          <p className="truncate text-xs font-semibold text-foreground/90">
                            {doc.filename}
                          </p>
                          <p className="text-[10px] text-muted-foreground mt-0.5">
                            {doc.page_count} pages · {doc.chunks} chunks
                          </p>
                        </div>
                      </div>

                      <span className={[
                        "shrink-0 rounded-full px-2.5 py-0.5 text-[10px] font-semibold tracking-wide border",
                        doc.status === "completed" 
                          ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-400"
                          : doc.status === "failed"
                          ? "border-destructive/20 bg-destructive/10 text-destructive"
                          : "border-violet-500/20 bg-violet-500/10 text-violet-400 animate-pulse"
                      ].join(" ")}>
                        {doc.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Card: Recent Conversations */}
          <Card className="glass-panel border-white/5 shadow-xl rounded-xl">
            <CardHeader className="border-b border-border/40 pb-4 flex flex-row items-center justify-between">
              <div>
                <CardTitle className="text-base font-semibold font-heading">Recent Conversations</CardTitle>
                <CardDescription className="text-xs">Your latest RAG active sessions.</CardDescription>
              </div>
              <Link href="/dashboard/chat" className="text-xs text-primary font-semibold hover:underline flex items-center gap-1">
                <span>Open Chat</span>
                <ArrowRight className="size-3" />
              </Link>
            </CardHeader>

            <CardContent className="pt-4">
              {sessions.length === 0 ? (
                <div className="py-8 text-center">
                  <MessageSquare className="mx-auto size-8 text-muted-foreground/40 mb-2" />
                  <p className="text-xs text-muted-foreground">No conversations yet.</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {sessions.slice(0, 5).map((session) => (
                    <button
                      key={session.id}
                      type="button"
                      onClick={() => router.push("/dashboard/chat")}
                      className="flex w-full items-center justify-between gap-4 rounded-xl border border-border/40 bg-background/30 p-3 hover:bg-muted/30 hover:border-primary/30 text-left transition duration-200 group"
                    >
                      <div className="min-w-0 flex items-center gap-3">
                        <div className="size-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center shrink-0">
                          <MessageSquare className="size-4" />
                        </div>
                        <div className="min-w-0">
                          <p className="truncate text-xs font-semibold text-foreground/90 group-hover:text-primary transition-colors">
                            {session.title || "Untitled Conversation"}
                          </p>
                          <p className="text-[10px] text-muted-foreground mt-0.5">
                            Session #{session.id}
                          </p>
                        </div>
                      </div>

                      <ArrowRight className="size-3 text-muted-foreground group-hover:translate-x-1 group-hover:text-primary transition-all" />
                    </button>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
