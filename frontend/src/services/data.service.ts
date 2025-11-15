/**
 * Data Service for Live Dashboard Statistics
 * Manages real-time tracking of screenings, results, and activities
 */

export interface ScreeningResult {
  id: string;
  timestamp: string;
  patientId: string;
  stage: number;
  confidence: number;
  riskLevel: string;
  stageName: string;
  fileName: string;
  imageQuality?: {
    qualityScore: number;
    brightness: number;
    contrast: number;
  };
}

export interface DashboardStats {
  totalScreenings: number;
  highRiskCases: number;
  reportsGenerated: number;
  thisWeekScreenings: number;
  weeklyChange: {
    totalScreenings: string;
    highRiskCases: string;
    reportsGenerated: string;
    thisWeekScreenings: string;
  };
}

export interface RecentActivity {
  id: string;
  time: string;
  action: string;
  patient: string;
  risk: string;
  details: string;
  timestamp: Date;
}

class DataService {
  private screeningResults: ScreeningResult[] = [];
  private activities: RecentActivity[] = [];
  
  // Load data from localStorage on initialization
  constructor() {
    this.loadFromStorage();
  }

  private loadFromStorage() {
    try {
      const storedResults = localStorage.getItem('opthalmo_screenings');
      const storedActivities = localStorage.getItem('opthalmo_activities');
      
      if (storedResults) {
        this.screeningResults = JSON.parse(storedResults);
      }
      
      if (storedActivities) {
        this.activities = JSON.parse(storedActivities).map((activity: any) => ({
          ...activity,
          timestamp: new Date(activity.timestamp)
        }));
      }
    } catch (error) {
      console.warn('Error loading dashboard data from storage:', error);
    }
  }

  private saveToStorage() {
    try {
      localStorage.setItem('opthalmo_screenings', JSON.stringify(this.screeningResults));
      localStorage.setItem('opthalmo_activities', JSON.stringify(this.activities));
    } catch (error) {
      console.warn('Error saving dashboard data to storage:', error);
    }
  }

  // Add a new screening result
  addScreeningResult(result: Omit<ScreeningResult, 'id' | 'timestamp' | 'patientId'>) {
    const screeningResult: ScreeningResult = {
      id: `DR-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
      timestamp: new Date().toISOString(),
      patientId: `P-${Date.now().toString().slice(-6)}`,
      ...result
    };

    this.screeningResults.push(screeningResult);
    
    // Add corresponding activity
    this.addActivity({
      action: 'Completed retinal analysis',
      patient: `Patient ID: ${screeningResult.patientId}`,
      risk: screeningResult.stageName,
      details: this.getStageDescription(screeningResult.stage, screeningResult.confidence),
      time: this.getRelativeTime(new Date())
    });

    this.saveToStorage();
    return screeningResult;
  }

  private addActivity(activity: Omit<RecentActivity, 'id' | 'timestamp'>) {
    const newActivity: RecentActivity = {
      id: `activity-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
      timestamp: new Date(),
      ...activity
    };

    this.activities.unshift(newActivity); // Add to beginning
    
    // Keep only last 50 activities
    if (this.activities.length > 50) {
      this.activities = this.activities.slice(0, 50);
    }

    this.saveToStorage();
  }

  private getStageDescription(stage: number, confidence: number): string {
    const confidencePercent = Math.round(confidence * 100);
    
    switch (stage) {
      case 0:
        return `Grade 0 - No diabetic retinopathy detected (${confidencePercent}% confidence)`;
      case 1:
        return `Grade 1 - Mild non-proliferative DR detected (${confidencePercent}% confidence)`;
      case 2:
        return `Grade 2 - Moderate non-proliferative DR detected (${confidencePercent}% confidence)`;
      case 3:
        return `Grade 3 - Severe non-proliferative DR detected (${confidencePercent}% confidence)`;
      case 4:
        return `Grade 4 - Proliferative DR detected (${confidencePercent}% confidence)`;
      default:
        return `Analysis completed (${confidencePercent}% confidence)`;
    }
  }

  private getRelativeTime(date: Date): string {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    return date.toLocaleDateString();
  }

