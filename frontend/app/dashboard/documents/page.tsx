"use client";

import {
  FileText,
  Loader2,
  Trash2,
  Upload,
} from "lucide-react";
import {
  ChangeEvent,
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
        if (!cancelled) {
          setDocuments(data);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setError("Unable to load documents.");
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [router]);

  async function handleUpload(
    event: ChangeEvent<HTMLInputElement>,
  ) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setUploading(true);
    setError("");

    try {
      await uploadDocument(file);
      await loadDocuments();
    } catch {
      setError(
        "Upload failed. The document may already exist.",
      );
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  async function handleDelete(
    documentId: number,
  ) {
    setDeletingId(documentId);
    setError("");

    try {
      await deleteDocument(documentId);

      setDocuments((current) =>
        current.filter(
          (document) => document.id !== documentId,
        ),
      );
    } catch {
      setError("Unable to delete document.");
    } finally {
      setDeletingId(null);
    }
  }

  function formatFileSize(bytes: number) {
    if (bytes === 0) {
      return "0 MB";
    }

    return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
  }

  return (
    <AppShell>
      <div className="mx-auto max-w-6xl space-y-6">
        <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-2xl font-semibold tracking-tight">
              Documents
            </h2>

            <p className="mt-1 text-muted-foreground">
              Upload and manage the PDFs available to your RAG assistant.
            </p>
          </div>

          <div>
            <Input
              id="pdf-upload"
              type="file"
              accept="application/pdf"
              className="hidden"
              onChange={handleUpload}
              disabled={uploading}
            />

            <label
              htmlFor="pdf-upload"
              className={[
                "inline-flex h-9 cursor-pointer items-center justify-center gap-2",
                "rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground",
                "transition-colors hover:bg-primary/90",
                uploading
                  ? "pointer-events-none opacity-50"
                  : "",
              ].join(" ")}
            >
              {uploading ? (
                <Loader2 className="size-4 animate-spin" />
              ) : (
                <Upload className="size-4" />
              )}

              {uploading ? "Indexing..." : "Upload PDF"}
            </label>
          </div>
        </div>

        {error ? (
          <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-3 text-sm text-destructive">
            {error}
          </div>
        ) : null}

        {loading ? (
          <div className="flex min-h-64 items-center justify-center">
            <Loader2 className="size-6 animate-spin text-muted-foreground" />
          </div>
        ) : documents.length === 0 ? (
          <Card>
            <CardContent className="flex min-h-64 flex-col items-center justify-center text-center">
              <FileText className="mb-4 size-10 text-muted-foreground" />

              <h3 className="font-semibold">
                No documents yet
              </h3>

              <p className="mt-1 max-w-sm text-sm text-muted-foreground">
                Upload a PDF and it will be chunked, embedded, and indexed for
                your assistant.
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 lg:grid-cols-2">
            {documents.map((document) => {
              const isDeleting =
                deletingId === document.id;

              return (
                <Card key={document.id}>
                  <CardHeader>
                    <div className="flex items-start justify-between gap-4">
                      <div className="min-w-0">
                        <CardTitle className="truncate text-base">
                          {document.filename}
                        </CardTitle>

                        <CardDescription className="mt-1">
                          {document.page_count} pages ·{" "}
                          {document.chunks} chunks
                        </CardDescription>
                      </div>

                      <Badge variant="secondary">
                        {document.status}
                      </Badge>
                    </div>
                  </CardHeader>

                  <CardContent className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <FileText className="size-4" />

                      {formatFileSize(document.file_size)}
                    </div>

                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      disabled={isDeleting}
                      aria-label={`Delete ${document.filename}`}
                      onClick={() =>
                        handleDelete(document.id)
                      }
                    >
                      {isDeleting ? (
                        <Loader2 className="size-4 animate-spin" />
                      ) : (
                        <Trash2 className="size-4" />
                      )}
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </AppShell>
  );
}