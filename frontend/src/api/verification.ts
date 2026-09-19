import { apiClient } from './client';

export const verifyCertificate = async (certificateId: string) => {
  const response = await apiClient.get(`/certificates/verify/${certificateId}`);
  return response.data;
};
