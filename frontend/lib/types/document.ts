export type Document = {
  id: number;
  user_id: number;
  filename: string;
  file_hash: string | null;
  file_size: number;
  page_count: number;
  chunks: number;
  status: string;
  created_at: string;
  updated_at: string;
};

export type UploadResponse = {
  filename: string;
  chunks: number;
  message: string;
};