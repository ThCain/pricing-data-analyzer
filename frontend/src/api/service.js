import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getFiles = async () => {
  const response = await api.get('/files');
  return response.data;
};

export const getFileInfo = async (fileId) => {
  const response = await api.get(`/files/${fileId}`);
  return response.data;
};

export const deleteFile = async (fileId) => {
  const response = await api.delete(`/files/${fileId}`);
  return response.data;
};

export const analyzeData = async (fileId) => {
  const response = await api.get(`/analyze/${fileId}`);
  return response.data;
};

export const getStatistics = async (fileId) => {
  const response = await api.get(`/stats/${fileId}`);
  return response.data;
};

export const generateReport = async (fileId) => {
  const response = await api.get(`/reports/${fileId}/download`);
  return response.data;
};

export const downloadReportFile = async (fileId) => {
  const response = await api.get(`/reports/${fileId}/download-file`, {
    responseType: 'blob',
  });
  return response;
};

export const getVisualizations = async (fileId) => {
  const response = await api.get(`/reports/${fileId}/visualizations`);
  return response.data;
};

export const deleteAnalysis = async (fileId) => {
  const response = await api.delete(`/analysis/${fileId}`);
  return response.data;
};

export default api;
