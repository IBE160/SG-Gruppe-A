import { render, screen } from '@testing-library/react';
import SuggestionsList from '../components/analysis/SuggestionsList';
import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom';

describe('SuggestionsList', () => {
  it('renders "Actionable Suggestions" heading', () => {
    render(<SuggestionsList suggestions={[]} />);
    expect(screen.getByText('Actionable Suggestions')).toBeInTheDocument();
  });

  it('renders a list of suggestions when provided', () => {
    const suggestions = [
      'Improve your leadership skills section',
      'Add more quantitative results',
    ];
    render(<SuggestionsList suggestions={suggestions} />);
    
    expect(screen.getByText('Improve your leadership skills section')).toBeInTheDocument();
    expect(screen.getByText('Add more quantitative results')).toBeInTheDocument();
  });

  it('renders a placeholder message when suggestions list is empty', () => {
    render(<SuggestionsList suggestions={[]} />);
    expect(screen.getByText('No specific suggestions generated.')).toBeInTheDocument();
  });
});
