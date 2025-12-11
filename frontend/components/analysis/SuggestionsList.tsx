import React from 'react';

interface SuggestionsListProps {
  suggestions: string[];
}

const SuggestionsList: React.FC<SuggestionsListProps> = ({ suggestions }) => {
  return (
    <div className="bg-blue-50 p-4 rounded-lg mt-6">
      <h3 className="text-lg font-semibold mb-2 text-blue-700 border-b border-blue-200 pb-2">
        Actionable Suggestions
      </h3>
      {suggestions.length === 0 ? (
        <p className="text-gray-500 italic">No specific suggestions generated.</p>
      ) : (
        <ul className="list-disc list-inside space-y-2">
          {suggestions.map((suggestion, index) => (
            <li key={index} className="text-gray-700 text-sm">
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SuggestionsList;
