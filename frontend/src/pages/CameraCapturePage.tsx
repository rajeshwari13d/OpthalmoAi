import React, { useState, useRef, useCallback, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  Camera, 
  RotateCcw, 
  Download, 
  AlertCircle, 
  CheckCircle, 
  X,
  Smartphone,
  Image as ImageIcon,
  Info,
  Play,
  Square
} from 'lucide-react';
import { analysisService } from '../services/api.client';

interface CapturedImage {
  blob: Blob;
  preview: string;
  id: string;
  timestamp: Date;
}

const CameraCapturePage: React.FC = () => {
  const [capturedImages, setCapturedImages] = useState<CapturedImage[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  // Start camera
  const startCamera = async () => {
    try {
      setCameraError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment', // Use back camera if available
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setCameraActive(true);
      }
    } catch (err) {
      console.error('Camera access error:', err);
      setCameraError('Unable to access camera. Please check permissions or use file upload instead.');
    }
  };

  // Stop camera
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setCameraActive(false);
  };

  // Capture photo from camera
  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext('2d');
    
    if (!context) return;

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw the current video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to blob
    canvas.toBlob((blob) => {
      if (!blob) return;
      
      const preview = canvas.toDataURL('image/jpeg', 0.8);
      const newImage: CapturedImage = {
        blob,
        preview,
        id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
        timestamp: new Date()
      };
      
      setCapturedImages(prev => [...prev, newImage]);
      setError(null);
    }, 'image/jpeg', 0.8);
  };

  // Handle file upload from gallery/files
  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    Array.from(files).forEach((file) => {
      if (!file.type.startsWith('image/')) {
        setError('Please select image files only.');
        return;
      }

      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        setError('File size must be less than 10MB.');
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const preview = e.target?.result as string;
        const newImage: CapturedImage = {
          blob: file,
          preview,
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
          timestamp: new Date()
        };
        
        setCapturedImages(prev => [...prev, newImage]);
        setError(null);
      };
      reader.readAsDataURL(file);
    });
  };

  const removeImage = (id: string) => {
    setCapturedImages(prev => prev.filter(img => img.id !== id));
  };

  const analyzeImages = async () => {
    if (capturedImages.length === 0) {
      setError('Please capture or select at least one image.');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      // Convert blob to File for the first image
      const firstImage = capturedImages[0];
      const file = new File([firstImage.blob], `retinal-capture-${firstImage.timestamp.getTime()}.jpg`, {
        type: 'image/jpeg'
      });
      
      const result = await analysisService.analyzeImage(file);
      
      if (result.success && result.data) {
        navigate(`/results/${result.data.result.id}`);
      } else {
        throw new Error(result.error || 'Analysis failed');
      }
    } catch (err) {
      // Don't log technical errors to console in production
      if (process.env.NODE_ENV === 'development') {
        console.error('Analysis error:', err);
      }
      setError(err instanceof Error ? err.message : 'Failed to analyze captured image');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const openGallery = () => {
    fileInputRef.current?.click();
  };

  // Cleanup camera on unmount
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Header */}
      <motion.div 
        className="text-center mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-clinical-500 to-clinical-600 rounded-full mb-4">
          <Camera className="h-8 w-8 text-white" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          Capture Retinal Images
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Take new retinal photographs using your device camera or select from your photo gallery for immediate AI analysis
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
            <p className="font-medium mb-1">Camera Capture Tips:</p>
            <p>Ensure good lighting, hold the device steady, and capture clear, focused images of the retina. Use the back camera for better quality when available.</p>
          </div>
        </div>
      </motion.div>

      {/* Camera Section */}
      <motion.div 
        className="mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
      >
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">Camera Capture</h3>
              <div className="flex space-x-2">
                {!cameraActive ? (
                  <button
                    onClick={startCamera}
                    className="inline-flex items-center px-4 py-2 bg-clinical-600 text-white rounded-lg font-medium hover:bg-clinical-700 transition-colors duration-200"
                  >
                    <Play className="h-4 w-4 mr-2" />
                    Start Camera
                  </button>
                ) : (
                  <>
                    <button
                      onClick={capturePhoto}
                      className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition-colors duration-200"
                    >
                      <Camera className="h-4 w-4 mr-2" />
                      Capture
                    </button>
                    <button
                      onClick={stopCamera}
                      className="inline-flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg font-medium hover:bg-gray-700 transition-colors duration-200"
                    >
                      <Square className="h-4 w-4 mr-2" />
                      Stop
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
          
          <div className="relative bg-gray-900 aspect-video">
            {cameraActive ? (
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center text-gray-400">
                  <Camera className="h-16 w-16 mx-auto mb-4 opacity-50" />
                  <p className="text-lg font-medium">Camera Preview</p>
                  <p className="text-sm">Click "Start Camera" to begin</p>
                </div>
              </div>
            )}
          </div>
          
          {cameraError && (
            <div className="p-4 bg-red-50 border-t border-red-200">
              <div className="flex items-center space-x-2">
                <AlertCircle className="h-5 w-5 text-red-600" />
                <p className="text-red-800 text-sm">{cameraError}</p>
              </div>
            </div>
          )}
        </div>
      </motion.div>

      {/* Gallery Upload Option */}
      <motion.div 
        className="mb-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.6 }}
      >
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="text-center">
            <Smartphone className="h-12 w-12 text-clinical-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Or Select from Gallery</h3>
            <p className="text-gray-600 mb-4">Choose existing photos from your device gallery</p>
            
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept="image/*"
              onChange={handleFileInput}
              className="hidden"
            />
            
            <button
              onClick={openGallery}
              className="inline-flex items-center px-6 py-3 bg-clinical-600 text-white rounded-lg font-medium hover:bg-clinical-700 transition-colors duration-200"
            >
              <ImageIcon className="h-4 w-4 mr-2" />
              Choose from Gallery
            </button>
          </div>
        </div>
      </motion.div>

      {/* Captured Images Display */}
      {capturedImages.length > 0 && (
        <motion.div 
          className="mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          <h3 className="text-lg font-medium text-gray-900 mb-4">Captured Images ({capturedImages.length})</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {capturedImages.map((image) => (
              <div key={image.id} className="relative group">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                  <div className="aspect-square bg-gray-100">
                    <img
                      src={image.preview}
                      alt="Captured retinal image"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="p-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Camera className="h-4 w-4 text-gray-500" />
                        <span className="text-sm text-gray-900 font-medium">
                          {image.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      <button
                        onClick={() => removeImage(image.id)}
                        className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      Captured: {image.timestamp.toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
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

      {/* Analysis Button */}
      <motion.div 
        className="flex justify-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.6 }}
      >
        <button
          onClick={analyzeImages}
          disabled={capturedImages.length === 0 || isAnalyzing}
          className={`
            px-8 py-4 rounded-lg font-medium text-lg transition-all duration-200 flex items-center space-x-3
            ${capturedImages.length > 0 && !isAnalyzing
              ? 'bg-gradient-to-r from-clinical-600 to-medical-600 text-white hover:from-clinical-700 hover:to-medical-700 shadow-lg hover:shadow-xl transform hover:scale-105'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }
          `}
        >
          {isAnalyzing ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Camera className="h-5 w-5" />
              <span>Start AI Analysis</span>
            </>
          )}
        </button>
      </motion.div>

      {/* Medical Disclaimer */}
      <motion.div 
        className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7, duration: 0.6 }}
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

      {/* Hidden canvas for photo capture */}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
};

export default CameraCapturePage;