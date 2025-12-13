'use client';

import React, { useState } from 'react';
import axios from 'axios';
import { createClient } from '@/utils/supabase/client';
import toast from 'react-hot-toast';
import { Copy, Check } from 'lucide-react';

interface CoverLetterGeneratorProps {
  cvText: string;
  jdText: string;
}

const CoverLetterGenerator: React.FC<CoverLetterGeneratorProps> = ({ cvText, jdText }) => {
  const [generatedLetter, setGeneratedLetter] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isCopied, setIsCopied] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setGeneratedLetter('');

    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;
      
      const headers = token ? { Authorization: `Bearer ${token}` } : {};

      const response = await axios.post('http://127.0.0.1:8000/api/v1/generation/cover-letter', {
        cv_text: cvText,
        job_description_text: jdText
      }, { headers });

      if (response.data && response.data.cover_letter) {
        setGeneratedLetter(response.data.cover_letter);
        toast.success('Cover letter generated!');
      } else {
        throw new Error('No cover letter returned');
      }
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || 'Failed to generate cover letter');
      toast.error('Generation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!generatedLetter) return;
    try {
      await navigator.clipboard.writeText(generatedLetter);
      toast.success('Copied to clipboard!');
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
      toast.error('Failed to copy to clipboard');
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mt-6">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Cover Letter Assistant</h2>
      
      {!generatedLetter && (
        <div className="text-center">
          <p className="mb-4 text-gray-600">Generate a tailored cover letter in Norwegian based on your CV and the job description.</p>
          <button
            onClick={handleGenerate}
            disabled={loading || !cvText || !jdText}
            className="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400 transition flex items-center justify-center mx-auto"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating... (this may take up to 2 mins)
              </>
            ) : 'Generate Cover Letter'}
          </button>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {generatedLetter && (
        <div className="mt-6 animate-fade-in">
          <h3 className="text-lg font-semibold mb-2 text-gray-700">Generated Cover Letter</h3>
          <textarea
            className="w-full h-96 p-4 border rounded-lg focus:ring-2 focus:ring-green-500 text-gray-800 font-serif leading-relaxed"
            value={generatedLetter}
            onChange={(e) => setGeneratedLetter(e.target.value)}
          />
          <div className="mt-4 flex justify-end space-x-4">
             <button
              onClick={handleCopy}
              className="px-4 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50 flex items-center space-x-2"
            >
              {isCopied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
              <span>{isCopied ? 'Copied!' : 'Copy to Clipboard'}</span>
            </button>
             <button
              onClick={() => setGeneratedLetter('')}
              className="px-4 py-2 text-gray-500 hover:text-gray-700"
            >
              Start Over
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CoverLetterGenerator;
