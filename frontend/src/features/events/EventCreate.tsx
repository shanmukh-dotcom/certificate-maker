import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createEvent } from '../../api/events';
import { ArrowLeft } from 'lucide-react';

export const EventCreate = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const mutation = useMutation({
    mutationFn: createEvent,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['events'] });
      navigate('/events/' + data.id);
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create event');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Event name is required');
      return;
    }
    mutation.mutate({ name, description });
  };

  return (
    <div className="max-w-3xl mx-auto animate-in fade-in duration-500">
      <button 
        onClick={() => navigate('/events')}
        className="flex items-center text-sm font-medium text-slate-500 hover:text-slate-900 mb-8 transition-colors"
      >
        <ArrowLeft size={16} className="mr-2" />
        Back to Events
      </button>

      <div className="bg-white rounded-3xl p-10 shadow-sm border border-slate-100">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">Create New Event</h1>
        <p className="text-slate-500 mb-8">Set up a new workspace for your upcoming certificates.</p>

        {error && <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-xl text-sm">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-slate-900 mb-2">Event Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all text-sm text-slate-900 bg-slate-50 focus:bg-white"
              placeholder="e.g. HARVEST Workshop 2026"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-900 mb-2">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all text-sm text-slate-900 bg-slate-50 focus:bg-white resize-none"
              placeholder="A brief description of the event..."
            />
          </div>

          <div className="flex justify-end pt-4">
            <button
              type="submit"
              disabled={mutation.isPending}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-medium shadow-lg shadow-blue-600/20 transition-all disabled:opacity-50"
            >
              {mutation.isPending ? 'Creating...' : 'Create Event Workspace'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
