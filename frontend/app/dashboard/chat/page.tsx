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
} from "lucide-react";
import {
  FormEvent,
  useEffect,
  useState,
} from "react";
import { useRouter } from "next/navigation";

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

import type {
  ChatMessage,
  ChatSession,
  SourceReference,
} from "@/lib/types/chat";
import type { Document } from "@/lib/types/document";

export default function ChatPage() {
  const router = useRouter();

  const [sessions, setSessions] =
    useState<ChatSession[]>([]);

  const [
    activeSessionId,
    setActiveSessionId,
  ] = useState<number | null>(null);

  const [messages, setMessages] =
    useState<ChatMessage[]>([]);

  const [sources, setSources] =
    useState<SourceReference[]>([]);

  const [documents, setDocuments] =
    useState<Document[]>([]);

  const [
    selectedDocumentIds,
    setSelectedDocumentIds,
  ] = useState<number[]>([]);

  const [question, setQuestion] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [sending, setSending] =
    useState(false);

  const [
    creatingChat,
    setCreatingChat,
  ] = useState(false);

  const [error, setError] =
    useState("");

  const [
    renameSessionId,
    setRenameSessionId,
  ] = useState<number | null>(null);

  const [renameTitle, setRenameTitle] = useState<string>("");

  const [renaming, setRenaming] =
    useState(false);

  const [
    deletingSessionId,
    setDeletingSessionId,
  ] = useState<number | null>(null);

  useEffect(() => {
    const token =
      localStorage.getItem("access_token");

    if (!token) {
      router.replace("/login");
      return;
    }

    let cancelled = false;

    async function initializePage() {
      try {
        const [
          sessionData,
          documentData,
        ] = await Promise.all([
          getChatSessions(),
          getDocuments(),
        ]);

        if (cancelled) {
          return;
        }

        setSessions(sessionData);
        setDocuments(documentData);

        setSelectedDocumentIds(
          documentData.map(
            (document) =>
              document.id,
          ),
        );

        if (
          sessionData.length > 0
        ) {
          const firstSessionId =
            sessionData[0].id;

          setActiveSessionId(
            firstSessionId,
          );

          const messageData =
            await getChatMessages(
              firstSessionId,
            );

          if (!cancelled) {
            setMessages(
              messageData,
            );
          }
        }
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load chat data.",
          );
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
      const session =
        await createChatSession();

      setSessions((current) => [
        session,
        ...current,
      ]);

      setActiveSessionId(
        session.id,
      );

      setMessages([]);
      setSources([]);
      setQuestion("");
    } catch {
      setError(
        "Unable to create a new chat.",
      );
    } finally {
      setCreatingChat(false);
    }
  }

  async function handleSelectSession(
    sessionId: number,
  ) {
    if (
      sessionId ===
      activeSessionId
    ) {
      return;
    }

    setActiveSessionId(
      sessionId,
    );

    setSources([]);
    setError("");

    try {
      const data =
        await getChatMessages(
          sessionId,
        );

      setMessages(data);
    } catch {
      setError(
        "Unable to load this conversation.",
      );
    }
  }

  function toggleDocument(
    documentId: number,
  ) {
    setSelectedDocumentIds(
      (current) => {
        if (
          current.includes(
            documentId,
          )
        ) {
          return current.filter(
            (id) =>
              id !== documentId,
          );
        }

        return [
          ...current,
          documentId,
        ];
      },
    );
  }

  function selectAllDocuments() {
    setSelectedDocumentIds(
      documents.map(
        (document) =>
          document.id,
      ),
    );
  }

  function clearDocuments() {
    setSelectedDocumentIds(
      [],
    );
  }

  function openRenameDialog(
    session: ChatSession,
    ) {
    setRenameSessionId(session.id);

    setRenameTitle(
        session.title ?? "New Chat",
    );
    }

  function closeRenameDialog() {
    setRenameSessionId(null);
    setRenameTitle("");
  }

  async function handleRenameSession() {
    if (
      renameSessionId === null
    ) {
      return;
    }

    const title =
      (renameTitle ?? "").trim();

    if (!title) {
      setError(
        "Chat title cannot be empty.",
      );

      return;
    }

    setRenaming(true);
    setError("");

    try {
      const updatedSession =
        await renameChatSession(
          renameSessionId,
          {
            title,
          },
        );

      setSessions(
        (current) =>
          current.map(
            (session) =>
              session.id ===
              updatedSession.id
                ? updatedSession
                : session,
          ),
      );

      closeRenameDialog();
    } catch {
      setError(
        "Unable to rename this conversation.",
      );
    } finally {
      setRenaming(false);
    }
  }

  async function handleDeleteSession(
    sessionId: number,
  ) {
    setDeletingSessionId(
      sessionId,
    );

    setError("");

    try {
      await deleteChatSession(
        sessionId,
      );

      const remainingSessions =
        sessions.filter(
          (session) =>
            session.id !==
            sessionId,
        );

      setSessions(
        remainingSessions,
      );

      if (
        activeSessionId ===
        sessionId
      ) {
        const nextSession =
          remainingSessions[0];

        if (nextSession) {
          setActiveSessionId(
            nextSession.id,
          );

          const nextMessages =
            await getChatMessages(
              nextSession.id,
            );

          setMessages(
            nextMessages,
          );
        } else {
          setActiveSessionId(
            null,
          );

          setMessages([]);
        }

        setSources([]);
        setQuestion("");
      }
    } catch {
      setError(
        "Unable to delete this conversation.",
      );
    } finally {
      setDeletingSessionId(
        null,
      );
    }
  }

  function buildChatTitle(
        userQuestion: string,
        ): string {
        const cleaned =
            userQuestion
            .trim()
            .replace(/\s+/g, " ");

        const words =
            cleaned.split(" ");

        const title =
            words
            .slice(0, 6)
            .join(" ");

        if (title.length > 50) {
            return `${title.slice(0, 47)}...`;
        }

        return title;
        }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
    ) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (
        !trimmedQuestion ||
        activeSessionId === null
    ) {
        return;
    }

    if (selectedDocumentIds.length === 0) {
        setError(
        "Select at least one document before asking a question.",
        );
        return;
    }

    setSending(true);
    setError("");

    try {
        const response =
        await sendChatMessage({
            session_id: activeSessionId,
            question: trimmedQuestion,
            document_ids: selectedDocumentIds,
        });

        setQuestion("");
        setSources(response.sources);

        /*
        * Automatically rename a brand-new chat
        * using the first user question.
        */
        const activeSession =
        sessions.find(
            (session) =>
            session.id === activeSessionId,
        );

        if (
        activeSession &&
        (
            !activeSession.title ||
            activeSession.title === "New Chat"
        )
        ) {
        const generatedTitle =
            buildChatTitle(
            trimmedQuestion,
            );

        try {
            const updatedSession =
            await renameChatSession(
                activeSessionId,
                {
                title: generatedTitle,
                },
            );

            setSessions((current) =>
            current.map((session) =>
                session.id === updatedSession.id
                ? updatedSession
                : session,
            ),
            );
        } catch {
            /*
            * Do not fail the chat request
            * if automatic title generation fails.
            */
        }
        }

        const updatedMessages =
        await getChatMessages(
            activeSessionId,
        );

        setMessages(
        updatedMessages,
        );
    } catch {
        setError(
        "Unable to send your question.",
        );
    } finally {
        setSending(false);
    }
    }

  return (
    <AppShell>
      <div className="mx-auto flex h-[calc(100vh-7rem)] max-w-7xl gap-4">
        <aside className="hidden w-72 shrink-0 rounded-xl border bg-background lg:flex lg:flex-col">
          <div className="p-4">
            <Button
              className="w-full"
              onClick={
                handleNewChat
              }
              disabled={
                creatingChat
              }
            >
              {creatingChat ? (
                <Loader2 className="size-4 animate-spin" />
              ) : (
                <Plus className="size-4" />
              )}

              {creatingChat
                ? "Creating..."
                : "New Chat"}
            </Button>
          </div>

          <div className="border-t px-3 py-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              Conversations
            </p>
          </div>

          <div className="flex-1 overflow-y-auto px-2 pb-4">
            {sessions.length ===
            0 ? (
              <p className="px-3 py-6 text-center text-xs text-muted-foreground">
                No conversations yet.
              </p>
            ) : (
              sessions.map(
                (session) => {
                  const deleting =
                    deletingSessionId ===
                    session.id;

                  return (
                    <div
                      key={
                        session.id
                      }
                      className={[
                        "group mb-1 flex items-center rounded-lg transition",
                        activeSessionId ===
                        session.id
                          ? "bg-muted"
                          : "hover:bg-muted/70",
                      ].join(
                        " ",
                      )}
                    >
                      <button
                        type="button"
                        disabled={
                          deleting
                        }
                        onClick={() =>
                          handleSelectSession(
                            session.id,
                          )
                        }
                        className={[
                          "flex min-w-0 flex-1 items-center gap-3 px-3 py-3 text-left text-sm",
                          activeSessionId ===
                          session.id
                            ? "font-medium text-foreground"
                            : "text-muted-foreground",
                        ].join(
                          " ",
                        )}
                      >
                        {deleting ? (
                          <Loader2 className="size-4 shrink-0 animate-spin" />
                        ) : (
                          <MessageSquare className="size-4 shrink-0" />
                        )}

                        <span className="truncate">
                          {
                            session.title
                          }
                        </span>
                      </button>

                      <DropdownMenu>
                        <DropdownMenuTrigger
                          render={
                            <button
                              type="button"
                              aria-label={`Manage ${session.title}`}
                              className="mr-2 flex size-8 shrink-0 items-center justify-center rounded-md text-muted-foreground opacity-0 transition hover:bg-background hover:text-foreground group-hover:opacity-100"
                            />
                          }
                        >
                          <MoreHorizontal className="size-4" />
                        </DropdownMenuTrigger>

                        <DropdownMenuContent
                          align="end"
                        >
                          <DropdownMenuItem
                            onClick={() =>
                              openRenameDialog(
                                session,
                              )
                            }
                          >
                            <Pencil className="size-4" />
                            Rename
                          </DropdownMenuItem>

                          <DropdownMenuItem
                            variant="destructive"
                            onClick={() =>
                              void handleDeleteSession(
                                session.id,
                              )
                            }
                          >
                            <Trash2 className="size-4" />
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  );
                },
              )
            )}
          </div>
        </aside>

        <section className="flex min-w-0 flex-1 flex-col overflow-hidden rounded-xl border bg-background">
          <div className="border-b px-5 py-4">
            <h2 className="font-semibold">
              RAG Chat
            </h2>

            <p className="text-sm text-muted-foreground">
              Ask questions about your selected documents.
            </p>
          </div>

          <div className="border-b bg-muted/20 px-4 py-3">
            <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <FileText className="size-4 text-muted-foreground" />

                <span className="text-xs font-medium text-muted-foreground">
                  Ask from
                </span>

                <span className="text-xs text-muted-foreground">
                  {
                    selectedDocumentIds.length
                  }
                  /
                  {
                    documents.length
                  }{" "}
                  selected
                </span>
              </div>

              {documents.length >
              0 ? (
                <div className="flex items-center gap-3 text-xs">
                  <button
                    type="button"
                    onClick={
                      selectAllDocuments
                    }
                    className="text-muted-foreground transition hover:text-foreground"
                  >
                    Select all
                  </button>

                  <button
                    type="button"
                    onClick={
                      clearDocuments
                    }
                    className="text-muted-foreground transition hover:text-foreground"
                  >
                    Clear
                  </button>
                </div>
              ) : null}
            </div>

            {documents.length ===
            0 ? (
              <p className="text-xs text-muted-foreground">
                Upload a document before asking questions.
              </p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {documents.map(
                  (document) => {
                    const selected =
                      selectedDocumentIds.includes(
                        document.id,
                      );

                    return (
                      <button
                        key={
                          document.id
                        }
                        type="button"
                        title={
                          document.filename
                        }
                        onClick={() =>
                          toggleDocument(
                            document.id,
                          )
                        }
                        className={[
                          "max-w-60 truncate rounded-full border px-3 py-1.5 text-xs transition",
                          selected
                            ? "border-primary bg-primary text-primary-foreground shadow-sm"
                            : "bg-background text-muted-foreground hover:bg-muted hover:text-foreground",
                        ].join(
                          " ",
                        )}
                      >
                        {
                          document.filename
                        }
                      </button>
                    );
                  },
                )}
              </div>
            )}
          </div>

          <div className="flex-1 overflow-y-auto p-5">
            {error ? (
              <p className="mb-4 rounded-lg border border-destructive/20 bg-destructive/5 p-3 text-sm text-destructive">
                {error}
              </p>
            ) : null}

            {loading ? (
              <div className="flex h-full items-center justify-center">
                <Loader2 className="size-6 animate-spin text-muted-foreground" />
              </div>
            ) : activeSessionId ===
              null ? (
              <div className="flex h-full flex-col items-center justify-center text-center">
                <MessageSquare className="mb-4 size-10 text-muted-foreground" />

                <h3 className="font-semibold">
                  Start a new conversation
                </h3>

                <p className="mt-1 max-w-sm text-sm text-muted-foreground">
                  Select the documents you want to search, create a chat, and start asking questions.
                </p>

                <Button
                  className="mt-5"
                  onClick={
                    handleNewChat
                  }
                  disabled={
                    creatingChat
                  }
                >
                  {creatingChat ? (
                    <Loader2 className="size-4 animate-spin" />
                  ) : (
                    <Plus className="size-4" />
                  )}

                  New Chat
                </Button>
              </div>
            ) : messages.length ===
              0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center">
                <MessageSquare className="mb-4 size-9 text-muted-foreground" />

                <h3 className="font-medium">
                  Ask your first question
                </h3>

                <p className="mt-1 max-w-sm text-sm text-muted-foreground">
                  Your answer will be grounded in the selected PDF documents.
                </p>
              </div>
            ) : (
              <div className="space-y-5">
                {messages.map(
                  (message) => (
                    <div
                      key={
                        message.id
                      }
                      className={
                        message.role ===
                        "user"
                          ? "flex justify-end"
                          : "flex justify-start"
                      }
                    >
                      <div
                        className={[
                          "max-w-[85%] rounded-2xl px-4 py-3 text-sm",
                          message.role ===
                          "user"
                            ? "bg-primary text-primary-foreground"
                            : "border bg-card text-card-foreground shadow-sm",
                        ].join(
                          " ",
                        )}
                      >
                        {message.role ===
                        "assistant" ? (
                          <MarkdownMessage
                            content={
                              message.message
                            }
                          />
                        ) : (
                          <p className="whitespace-pre-wrap leading-6">
                            {
                              message.message
                            }
                          </p>
                        )}
                      </div>
                    </div>
                  ),
                )}

                {sources.length >
                0 ? (
                  <div className="mt-6">
                    <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                      Sources
                    </p>

                    <div className="grid gap-2 sm:grid-cols-2">
                      {sources.map(
                        (
                          source,
                        ) => (
                          <div
                            key={`${source.reference}-${source.file_name}-${source.page_number}-${source.chunk_number}`}
                            className="rounded-lg border bg-muted/30 p-3 transition hover:bg-muted/60"
                          >
                            <div className="flex items-center justify-between gap-3">
                              <span className="text-xs font-semibold">
                                {
                                  source.reference
                                }
                              </span>

                              <span className="text-xs text-muted-foreground">
                                {(
                                  source.score *
                                  100
                                ).toFixed(
                                  0,
                                )}
                                % match
                              </span>
                            </div>

                            <p className="mt-2 truncate text-sm font-medium">
                              {
                                source.file_name
                              }
                            </p>

                            <p className="mt-1 text-xs text-muted-foreground">
                              Page{" "}
                              {
                                source.page_number
                              }{" "}
                              · Chunk{" "}
                              {
                                source.chunk_number
                              }
                            </p>
                          </div>
                        ),
                      )}
                    </div>
                  </div>
                ) : null}
              </div>
            )}
          </div>

          <form
            onSubmit={
              handleSubmit
            }
            className="border-t p-4"
          >
            <div className="flex gap-2">
              <Input
                value={
                  question
                }
                onChange={(
                  event,
                ) =>
                  setQuestion(
                    event
                      .target
                      .value,
                  )
                }
                placeholder={
                  selectedDocumentIds.length >
                  0
                    ? "Ask a question about your selected documents..."
                    : "Select at least one document first..."
                }
                disabled={
                  sending ||
                  activeSessionId ===
                    null ||
                  selectedDocumentIds.length ===
                    0
                }
              />

              <Button
                type="submit"
                size="icon"
                aria-label="Send question"
                disabled={
                  sending ||
                  activeSessionId ===
                    null ||
                  selectedDocumentIds.length ===
                    0 ||
                  !question.trim()
                }
              >
                {sending ? (
                  <Loader2 className="size-4 animate-spin" />
                ) : (
                  <Send className="size-4" />
                )}
              </Button>
            </div>

            <p className="mt-2 text-xs text-muted-foreground">
              Answers are generated from the selected documents. Always verify important information against the cited pages.
            </p>
          </form>
        </section>
      </div>

      <Dialog
        open={
          renameSessionId !==
          null
        }
        onOpenChange={(
          open,
        ) => {
          if (!open) {
            closeRenameDialog();
          }
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              Rename conversation
            </DialogTitle>

            <DialogDescription>
              Give this chat a short descriptive title.
            </DialogDescription>
          </DialogHeader>

          <Input
            value={renameTitle ?? ""}
            maxLength={255}
            autoFocus
            placeholder="C++ Basics"
            onChange={(event) =>
                setRenameTitle(event.target.value)
            }
            onKeyDown={(
              event,
            ) => {
              if (
                event.key ===
                  "Enter" &&
                !renaming
              ) {
                event.preventDefault();

                void handleRenameSession();
              }
            }}
          />

          <DialogFooter>
            <Button
              variant="outline"
              onClick={
                closeRenameDialog
              }
            >
              Cancel
            </Button>

            <Button
              onClick={() =>
                void handleRenameSession()
              }
              disabled={
                renaming ||
                !(renameTitle ?? "").trim()
              }
            >
              {renaming ? (
                <>
                  <Loader2 className="size-4 animate-spin" />
                  Saving...
                </>
              ) : (
                "Save"
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </AppShell>
  );
}