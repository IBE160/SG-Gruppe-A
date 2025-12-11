import React from 'react';

interface ATSScoreGaugeProps {
  score: number;
  summary?: string;
}

const ATSScoreGauge: React.FC<ATSScoreGaugeProps> = ({ score, summary }) => {
  const radius = 60;
  const stroke = 8;
  const normalizedRadius = radius - stroke * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let color = 'text-red-500';
  if (score >= 70) color = 'text-green-500';
  else if (score >= 40) color = 'text-yellow-500';

  return (
    <div className="flex flex-col items-center p-4">
      <div className="relative flex items-center justify-center">
        <svg
          height={radius * 2}
          width={radius * 2}
          className="transform -rotate-90"
        >
          <circle
            stroke="currentColor"
            strokeWidth={stroke}
            fill="transparent"
            r={normalizedRadius}
            cx={radius}
            cy={radius}
            className="text-gray-200"
          />
          <circle
            stroke="currentColor"
            strokeWidth={stroke}
            strokeDasharray={circumference + ' ' + circumference}
            style={{ strokeDashoffset }}
            strokeLinecap="round"
            fill="transparent"
            r={normalizedRadius}
            cx={radius}
            cy={radius}
            className={`${color} transition-all duration-1000 ease-out`}
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
             <span className="text-3xl font-bold text-gray-800">{score}</span>
             <span className="text-xs text-gray-500">ATS Score</span>
        </div>
      </div>
      {summary && (
        <div className="mt-4 text-center">
             <h4 className="font-semibold text-gray-700 mb-1">Score Insight</h4>
             <p className="text-gray-600 text-sm max-w-sm italic">
               "{summary}"
             </p>
        </div>
      )}
    </div>
  );
};

export default ATSScoreGauge;
