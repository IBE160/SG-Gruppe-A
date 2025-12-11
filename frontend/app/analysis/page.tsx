'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GapAnalysisDisplay from '../../components/analysis/GapAnalysisDisplay';
import { createClient } from '@/utils/supabase/client';
import toast from 'react-hot-toast';

export default function AnalysisPage() {
  const [cvText, setCvText] = useState('');
  const [jdText, setJdText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
          const cvRes = await axios.get('http://127.0.0.1:8000/api/cv/latest', config);
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
          const jdRes = await axios.get('http://127.0.0.1:8000/api/job-description/latest', config);
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

      const response = await axios.post('http://127.0.0.1:8000/ai/analyze-gap/', {
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
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">CV Gap Analysis</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-white mb-2">Your CV Text</label>
          <textarea
            className="w-full h-64 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 text-white bg-gray-900 placeholder-gray-400"
            value={cvText}
            onChange={(e) => setCvText(e.target.value)}
            placeholder="Paste your CV content here..."
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-white mb-2">Job Description</label>
          <textarea
            className="w-full h-64 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 text-white bg-gray-900 placeholder-gray-400"
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste the job description here..."
          />
        </div>
      </div>

      <div className="text-center">
        <button
          onClick={handleAnalyze}
          disabled={loading || !cvText || !jdText}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          {loading ? 'Analyzing...' : 'Analyze Gap'}
        </button>
      </div>

      <GapAnalysisDisplay result={result} isLoading={loading} error={error} />
    </div>
  );
}