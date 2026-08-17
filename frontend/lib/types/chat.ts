export type ChatSession = {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
};

export type ChatMessage = {
  id: number;
  role: "user" | "assistant";
  message: string;
  sources: SourceReference[];
  created_at: string;
};


export type SourceReference = {
  reference: string;
  file_name: string;
  page_number: number;
  chunk_number: number;
  score: number;
};

export type ChatResponse = {
  answer: string;
  sources: SourceReference[];
};

export type ChatRequest = {
  session_id: number;
  question: string;
  document_ids?: number[];
};

export type ChatSessionUpdate = {
  title: string;
};

export type DeleteChatSessionResponse = {
  message: string;
  session_id: number;
};