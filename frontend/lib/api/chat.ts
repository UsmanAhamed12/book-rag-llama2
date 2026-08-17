import { apiRequest } from "@/lib/api/client";

import type {
  ChatMessage,
  ChatRequest,
  ChatResponse,
  ChatSession,
  ChatSessionUpdate,
  DeleteChatSessionResponse,
} from "@/lib/types/chat";

function getToken(): string {
  if (typeof window === "undefined") {
    return "";
  }

  return localStorage.getItem("access_token") ?? "";
}

function authHeaders() {
  return {
    Authorization: `Bearer ${getToken()}`,
  };
}

export function createChatSession(): Promise<ChatSession> {
  return apiRequest<ChatSession>(
    "/chat/sessions/",
    {
      method: "POST",
      headers: authHeaders(),
    },
  );
}

export function getChatSessions(): Promise<ChatSession[]> {
  return apiRequest<ChatSession[]>(
    "/chat/sessions/",
    {
      headers: authHeaders(),
    },
  );
}

export function getChatMessages(
  sessionId: number,
): Promise<ChatMessage[]> {
  return apiRequest<ChatMessage[]>(
    `/chat/sessions/${sessionId}/messages`,
    {
      headers: authHeaders(),
    },
  );
}

export function sendChatMessage(
  payload: ChatRequest,
): Promise<ChatResponse> {
  return apiRequest<ChatResponse>(
    "/chat/",
    {
      method: "POST",
      headers: {
        ...authHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
  );
}

export function renameChatSession(
  sessionId: number,
  payload: ChatSessionUpdate,
): Promise<ChatSession> {
  return apiRequest<ChatSession>(
    `/chat/sessions/${sessionId}`,
    {
      method: "PATCH",
      headers: {
        ...authHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
  );
}

export function deleteChatSession(
  sessionId: number,
): Promise<DeleteChatSessionResponse> {
  return apiRequest<DeleteChatSessionResponse>(
    `/chat/sessions/${sessionId}`,
    {
      method: "DELETE",
      headers: authHeaders(),
    },
  );
}