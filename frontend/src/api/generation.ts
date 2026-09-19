import { apiClient } from './client';

export const startGeneration = async (eventId: number) => {
  const response = await apiClient.post('/generation/' + eventId);
  return response.data;
};

export const getGenerationStatus = async (eventId: number) => {
  const response = await apiClient.get('/generation/' + eventId);
  return response.data;
};
