import os

files = {
    'src/api/participants.ts': '''import { apiClient } from './client';

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
''',

    'src/features/participants/ParticipantsManager.tsx': '''import React, { useState, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getEvent } from '../../api/events';
import { getParticipants, uploadParticipants, deleteParticipant } from '../../api/participants';
import { Upload, FileSpreadsheet, Trash2, ArrowLeft, Users, CheckCircle2, AlertTriangle, FileType } from 'lucide-react';

export const ParticipantsManager = () => {
  const [searchParams] = useSearchParams();
  const eventId = searchParams.get('event');
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [file, setFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const { data: event } = useQuery({ 
    queryKey: ['event', eventId], 
    queryFn: () => getEvent(Number(eventId)),
    enabled: !!eventId
  });

  const { data: participants, isLoading } = useQuery({
    queryKey: ['participants', eventId],
    queryFn: () => getParticipants(Number(eventId)),
    enabled: !!eventId
  });

  const uploadMutation = useMutation({
    mutationFn: (f: File) => uploadParticipants(Number(eventId), f),
    onSuccess: (data) => {
      setUploadResult(data);
      queryClient.invalidateQueries({ queryKey: ['participants', eventId] });
      setFile(null);
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to upload file');
      setFile(null);
    }
  });

  const deleteMutation = useMutation({
    mutationFn: deleteParticipant,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['participants', eventId] });
    }
  });

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && (droppedFile.name.endsWith('.csv') || droppedFile.name.endsWith('.xlsx'))) {
      setFile(droppedFile);
      setError(null);
    } else {
      setError('Please upload a valid .csv or .xlsx file');
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (selected) {
      setFile(selected);
      setError(null);
    }
  };

  const handleUpload = () => {
    if (file) {
      uploadMutation.mutate(file);
    }
  };

  if (!eventId) return <div className="p-8 text-center text-slate-500">No event selected. Please go back to the Dashboard.</div>;

  return (
    <div className="max-w-7xl mx-auto animate-in fade-in duration-500 pb-12">
      <div className="flex items-center text-sm font-medium text-slate-500 mb-6 space-x-2">
        <span className="cursor-pointer hover:text-slate-900 transition-colors" onClick={() => navigate('/events')}>Events</span>
        <span>›</span>
        <span className="cursor-pointer hover:text-slate-900 transition-colors" onClick={() => navigate(`/events/${eventId}`)}>{event?.name || 'Event'}</span>
        <span>›</span>
        <span className="text-slate-900">Manage Participants</span>
      </div>

      <div className="flex justify-between items-start mb-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Participants</h1>
          <p className="text-slate-500 font-medium">Manage and import participants for {event?.name}</p>
        </div>
        <button onClick={() => navigate(`/events/${eventId}`)} className="bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 px-4 py-2.5 rounded-xl font-medium transition-colors flex items-center text-sm shadow-sm">
          <ArrowLeft size={16} className="mr-2" /> Back to Event
        </button>
      </div>

      <div className="grid grid-cols-3 gap-8">
        <div className="col-span-1 space-y-6">
          <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
            <h3 className="text-lg font-bold text-slate-900 mb-4">Import Data</h3>
            
            <div 
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleFileDrop}
              className={`border-2 border-dashed rounded-2xl p-8 text-center transition-colors cursor-pointer
                ${file ? 'border-blue-500 bg-blue-50' : 'border-slate-200 hover:border-blue-400 hover:bg-slate-50'}`}
              onClick={() => !file && fileInputRef.current?.click()}
            >
              <input type="file" ref={fileInputRef} className="hidden" accept=".csv,.xlsx" onChange={handleFileSelect} />
              
              {!file ? (
                <>
                  <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Upload size={24} className="text-blue-600" />
                  </div>
                  <p className="font-semibold text-slate-900 mb-1">Click or drag file to upload</p>
                  <p className="text-xs text-slate-500">Supports .CSV and .XLSX files</p>
                </>
              ) : (
                <>
                  <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <FileType size={24} className="text-white" />
                  </div>
                  <p className="font-bold text-blue-700 mb-1">{file.name}</p>
                  <p className="text-xs text-blue-500 mb-4">{(file.size / 1024).toFixed(1)} KB</p>
                  <div className="flex space-x-3 justify-center">
                    <button onClick={(e) => { e.stopPropagation(); handleUpload(); }} disabled={uploadMutation.isPending} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded-lg shadow-sm">
                      {uploadMutation.isPending ? 'Uploading...' : 'Confirm Import'}
                    </button>
                    <button onClick={(e) => { e.stopPropagation(); setFile(null); }} className="px-4 py-2 bg-white text-slate-700 text-sm font-bold rounded-lg border border-slate-200 hover:bg-slate-50">
                      Cancel
                    </button>
                  </div>
                </>
              )}
            </div>
            
            {error && (
              <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-xl text-sm flex items-start">
                <AlertTriangle size={16} className="mr-2 mt-0.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}
            
            {uploadResult && (
              <div className="mt-4 p-4 bg-green-50 rounded-xl">
                <div className="flex items-center text-green-700 font-bold mb-2">
                  <CheckCircle2 size={16} className="mr-2" /> Import Complete
                </div>
                <div className="text-sm text-green-800 space-y-1">
                  <p>Total Processed: <strong>{uploadResult.total}</strong></p>
                  <p>Valid Records: <strong>{uploadResult.valid}</strong></p>
                  <p className="text-red-600">Invalid Records: <strong>{uploadResult.errors}</strong></p>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="col-span-2">
          <div className="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
              <h3 className="font-bold text-slate-900 flex items-center">
                <Users size={18} className="mr-2 text-blue-600" /> Imported Participants ({participants?.length || 0})
              </h3>
            </div>
            
            <div className="overflow-x-auto max-h-[600px] custom-scrollbar">
              <table className="w-full text-left">
                <thead className="bg-white sticky top-0 border-b border-slate-200">
                  <tr className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                    <th className="py-4 px-6">Name</th>
                    <th className="py-4 px-6">Email</th>
                    <th className="py-4 px-6">Role</th>
                    <th className="py-4 px-6 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {isLoading ? (
                    <tr><td colSpan={4} className="py-8 text-center text-slate-500">Loading...</td></tr>
                  ) : participants?.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="py-16 text-center text-slate-500">
                        <FileSpreadsheet size={32} className="mx-auto mb-4 text-slate-300" />
                        <p>No participants found.</p>
                        <p className="text-xs mt-1">Import a CSV file to get started.</p>
                      </td>
                    </tr>
                  ) : (
                    participants?.map((p: any) => (
                      <tr key={p.id} className="border-b border-slate-50 hover:bg-slate-50/50">
                        <td className="py-4 px-6 font-semibold text-slate-900">{p.name}</td>
                        <td className="py-4 px-6 text-slate-600">{p.email || '-'}</td>
                        <td className="py-4 px-6 text-slate-600">
                          {p.role ? <span className="px-2.5 py-1 bg-slate-100 rounded-md text-xs font-medium">{p.role}</span> : '-'}
                        </td>
                        <td className="py-4 px-6 text-right">
                          <button 
                            onClick={() => { if(window.confirm('Delete participant?')) deleteMutation.mutate(p.id); }}
                            className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                          >
                            <Trash2 size={16} />
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
'''
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("ParticipantsManager created")
