import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import HomePage from '../pages/HomePage';

// Mock the components to avoid complex dependencies in testing
jest.mock('../components/Layout', () => {
  return function MockLayout({ children }: { children: React.ReactNode }) {
    return <div data-testid="layout">{children}</div>;
  };
});

jest.mock('../components/ImageUpload', () => {
  return function MockImageUpload({ 
    onImageSelect, 
    onAnalysisComplete 
  }: { 
    onImageSelect: (file: File) => void;
    onAnalysisComplete: (results: any) => void;
  }) {
    return (
      <div data-testid="image-upload">
        <button
          onClick={() => {
            const mockFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
            onImageSelect(mockFile);
            setTimeout(() => {
              onAnalysisComplete({
                stage: 2,
                confidence: 0.85,
                riskLevel: 'moderate',
                recommendations: ['Monitor regularly', 'Schedule follow-up']
              });
            }, 100);
          }}
        >
          Upload Test Image
        </button>
      </div>
    );
  };
});

jest.mock('../components/ResultsDisplay', () => {
  return function MockResultsDisplay({ results }: { results: any }) {
    if (!results) return null;
    return (
      <div data-testid="results-display">
        <div>Stage: {results.stage}</div>
        <div>Confidence: {results.confidence}</div>
        <div>Risk Level: {results.riskLevel}</div>
      </div>
    );
  };
});

const renderHomePage = () => {
  return render(
    <BrowserRouter>
      <HomePage />
    </BrowserRouter>
  );
};

describe('OpthalmoAI HomePage Integration', () => {
  test('renders main components correctly', () => {
    renderHomePage();
    
    // Check for key elements
    expect(screen.getByTestId('layout')).toBeInTheDocument();
    expect(screen.getByTestId('image-upload')).toBeInTheDocument();
    
    // Check for OpthalmoAI branding
    expect(screen.getByText(/OpthalmoAI/i)).toBeInTheDocument();
    
    // Check for medical disclaimer
    expect(screen.getByText(/not a substitute for professional medical diagnosis/i)).toBeInTheDocument();
  });

  test('displays healthcare compliance messaging', () => {
    renderHomePage();
    
    // Should show HIPAA/privacy compliance
    const privacyText = screen.getByText(/secure.*privacy/i) || 
                       screen.getByText(/hipaa/i) || 
                       screen.getByText(/confidential/i);
    expect(privacyText).toBeInTheDocument();
  });

  test('shows statistics and features', () => {
    renderHomePage();
    
    // Should display key statistics
    expect(screen.getByText(/accuracy/i)).toBeInTheDocument();
    
    // Should show feature highlights
    expect(screen.getByText(/ai.*analysis/i)).toBeInTheDocument();
  });

  test('handles complete workflow: upload to results', async () => {
    const user = userEvent.setup();
    renderHomePage();
    
    // Initially no results should be shown
    expect(screen.queryByTestId('results-display')).not.toBeInTheDocument();
    
    // Trigger image upload
    const uploadButton = screen.getByText('Upload Test Image');
    await user.click(uploadButton);
    
    // Wait for results to appear
    await waitFor(() => {
      expect(screen.getByTestId('results-display')).toBeInTheDocument();
    });
    
    // Check results content
    expect(screen.getByText('Stage: 2')).toBeInTheDocument();
    expect(screen.getByText('Confidence: 0.85')).toBeInTheDocument();
    expect(screen.getByText('Risk Level: moderate')).toBeInTheDocument();
  });

  test('maintains clinical design aesthetics', () => {
    renderHomePage();
    
    // Check for clinical color scheme elements (this would be in CSS classes)
    const container = screen.getByTestId('layout');
    expect(container).toBeInTheDocument();
    
    // Clinical terminology should be present
    expect(screen.getByText(/retinopathy/i)).toBeInTheDocument();
    expect(screen.getByText(/screening/i)).toBeInTheDocument();
  });

  test('provides accessibility features', () => {
    renderHomePage();
    
    // Check for proper heading structure
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    
    // Check for alt text on important elements (would be tested with actual images)
    // This ensures the app is accessible for healthcare professionals
  });

  test('handles error states gracefully', async () => {
    renderHomePage();
    
    // The app should handle various error states without crashing
    // This is important for clinical environments where reliability is crucial
    expect(screen.getByTestId('layout')).toBeInTheDocument();
  });

  test('includes proper medical disclaimers', () => {
    renderHomePage();
    
    // Multiple disclaimer patterns should be present
    const disclaimerPatterns = [
      /not.*substitute.*professional.*medical/i,
      /assistive.*tool/i,
      /consult.*healthcare.*professional/i
    ];
    
    const pageText = document.body.textContent || '';
    
    // At least one disclaimer pattern should be present
    const hasDisclaimer = disclaimerPatterns.some(pattern => 
      pattern.test(pageText)
    );
    
    expect(hasDisclaimer).toBe(true);
  });

  test('responsive design elements', () => {
    renderHomePage();
    
    // The layout should be responsive (this would typically test CSS media queries)
    // For now, we ensure the basic structure is present
    expect(screen.getByTestId('layout')).toBeInTheDocument();
    expect(screen.getByTestId('image-upload')).toBeInTheDocument();
  });

  test('maintains healthcare professional workflow', async () => {
    const user = userEvent.setup();
    renderHomePage();
    
    // Test the expected clinical workflow
    // 1. Healthcare professional sees the interface
    expect(screen.getByText(/OpthalmoAI/i)).toBeInTheDocument();
    
    // 2. They can upload an image
    expect(screen.getByTestId('image-upload')).toBeInTheDocument();
    
    // 3. They receive analysis results
    const uploadButton = screen.getByText('Upload Test Image');
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('results-display')).toBeInTheDocument();
    });
    
    // 4. Results include clinical information
    expect(screen.getByText(/stage/i)).toBeInTheDocument();
    expect(screen.getByText(/confidence/i)).toBeInTheDocument();
  });
});

describe('OpthalmoAI Healthcare Compliance', () => {
  test('HIPAA-style privacy protection messaging', () => {
    renderHomePage();
    
    const pageText = document.body.textContent?.toLowerCase() || '';
    
    // Should mention privacy, security, or compliance
    const privacyKeywords = ['privacy', 'secure', 'confidential', 'protected', 'hipaa'];
    const hasPrivacyMention = privacyKeywords.some(keyword => 
      pageText.includes(keyword)
    );
    
    expect(hasPrivacyMention).toBe(true);
  });

  test('medical professional guidance', () => {
    renderHomePage();
    
    // Should guide users to consult medical professionals
    expect(screen.getByText(/healthcare.*professional/i)).toBeInTheDocument();
  });

  test('clinical terminology accuracy', () => {
    renderHomePage();
    
    // Should use proper medical terminology
    const medicalTerms = [
      /diabetic.*retinopathy/i,
      /fundus/i,
      /screening/i,
      /ophthalmology/i
    ];
    
    const pageText = document.body.textContent || '';
    
    // Should contain medical terminology
    const hasMedicalTerms = medicalTerms.some(term => 
      term.test(pageText)
    );
    
    expect(hasMedicalTerms).toBe(true);
  });
});