import React, { useState } from 'react';
import { useAuthStore } from '../../store/authStore';
import { loginApi } from '../../api/auth';
import { useNavigate } from 'react-router-dom';
import { GraduationCap, FileText, Users, ShieldCheck, BarChart2, User, Lock, Eye, EyeOff } from 'lucide-react';

export const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const setToken = useAuthStore((state) => state.setToken);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      const data = await loginApi(username, password);
      setToken(data.access_token);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4 font-sans text-slate-900">
      <div className="flex flex-col md:flex-row bg-white rounded-3xl overflow-hidden shadow-2xl max-w-6xl w-full h-[calc(100vh-2rem)] border border-gray-100">
        
        {/* Left Side */}
        <div className="hidden md:flex flex-col justify-between w-1/2 p-10 bg-gradient-to-br from-slate-50 to-blue-50/30">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-2xl font-black tracking-widest text-slate-900">CERTIFY</span>
            </div>
            <p className="text-xs font-semibold tracking-[0.2em] text-slate-400 mb-10">
              CREATE &nbsp;|&nbsp; ISSUE &nbsp;|&nbsp; VERIFY &nbsp;|&nbsp; EMPOWER
            </p>
            
            <h1 className="text-5xl font-bold leading-tight mb-4 text-slate-900">
              Certificates<br />
              for a brighter<br />
              <span className="text-blue-600">tomorrow.</span>
            </h1>
            
            <div className="w-12 h-1 bg-blue-600 mb-6 rounded-full"></div>
            
            <p className="text-lg text-slate-500 mb-10 max-w-md">
              A simple and powerful platform for managing event certificates.
            </p>
            
            <div className="flex space-x-6">
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-2 text-blue-600">
                  <FileText size={22} strokeWidth={1.5} />
                </div>
                <span className="text-xs font-medium text-slate-600 text-center leading-tight">Create<br/>Events</span>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-2 text-blue-600">
                  <Users size={22} strokeWidth={1.5} />
                </div>
                <span className="text-xs font-medium text-slate-600 text-center leading-tight">Issue<br/>Certificates</span>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-2 text-blue-600">
                  <ShieldCheck size={22} strokeWidth={1.5} />
                </div>
                <span className="text-xs font-medium text-slate-600 text-center leading-tight">Ensure<br/>Authenticity</span>
              </div>
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-2 text-blue-600">
                  <BarChart2 size={22} strokeWidth={1.5} />
                </div>
                <span className="text-xs font-medium text-slate-600 text-center leading-tight">Build<br/>Impact</span>
              </div>
            </div>
          </div>
          
          <div className="mt-4">
            <p className="text-slate-500 italic text-base mb-2">"People grow when their efforts are recognized."</p>
            <p className="text-xs font-semibold tracking-widest text-slate-400 uppercase">— CERTIFY</p>
          </div>
        </div>
        
        {/* Right Side */}
        <div className="w-full md:w-1/2 p-8 md:p-12 flex flex-col items-center justify-center relative">
          <div className="absolute top-6 right-6 flex space-x-4 text-slate-400 text-sm font-medium">
            <span className="cursor-pointer hover:text-slate-900 transition-colors">EN ∨</span>
          </div>
          
          <div className="w-full max-w-sm flex flex-col items-center">
            <div className="mb-3">
               <div className="w-16 h-16 bg-blue-600 text-white rounded-xl flex items-center justify-center mb-4 shadow-lg shadow-blue-600/30">
                  <GraduationCap size={32} />
               </div>
            </div>
            <h2 className="text-xl font-black tracking-widest text-slate-900 mb-1">CERTIFY</h2>
            <p className="text-slate-500 text-sm mb-8">Certificate Management Platform</p>
            
            <h3 className="text-2xl font-bold text-slate-900 mb-1">Welcome Back</h3>
            <p className="text-slate-500 mb-6 text-sm">Sign in to continue to your workspace.</p>
            
            <form onSubmit={handleLogin} className="w-full">
              {error && <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-xl text-sm">{error}</div>}
              
              <div className="mb-5">
                <label className="block text-sm font-medium text-slate-700 mb-2">Email / Username</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
                    <User size={18} />
                  </div>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all text-sm text-slate-700"
                    placeholder="Enter your email or username"
                    required
                  />
                </div>
              </div>
              
              <div className="mb-2">
                <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
                    <Lock size={18} />
                  </div>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-11 pr-12 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all text-sm text-slate-700"
                    placeholder="Enter your password"
                    required
                  />
                  <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="text-slate-400 hover:text-slate-600">
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="flex justify-end mb-8">
                <a href="#" className="text-sm font-medium text-blue-600 hover:text-blue-700">Forgot password?</a>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3.5 rounded-xl transition-colors shadow-lg shadow-blue-600/20 flex items-center justify-center space-x-2"
              >
                <span>{loading ? 'Signing In...' : 'Sign In'}</span>
                {!loading && <span>→</span>}
              </button>
            </form>
            
            <div className="flex items-center w-full my-8">
              <div className="flex-grow border-t border-slate-100"></div>
              <span className="flex-shrink-0 mx-4 text-slate-400 text-sm">or</span>
              <div className="flex-grow border-t border-slate-100"></div>
            </div>
            
            <div className="w-full bg-slate-50 p-4 rounded-xl flex items-start space-x-4 text-sm text-slate-600 border border-slate-100">
              <Users className="text-slate-400 shrink-0 mt-0.5" size={20} />
              <div>
                <p className="font-medium text-slate-800">Access restricted to authorized club core members.</p>
                <p className="text-slate-500">Need an account? Contact your club administrator.</p>
              </div>
            </div>
            
          </div>
        </div>
        
      </div>
    </div>
  );
};
