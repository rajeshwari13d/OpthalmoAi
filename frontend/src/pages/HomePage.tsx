import React, { useState } from 'react';
import { Layout } from '../components/Layout';
import { ImageUpload } from '../components/ImageUpload';
import { ResultsDisplay } from '../components/ResultsDisplay';
import { Card, Button, Badge } from '../components/ui';
import { 
  Eye, 
  Shield, 
  Zap, 
  Users, 
  Award, 
  ArrowRight,
  CheckCircle,
  Star,
  Brain,
  Heart,
  Activity
} from 'lucide-react';

interface AnalysisResult {
  stage: number;
  confidence: number;
  riskLevel: 'low' | 'moderate' | 'high';
  recommendations: string[];
}

const HomePage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [currentStep, setCurrentStep] = useState<'upload' | 'results'>('upload');

  const handleImageSelect = (file: File) => {
    setSelectedFile(file);
    setAnalysisResult(null);
  };

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result);
    setCurrentStep('results');
  };

  const handleNewAnalysis = () => {
    setSelectedFile(null);
    setAnalysisResult(null);
    setCurrentStep('upload');
  };

  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Analysis',
      description: 'Advanced deep learning models trained on thousands of retinal images for accurate diabetic retinopathy detection.'
    },
    {
      icon: Shield,
      title: 'HIPAA Compliant',
      description: 'Secure, encrypted processing with automatic data deletion to protect patient privacy and ensure healthcare compliance.'
    },
    {
      icon: Zap,
      title: 'Rapid Results',
      description: 'Get comprehensive analysis results in under 60 seconds with detailed confidence scores and clinical recommendations.'
    },
    {
      icon: Heart,
      title: 'Healthcare Focused',
      description: 'Designed specifically for healthcare professionals to assist in early detection and patient care decisions.'
    }
  ];

  const stats = [
    { label: 'Accuracy Rate', value: '94.2%', icon: Activity },
    { label: 'Images Analyzed', value: '50K+', icon: Eye },
    { label: 'Healthcare Partners', value: '200+', icon: Users },
    { label: 'Detection Speed', value: '<60s', icon: Zap }
  ];

  return (
    <Layout>
      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Badge variant="info" className="mb-6 text-sm px-4 py-2">
              <Award className="h-4 w-4 mr-2" />
              FDA-Ready AI Technology
            </Badge>
            
            <h1 className="text-5xl md:text-6xl font-bold text-slate-800 mb-6 leading-tight">
              AI-Powered{' '}
              <span className="bg-gradient-to-r from-teal-600 to-blue-600 bg-clip-text text-transparent">
                Diabetic Retinopathy
              </span>{' '}
              Screening
            </h1>
            
            <p className="text-xl text-slate-600 max-w-3xl mx-auto mb-8 leading-relaxed">
              Advanced artificial intelligence technology designed to assist healthcare professionals 
              in early detection and screening of diabetic retinopathy through retinal fundus image analysis.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="px-8 py-4">
                <Eye className="h-5 w-5 mr-2" />
                Start Screening
              </Button>
              <Button variant="outline" size="lg" className="px-8 py-4">
                <Shield className="h-5 w-5 mr-2" />
                Learn More
              </Button>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
            {stats.map((stat, index) => {
              const IconComponent = stat.icon;
              return (
                <Card key={index} className="text-center p-6" hover>
                  <IconComponent className="h-8 w-8 text-teal-600 mx-auto mb-3" />
                  <div className="text-2xl font-bold text-slate-800 mb-1">
                    {stat.value}
                  </div>
                  <div className="text-sm text-slate-600">
                    {stat.label}
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Main Application */}
      <section className="py-16">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          {currentStep === 'upload' && (
            <div>
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-slate-800 mb-4">
                  Retinal Image Analysis
                </h2>
                <p className="text-lg text-slate-600 max-w-2xl mx-auto">
                  Upload a high-quality retinal fundus image to begin AI-powered diabetic retinopathy screening. 
                  Our advanced algorithms will analyze the image and provide detailed clinical insights.
                </p>
              </div>
              
              <ImageUpload 
                onImageSelect={handleImageSelect}
                onAnalysisComplete={handleAnalysisComplete}
              />
            </div>
          )}

          {currentStep === 'results' && analysisResult && (
            <div>
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-slate-800 mb-4">
                  Analysis Complete
                </h2>
                <p className="text-lg text-slate-600 max-w-2xl mx-auto">
                  Our AI has completed the analysis of your retinal image. Review the results below 
                  and share them with your healthcare provider for professional medical evaluation.
                </p>
              </div>
              
              <ResultsDisplay 
                result={analysisResult}
                onNewAnalysis={handleNewAnalysis}
              />
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white/40 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-800 mb-4">
              Advanced Healthcare AI Technology
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Our platform combines cutting-edge artificial intelligence with healthcare expertise 
              to provide reliable, accurate, and secure diabetic retinopathy screening.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => {
              const IconComponent = feature.icon;
              return (
                <Card key={index} className="p-8" hover>
                  <div className="flex items-start space-x-4">
                    <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-teal-500 to-blue-600 rounded-xl shadow-lg flex-shrink-0">
                      <IconComponent className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-slate-800 mb-2">
                        {feature.title}
                      </h3>
                      <p className="text-slate-600 leading-relaxed">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Card className="p-12 bg-gradient-to-r from-teal-50 to-blue-50 border-teal-200/50" glow>
            <h2 className="text-3xl font-bold text-slate-800 mb-4">
              Ready to Start Screening?
            </h2>
            <p className="text-lg text-slate-600 mb-8 max-w-2xl mx-auto">
              Join healthcare professionals worldwide who trust OpthalmoAI for diabetic retinopathy screening. 
              Start your analysis today and take the first step towards better patient care.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="px-8 py-4">
                <Eye className="h-5 w-5 mr-2" />
                Begin Analysis
                <ArrowRight className="h-5 w-5 ml-2" />
              </Button>
              <Button variant="outline" size="lg" className="px-8 py-4">
                <Users className="h-5 w-5 mr-2" />
                Contact Our Team
              </Button>
            </div>

            <div className="flex items-center justify-center space-x-6 mt-8 pt-8 border-t border-teal-200/50">
              <div className="flex items-center space-x-2 text-teal-700">
                <CheckCircle className="h-5 w-5" />
                <span className="text-sm font-medium">HIPAA Compliant</span>
              </div>
              <div className="flex items-center space-x-2 text-teal-700">
                <Star className="h-5 w-5" />
                <span className="text-sm font-medium">FDA-Ready Technology</span>
              </div>
              <div className="flex items-center space-x-2 text-teal-700">
                <Shield className="h-5 w-5" />
                <span className="text-sm font-medium">Secure & Private</span>
              </div>
            </div>
          </Card>
        </div>
      </section>
    </Layout>
  );
};

export default HomePage;