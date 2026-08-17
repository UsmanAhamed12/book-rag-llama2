"use client";

import {
  FileText,
  Loader2,
  MessageSquare,
  MoreHorizontal,
  Pencil,
  Plus,
  Send,
  Trash2,
  BookOpen,
  Database,
  Layers,
  Sparkles,
} from "lucide-react";
import { FormEvent, useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { MarkdownMessage } from "@/components/chat/markdown-message";
import { AppShell } from "@/components/layout/app-shell";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Input } from "@/components/ui/input";

import {
  createChatSession,
  deleteChatSession,
  getChatMessages,
  getChatSessions,
  renameChatSession,
  sendChatMessage,
} from "@/lib/api/chat";
import { getDocuments } from "@/lib/api/documents";

import type { ChatMessage, ChatSession } from "@/lib/types/chat";
import type { Document } from "@/lib/types/document";

export default function ChatPage() {
  const router = useRouter();

  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedDocumentIds, setSelectedDocumentIds] = useState<number[]>([]);
  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [creatingChat, setCreatingChat] = useState(false);
  const [error, setError] = useState("");

  const [renameSessionId, setRenameSessionId] = useState<number | null>(null);
  const [renameTitle, setRenameTitle] = useState<string>("");
  const [renaming, setRenaming] = useState(false);
  const [deletingSessionId, setDeletingSessionId] = useState<number | null>(null);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      router.replace("/login");
      return;
    }

    let cancelled = false;

    async function initializePage() {
      try {
        const [sessionData, documentData] = await Promise.all([
          getChatSessions(),
          getDocuments(),
        ]);

        if (cancelled) return;

        setSessions(sessionData);
        setDocuments(documentData);

        // Auto-select all documents by default
        setSelectedDocumentIds(documentData.map((doc) => doc.id));

        if (sessionData.length > 0) {
          const firstSessionId = sessionData[0].id;
          setActiveSessionId(firstSessionId);
          const messageData = await getChatMessages(firstSessionId);

          if (!cancelled) {
            setMessages(messageData);
          }
        }
      } catch {
        if (!cancelled) {
          setError("Unable to load chat data.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void initializePage();

    return () => {
      cancelled = true;
    };
  }, [router]);

  async function handleNewChat() {
    setCreatingChat(true);
    setError("");

    try {
      const session = await createChatSession();
      setSessions((current) => [session, ...current]);
      setActiveSessionId(session.id);
      setMessages([]);
      setQuestion("");
    } catch {
      setError("Unable to create a new chat.");
    } finally {
      setCreatingChat(false);
    }
  }

  async function handleSelectSession(sessionId: number) {
    if (sessionId === activeSessionId) return;

    setActiveSessionId(sessionId);
    setError("");
    setMessages([]);

    try {
      const data = await getChatMessages(sessionId);
      setMessages(data);
    } catch {
      setError("Unable to load this conversation.");
    }
  }

  function toggleDocument(documentId: number) {
    setSelectedDocumentIds((current) =>
      current.includes(documentId)
        ? current.filter((id) => id !== documentId)
        : [...current, documentId]
    );
  }

  function selectAllDocuments() {
    setSelectedDocumentIds(documents.map((doc) => doc.id));
  }

  function clearDocuments() {
    setSelectedDocumentIds([]);
  }

  function openRenameDialog(session: ChatSession) {
    setRenameSessionId(session.id);
    setRenameTitle(session.title ?? "New Chat");
  }

  function closeRenameDialog() {
    setRenameSessionId(null);
    setRenameTitle("");
  }

  async function handleRenameSession() {
    if (renameSessionId === null) return;

    const title = renameTitle.trim();
    if (!title) {
      setError("Chat title cannot be empty.");
      return;
    }

    setRenaming(true);
    setError("");

    try {
      const updatedSession = await renameChatSession(renameSessionId, { title });
      setSessions((current) =>
        current.map((session) =>
          session.id === updatedSession.id ? updatedSession : session
        )
      );
      closeRenameDialog();
    } catch {
      setError("Unable to rename this conversation.");
    } finally {
      setRenaming(false);
    }
  }

  async function handleDeleteSession(sessionId: number) {
    setDeletingSessionId(sessionId);
    setError("");

    try {
      await deleteChatSession(sessionId);
      const remainingSessions = sessions.filter((s) => s.id !== sessionId);
      setSessions(remainingSessions);

      if (activeSessionId === sessionId) {
        const nextSession = remainingSessions[0];
        if (nextSession) {
          setActiveSessionId(nextSession.id);
          const nextMessages = await getChatMessages(nextSession.id);
          setMessages(nextMessages);
        } else {
          setActiveSessionId(null);
          setMessages([]);
        }
        setQuestion("");
      }
    } catch {
      setError("Unable to delete this conversation.");
    } finally {
      setDeletingSessionId(null);
    }
  }

  function buildChatTitle(userQuestion: string): string {
    const cleaned = userQuestion.trim().replace(/\s+/g, " ");
    const words = cleaned.split(" ");
    const title = words.slice(0, 6).join(" ");
    return title.length > 50 ? `${title.slice(0, 47)}...` : title;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || activeSessionId === null) return;

    if (selectedDocumentIds.length === 0) {
      setError("Select at least one document before asking a question.");
      return;
    }

    setSending(true);
    setError("");

    try {
      await sendChatMessage({
        session_id: activeSessionId,
        question: trimmedQuestion,
        document_ids: selectedDocumentIds,
      });

      setQuestion("");

      const activeSession = sessions.find((s) => s.id === activeSessionId);
      if (activeSession && (!activeSession.title || activeSession.title === "New Chat")) {
        const generatedTitle = buildChatTitle(trimmedQuestion);
        try {
          const updatedSession = await renameChatSession(activeSessionId, {
            title: generatedTitle,
          });
          setSessions((current) =>
            current.map((s) => (s.id === updatedSession.id ? updatedSession : s))
          );
        } catch {
          // Auto-title failed but search chat succeeded. Silence error.
        }
      }

      const updatedMessages = await getChatMessages(activeSessionId);
      setMessages(updatedMessages);
    } catch {
      setError("Unable to send your question.");
    } finally {
      setSending(false);
    }
  }

  const activeSession = sessions.find((s) => s.id === activeSessionId);

  return (
    <AppShell>
      <div className="mx-auto flex h-[calc(100vh-7rem)] max-w-7xl gap-6 overflow-hidden">
        {/* Chat History Sidebar */}
        <aside className="hidden w-72 shrink-0 flex-col rounded-2xl border border-border/40 bg-sidebar/50 backdrop-blur-md lg:flex">
          <div className="p-4">
            <Button
              className="w-full bg-linear-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white border-0 shadow-lg shadow-indigo-500/10 hover:scale-[1.01] transition-all rounded-xl"
              onClick={handleNewChat}
              disabled={creatingChat}
            >
              {creatingChat ? (
                <Loader2 className="size-4 animate-spin" />
              ) : (
                <Plus className="size-4" />
              )}
              {creatingChat ? "Creating..." : "New Chat"}
            </Button>
          </div>

          <div className="px-5 py-2">
            <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
              Conversations
            </p>
          </div>

          {/* List of chat sessions */}
          <div className="flex-1 overflow-y-auto px-2 pb-4 scrollbar-thin">
            {sessions.length === 0 ? (
              <div className="px-4 py-8 text-center">
                <MessageSquare className="mx-auto size-8 text-muted-foreground/30 mb-2" />
                <p className="text-xs text-muted-foreground">No conversations yet.</p>
              </div>
            ) : (
              sessions.map((session) => {
                const deleting = deletingSessionId === session.id;
                const isActive = activeSessionId === session.id;

                return (
                  <div
                    key={session.id}
                    className={[
                      "group mb-1 flex items-center rounded-xl transition duration-150 relative overflow-hidden",
                      isActive
                        ? "bg-primary/10 text-primary"
                        : "hover:bg-muted/40 text-muted-foreground hover:text-foreground",
                    ].join(" ")}
                  >
                    {isActive && (
                      <div className="absolute left-0 inset-y-0 w-0.75 bg-primary rounded-r-md" />
                    )}

                    <button
                      type="button"
                      disabled={deleting}
                      onClick={() => void handleSelectSession(session.id)}
                      className={[
                        "flex min-w-0 flex-1 items-center gap-3 px-3.5 py-3 text-left text-xs font-semibold",
                        isActive ? "text-primary" : "text-muted-foreground",
                      ].join(" ")}
                    >
                      {deleting ? (
                        <Loader2 className="size-3.5 shrink-0 animate-spin" />
                      ) : (
                        <MessageSquare className="size-3.5 shrink-0" />
                      )}
                      <span className="truncate">{session.title || "Untitled Chat"}</span>
                    </button>

                    <DropdownMenu>
                      <DropdownMenuTrigger
                        render={
                          <button
                            type="button"
                            aria-label={`Manage ${session.title}`}
                            className="mr-2 flex size-7 shrink-0 items-center justify-center rounded-lg opacity-0 transition-opacity duration-150 hover:bg-background/80 group-hover:opacity-100"
                          />
                        }
                      >
                        <MoreHorizontal className="size-3.5" />
                      </DropdownMenuTrigger>

                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => openRenameDialog(session)}>
                          <Pencil className="size-3.5" />
                          <span>Rename</span>
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          variant="destructive"
                          onClick={() => void handleDeleteSession(session.id)}
                        >
                          <Trash2 className="size-3.5" />
                          <span>Delete</span>
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                );
              })
            )}
          </div>
        </aside>

        {/* Chat Interface Panel */}
        <section className="flex min-w-0 flex-1 flex-col overflow-hidden rounded-2xl border border-border/40 bg-sidebar/20 backdrop-blur-md">
          {/* Active Chat Header */}
          <div className="flex items-center justify-between border-b border-border/40 px-6 py-4 bg-background/50">
            <div>
              <h2 className="font-heading font-bold text-sm tracking-tight">
                {activeSession?.title || "AI Chat Assistant"}
              </h2>
              <p className="text-[10px] text-muted-foreground mt-0.5">
                Ask questions grounded in vector-embedded context documents
              </p>
            </div>

            {/* Document Grounding Toggle Drawer */}
            <Sheet>
              <SheetTrigger
                render={
                  <Button
                    variant="outline"
                    className="h-8 gap-2 px-3 border-border/40 hover:bg-muted/50 rounded-lg text-xs font-semibold"
                  />
                }
              >
                <Layers className="size-3.5 text-primary" />
                <span>Grounding: {selectedDocumentIds.length} PDFs</span>
              </SheetTrigger>

              <SheetContent side="right" className="w-95 sm:max-w-md p-6 glass-panel border-l border-white/5">
                <SheetHeader className="p-0 border-b border-border/40 pb-4">
                  <SheetTitle className="font-heading font-bold flex items-center gap-2">
                    <Database className="size-4.5 text-primary" />
                    <span>Grounding Sources</span>
                  </SheetTitle>
                  <SheetDescription className="text-xs">
                    Select which books or PDF documents the AI agent should use to answer your questions.
                  </SheetDescription>
                </SheetHeader>

                <div className="py-6 space-y-4">
                  <div className="flex items-center justify-between text-xs border-b border-border/20 pb-2">
                    <span className="text-muted-foreground font-semibold">
                      Selected Sources ({selectedDocumentIds.length} / {documents.length})
                    </span>
                    {documents.length > 0 && (
                      <div className="flex items-center gap-3">
                        <button
                          type="button"
                          onClick={selectAllDocuments}
                          className="text-primary font-semibold hover:underline"
                        >
                          Select all
                        </button>
                        <button
                          type="button"
                          onClick={clearDocuments}
                          className="text-muted-foreground font-semibold hover:text-foreground"
                        >
                          Clear
                        </button>
                      </div>
                    )}
                  </div>

                  {documents.length === 0 ? (
                    <div className="py-12 text-center">
                      <FileText className="mx-auto size-8 text-muted-foreground/35 mb-2" />
                      <p className="text-xs text-muted-foreground">No documents uploaded yet.</p>
                      <Link href="/dashboard/documents" className="mt-2 text-xs text-primary font-semibold inline-block hover:underline">
                        Upload first document
                      </Link>
                    </div>
                  ) : (
                    <div className="max-h-[60vh] overflow-y-auto space-y-2 pr-1 scrollbar-thin">
                      {documents.map((doc) => {
                        const isSelected = selectedDocumentIds.includes(doc.id);
                        return (
                          <button
                            key={doc.id}
                            type="button"
                            onClick={() => toggleDocument(doc.id)}
                            className={[
                              "flex w-full items-start gap-3 rounded-xl border p-3 text-left transition-all",
                              isSelected
                                ? "border-primary bg-primary/5 text-foreground shadow-sm"
                                : "border-border/40 hover:bg-muted/40 text-muted-foreground hover:text-foreground",
                            ].join(" ")}
                          >
                            <div
                              className={[
                                "mt-0.5 flex size-4 shrink-0 items-center justify-center rounded-md border text-white transition-colors",
                                isSelected ? "border-primary bg-primary" : "border-border/60 bg-transparent",
                              ].join(" ")}
                            >
                              {isSelected && <span className="text-[10px]">✓</span>}
                            </div>

                            <div className="min-w-0 text-xs">
                              <p className="truncate font-semibold text-foreground/90">
                                {doc.filename}
                              </p>
                              <p className="text-[10px] text-muted-foreground mt-0.5">
                                {doc.page_count} pages · {doc.chunks} chunks · {doc.status}
                              </p>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              </SheetContent>
            </Sheet>
          </div>

          {/* Main Chat Feed */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">
            {error ? (
              <div className="rounded-xl border border-destructive/20 bg-destructive/10 p-4 text-xs text-destructive flex items-start gap-2 animate-in fade-in duration-200">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            ) : null}

            {loading ? (
              <div className="flex h-full items-center justify-center flex-col gap-3">
                <Loader2 className="size-6 animate-spin text-primary" />
                <p className="text-xs text-muted-foreground">Initializing chat stream...</p>
              </div>
            ) : activeSessionId === null ? (
              <div className="flex h-full flex-col items-center justify-center text-center max-w-sm mx-auto">
                <div className="flex size-14 items-center justify-center rounded-2xl bg-primary/10 text-primary mb-4 shadow-xl shadow-primary/5">
                  <Sparkles className="size-7" />
                </div>
                <h3 className="font-heading font-extrabold text-base text-foreground/90">
                  Ground-Truth Knowledge Base Chat
                </h3>
                <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
                  Select which books or PDF documents you want to ground answers in, spin up a new chat session, and ask away!
                </p>
                <Button
                  className="mt-6 bg-linear-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white border-0 shadow-lg shadow-indigo-500/20"
                  onClick={handleNewChat}
                  disabled={creatingChat}
                >
                  {creatingChat ? (
                    <Loader2 className="size-4 animate-spin" />
                  ) : (
                    <Plus className="size-4" />
                  )}
                  <span>Create First Conversation</span>
                </Button>
              </div>
            ) : messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center max-w-sm mx-auto">
                <div className="flex size-12 items-center justify-center rounded-2xl bg-indigo-500/10 text-indigo-400 mb-4 animate-bounce">
                  <BookOpen className="size-6" />
                </div>
                <h3 className="font-heading font-bold text-sm text-foreground/90">
                  Ask your first question
                </h3>
                <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
                  The model will pull semantic chunks from your selected books and formulate a precise response with cited sources.
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message) => {
                  const isUser = message.role === "user";

                  return (
                    <div
                      key={message.id}
                      className={["flex w-full items-start gap-4", isUser ? "justify-end" : "justify-start"].join(" ")}
                    >
                      {/* Avatar */}
                      {!isUser && (
                        <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-linear-to-tr from-violet-600 to-indigo-600 text-white text-[10px] font-bold shadow-lg shadow-indigo-500/15">
                          AI
                        </div>
                      )}

                      <div
                        className={[
                          "max-w-[85%] rounded-2xl px-4 py-3 text-xs leading-relaxed shadow-sm border",
                          isUser
                            ? "bg-primary text-primary-foreground border-transparent rounded-tr-none shadow-indigo-500/5"
                            : "bg-card text-card-foreground border-border/40 rounded-tl-none",
                        ].join(" ")}
                      >
                        {isUser ? (
                          <p className="whitespace-pre-wrap leading-relaxed">{message.message}</p>
                        ) : (
                          <div className="space-y-4">
                            <MarkdownMessage content={message.message} />

                            {/* Citations / References */}
                            {message.sources && message.sources.length > 0 ? (
                              <div className="mt-4 border-t border-border/30 pt-4">
                                <p className="mb-2 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                                  Grounding Citations
                                </p>
                                <div className="grid gap-2 sm:grid-cols-2">
                                  {message.sources.map((source) => (
                                    <div
                                      key={`${message.id}-${source.reference}-${source.file_name}-${source.page_number}-${source.chunk_number}`}
                                      className="rounded-xl border border-border/30 bg-muted/20 p-3 hover:bg-muted/40 transition duration-150"
                                    >
                                      <div className="flex items-center justify-between gap-3 text-[10px] font-bold">
                                        <span className="text-primary uppercase">
                                          {source.reference}
                                        </span>
                                        <span className="text-emerald-400">
                                          {(source.score * 100).toFixed(0)}% Match
                                        </span>
                                      </div>
                                      <p className="mt-2 truncate font-semibold text-foreground/90">
                                        {source.file_name}
                                      </p>
                                      <p className="mt-1 text-[10px] text-muted-foreground">
                                        Page {source.page_number} · Chunk {source.chunk_number}
                                      </p>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            ) : null}
                          </div>
                        )}
                      </div>

                      {isUser && (
                        <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-muted text-[10px] font-bold border border-border/40">
                          ME
                        </div>
                      )}
                    </div>
                  );
                })}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Chat Form Area */}
          <form onSubmit={handleSubmit} className="border-t border-border/40 p-4 bg-background/50">
            <div className="flex items-center gap-2 relative bg-background border border-border/50 rounded-xl px-3 py-1.5 focus-within:border-primary/50 focus-within:ring-2 focus-within:ring-primary/10 transition duration-200">
              <Input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder={
                  selectedDocumentIds.length > 0
                    ? "Ask a question about your selected documents..."
                    : "Select at least one document first..."
                }
                disabled={sending || activeSessionId === null || selectedDocumentIds.length === 0}
                className="flex-1 bg-transparent border-0 ring-0 focus:ring-0 focus-visible:ring-0 focus-visible:ring-offset-0 px-1 text-xs h-9"
              />

              <Button
                type="submit"
                size="icon"
                disabled={
                  sending ||
                  activeSessionId === null ||
                  selectedDocumentIds.length === 0 ||
                  !question.trim()
                }
                className="size-8 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground shadow-md shadow-indigo-500/10"
              >
                {sending ? (
                  <Loader2 className="size-4 animate-spin" />
                ) : (
                  <Send className="size-3.5" />
                )}
              </Button>
            </div>

            <div className="mt-2.5 flex items-center justify-between text-[10px] text-muted-foreground px-1">
              <span>Verified Answers only. AI references context matches.</span>
              <span>{selectedDocumentIds.length} sources active</span>
            </div>
          </form>
        </section>
      </div>

      {/* Rename Chat Title Dialog */}
      <Dialog open={renameSessionId !== null} onOpenChange={(open) => !open && closeRenameDialog()}>
        <DialogContent className="glass-panel border-white/5 rounded-2xl p-6 shadow-2xl">
          <DialogHeader>
            <DialogTitle className="font-heading font-bold text-base">Rename Conversation</DialogTitle>
            <DialogDescription className="text-xs">
              Give this chat session a short, descriptive title.
            </DialogDescription>
          </DialogHeader>

          <Input
            value={renameTitle}
            maxLength={255}
            autoFocus
            placeholder="E.g. Rust Microservices, Chapter 4 Q&A"
            onChange={(e) => setRenameTitle(e.target.value)}
            className="h-10 bg-background/50 border-border/40 focus:border-primary/50 focus:ring-primary/20 rounded-lg text-xs"
            onKeyDown={(e) => {
              if (e.key === "Enter" && !renaming) {
                e.preventDefault();
                void handleRenameSession();
              }
            }}
          />

          <DialogFooter className="gap-2 sm:gap-0 mt-4">
            <Button variant="outline" className="text-xs rounded-lg" onClick={closeRenameDialog}>
              Cancel
            </Button>
            <Button
              className="text-xs bg-linear-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 border-0 rounded-lg text-white font-medium"
              onClick={() => void handleRenameSession()}
              disabled={renaming || !renameTitle.trim()}
            >
              {renaming ? (
                <>
                  <Loader2 className="size-3.5 animate-spin" />
                  <span>Saving...</span>
                </>
              ) : (
                "Save Title"
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </AppShell>
  );
}