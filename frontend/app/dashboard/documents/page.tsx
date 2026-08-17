"use client";

import {
  FileText,
  Loader2,
  Trash2,
  Upload,
  AlertCircle,
  Database,
  Layers,
} from "lucide-react";
import {
  ChangeEvent,
  DragEvent,
  useCallback,
  useEffect,
  useState,
} from "react";
import { useRouter } from "next/navigation";

import { AppShell } from "@/components/layout/app-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  deleteDocument,
  getDocuments,
  uploadDocument,
} from "@/lib/api/documents";
import type { Document } from "@/lib/types/document";

export default function DocumentsPage() {
  const router = useRouter();

  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [isDragActive, setIsDragActive] = useState(false);

  const loadDocuments = useCallback(async () => {
    setLoading(true);
    try {
      setError("");
      const data = await getDocuments();
      setDocuments(data);
    } catch {
      setError("Unable to load documents.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      router.replace("/login");
      return;
    }

    let cancelled = false;

    getDocuments()
      .then((data) => {
        if (!cancelled) setDocuments(data);
      })
      .catch(() => {
        if (!cancelled) setError("Unable to load documents.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [router]);

  async function processFile(file: File) {
    if (file.type !== "application/pdf") {
      setError("Only PDF files are supported for document grounding.");
      return;
    }

    setUploading(true);
    setError("");

    try {
      await uploadDocument(file);
      const data = await getDocuments();
      setDocuments(data);
    } catch {
      setError("Upload failed. The document may already exist.");
    } finally {
      setUploading(false);
    }
  }

  async function handleUpload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (file) {
      await processFile(file);
    }
    event.target.value = "";
  }

  function handleDrag(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    event.stopPropagation();
    if (event.type === "dragenter" || event.type === "dragover") {
      setIsDragActive(true);
    } else if (event.type === "dragleave") {
      setIsDragActive(false);
    }
  }

  async function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(false);

    const file = event.dataTransfer.files?.[0];
    if (file) {
      await processFile(file);
    }
  }

  async function handleDelete(documentId: number) {
    setDeletingId(documentId);
    setError("");

    try {
      await deleteDocument(documentId);
      setDocuments((current) => current.filter((doc) => doc.id !== documentId));
    } catch {
      setError("Unable to delete document.");
    } finally {
      setDeletingId(null);
    }
  }

  function formatFileSize(bytes: number) {
    if (bytes === 0) return "0 MB";
    return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
  }

  return (
    <AppShell>
      <div className="space-y-8">
        {/* Header Title Section */}
        <div>
          <h2 className="text-3xl font-heading font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
            Documents Indexer
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Ingest your reference PDF books. The system will slice them, extract embeddings, and index them into the vector database.
          </p>
        </div>

        {error ? (
          <div className="rounded-xl border border-destructive/20 bg-destructive/10 p-4 text-sm text-destructive flex items-center gap-2 animate-in fade-in duration-200">
            <AlertCircle className="size-5 shrink-0" />
            <span>{error}</span>
          </div>
        ) : null}

        {/* Drag-and-Drop Area */}
        <div
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          className={[
            "relative flex flex-col items-center justify-center rounded-2xl border border-dashed p-10 text-center transition-all duration-300",
            isDragActive
              ? "border-primary bg-primary/5 scale-[1.01]"
              : "border-border/60 bg-sidebar/20 hover:bg-sidebar/40 hover:border-primary/40",
            uploading ? "pointer-events-none opacity-50" : "cursor-pointer",
          ].join(" ")}
        >
          <Input
            id="pdf-upload"
            type="file"
            accept="application/pdf"
            className="hidden"
            onChange={handleUpload}
            disabled={uploading}
          />
          <label htmlFor="pdf-upload" className="w-full h-full cursor-pointer flex flex-col items-center justify-center gap-4">
            <div className="flex size-14 items-center justify-center rounded-2xl bg-primary/10 text-primary shadow-xl shadow-primary/5">
              {uploading ? (
                <Loader2 className="size-7 animate-spin" />
              ) : (
                <Upload className="size-7" />
              )}
            </div>

            <div>
              <p className="font-heading font-bold text-sm text-foreground/90">
                {uploading ? "Indexing your document..." : "Drag & Drop your PDF file here"}
              </p>
              <p className="text-xs text-muted-foreground mt-1.5 max-w-xs mx-auto leading-relaxed">
                {uploading
                  ? "We are currently chunking, creating vectors, and syncing metadata with ChromaDB."
                  : "Or click to browse files. Supports only PDF documents."}
              </p>
            </div>
          </label>
        </div>

        {/* Ingested Documents List */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Database className="size-4 text-muted-foreground" />
            <h3 className="font-heading font-bold text-sm text-foreground/90">
              Ingested Books Vector DB ({documents.length})
            </h3>
          </div>

          {loading ? (
            <div className="flex min-h-64 items-center justify-center flex-col gap-3">
              <Loader2 className="size-6 animate-spin text-primary" />
              <p className="text-xs text-muted-foreground">Reading database records...</p>
            </div>
          ) : documents.length === 0 ? (
            <Card className="glass-panel border-white/5 shadow-xl rounded-xl">
              <CardContent className="flex min-h-64 flex-col items-center justify-center text-center p-6">
                <FileText className="mb-4 size-12 text-muted-foreground/35" />
                <h3 className="font-heading font-bold text-sm text-foreground/90">
                  No documents synced
                </h3>
                <p className="mt-2 max-w-sm text-xs text-muted-foreground leading-relaxed">
                  Your RAG assistant is empty. Ingest a PDF document using the drop zone above to start chatting.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4 md:grid-cols-2">
              {documents.map((doc) => {
                const isDeleting = deletingId === doc.id;
                const completed = doc.status === "completed";
                const failed = doc.status === "failed";

                return (
                  <Card key={doc.id} className="aurora-glow-card glass-panel rounded-xl shadow-lg border border-white/5 relative overflow-hidden group">
                    <CardHeader className="pb-3 border-b border-border/40">
                      <div className="flex items-start justify-between gap-4">
                        <div className="min-w-0">
                          <CardTitle className="truncate text-sm font-semibold font-heading text-foreground/90" title={doc.filename}>
                            {doc.filename}
                          </CardTitle>
                          <CardDescription className="text-[10px] mt-1 text-muted-foreground flex items-center gap-1.5">
                            <Layers className="size-3 text-violet-500" />
                            <span>{doc.page_count} pages · {doc.chunks} chunks</span>
                          </CardDescription>
                        </div>

                        <span className={[
                          "shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider border",
                          completed
                            ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-400"
                            : failed
                            ? "border-destructive/20 bg-destructive/10 text-destructive"
                            : "border-violet-500/20 bg-violet-500/10 text-violet-400 animate-pulse"
                        ].join(" ")}>
                          {doc.status}
                        </span>
                      </div>
                    </CardHeader>

                    <CardContent className="pt-3 flex items-center justify-between">
                      <div className="flex items-center gap-2 text-xs text-muted-foreground font-medium">
                        <FileText className="size-3.5 text-muted-foreground" />
                        <span>{formatFileSize(doc.file_size)}</span>
                      </div>

                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        disabled={isDeleting}
                        aria-label={`Delete ${doc.filename}`}
                        onClick={() => void handleDelete(doc.id)}
                        className="size-8 rounded-lg hover:bg-destructive/10 hover:text-destructive text-muted-foreground transition-colors shrink-0"
                      >
                        {isDeleting ? (
                          <Loader2 className="size-3.5 animate-spin text-destructive" />
                        ) : (
                          <Trash2 className="size-3.5" />
                        )}
                      </Button>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}