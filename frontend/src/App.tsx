import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Login } from './features/auth/Login';
import { AppLayout } from './components/layout/AppLayout';
import { Dashboard } from './features/dashboard/Dashboard';
import { EventList } from './features/events/EventList';
import { EventCreate } from './features/events/EventCreate';
import { EventWorkspace } from './features/events/EventWorkspace';
import { TemplateEditor } from './features/templates/editor/TemplateEditor';
import { GenerationCenter } from './features/generation/GenerationCenter';
import { CertificateManager } from './features/certificates/CertificateManager';
import { ParticipantsManager } from './features/participants/ParticipantsManager';

import { PublicVerification } from './features/verification/PublicVerification';




import { useAuthStore } from './store/authStore';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/verify" element={<PublicVerification />} />

          <Route path="/templates/new" element={<ProtectedRoute><TemplateEditor /></ProtectedRoute>} />

          
          <Route path="/" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            
            {/* Events routes */}
            <Route path="events">
              <Route index element={<EventList />} />
              <Route path="new" element={<EventCreate />} />
              <Route path=":id" element={<EventWorkspace />} />
            </Route>

            <Route path="templates" element={<div className="p-8">Templates placeholder</div>} />
            <Route path="participants" element={<ParticipantsManager />} />
            <Route path="certificates" element={<CertificateManager />} />
            <Route path="generation" element={<GenerationCenter />} />
            <Route path="verification" element={<div className="p-8">Verification placeholder</div>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
