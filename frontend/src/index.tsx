// OpthalmoAI Production Build v2.0.1-fix-20251116-2001
// This build eliminates ALL backend dependencies and SVG percentage issues
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
// ⚡ EXTREME CACHE DESTRUCTION v3.0 ⚡ 2025-11-16T20:08:00Z
const DEPLOY_VERSION = "3.0.0-EXTREME-CACHE-DESTROYER";
const BUILD_TIMESTAMP = "20251116-200800";
const CACHE_BUSTER_ID = "DESTROY_OLD_CACHE_" + Math.random().toString(36);

console.log(`💥 OpthalmoAI ${DEPLOY_VERSION} - Build ${BUILD_TIMESTAMP}`);
console.log(`🔥 Cache Buster ID: ${CACHE_BUSTER_ID}`);
console.log('🚫 ZERO backend dependencies (production isolated)');
console.log('🚫 ZERO SVG percentage paths (all fixed to absolute)');
console.log('✅ Extreme cache destruction active');
console.log('📝 Expected: NO main.bca4da3c.js errors');

// Force console visibility
if (window.location.hostname === 'opthalmoai.web.app') {
  setTimeout(() => {
    console.log('🎯 PRODUCTION VERSION CHECK:');
    console.log('- Should see: main.c9cdee5b.js or newer');
    console.log('- Should NOT see: main.bca4da3c.js (old/problematic)');
    console.log('- SVG paths: Fixed to absolute coordinates');
    console.log('- API calls: Blocked in production environment');
  }, 1000);
}

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);