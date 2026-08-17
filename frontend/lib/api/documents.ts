import { apiRequest } from "@/lib/api/client";
import type {
  Document,
  UploadResponse,
} from "@/lib/types/document";

function getToken(): string {
  if (typeof window === "undefined") {
    return "";
  }

  return localStorage.getItem("access_token") ?? "";
}

export function getDocuments(): Promise<Document[]> {
  return apiRequest<Document[]>("/documents/", {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });
}

export function deleteDocument(
  documentId: number,
): Promise<{
  message: string;
  document_id: number;
}> {
  return apiRequest(
    `/documents/${documentId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    },
  );
}

export async function uploadDocument(
  file: File,
): Promise<UploadResponse> {
  const token = getToken();

  const formData = new FormData();
  formData.append("file", file);

  return apiRequest<UploadResponse>(
    "/upload/",
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    },
  );
}