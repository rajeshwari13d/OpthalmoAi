import React, { useState, useCallback, useRef } from 'react';
import { Upload, Camera, FileImage, AlertCircle, Check, Eye, Loader2 } from 'lucide-react';
import { Button, Card, Alert, Progress, Badge } from './ui';
import { analysisService } from '../services';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  onAnalysisComplete?: (result: AnalysisResult) => void;
}

interface AnalysisResult {
  id: string;
  stage: number;
  confidence: number;
  riskLevel: 'low' | 'moderate' | 'high';
  recommendations: string[];
  timestamp: string;
  stageName?: string;
  imageQuality?: {
    qualityScore: number;
    brightness: number;
    contrast: number;
  };
}

export const ImageUpload: React.FC<ImageUploadProps> = ({ onImageSelect, onAnalysisComplete }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [cameraActive, setCameraActive] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const validateFile = useCallback((file: File): boolean => {
    // Healthcare-specific validations
    const allowedTypes = ['image/jpeg', 'image/png', 'image/tiff'];
    const maxSize = 10 * 1024 * 1024; // 10MB for high-quality retinal images
    const minSize = 100 * 1024; // 100KB minimum for quality

    if (!allowedTypes.includes(file.type)) {
      setError('Please upload a JPEG, PNG, or TIFF image file.');
      return false;
    }

    if (file.size > maxSize) {
      setError('Image file must be smaller than 10MB.');
      return false;
    }

    if (file.size < minSize) {
      setError('Image file appears too small. Please ensure high-quality retinal images.');
      return false;
    }

    return true;
  }, []);

  const handleFileSelect = useCallback((file: File) => {
    if (!validateFile(file)) return;

    setError(null);
    setSelectedFile(file);
    onImageSelect(file);

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target?.result as string);
    };
    reader.readAsDataURL(file);
  }, [validateFile, onImageSelect]);

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

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      handleFileSelect(files[0]);
    }
  }, [handleFileSelect]);

  const startCamera = useCallback(async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'environment' // Prefer back camera for retinal imaging
        }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
      }
    } catch (err) {
      setError('Camera access denied. Please enable camera permissions or upload an image file.');
      console.error('Camera error:', err);
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      setCameraActive(false);
    }
  }, []);

  const captureImage = useCallback(() => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');

      if (context) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);

        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'retinal-capture.jpg', { type: 'image/jpeg' });
            handleFileSelect(file);
            stopCamera();
          }
        }, 'image/jpeg', 0.9);
      }
    }
  }, [handleFileSelect, stopCamera]);

  const analyzeImage = useCallback(async () => {
    if (!selectedFile) return;

    setAnalyzing(true);
    setAnalysisProgress(0);
    setError(null);

    try {
      // Show progress updates while analysis is happening
      const progressUpdates = [
        { progress: 10, message: 'Uploading image...' },
        { progress: 30, message: 'Preprocessing retinal image...' },
        { progress: 50, message: 'Running AI model inference...' },
        { progress: 70, message: 'Analyzing retinal features...' },
        { progress: 90, message: 'Generating medical insights...' }
      ];

      // Start progress simulation
      const progressInterval = setInterval(() => {
        const currentStep = progressUpdates.find(step => step.progress > analysisProgress);
        if (currentStep && analysisProgress < currentStep.progress) {
          setAnalysisProgress(prev => Math.min(prev + 2, currentStep.progress));
        }
      }, 100);

      // Make API call to analyze image
      const response = await analysisService.analyzeImage(selectedFile);

      clearInterval(progressInterval);
      setAnalysisProgress(100);

      if (response.success && response.data) {
        const apiResult = response.data.result;
        
        // Convert API result to component format
        const analysisResult: AnalysisResult = {
          id: apiResult.id,
          stage: apiResult.stage,
          confidence: apiResult.confidence,
          riskLevel: apiResult.riskLevel,
          recommendations: apiResult.recommendations,
          timestamp: apiResult.timestamp
        };

        setTimeout(() => {
          setAnalyzing(false);
          onAnalysisComplete?.(analysisResult);
        }, 500);

      } else {
        throw new Error(response.error || 'Analysis failed');
      }

    } catch (error) {
      setAnalyzing(false);
      setAnalysisProgress(0);
      
      const errorMessage = error instanceof Error ? error.message : 'Analysis failed. Please try again.';
      setError(errorMessage);
      
      console.error('Analysis error:', error);
    }
  }, [selectedFile, onAnalysisComplete, analysisProgress]);

  return (
    <div className="space-y-6">
      {/* Medical Disclaimer */}
      <Alert variant="info" className="bg-blue-50/80 backdrop-blur-sm border-blue-200/50">
        <div className="flex items-start space-x-3">
          <Eye className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-medium text-blue-800 mb-1">Medical Screening Tool</p>
            <p className="text-blue-700 text-sm">
              This AI analysis is designed to assist healthcare professionals and is <strong>not a substitute for professional medical diagnosis</strong>. 
              Always consult with qualified healthcare providers for proper medical evaluation.
            </p>
          </div>
        </div>
      </Alert>

      {/* Upload Interface */}
      <Card className="relative overflow-hidden" glow>
        {/* Camera View */}
        {cameraActive && (
          <div className="relative">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full h-48 sm:h-64 object-cover rounded-lg bg-slate-100"
            />
            <canvas ref={canvasRef} className="hidden" />
            <div className="absolute inset-0 flex items-center justify-center bg-black/10">
              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
                <Button onClick={captureImage} size="lg" className="min-h-[48px]">
                  <Camera className="h-5 w-5 mr-2" />
                  Capture Image
                </Button>
                <Button variant="outline" onClick={stopCamera} className="min-h-[48px]">
                  Cancel
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* File Preview */}
        {preview && !cameraActive && (
          <div className="relative">
            <img
              src={preview}
              alt="Retinal scan preview"
              className="w-full h-48 sm:h-64 object-cover rounded-lg"
            />
            <div className="absolute top-4 right-4">
              <Badge variant="success">
                <Check className="h-4 w-4 mr-1" />
                Image Ready
              </Badge>
            </div>
          </div>
        )}

        {/* Upload Area */}
        {!preview && !cameraActive && (
          <div
            className={`relative border-2 border-dashed rounded-2xl p-6 sm:p-8 lg:p-12 text-center transition-all duration-300 ${
              dragActive 
                ? 'border-teal-400 bg-teal-50/50 transform scale-105' 
                : 'border-slate-300 hover:border-teal-300 hover:bg-teal-50/30'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/tiff"
              onChange={handleFileInput}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />

            <div className="space-y-4 sm:space-y-6">
              <div className="flex justify-center">
                <div className="flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-r from-teal-500 to-blue-600 rounded-2xl shadow-lg">
                  <FileImage className="h-8 w-8 sm:h-10 sm:w-10 text-white" />
                </div>
              </div>

              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-slate-800 mb-2">
                  Upload Retinal Fundus Image
                </h3>
                <p className="text-slate-600 mb-4 text-sm sm:text-base px-4">
                  Drag and drop your retinal scan or click to browse files
                </p>
                <p className="text-xs sm:text-sm text-slate-500 px-4">
                  Supports JPEG, PNG, TIFF • Max 10MB • High resolution recommended
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
                <Button
                  onClick={() => fileInputRef.current?.click()}
                  size="lg"
                  className="w-full sm:w-auto min-w-[160px] min-h-[48px]"
                >
                  <Upload className="h-5 w-5 mr-2" />
                  Browse Files
                </Button>
                <Button
                  variant="secondary"
                  onClick={startCamera}
                  size="lg"
                  className="w-full sm:w-auto min-w-[160px] min-h-[48px]"
                >
                  <Camera className="h-5 w-5 mr-2" />
                  Use Camera
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <Alert variant="error" className="mt-4">
            <AlertCircle className="h-5 w-5" />
            <div>
              <p className="font-medium">Upload Error</p>
              <p className="text-sm mt-1">{error}</p>
            </div>
          </Alert>
        )}

        {/* Analysis Progress */}
        {analyzing && (
          <div className="mt-6 p-6 bg-gradient-to-r from-teal-50 to-blue-50 rounded-2xl border border-teal-200/50">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <Loader2 className="h-6 w-6 text-teal-600 animate-spin" />
                <h3 className="text-lg font-semibold text-teal-800">
                  AI Analysis in Progress
                </h3>
              </div>
              <Badge variant="info">
                Processing
              </Badge>
            </div>
            <Progress 
              value={analysisProgress} 
              className="mb-3" 
              showLabel 
            />
            <p className="text-sm text-teal-700">
              Our AI is carefully analyzing your retinal image for signs of diabetic retinopathy...
            </p>
          </div>
        )}

        {/* Start Analysis Button */}
        {preview && !analyzing && (
          <div className="mt-6 flex justify-center">
            <Button
              onClick={analyzeImage}
              size="lg"
              className="w-full sm:w-auto min-w-[200px] min-h-[48px]"
              loading={analyzing}
            >
              <Eye className="h-5 w-5 mr-2" />
              Start AI Analysis
            </Button>
          </div>
        )}
      </Card>
    </div>
  );
};