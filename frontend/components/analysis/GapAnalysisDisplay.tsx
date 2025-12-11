import React from 'react';
import ATSScoreGauge from './ATSScoreGauge';
import SuggestionsList from './SuggestionsList';

interface GapAnalysisResult {
  missing_skills: string[];
  missing_qualifications: string[];
  match_percentage: number;
  ats_score_summary?: string;
  actionable_suggestions?: string[];
}

interface GapAnalysisDisplayProps {
  result: GapAnalysisResult | null;
  isLoading: boolean;
  error: string | null;
}

const GapAnalysisDisplay: React.FC<GapAnalysisDisplayProps> = ({ result, isLoading, error }) => {
  if (isLoading) return <div className="text-center p-4">Analyzing...</div>;
  if (error) return <div className="text-center text-red-500 p-4">Error: {error}</div>;
  if (!result) return null;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mt-6">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Analysis Results</h2>
      
      <div className="mb-8 flex justify-center">
        <ATSScoreGauge 
          score={result.match_percentage} 
          summary={result.ats_score_summary}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-red-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-2 text-red-700 border-b border-red-200 pb-2">Missing Skills</h3>
          {result.missing_skills.length === 0 ? (
            <p className="text-green-600">Great job! No major skills missing.</p>
          ) : (
            <ul className="list-disc list-inside space-y-2">
              {result.missing_skills.map((skill, index) => (
                <li key={index} className="text-gray-700 text-sm">{skill}</li>
              ))}
            </ul>
          )}
        </div>

        <div className="bg-yellow-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-2 text-yellow-700 border-b border-yellow-200 pb-2">Missing Qualifications</h3>
          {result.missing_qualifications.length === 0 ? (
            <p className="text-green-600">You meet the core qualifications.</p>
          ) : (
            <ul className="list-disc list-inside space-y-2">
              {result.missing_qualifications.map((qual, index) => (
                <li key={index} className="text-gray-700 text-sm">{qual}</li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {result.actionable_suggestions && (
        <SuggestionsList suggestions={result.actionable_suggestions} />
      )}
    </div>
  );
};

export default GapAnalysisDisplay;