  // Get current dashboard statistics
  getDashboardStats(): DashboardStats {
    const now = new Date();
    const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    const twoWeeksAgo = new Date(now.getTime() - 14 * 24 * 60 * 60 * 1000);

    // Current period stats
    const totalScreenings = this.screeningResults.length;
    const highRiskCases = this.screeningResults.filter(result => 
      result.stage >= 3 || (result.stage >= 2 && result.confidence > 0.8)
    ).length;
    const reportsGenerated = this.screeningResults.length; // Each screening generates a report
    const thisWeekScreenings = this.screeningResults.filter(result => 
      new Date(result.timestamp) >= oneWeekAgo
    ).length;

    // Previous period stats for comparison
    const prevWeekScreenings = this.screeningResults.filter(result => {
      const date = new Date(result.timestamp);
      return date >= twoWeeksAgo && date < oneWeekAgo;
    }).length;

    const prevHighRiskCases = this.screeningResults.filter(result => {
      const date = new Date(result.timestamp);
      return (date >= twoWeeksAgo && date < oneWeekAgo) && 
             (result.stage >= 3 || (result.stage >= 2 && result.confidence > 0.8));
    }).length;

    // Calculate percentage changes
    const calculateChange = (current: number, previous: number): string => {
      if (previous === 0) return current > 0 ? '+100%' : '0%';
      const change = ((current - previous) / previous) * 100;
      return `${change >= 0 ? '+' : ''}${Math.round(change)}%`;
    };

    return {
      totalScreenings,
      highRiskCases,
      reportsGenerated,
      thisWeekScreenings,
      weeklyChange: {
        totalScreenings: calculateChange(thisWeekScreenings, prevWeekScreenings),
        highRiskCases: calculateChange(
          this.screeningResults.filter(result => {
            const date = new Date(result.timestamp);
            return date >= oneWeekAgo && (result.stage >= 3 || (result.stage >= 2 && result.confidence > 0.8));
          }).length,
          prevHighRiskCases
        ),
        reportsGenerated: calculateChange(thisWeekScreenings, prevWeekScreenings),
        thisWeekScreenings: calculateChange(thisWeekScreenings, prevWeekScreenings)
      }
    };
  }

  // Get recent activities with live time updates
  getRecentActivities(limit: number = 5): RecentActivity[] {
    return this.activities
      .slice(0, limit)
      .map(activity => ({
        ...activity,
        time: this.getRelativeTime(activity.timestamp)
      }));
  }

  // Get all screening results
  getAllScreenings(): ScreeningResult[] {
    return [...this.screeningResults].sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  }

  // Delete a specific screening result
  deleteScreeningResult(id: string): boolean {
    const initialLength = this.screeningResults.length;
    this.screeningResults = this.screeningResults.filter(result => result.id !== id);
    
    if (this.screeningResults.length < initialLength) {
      this.saveToStorage();
      return true;
    }
    return false;
  }

  // Clear all data (for testing/reset)
  clearAllData() {
    this.screeningResults = [];
    this.activities = [];
    localStorage.removeItem('opthalmo_screenings');
    localStorage.removeItem('opthalmo_activities');
  }

  // Add some sample data for new users
  addSampleData() {
    if (this.screeningResults.length === 0) {
      // Add a few sample screenings from the past week
      const sampleScreenings = [
        { stage: 0, confidence: 0.92, riskLevel: 'low', stageName: 'No DR', fileName: 'fundus_001.jpg' },
        { stage: 1, confidence: 0.78, riskLevel: 'low-moderate', stageName: 'Mild NPDR', fileName: 'fundus_002.jpg' },
        { stage: 2, confidence: 0.85, riskLevel: 'moderate', stageName: 'Moderate NPDR', fileName: 'fundus_003.jpg' },
        { stage: 0, confidence: 0.89, riskLevel: 'low', stageName: 'No DR', fileName: 'fundus_004.jpg' },
        { stage: 3, confidence: 0.81, riskLevel: 'high', stageName: 'Severe NPDR', fileName: 'fundus_005.jpg' }
      ];

      // Add samples with timestamps spread over the past week
      sampleScreenings.forEach((sample, index) => {
        const daysAgo = index + 1;
        const timestamp = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000).toISOString();
        
        const result: ScreeningResult = {
          id: `DR-sample-${index + 1}`,
          timestamp,
          patientId: `P-${String(index + 1).padStart(6, '0')}`,
          ...sample
        };

        this.screeningResults.push(result);
        
        // Add corresponding activity
        const activityTime = new Date(timestamp);
        this.activities.unshift({
          id: `activity-sample-${index + 1}`,
          timestamp: activityTime,
          action: 'Completed retinal analysis',
          patient: `Patient ID: ${result.patientId}`,
          risk: result.stageName,
          details: this.getStageDescription(result.stage, result.confidence),
          time: this.getRelativeTime(activityTime)
        });
      });

      this.saveToStorage();
    }
  }
}

// Export singleton instance
export const dataService = new DataService();