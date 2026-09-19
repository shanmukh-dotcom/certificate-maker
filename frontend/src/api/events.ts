import { apiClient } from './client';

export const getEvents = async () => {
  const response = await apiClient.get('/events/');
  return response.data;
};

export const getEvent = async (id: number) => {
  const response = await apiClient.get('/events/' + id);
  return response.data;
};

export const createEvent = async (data: any) => {
  const response = await apiClient.post('/events/', data);
  return response.data;
};

export const updateEvent = async (id: number, data: any) => {
  const response = await apiClient.put('/events/' + id, data);
  return response.data;
};
