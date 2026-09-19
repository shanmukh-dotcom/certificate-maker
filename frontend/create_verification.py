import os

files = {
    'src/api/verification.ts': '''import { apiClient } from './client';

export const verifyCertificate = async (certificateId: string) => {
  const response = await apiClient.get(`/certificates/verify/${certificateId}`);
  return response.data;
};
''',

    'src/features/verification/PublicVerification.tsx': '''import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { verifyCertificate } from '../../api/verification';
import { ShieldCheck, Search, CheckCircle2, XCircle, AlertTriangle, Calendar, Building, User, FileBadge } from 'lucide-react';

export const PublicVerification = () => {
  const [certificateId, setCertificateId] = useState('');
  const [result, setResult] = useState<any>(null);
  const [errorStatus, setErrorStatus] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: verifyCertificate,
    onSuccess: (data) => {
      setResult(data);
      setErrorStatus(null);
    },
    onError: (error: any) => {
      setResult(null);
      if (error.response?.status === 404) setErrorStatus('NOT_FOUND');
      else if (error.response?.data?.detail === 'CERTIFICATE REVOKED') setErrorStatus('REVOKED');
      else setErrorStatus('INVALID');
    }
  });

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    if (!certificateId.trim()) return;
    mutation.mutate(certificateId.trim());
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl animate-in fade-in slide-in-from-bottom-4 duration-700">
        
        {/* Header */}
        <div className="text-center mb-10">
          <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl shadow-blue-600/20">
            <ShieldCheck size={32} className="text-white" />
          </div>
          <h1 className="text-3xl font-black tracking-tight text-slate-900 mb-2">CERTIFY</h1>
          <p className="text-slate-500 font-medium">Official Certificate Verification Portal</p>
        </div>

        {/* Search Box */}
        <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 mb-8">
          <form onSubmit={handleVerify} className="relative">
            <label className="block text-sm font-bold text-slate-700 mb-3 ml-1">Enter Certificate ID</label>
            <div className="relative flex items-center">
              <Search size={20} className="absolute left-4 text-slate-400" />
              <input
                type="text"
                value={certificateId}
                onChange={(e) => setCertificateId(e.target.value)}
                placeholder="e.g. HARVEST-2026-0306"
                className="w-full pl-12 pr-32 py-4 bg-slate-50 border border-slate-200 rounded-2xl font-medium text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all focus:bg-white uppercase"
              />
              <button 
                type="submit"
                disabled={mutation.isPending || !certificateId.trim()}
                className="absolute right-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold text-sm rounded-xl transition-colors shadow-sm"
              >
                {mutation.isPending ? 'Checking...' : 'Verify'}
              </button>
            </div>
          </form>
        </div>

        {/* Results Area */}
        {result && (
          <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center justify-center space-x-3 mb-8 pb-8 border-b border-slate-100">
              <div className="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center">
                <CheckCircle2 size={24} className="text-green-600" />
              </div>
              <div>
                <h2 className="text-xl font-black text-slate-900">Certificate is Valid</h2>
                <p className="text-sm text-green-600 font-semibold flex items-center mt-1">
                  <ShieldCheck size={14} className="mr-1" /> Authenticity Verified
                </p>
              </div>
            </div>

            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <User size={20} className="text-slate-400 mt-1 shrink-0" />
                <div>
                  <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Issued To</p>
                  <p className="text-lg font-bold text-slate-900">{result.name}</p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <FileBadge size={20} className="text-slate-400 mt-1 shrink-0" />
                <div>
                  <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">For Participation In</p>
                  <p className="text-base font-bold text-slate-900">{result.event_name}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div className="flex items-start space-x-4">
                  <Building size={20} className="text-slate-400 mt-1 shrink-0" />
                  <div>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Issued By</p>
                    <p className="text-sm font-semibold text-slate-700">{result.issued_by}</p>
                  </div>
                </div>
                
                <div className="flex items-start space-x-4">
                  <Calendar size={20} className="text-slate-400 mt-1 shrink-0" />
                  <div>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Issued On</p>
                    <p className="text-sm font-semibold text-slate-700">
                      {new Date(result.issued_on).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {errorStatus === 'NOT_FOUND' && (
          <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <Search size={24} className="text-slate-400" />
            </div>
            <h2 className="text-lg font-black text-slate-900 mb-2">Certificate Not Found</h2>
            <p className="text-sm text-slate-500">We couldn't find a certificate matching that ID. Please check for typos and try again.</p>
          </div>
        )}

        {errorStatus === 'REVOKED' && (
          <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <XCircle size={32} className="text-red-500" />
            </div>
            <h2 className="text-lg font-black text-slate-900 mb-2">Certificate Revoked</h2>
            <p className="text-sm text-red-600 font-medium">This certificate has been administratively revoked by the issuing organization and is no longer valid.</p>
          </div>
        )}

        {errorStatus === 'INVALID' && (
          <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="w-16 h-16 bg-orange-50 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertTriangle size={32} className="text-orange-500" />
            </div>
            <h2 className="text-lg font-black text-slate-900 mb-2">Invalid Certificate</h2>
            <p className="text-sm text-orange-600 font-medium">This certificate is invalid or has encountered an error.</p>
          </div>
        )}

      </div>
      
      <div className="mt-auto pt-12 pb-4 text-center">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Powered by CERTIFY</p>
      </div>
    </div>
  );
};
'''
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
