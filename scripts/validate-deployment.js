#!/usr/bin/env node

/**
 * OpthalmoAI Firebase Deployment Validator
 * Healthcare compliance and security validation tool
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  projectId: process.env.FIREBASE_PROJECT_ID || 'OPTHALMOAI_PROJECT_ID',
  siteId: process.env.FIREBASE_SITE_ID || 'OPTHALMOAI_SITE_ID',
  region: process.env.CLOUD_RUN_REGION || 'us-central1',
  serviceId: process.env.CLOUD_RUN_SERVICE || 'opthalmoai-api'
};

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function log(level, message) {
  const timestamp = new Date().toISOString();
  const color = colors[level] || colors.reset;
  console.log(`${color}[${level.toUpperCase()}] ${timestamp} - ${message}${colors.reset}`);
}

// Validation functions
class OpthalmoAIValidator {
  constructor() {
    this.results = {
      passed: 0,
      failed: 0,
      warnings: 0,
      tests: []
    };
  }

  async validateConfiguration() {
    log('blue', 'Validating Firebase configuration files...');
    
    // Check firebase.json
    await this.checkFile('firebase.json', (content) => {
      const config = JSON.parse(content);
      
      this.test('Firebase hosting configuration exists', 
        !!config.hosting, 
        'firebase.json must have hosting configuration'
      );
      
      this.test('Site ID configured', 
        config.hosting.site && config.hosting.site !== 'OPTHALMOAI_SITE_ID',
        'Site ID must be replaced with actual Firebase site ID'
      );
      
      this.test('API proxy configured', 
        config.hosting.rewrites && config.hosting.rewrites.some(r => r.source === '/api/**'),
        'API proxy to Cloud Run must be configured'
      );
      
      this.test('Security headers present', 
        config.hosting.headers && config.hosting.headers.length > 0,
        'Security headers must be configured for healthcare compliance'
      );
      
      this.test('HSTS header configured', 
        JSON.stringify(config).includes('Strict-Transport-Security'),
        'HSTS header required for medical data security'
      );
      
      this.test('CSP header configured', 
        JSON.stringify(config).includes('Content-Security-Policy'),
        'Content Security Policy required for XSS protection'
      );
    });

    // Check .firebaserc
    await this.checkFile('.firebaserc', (content) => {
      const config = JSON.parse(content);
      
      this.test('Firebase project configured', 
        config.projects && config.projects.default !== 'OPTHALMOAI_PROJECT_ID',
        'Project ID must be replaced with actual Firebase project ID'
      );
    });

    // Check frontend configuration
    await this.checkFile('frontend/firebase.json', (content) => {
      const config = JSON.parse(content);
      
      this.test('Frontend Firebase config exists', 
        !!config.hosting,
        'Frontend firebase.json must exist and be configured'
      );
    });
  }

  async validateFrontendBuild() {
    log('blue', 'Validating frontend build configuration...');
    
    // Check package.json
    await this.checkFile('frontend/package.json', (content) => {
      const pkg = JSON.parse(content);
      
      this.test('React scripts present', 
        pkg.dependencies && pkg.dependencies['react-scripts'],
        'React scripts required for building'
      );
      
      this.test('Build script configured', 
        pkg.scripts && pkg.scripts.build,
        'Build script must be configured'
      );
      
      this.test('Firebase scripts present', 
        pkg.scripts && (pkg.scripts['firebase:build'] || pkg.scripts['firebase:deploy']),
        'Firebase deployment scripts should be configured'
      );
    });

    // Check if build directory exists
    const buildPath = path.join('frontend', 'build');
    if (fs.existsSync(buildPath)) {
      this.test('Build directory exists', true, 'Frontend has been built');
      
      // Check essential build files
      const indexPath = path.join(buildPath, 'index.html');
      this.test('index.html exists in build', 
        fs.existsSync(indexPath),
        'index.html must exist in build directory'
      );
      
      if (fs.existsSync(indexPath)) {
        const indexContent = fs.readFileSync(indexPath, 'utf8');
        this.test('React app mounted', 
          indexContent.includes('<div id="root">'),
          'React mount point must exist in index.html'
        );
      }
    } else {
      this.test('Build directory exists', false, 'Run npm run build first');
    }
  }

  async validateHealthcareCompliance() {
    log('blue', 'Validating healthcare compliance features...');
    
    // Check for medical disclaimers in source code
    const srcPath = 'frontend/src';
    if (fs.existsSync(srcPath)) {
      const hasDisclaimers = this.searchInDirectory(srcPath, [
        'medical disclaimer',
        'assistive screening',
        'professional medical',
        'healthcare professional',
        'not a diagnostic'
      ]);
      
      this.test('Medical disclaimers present', 
        hasDisclaimers,
        'Medical disclaimers must be present in the application'
      );
    }
  }

  async validateDeploymentReadiness() {
    log('blue', 'Validating deployment readiness...');
    
    // Check GitHub Actions workflow
    const workflowPath = '.github/workflows/deploy-hosting.yml';
    if (fs.existsSync(workflowPath)) {
      await this.checkFile(workflowPath, (content) => {
        this.test('GitHub Actions workflow exists', true, 'CI/CD pipeline configured');
        
        this.test('Firebase action configured', 
          content.includes('FirebaseExtended/action-hosting-deploy'),
          'Firebase deployment action must be configured'
        );
        
        this.test('Node.js setup configured', 
          content.includes('actions/setup-node'),
          'Node.js setup required for build'
        );
      });
    } else {
      this.test('GitHub Actions workflow exists', false, 'CI/CD pipeline not configured (optional)');
    }

    // Check deployment scripts
    const scripts = ['scripts/deploy-frontend.sh', 'scripts/deploy-frontend.bat'];
    scripts.forEach(script => {
      this.test(`Deployment script exists: ${script}`, 
        fs.existsSync(script),
        'Deployment scripts available for manual deployment'
      );
    });
  }

  async validateSecurity() {
    log('blue', 'Validating security configuration...');
    
    // Check for sensitive data in configuration
    const sensitivePatterns = [
      /api[_-]?key/i,
      /secret/i,
      /password/i,
      /token(?!_expire)/i
    ];
    
    const configFiles = ['firebase.json', '.firebaserc', 'frontend/firebase.json'];
    
    configFiles.forEach(file => {
      if (fs.existsSync(file)) {
        const content = fs.readFileSync(file, 'utf8');
        const hasSensitiveData = sensitivePatterns.some(pattern => pattern.test(content));
        
        this.test(`No sensitive data in ${file}`, 
          !hasSensitiveData,
          `${file} should not contain API keys or secrets`
        );
      }
    });
  }

  // Helper methods
  async checkFile(filePath, validator) {
    if (fs.existsSync(filePath)) {
      try {
        const content = fs.readFileSync(filePath, 'utf8');
        validator(content);
      } catch (error) {
        this.test(`${filePath} is valid`, false, `Error reading ${filePath}: ${error.message}`);
      }
    } else {
      this.test(`${filePath} exists`, false, `${filePath} is required`);
    }
  }

  searchInDirectory(dirPath, patterns) {
    try {
      const files = this.getAllFiles(dirPath);
      return files.some(file => {
        if (path.extname(file).match(/\.(js|jsx|ts|tsx)$/)) {
          const content = fs.readFileSync(file, 'utf8').toLowerCase();
          return patterns.some(pattern => content.includes(pattern.toLowerCase()));
        }
        return false;
      });
    } catch (error) {
      return false;
    }
  }

  getAllFiles(dirPath, files = []) {
    const items = fs.readdirSync(dirPath);
    
    items.forEach(item => {
      const fullPath = path.join(dirPath, item);
      if (fs.statSync(fullPath).isDirectory()) {
        this.getAllFiles(fullPath, files);
      } else {
        files.push(fullPath);
      }
    });
    
    return files;
  }

  test(description, condition, message) {
    const result = {
      description,
      passed: !!condition,
      message
    };
    
    this.results.tests.push(result);
    
    if (condition) {
      this.results.passed++;
      log('green', `✓ ${description}`);
    } else {
      this.results.failed++;
      log('red', `✗ ${description}: ${message}`);
    }
  }

  warning(description, message) {
    this.results.warnings++;
    this.results.tests.push({
      description,
      passed: false,
      warning: true,
      message
    });
    log('yellow', `⚠ ${description}: ${message}`);
  }

  async run() {
    log('blue', '🏥 Starting OpthalmoAI Deployment Validation');
    log('blue', '===============================================');
    
    await this.validateConfiguration();
    await this.validateFrontendBuild();
    await this.validateHealthcareCompliance();
    await this.validateDeploymentReadiness();
    await this.validateSecurity();
    
    this.generateReport();
  }

  generateReport() {
    console.log('\n' + '='.repeat(50));
    log('blue', '🏥 OpthalmoAI Deployment Validation Report');
    console.log('='.repeat(50));
    
    log('green', `✓ Tests Passed: ${this.results.passed}`);
    log('red', `✗ Tests Failed: ${this.results.failed}`);
    log('yellow', `⚠ Warnings: ${this.results.warnings}`);
    
    const total = this.results.passed + this.results.failed;
    const passRate = total > 0 ? (this.results.passed / total * 100).toFixed(1) : 0;
    
    console.log(`\nOverall Pass Rate: ${passRate}%`);
    
    if (this.results.failed === 0) {
      log('green', '🎉 All validation tests passed! OpthalmoAI is ready for deployment.');
      log('blue', 'Next steps:');
      console.log('  1. Replace placeholder values in configuration files');
      console.log('  2. Deploy Cloud Run backend service');
      console.log('  3. Run deployment using provided scripts');
      console.log('  4. Validate healthcare compliance post-deployment');
    } else {
      log('red', '❌ Some validation tests failed. Please address the issues above before deployment.');
      log('yellow', 'Critical issues must be resolved for healthcare compliance.');
    }
    
    // Generate JSON report
    const reportPath = 'validation-report.json';
    fs.writeFileSync(reportPath, JSON.stringify(this.results, null, 2));
    log('blue', `📋 Detailed report saved to: ${reportPath}`);
  }
}

// Run validation if called directly
if (require.main === module) {
  const validator = new OpthalmoAIValidator();
  validator.run().catch(error => {
    console.error('Validation failed:', error);
    process.exit(1);
  });
}

module.exports = OpthalmoAIValidator;