import React from 'react';
import { useNavigate } from 'react-router-dom';
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
  Activity,
  Globe,
  Target,
  TrendingUp,
  BookOpen,
  Stethoscope,
  Building,
  Mail,
  Phone
} from 'lucide-react';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const companyValues = [
    {
      icon: Heart,
      title: 'Patient-Centered Care',
      description: 'Every feature is designed with patient outcomes in mind, ensuring healthcare professionals have the tools they need for early detection and prevention.'
    },
    {
      icon: Shield,
      title: 'Privacy & Security',
      description: 'HIPAA-compliant infrastructure with end-to-end encryption, ensuring patient data remains secure and private throughout the analysis process.'
    },
    {
      icon: Brain,
      title: 'AI Innovation',
      description: 'Cutting-edge machine learning models trained on diverse datasets to provide accurate, reliable, and unbiased diabetic retinopathy screening.'
    },
    {
      icon: Globe,
      title: 'Global Accessibility',
      description: 'Making advanced AI diagnostics accessible to healthcare providers worldwide, especially in underserved communities with limited access to specialists.'
    }
  ];

  const platformFeatures = [
    {
      icon: Eye,
      title: 'Advanced AI Analysis',
      description: 'State-of-the-art deep learning algorithms trained on thousands of retinal images for precise diabetic retinopathy detection across all stages.',
      stats: '94.7% Accuracy'
    },
    {
      icon: Zap,
      title: 'Real-Time Processing',
      description: 'Get comprehensive analysis results in under 60 seconds with detailed confidence scores and clinical recommendations.',
      stats: '<60s Response'
    },
    {
      icon: Users,
      title: 'Healthcare Integration',
      description: 'Seamlessly integrates into existing clinical workflows with support for DICOM standards and EHR systems.',
      stats: '200+ Partners'
    },
    {
      icon: Award,
      title: 'Clinical Validation',
      description: 'Rigorously tested and validated with clinical studies, meeting FDA guidelines for medical AI devices.',
      stats: 'FDA-Ready'
    }
  ];

  const teamMembers = [
    {
      name: 'Healthcare AI Team',
      role: 'Medical Technology Specialists',
      description: 'Experienced professionals combining medical expertise with AI innovation for better patient outcomes.'
    },
    {
      name: 'Clinical Advisory Board',
      role: 'Ophthalmology Experts',
      description: 'Board-certified ophthalmologists ensuring clinical relevance and accuracy in our AI models.'
    },
    {
      name: 'AI Research Division',
      role: 'Machine Learning Engineers',
      description: 'PhD-level researchers advancing the state of AI in medical imaging and diagnostic applications.'
    }
  ];

  const stats = [
    { label: 'Detection Accuracy', value: '94.7%', icon: Target },
    { label: 'Images Analyzed', value: '50K+', icon: Eye },
    { label: 'Healthcare Partners', value: '200+', icon: Users },
    { label: 'Countries Served', value: '25+', icon: Globe }
  ];

  return (
    <>
      {/* Hero Section - About OpthalmoAI */}
      <section className="relative py-12 sm:py-16 lg:py-20 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 sm:mb-16">
            <Badge variant="info" className="mb-6 text-sm px-4 py-2">
              <Award className="h-4 w-4 mr-2" />
              Revolutionizing Eye Care with AI
            </Badge>
            
            <div className="flex flex-col items-center mb-8">
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-teal-100">
                <img 
                  src="/opthalmo-logo.svg" 
                  alt="OpthalmoAI - AI-Powered Retinal Screening" 
                  className="w-80 h-52 drop-shadow-lg"
                />
              </div>
            </div>
            <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-slate-800 mb-6 leading-tight px-4">
              About OpthalmoAI
            </h1>
            
            <p className="text-base sm:text-lg lg:text-xl text-slate-600 max-w-4xl mx-auto mb-8 leading-relaxed px-4">
              OpthalmoAI is a cutting-edge healthcare technology platform that harnesses the power of artificial intelligence 
              to revolutionize diabetic retinopathy screening. Our mission is to make advanced eye care accessible to 
              healthcare professionals worldwide, enabling early detection and better patient outcomes.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="w-full sm:w-auto px-8 py-4 min-h-[48px]" onClick={() => navigate('/analysis')}>
                <Eye className="h-5 w-5 mr-2" />
                Try Our Platform
              </Button>
              <Button variant="outline" size="lg" className="w-full sm:w-auto px-8 py-4 min-h-[48px]" onClick={() => {
                const missionSection = document.getElementById('mission-section');
                if (missionSection) {
                  missionSection.scrollIntoView({ behavior: 'smooth' });
                }
              }}>
                <BookOpen className="h-5 w-5 mr-2" />
                Our Mission
              </Button>
            </div>
          </div>

          {/* Company Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6 mb-12 sm:mb-16">
            {stats.map((stat, index) => {
              const IconComponent = stat.icon;
              return (
                <Card key={index} className="text-center p-4 sm:p-6" hover>
                  <IconComponent className="h-6 w-6 sm:h-8 sm:w-8 text-teal-600 mx-auto mb-3" />
                  <div className="text-lg sm:text-2xl font-bold text-slate-800 mb-1">
                    {stat.value}
                  </div>
                  <div className="text-xs sm:text-sm text-slate-600">
                    {stat.label}
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Mission & Vision Section */}
      <section className="py-12 sm:py-16 lg:py-20 bg-white/40 backdrop-blur-sm" id="mission-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-800 mb-6">
                Our Mission
              </h2>
              <p className="text-base sm:text-lg text-slate-600 mb-6 leading-relaxed">
                To democratize access to advanced eye care by providing healthcare professionals with 
                AI-powered tools that enable early detection of diabetic retinopathy, ultimately 
                preventing vision loss and improving patient quality of life worldwide.
              </p>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-5 w-5 sm:h-6 sm:w-6 text-teal-600 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-slate-800 text-sm sm:text-base">Early Detection</h4>
                    <p className="text-slate-600 text-sm sm:text-base">Identifying diabetic retinopathy in its earliest stages when treatment is most effective.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-5 w-5 sm:h-6 sm:w-6 text-teal-600 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-slate-800 text-sm sm:text-base">Global Accessibility</h4>
                    <p className="text-slate-600 text-sm sm:text-base">Making expert-level screening available in underserved communities and remote locations.</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <CheckCircle className="h-6 w-6 text-teal-600 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-slate-800">Healthcare Empowerment</h4>
                    <p className="text-slate-600">Supporting healthcare professionals with AI-powered insights for better clinical decisions.</p>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <Card className="p-8 bg-gradient-to-br from-teal-50 to-blue-50 border-teal-200/50">
                <h3 className="text-2xl font-bold text-slate-800 mb-4">
                  Our Vision
                </h3>
                <p className="text-lg text-slate-600 mb-6 leading-relaxed">
                  A world where diabetic retinopathy-related blindness is preventable through 
                  accessible, accurate, and timely AI-powered screening.
                </p>
                <div className="flex items-center space-x-4 text-sm text-teal-700">
                  <div className="flex items-center space-x-2">
                    <Globe className="h-4 w-4" />
                    <span>Global Impact</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Heart className="h-4 w-4" />
                    <span>Patient-First</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Brain className="h-4 w-4" />
                    <span>AI-Powered</span>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Core Values Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-800 mb-4">
              Our Core Values
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Every aspect of OpthalmoAI is built upon these fundamental principles that guide 
              our technology development and healthcare partnerships.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {companyValues.map((value, index) => {
              const IconComponent = value.icon;
              return (
                <Card key={index} className="p-8" hover>
                  <div className="flex items-start space-x-4">
                    <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-teal-500 to-blue-600 rounded-xl shadow-lg flex-shrink-0">
                      <IconComponent className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-slate-800 mb-2">
                        {value.title}
                      </h3>
                      <p className="text-slate-600 leading-relaxed">
                        {value.description}
                      </p>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Platform Features Section */}
      <section className="py-20 bg-white/40 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-800 mb-4">
              Advanced Healthcare Technology
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              OpthalmoAI combines cutting-edge artificial intelligence with clinical expertise 
              to deliver reliable, accurate, and secure diabetic retinopathy screening.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {platformFeatures.map((feature, index) => {
              const IconComponent = feature.icon;
              return (
                <Card key={index} className="p-8" hover>
                  <div className="flex items-start space-x-4">
                    <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-teal-500 to-blue-600 rounded-xl shadow-lg flex-shrink-0">
                      <IconComponent className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-xl font-semibold text-slate-800">
                          {feature.title}
                        </h3>
                        <Badge variant="success" className="text-xs">
                          {feature.stats}
                        </Badge>
                      </div>
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

      {/* Team Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-800 mb-4">
              Expert Team
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Our multidisciplinary team combines medical expertise, AI research, and healthcare 
              technology experience to deliver world-class solutions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {teamMembers.map((member, index) => (
              <Card key={index} className="p-8 text-center" hover>
                <div className="w-16 h-16 bg-gradient-to-r from-teal-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">
                  {member.name}
                </h3>
                <p className="text-teal-600 font-medium mb-3">
                  {member.role}
                </p>
                <p className="text-slate-600 leading-relaxed">
                  {member.description}
                </p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Healthcare Compliance Section */}
      <section className="py-20 bg-white/40 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-800 mb-4">
              Healthcare Compliance & Security
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              OpthalmoAI is built to meet the highest standards of healthcare security, 
              privacy, and regulatory compliance.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="p-8 text-center" hover>
              <Shield className="h-12 w-12 text-teal-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-slate-800 mb-3">
                HIPAA Compliance
              </h3>
              <p className="text-slate-600 leading-relaxed">
                Full HIPAA compliance with encrypted data transmission, secure storage, 
                and automatic data deletion protocols.
              </p>
            </Card>
            
            <Card className="p-8 text-center" hover>
              <Award className="h-12 w-12 text-teal-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-slate-800 mb-3">
                FDA Guidelines
              </h3>
              <p className="text-slate-600 leading-relaxed">
                Developed following FDA guidelines for AI/ML-based medical devices 
                with comprehensive clinical validation.
              </p>
            </Card>
            
            <Card className="p-8 text-center" hover>
              <Stethoscope className="h-12 w-12 text-teal-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-slate-800 mb-3">
                Clinical Standards
              </h3>
              <p className="text-slate-600 leading-relaxed">
                Adheres to international clinical standards for diabetic retinopathy 
                classification and medical imaging protocols.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Contact & Partnership Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Card className="p-12 bg-gradient-to-r from-teal-50 to-blue-50 border-teal-200/50" glow>
            <h2 className="text-3xl font-bold text-slate-800 mb-4">
              Partner with OpthalmoAI
            </h2>
            <p className="text-lg text-slate-600 mb-8 max-w-2xl mx-auto">
              Join healthcare institutions worldwide that trust OpthalmoAI for diabetic retinopathy screening. 
              Contact us to learn how we can support your patient care initiatives.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Button size="lg" className="px-8 py-4" onClick={() => navigate('/analysis')}>
                <Eye className="h-5 w-5 mr-2" />
                Try Our Platform
                <ArrowRight className="h-5 w-5 ml-2" />
              </Button>
              <Button variant="outline" size="lg" className="px-8 py-4" onClick={() => navigate('/reports')}>
                <Building className="h-5 w-5 mr-2" />
                Partnership Inquiry
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8 pt-8 border-t border-teal-200/50">
              <div className="flex items-center justify-center space-x-3 text-teal-700">
                <Mail className="h-5 w-5" />
                <span className="text-sm font-medium">pimpretech@gmail.com</span>
              </div>
              <div className="flex items-center justify-center space-x-3 text-teal-700">
                <Phone className="h-5 w-5" />
                <span className="text-sm font-medium">Healthcare Partnerships</span>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-teal-200/30">
              <p className="text-sm text-slate-500 text-center">
                Developed by <span className="font-medium text-teal-600">Pimpre</span>
              </p>
            </div>

            <div className="flex items-center justify-center space-x-6 mt-6">
              <div className="flex items-center space-x-2 text-teal-700">
                <CheckCircle className="h-5 w-5" />
                <span className="text-sm font-medium">HIPAA Compliant</span>
              </div>
              <div className="flex items-center space-x-2 text-teal-700">
                <Star className="h-5 w-5" />
                <span className="text-sm font-medium">FDA-Ready Technology</span>
              </div>
              <div className="flex items-center space-x-2 text-teal-700">
                <TrendingUp className="h-5 w-5" />
                <span className="text-sm font-medium">Proven Results</span>
              </div>
            </div>
          </Card>
        </div>
      </section>
    </>
  );
};

export default HomePage;