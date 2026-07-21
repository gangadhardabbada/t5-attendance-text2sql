import axios from 'axios';
import type { PredictRequest, PredictResponse } from '../types';

const API_URL = 'http://localhost:8000';

export const predictSql = async (request: PredictRequest): Promise<PredictResponse> => {
  try {
    const response = await axios.post<PredictResponse>(`${API_URL}/predict`, request);
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.data) {
      return error.response.data; // Handles the 403 Forbidden detail
    }
    throw new Error(error.message || 'An error occurred while connecting to the API');
  }
};
