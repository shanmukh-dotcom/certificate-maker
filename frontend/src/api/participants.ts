import { apiClient } from './client';

export const getParticipants = async (eventId: number) => {
  const response = await apiClient.get(`/participants/${eventId}`);
  return response.data;
};

export const uploadParticipants = async (eventId: number, file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await apiClient.post(`/participants/${eventId}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const deleteParticipant = async (participantId: number) => {
  const response = await apiClient.delete(`/participants/${participantId}`);
  return response.data;
};
