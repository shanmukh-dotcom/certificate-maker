import { apiClient } from './client';

export const getCertificates = async () => {
  const response = await apiClient.get('/certificates/');
  return response.data;
};

export const revokeCertificate = async (certificateId: string, reason: string) => {
  const response = await apiClient.post(`/certificates/${certificateId}/revoke`, { reason });
  return response.data;
};
