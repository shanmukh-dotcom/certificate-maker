import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getCertificates, revokeCertificate } from '../../api/certificates';
import { Search, Filter, Download, Mail, Ban, CheckCircle2, AlertTriangle, FileBadge, MoreVertical } from 'lucide-react';

export const CertificateManager = () => {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  
  const { data: certificates, isLoading } = useQuery({
    queryKey: ['certificates'],
    queryFn: getCertificates
  });

  const revokeMutation = useMutation({
    mutationFn: ({ id, reason }: { id: string, reason: string }) => revokeCertificate(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['certificates'] });
    }
  });

  
  const handleDownload = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:8000/certificates/${id}/download`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
      });
      if (!response.ok) throw new Error('Download failed');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (e) {
      alert('Failed to download certificate.');
    }
  };

  const handleRevoke = (id: string) => {
    if (window.confirm('Are you sure you want to revoke this certificate? This action cannot be undone.')) {
      revokeMutation.mutate({ id, reason: 'Administrative revocation' });
    }
  };

  const filteredCerts = certificates?.filter((c: any) => 
    c.participant_name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    c.certificate_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.event_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500 pb-12">
      <div className="flex justify-between items-center">
        <div>
          <p className="text-xs font-bold tracking-[0.15em] text-slate-500 uppercase mb-2">Issued Certificates</p>
          <h1 className="text-3xl font-bold text-slate-900">Certificate Manager</h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search ID, Name or Event..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all w-64"
            />
          </div>
          <button className="flex items-center px-4 py-2.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-sm font-medium transition-colors shadow-sm">
            <Filter size={16} className="mr-2 text-slate-400" /> Filter
          </button>
        </div>
      </div>

      <div className="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50/50">
            <tr className="text-slate-500 text-sm border-b border-slate-100">
              <th className="font-medium py-4 px-6">Participant & ID</th>
              <th className="font-medium py-4 px-6">Event</th>
              <th className="font-medium py-4 px-6">Issued Date</th>
              <th className="font-medium py-4 px-6">Status</th>
              <th className="font-medium py-4 px-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="text-sm">
            {isLoading ? (
              <tr><td colSpan={5} className="py-8 text-center text-slate-500">Loading certificates...</td></tr>
            ) : filteredCerts?.length === 0 ? (
              <tr><td colSpan={5} className="py-16 text-center text-slate-500">No certificates found.</td></tr>
            ) : (
              filteredCerts?.map((cert: any) => (
                <tr key={cert.certificate_id} className="border-b border-slate-50 last:border-0 hover:bg-slate-50/50 transition-colors">
                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0">
                         <FileBadge size={18} />
                      </div>
                      <div>
                        <p className="font-bold text-slate-900">{cert.participant_name}</p>
                        <p className="text-xs font-medium text-slate-500 mt-0.5">{cert.certificate_id}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-6 font-medium text-slate-700">{cert.event_name}</td>
                  <td className="py-4 px-6 text-slate-500">
                    {new Date(cert.issued_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </td>
                  <td className="py-4 px-6">
                    {cert.status === 'ISSUED' ? (
                      <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-green-50 text-green-700">
                        <CheckCircle2 size={12} className="mr-1.5" /> Issued
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-red-50 text-red-700">
                        <AlertTriangle size={12} className="mr-1.5" /> Revoked
                      </span>
                    )}
                  </td>
                  <td className="py-4 px-6 text-right">
                    <div className="flex items-center justify-end space-x-2">
                      <button onClick={() => handleDownload(cert.certificate_id)} className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors group relative" title="Download PDF">
                        <Download size={16} />
                      </button>
                      <button className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors group relative" title="Email Certificate">
                        <Mail size={16} />
                      </button>
                      {cert.status === 'ISSUED' && (
                        <button 
                          onClick={() => handleRevoke(cert.certificate_id)}
                          className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors group relative" 
                          title="Revoke Certificate"
                        >
                          <Ban size={16} />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
