export interface PredictRequest {
  question: string;
}

export interface PredictResponse {
  sql?: string;
  detail?: string;
}
