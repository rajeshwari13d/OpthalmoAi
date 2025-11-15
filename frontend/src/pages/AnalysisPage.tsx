import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { ImageUpload } from '../components/ImageUpload';
import { LoadingSpinner } from '../components/LoadingComponents';
import { Card, Button, Progress, Alert } from '../components/ui';
import { analysisService } from '../services';
import { 
  Eye, 
  ArrowLeft,
  CheckCircle,
  AlertCircle,
  Brain,
  Activity,
  Shield
} from 'lucide-react';

interface AnalysisState {
  file: File | null;
  isAnalyzing: boolean;
  progress: number;
  stage: string;
  error: string | null;
}

const AnalysisPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [analysisState, setAnalysisState] = useState<AnalysisState>({
    file: null,
    isAnalyzing: false,
    progress: 0,
    stage: 'Select Image',
    error: null
  });

  // Check if we have an uploaded file from navigation state
  useEffect(() => {
    if (location.state?.file) {
      setAnalysisState(prev => ({
        ...prev,
        file: location.state.file
      }));
    }
  }, [location.state]);

  const handleImageSelect = (file: File) => {
    setAnalysisState(prev => ({
      ...prev,
      file,
      error: null
    }));
  };

  const handleStartAnalysis = async () => {
    if (!analysisState.file) return;

    setAnalysisState(prev => ({
      ...prev,
      isAnalyzing: true,
      progress: 0,
      stage: 'Preparing Image',
      error: null
    }));

    try {
      // Show progress updates during analysis
      const stages = [
        'Uploading Image',
        'Preprocessing Fundus Image', 
        'Running AI Analysis',
        'Detecting Retinal Features',
        'Assessing Diabetic Retinopathy',
        'Generating Report'
      ];

      // Start progress simulation
      let stageIndex = 0;
      const progressInterval = setInterval(() => {
        if (stageIndex < stages.length) {
          setAnalysisState(prev => ({
            ...prev,
            stage: stages[stageIndex],
            progress: ((stageIndex + 1) / stages.length) * 90 // Leave 10% for completion
          }));
          stageIndex++;
        }
      }, 1000);

      // Make actual API call
      const response = await analysisService.analyzeImage(analysisState.file);
      
      clearInterval(progressInterval);

      if (response.success && response.data) {
        setAnalysisState(prev => ({
          ...prev,
          stage: 'Analysis Complete',
          progress: 100
        }));

        const result = response.data.result;
        
        // Navigate to results with real API data
        navigate(`/results/${result.id}`, { 
          state: { 
            result: result, 
            file: analysisState.file,
            medicalDisclaimer: response.data.medical_disclaimer 
          } 
        });

      } else {
        throw new Error(response.error || 'Analysis failed');
      }

    } catch (error) {
      setAnalysisState(prev => ({
        ...prev,
        isAnalyzing: false,
        error: error instanceof Error ? error.message : 'Analysis failed. Please try again.',
        progress: 0,
        stage: 'Error'
      }));
    }
  };

  const handleGoBack = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-teal-50/50 py-4 sm:py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-6 sm:mb-8">
          <Button
            variant="ghost"
            onClick={handleGoBack}
            className="mb-4 text-slate-600 hover:text-teal-600"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
          
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <div className="flex items-center justify-center w-12 h-12 sm:w-16 sm:h-16 bg-gradient-to-r from-teal-500 to-blue-600 rounded-2xl shadow-lg">
                <Brain className="h-6 w-6 sm:h-8 sm:w-8 text-white" />
              </div>
            </div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold bg-gradient-to-r from-teal-600 to-blue-600 bg-clip-text text-transparent mb-2">
              AI Analysis Center
            </h1>
            <p className="text-slate-600 text-sm sm:text-base lg:text-lg max-w-2xl mx-auto px-4">
              Upload your retinal fundus image for comprehensive diabetic retinopathy screening using advanced AI technology.
            </p>
          </div>
        </div>

        {/* Analysis Flow */}
        {!analysisState.isAnalyzing ? (
          <div className="space-y-6 sm:space-y-8">
            {/* Image Upload Section */}
            <Card className="p-4 sm:p-6 lg:p-8" glow={!!analysisState.file}>
              <div className="text-center mb-4 sm:mb-6">
                <Eye className="w-8 h-8 sm:w-10 sm:h-10 lg:w-12 lg:h-12 mx-auto text-teal-600 mb-4" />
                <h2 className="text-xl sm:text-2xl font-bold text-slate-800 mb-2">
                  Upload Fundus Image
                </h2>
                <p className="text-slate-600 text-sm sm:text-base px-4">
                  Select a high-quality retinal fundus photograph for analysis
                </p>
              </div>
              
              <ImageUpload
                onImageSelect={handleImageSelect}
              />

              {analysisState.error && (
                <Alert variant="error" className="mt-4">
                  <AlertCircle className="w-4 h-4" />
                  {analysisState.error}
                </Alert>
              )}
            </Card>

            {/* Analysis Controls */}
            {analysisState.file && (
              <Card className="p-4 sm:p-6">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 bg-emerald-100 rounded-lg flex-shrink-0">
                      <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-emerald-600" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <h3 className="font-semibold text-slate-800 text-sm sm:text-base">Image Ready for Analysis</h3>
                      <p className="text-xs sm:text-sm text-slate-600 truncate">
                        File: {analysisState.file.name} ({Math.round(analysisState.file.size / 1024)} KB)
                      </p>
                    </div>
                  </div>
                  
                  <Button
                    onClick={handleStartAnalysis}
                    size="lg"
                    className="flex items-center justify-center space-x-2 w-full sm:w-auto min-h-[48px]"
                  >
                    <Activity className="w-5 h-5" />
                    <span>Start AI Analysis</span>
                  </Button>
                </div>
              </Card>
            )}
          </div>
        ) : (
          /* Analysis Progress */
          <Card className="p-6 sm:p-8">
            <div className="text-center">
              <div className="flex items-center justify-center mb-6">
                <div className="relative">
                  <LoadingSpinner size="lg" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Brain className="w-6 h-6 sm:w-8 sm:h-8 text-teal-600 animate-pulse" />
                  </div>
                </div>
              </div>
              
              <h2 className="text-xl sm:text-2xl font-bold text-slate-800 mb-2">
                Analyzing Retinal Image
              </h2>
              <p className="text-slate-600 mb-6 text-sm sm:text-base px-4">
                Our AI is carefully examining your fundus image for signs of diabetic retinopathy
              </p>

              <div className="max-w-md mx-auto space-y-4">
                <div className="text-left">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-slate-700">
                      {analysisState.stage}
                    </span>
                    <span className="text-sm text-slate-500">
                      {Math.round(analysisState.progress)}%
                    </span>
                  </div>
                  <Progress 
                    value={analysisState.progress} 
                    className="h-3"
                  />
                </div>

                <Alert variant="info" className="text-left">
                  <Brain className="w-4 h-4" />
                  AI analysis typically takes 30-60 seconds for accurate results
                </Alert>
              </div>
            </div>
          </Card>
        )}

        {/* Medical Disclaimer */}
        <div className="mt-8">
          <Alert variant="warning">
            <Shield className="w-4 h-4" />
            <div>
              <strong>Medical Disclaimer:</strong> This AI screening tool is for assistive purposes only 
              and should not replace professional medical diagnosis. Always consult with a qualified 
              healthcare provider for proper medical evaluation and treatment decisions.
            </div>
          </Alert>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;