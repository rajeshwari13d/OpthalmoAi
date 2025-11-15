import React, { useState, useCallback, useRef } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, 
  FileImage, 
  AlertCircle, 
  CheckCircle, 
  X,
  File,
  Image as ImageIcon,
  Info
} from 'lucide-react';
import { analysisService, dataService } from '../services';

interface UploadedFile {
  file: File;
  preview: string;
  id: string;
  result?: any;
  analyzing?: boolean;
  error?: string;
}

const RetinalUploadPage: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [selectedImageId, setSelectedImageId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
  const maxFileSize = 10 * 1024 * 1024; // 10MB

  const validateFile = (file: File): string | null => {
    if (!allowedTypes.includes(file.type)) {
      return 'Please upload JPEG, PNG, or WebP images only.';
    }
    if (file.size > maxFileSize) {
      return 'File size must be less than 10MB.';
    }
    return null;
  };

  const handleFiles = useCallback((files: FileList | null) => {
    if (!files) return;

    Array.from(files).forEach((file) => {
      const validationError = validateFile(file);
      if (validationError) {
        setError(validationError);
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const preview = e.target?.result as string;
        const newFile: UploadedFile = {
          file,
          preview,
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9)
        };
        
        setUploadedFiles(prev => [...prev, newFile]);
        setError(null);
      };
      reader.readAsDataURL(file);
    });
  }, []);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  }, [handleFiles]);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  };

  const removeFile = (id: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== id));
  };

  const analyzeImage = async (fileId: string) => {
    const fileIndex = uploadedFiles.findIndex(f => f.id === fileId);
    if (fileIndex === -1) return;

    // Update file status to analyzing
    setUploadedFiles(prev => prev.map(f => 
      f.id === fileId ? { ...f, analyzing: true, error: undefined } : f
    ));

    try {
      const file = uploadedFiles[fileIndex];
      const result = await analysisService.analyzeImage(file.file);
      
      if (result.success && result.data?.result) {
        // Record the screening result in data service
        dataService.addScreeningResult({
          stage: result.data.result.stage,
          confidence: result.data.result.confidence,
          riskLevel: result.data.result.riskLevel,
          stageName: result.data.result.stageName || `Stage ${result.data.result.stage}`,
          fileName: file.file.name,
          imageQuality: result.data.result.imageQuality
        });

        // Update file with results
        setUploadedFiles(prev => prev.map(f => 
          f.id === fileId ? { 
            ...f, 
            analyzing: false, 
            result: result.data?.result,
            error: undefined 
          } : f
        ));
      } else {
        throw new Error(result.error || 'Analysis failed');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setUploadedFiles(prev => prev.map(f => 
        f.id === fileId ? { 
          ...f, 
          analyzing: false, 
          error: err instanceof Error ? err.message : 'Analysis failed'
        } : f
      ));
    }
  };

  const analyzeAllImages = async () => {
    const unanalyzedFiles = uploadedFiles.filter(f => !f.result && !f.analyzing && !f.error);
    if (unanalyzedFiles.length === 0) {
      setError('No unanalyzed images to process.');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    // Analyze files sequentially to avoid overwhelming the server
    for (const file of unanalyzedFiles) {
      await analyzeImage(file.id);
    }

    setIsAnalyzing(false);
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Header */}
      <motion.div 
        className="text-center mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-medical-500 to-medical-600 rounded-full mb-4">
          <FileImage className="h-8 w-8 text-white" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          Upload Retinal Images
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Upload existing retinal fundus photographs or medical reports for AI-powered diabetic retinopathy analysis
        </p>
      </motion.div>

      {/* Information Panel */}
      <motion.div 
        className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.6 }}
      >
        <div className="flex items-start space-x-3">
          <Info className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-blue-800">
            <p className="font-medium mb-1">Supported File Types:</p>
            <p>JPEG, PNG, WebP images up to 10MB each. High-quality retinal fundus photographs provide the best analysis results.</p>
          </div>
        </div>
      </motion.div>

      {/* Upload Area */}
      <motion.div 
        className="mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
      >
        <div
          className={`
            relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300
            ${dragActive 
              ? 'border-medical-500 bg-medical-50' 
              : 'border-gray-300 bg-gray-50 hover:border-medical-400 hover:bg-medical-25'
            }
            ${uploadedFiles.length > 0 ? 'border-green-400 bg-green-50' : ''}
          `}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept="image/*"
            onChange={handleFileInput}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          
          <div className="space-y-4">
            <div className={`mx-auto w-12 h-12 rounded-full flex items-center justify-center ${
              uploadedFiles.length > 0 ? 'bg-green-100' : 'bg-medical-100'
            }`}>
              {uploadedFiles.length > 0 ? (
                <CheckCircle className="h-6 w-6 text-green-600" />
              ) : (
                <Upload className="h-6 w-6 text-medical-600" />
              )}
            </div>
            
            <div>
              <p className="text-lg font-medium text-gray-900 mb-2">
                {uploadedFiles.length > 0 
                  ? `${uploadedFiles.length} image(s) uploaded` 
                  : 'Drag and drop retinal images here'
                }
              </p>
              <p className="text-gray-600 mb-4">
                or click to browse your files
              </p>
              <button
                type="button"
                onClick={openFileDialog}
                className="inline-flex items-center px-6 py-3 bg-medical-600 text-white rounded-lg font-medium hover:bg-medical-700 transition-colors duration-200"
              >
                <File className="h-4 w-4 mr-2" />
                Choose Files
              </button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Uploaded Files Display */}
      {uploadedFiles.length > 0 && (
        <motion.div 
          className="mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          <h3 className="text-lg font-medium text-gray-900 mb-4">Uploaded Images ({uploadedFiles.length})</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {uploadedFiles.map((uploadedFile) => (
              <div key={uploadedFile.id} className="relative group">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                  <div className="aspect-square bg-gray-100">
                    <img
                      src={uploadedFile.preview}
                      alt="Retinal image preview"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="p-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <ImageIcon className="h-4 w-4 text-gray-500" />
                        <span className="text-sm text-gray-900 truncate font-medium">
                          {uploadedFile.file.name}
                        </span>
                      </div>
                      <button
                        onClick={() => removeFile(uploadedFile.id)}
                        className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {(uploadedFile.file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                    
                    {/* Analysis Button and Result */}
                    <div className="mt-3 space-y-2">
                      {!uploadedFile.result && !uploadedFile.analyzing && (
                        <button
                          onClick={() => analyzeImage(uploadedFile.id)}
                          className="w-full px-3 py-2 bg-medical-600 text-white text-sm rounded-lg hover:bg-medical-700 transition-colors flex items-center justify-center space-x-2"
                        >
                          <FileImage className="h-4 w-4" />
                          <span>Analyze</span>
                        </button>
                      )}
                      
                      {uploadedFile.analyzing && (
                        <div className="w-full px-3 py-2 bg-gray-100 text-gray-600 text-sm rounded-lg flex items-center justify-center space-x-2">
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-medical-600"></div>
                          <span>Analyzing...</span>
                        </div>
                      )}
                      
                      {uploadedFile.result && (
                        <button
                          onClick={() => setSelectedImageId(uploadedFile.id)}
                          className="w-full px-3 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
                        >
                          <CheckCircle className="h-4 w-4" />
                          <span>View Results</span>
                        </button>
                      )}
                      
                      {uploadedFile.error && (
                        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                          <div className="flex items-center space-x-2">
                            <AlertCircle className="h-4 w-4 text-red-600" />
                            <span className="text-sm text-red-800">{uploadedFile.error}</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Full Results Display */}
      {selectedImageId && (
        <motion.div 
          className="mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {(() => {
            const selectedFile = uploadedFiles.find(f => f.id === selectedImageId);
            if (!selectedFile?.result) return null;

            const result = selectedFile.result;
            // Get stage-specific styling and info
            let stageName, stageClass, severity;
            switch (result.stage) {
              case 0:
                stageName = 'No DR';
                stageClass = 'border-green-200 bg-green-50';
                severity = 'No diabetic retinopathy detected';
                break;
              case 1:
                stageName = 'Mild DR';
                stageClass = 'border-yellow-200 bg-yellow-50';
                severity = 'Mild non-proliferative diabetic retinopathy';
                break;
              case 2:
                stageName = 'Moderate DR';
                stageClass = 'border-orange-200 bg-orange-50';
                severity = 'Moderate non-proliferative diabetic retinopathy';
                break;
              case 3:
                stageName = 'Severe DR';
                stageClass = 'border-red-200 bg-red-50';
                severity = 'Severe non-proliferative diabetic retinopathy';
                break;
              case 4:
                stageName = 'Proliferative DR';
                stageClass = 'border-red-200 bg-red-50';
                severity = 'Proliferative diabetic retinopathy';
                break;
              default:
                stageName = 'Unknown';
                stageClass = 'border-gray-200 bg-gray-50';
                severity = 'Unable to determine';
            }
            
            return (
              <div className="bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden">
                {/* Header */}
                <div className="bg-gradient-to-r from-medical-600 to-clinical-600 text-white p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h2 className="text-xl font-bold">AI Analysis Results</h2>
                      <p className="text-medical-100 text-sm">{selectedFile.file.name}</p>
                    </div>
                    <button
                      onClick={() => setSelectedImageId(null)}
                      className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>
                </div>

                <div className="p-6">
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Image Display */}
                    <div className="space-y-4">
                      <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                        <img
                          src={selectedFile.preview}
                          alt="Retinal analysis"
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="text-sm text-gray-600 space-y-1">
                        <p><strong>File Size:</strong> {(selectedFile.file.size / 1024 / 1024).toFixed(2)} MB</p>
                        <p><strong>File Type:</strong> {selectedFile.file.type}</p>
                        {result.imageQuality && (
                          <>
                            <p><strong>Resolution:</strong> {result.imageQuality.resolution}</p>
                            <p><strong>Quality Score:</strong> {(result.imageQuality.qualityScore * 100).toFixed(0)}%</p>
                            <p><strong>Brightness:</strong> {result.imageQuality.brightness}</p>
                            <p><strong>Contrast:</strong> {result.imageQuality.contrast}</p>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Results Details */}
                    <div className="space-y-6">
                      {/* Stage Classification */}
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">Diabetic Retinopathy Classification</h3>
                        <div className={`p-4 rounded-lg border-2 ${stageClass}`}>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-lg font-bold text-gray-800">
                              Stage {result.stage}: {stageName}
                            </span>
                            <span className="text-sm px-2 py-1 bg-medical-100 text-medical-800 rounded-full">
                              {(result.confidence * 100).toFixed(1)}% Confidence
                            </span>
                          </div>
                          <p className="text-gray-700 text-sm">
                            {severity}
                          </p>
                        </div>
                      </div>

                      {/* Confidence Score */}
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">AI Confidence Analysis</h3>
                        <div className="space-y-3">
                          <div className="flex justify-between text-sm">
                            <span>Confidence Level</span>
                            <span className="font-medium">{(result.confidence * 100).toFixed(1)}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-3">
                            <div 
                              className="bg-gradient-to-r from-medical-500 to-clinical-500 h-3 rounded-full transition-all duration-500"
                              style={{ width: `${result.confidence * 100}%` }}
                            />
                          </div>
                          <div className="grid grid-cols-3 text-xs text-gray-500">
                            <span>Low (0-60%)</span>
                            <span className="text-center">Moderate (60-80%)</span>
                            <span className="text-right">High (80-100%)</span>
                          </div>
                        </div>
                      </div>

                      {/* Detailed Description */}
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">Analysis Details</h3>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <p className="text-gray-700 leading-relaxed">
                            {result.description}
                          </p>
                        </div>
                      </div>

                      {/* AI Analysis Factors */}
                      {result.analysisFactors && result.analysisFactors.length > 0 && (
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900 mb-3">Key Analysis Factors</h3>
                          <div className="bg-blue-50 p-4 rounded-lg">
                            <div className="grid grid-cols-1 gap-2">
                              {result.analysisFactors.map((factor: string, index: number) => (
                                <div key={index} className="flex items-center space-x-2">
                                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                                  <span className="text-blue-800 text-sm font-medium">{factor}</span>
                                </div>
                              ))}
                            </div>
                            <div className="mt-3 pt-3 border-t border-blue-200">
                              <span className="text-blue-700 text-sm">
                                Risk Score: <strong>{result.riskScore}</strong>
                              </span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* Recommendations */}
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-3">Medical Recommendations</h3>
                        <div className="space-y-2">
                          <div className={`p-4 rounded-lg border ${
                            result.stage === 0 ? 'bg-green-50 border-green-200' :
                            result.stage <= 2 ? 'bg-yellow-50 border-yellow-200' :
                            'bg-red-50 border-red-200'
                          }`}>
                            <div className="space-y-2">
                              {result.recommendations && result.recommendations.map((rec: string, index: number) => (
                                <div key={index} className="flex items-start space-x-2">
                                  <div className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${
                                    result.stage === 0 ? 'bg-green-500' :
                                    result.stage <= 2 ? 'bg-yellow-500' :
                                    'bg-red-500'
                                  }`}></div>
                                  <span className={`text-sm ${
                                    result.stage === 0 ? 'text-green-800' :
                                    result.stage <= 2 ? 'text-yellow-800' :
                                    'text-red-800'
                                  }`}>
                                    {rec}
                                  </span>
                                </div>
                              ))}
                            </div>
                            
                            <div className={`mt-3 pt-3 border-t text-xs ${
                              result.stage === 0 ? 'border-green-200 text-green-700' :
                              result.stage <= 2 ? 'border-yellow-200 text-yellow-700' :
                              'border-red-200 text-red-700'
                            }`}>
                              Risk Level: <strong className="capitalize">{result.riskLevel}</strong> | 
                              Analysis ID: {result.id}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })()}
        </motion.div>
      )}

      {/* Error Display */}
      {error && (
        <motion.div 
          className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-5 w-5 text-red-600" />
            <p className="text-red-800">{error}</p>
          </div>
        </motion.div>
      )}

      {/* Analyze All Button - Only show if there are unanalyzed images */}
      {uploadedFiles.length > 0 && uploadedFiles.some(file => !file.result && !file.analyzing) && (
        <motion.div 
          className="flex justify-center mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          <button
            onClick={analyzeAllImages}
            disabled={isAnalyzing}
            className={`
              px-8 py-4 rounded-lg font-medium text-lg transition-all duration-200 flex items-center space-x-3
              ${!isAnalyzing
                ? 'bg-gradient-to-r from-medical-600 to-clinical-600 text-white hover:from-medical-700 hover:to-clinical-700 shadow-lg hover:shadow-xl transform hover:scale-105'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }
            `}
          >
            {isAnalyzing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Analyzing All...</span>
              </>
            ) : (
              <>
                <FileImage className="h-5 w-5" />
                <span>Analyze All Remaining</span>
              </>
            )}
          </button>
        </motion.div>
      )}

      {/* Medical Disclaimer */}
      <motion.div 
        className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.6 }}
      >
        <div className="flex items-start space-x-2">
          <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-yellow-800">
            <p className="font-medium mb-1">Medical Disclaimer</p>
            <p>
              This AI analysis is for screening purposes only and should not replace professional medical diagnosis. 
              Always consult with a qualified healthcare professional for proper medical evaluation and treatment decisions.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default RetinalUploadPage;