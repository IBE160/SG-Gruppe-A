'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GapAnalysisDisplay from '../../components/analysis/GapAnalysisDisplay';
import CoverLetterGenerator from '../../components/analysis/CoverLetterGenerator';
import { createClient } from '@/utils/supabase/client';
import toast from 'react-hot-toast';

export default function AnalysisPage() {
  const [cvText, setCvText] = useState('');
  const [jdText, setJdText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  useEffect(() => {
    // Fetch latest CV and JD on mount
    const fetchData = async () => {
      try {
        const supabase = createClient();
        const { data: { session } } = await supabase.auth.getSession();
        const token = session?.access_token;
        
        if (!token) {
            console.log("No token found in AnalysisPage useEffect");
            return;
        }

        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };

        // Fetch CV
        try {
          console.log("Fetching latest CV...");
          const cvRes = await axios.get(`${API_URL}/api/cv/latest`, config);
          console.log("CV Response:", cvRes.data);
          if (cvRes.data && cvRes.data.extracted_text) {
            setCvText(cvRes.data.extracted_text);
            toast.success('Loaded latest CV');
          } else {
             console.log("CV found but no extracted_text");
          }
        } catch (e: any) {
            console.error("Error fetching CV:", e.response?.data || e.message);
        }

        // Fetch JD
        try {
          console.log("Fetching latest JD...");
          const jdRes = await axios.get(`${API_URL}/api/job-description/latest`, config);
          console.log("JD Response:", jdRes.data);
          if (jdRes.data && jdRes.data.content) {
            setJdText(jdRes.data.content);
            toast.success('Loaded latest Job Description');
          }
        } catch (e: any) {
            console.error("Error fetching JD:", e.response?.data || e.message);
        }

      } catch (err) {
        console.error("Error loading data", err);
      }
    };
    fetchData();
  }, []);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;
      
      const headers = token ? { Authorization: `Bearer ${token}` } : {};

      const response = await axios.post(`${API_URL}/ai/analyze-gap/`, {
        cv_text: cvText,
        job_description: jdText
      }, { headers });
      
      setResult(response.data);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 md:p-8 max-w-7xl">
      <h1 className="text-3xl font-bold mb-6 text-white">Application Analysis</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column: Inputs and Analysis */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">1. Inputs</h2>
            <div className="space-y-4">
              <div>
                <label htmlFor="cv-text" className="block text-sm font-medium text-gray-700 mb-2">Your CV Text</label>
                <textarea
                  id="cv-text"
                  className="w-full h-48 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 text-gray-800 bg-white placeholder-gray-400"
                  value={cvText}
                  onChange={(e) => setCvText(e.target.value)}
                  placeholder="Paste your CV content here..."
                />
              </div>
              <div>
                <label htmlFor="jd-text" className="block text-sm font-medium text-gray-700 mb-2">Job Description</label>
                <textarea
                  id="jd-text"
                  className="w-full h-48 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 text-gray-800 bg-white placeholder-gray-400"
                  value={jdText}
                  onChange={(e) => setJdText(e.target.value)}
                  placeholder="Paste the job description here..."
                />
              </div>
              
              <button
                onClick={handleAnalyze}
                disabled={loading || !cvText || !jdText}
                className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                {loading ? 'Analyzing...' : 'Analyze Gap'}
              </button>
            </div>
          </div>

          <GapAnalysisDisplay result={result} isLoading={loading} error={error} />
        </div>

        {/* Right Column: Generated Letter */}
        <div className="lg:border-l lg:pl-8 lg:border-gray-200">
           {(cvText && jdText) ? (
             <CoverLetterGenerator cvText={cvText} jdText={jdText} />
           ) : (
             <div className="bg-gray-50 p-6 rounded-lg border-2 border-dashed border-gray-300 text-center text-gray-500 h-full flex items-center justify-center">
                <p>Enter your CV and a Job Description to generate a cover letter.</p>
             </div>
           )}
        </div>
      </div>
    </div>
  );
}