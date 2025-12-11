import { render, screen } from '@testing-library/react';
import GapAnalysisDisplay from '../components/analysis/GapAnalysisDisplay';
import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom';

describe('GapAnalysisDisplay', () => {
  const mockResult = {
    missing_skills: ['Skill A'],
    missing_qualifications: ['Qual B'],
    match_percentage: 80,
    ats_score_summary: 'Good match',
    actionable_suggestions: ['Suggestion 1', 'Suggestion 2']
  };

  it('renders SuggestionsList when actionable_suggestions are present', () => {
    render(
      <GapAnalysisDisplay 
        result={mockResult} 
        isLoading={false} 
        error={null} 
      />
    );

    expect(screen.getByText('Actionable Suggestions')).toBeInTheDocument();
    expect(screen.getByText('Suggestion 1')).toBeInTheDocument();
    expect(screen.getByText('Suggestion 2')).toBeInTheDocument();
  });

  it('does not render SuggestionsList when actionable_suggestions are undefined', () => {
    const resultWithoutSuggestions = {
      ...mockResult,
      actionable_suggestions: undefined
    };

    render(
      <GapAnalysisDisplay 
        result={resultWithoutSuggestions} 
        isLoading={false} 
        error={null} 
      />
    );

    expect(screen.queryByText('Actionable Suggestions')).not.toBeInTheDocument();
  });
});
