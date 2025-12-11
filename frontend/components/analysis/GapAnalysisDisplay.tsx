import React from 'react';

interface GapAnalysisResult {
  missing_skills: string[];
  missing_qualifications: string[];
  match_percentage: number;
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
      <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
      
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2">Match Score</h3>
        <div className="flex items-center">
          <div className="w-full bg-gray-200 rounded-full h-4 mr-4">
            <div 
              className={`h-4 rounded-full ${result.match_percentage > 70 ? 'bg-green-500' : result.match_percentage > 40 ? 'bg-yellow-500' : 'bg-red-500'}`}
              style={{ width: `${result.match_percentage}%` }}
            ></div>
          </div>
          <span className="font-bold text-xl">{result.match_percentage}%</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold mb-2 text-red-600">Missing Skills</h3>
          {result.missing_skills.length === 0 ? (
            <p className="text-green-600">Great job! No major skills missing.</p>
          ) : (
            <ul className="list-disc list-inside space-y-1">
              {result.missing_skills.map((skill, index) => (
                <li key={index} className="text-gray-700">{skill}</li>
              ))}
            </ul>
          )}
        </div>

        <div>
          <h3 className="text-lg font-semibold mb-2 text-red-600">Missing Qualifications</h3>
          {result.missing_qualifications.length === 0 ? (
            <p className="text-green-600">You meet the core qualifications.</p>
          ) : (
            <ul className="list-disc list-inside space-y-1">
              {result.missing_qualifications.map((qual, index) => (
                <li key={index} className="text-gray-700">{qual}</li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default GapAnalysisDisplay;
