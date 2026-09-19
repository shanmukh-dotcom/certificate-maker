import { apiClient } from './client';

export const createTemplate = async (name: string, file?: File) => {
  const formData = new FormData();
  formData.append('name', name);
  if (file) formData.append('file', file);
  
  const response = await apiClient.post('/templates/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const getTemplates = async () => {
  const response = await apiClient.get('/templates/');
  return response.data;
};

export const createTemplateVersion = async (templateId: number, configuration: any) => {
  const response = await apiClient.post(`/templates/${templateId}/versions`, { configuration });
  return response.data;
};

export const generateTestCertificate = async (templateId: number, versionId: number) => {
  const response = await apiClient.post(
    `/templates/${templateId}/versions/${versionId}/test`, 
    {}, 
    { responseType: 'blob' }
  );
  return response.data;
};
