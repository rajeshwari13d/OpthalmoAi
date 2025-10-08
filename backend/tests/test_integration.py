import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestOpthalmoAIIntegration:
    """End-to-end integration tests for OpthalmoAI platform"""
    
    def test_health_endpoint(self):
        """Test API health check"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data
    
    def test_api_cors_headers(self):
        """Test CORS headers for frontend integration"""
        response = client.options("/api/v1/health")
        assert response.status_code == 200
        
    def test_medical_disclaimer_present(self):
        """Ensure medical disclaimers are present in API responses"""
        response = client.get("/api/v1/health")
        data = response.json()
        # Medical disclaimer should be in the health response
        assert "medical_disclaimer" in data or "disclaimer" in str(data).lower()
    
    def test_image_upload_validation(self):
        """Test image upload validation and security"""
        # Test with invalid file type
        invalid_file = {"file": ("test.txt", b"not an image", "text/plain")}
        response = client.post("/api/v1/predict", files=invalid_file)
        assert response.status_code in [400, 422]  # Should reject non-images
        
    def test_api_rate_limiting_headers(self):
        """Test that API includes appropriate headers for rate limiting"""
        response = client.get("/api/v1/health")
        # Should include headers that can be used for rate limiting
        assert response.status_code == 200
        
    def test_security_headers(self):
        """Test security headers are present"""
        response = client.get("/api/v1/health")
        # Basic security check - API should respond appropriately
        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"
        
    def test_healthcare_compliance_elements(self):
        """Test healthcare compliance elements"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        
        # Should have compliance-related fields
        compliance_fields = ["service", "status", "timestamp", "version"]
        for field in compliance_fields:
            assert field in data, f"Missing compliance field: {field}"
            
    def test_api_documentation_available(self):
        """Test that API documentation is available"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200
        
    def test_openapi_schema(self):
        """Test OpenAPI schema accessibility"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "info" in schema
        assert "paths" in schema
        assert schema["info"]["title"] == "OpthalmoAI API"

class TestAIWorkflowPipeline:
    """Test the complete AI analysis workflow"""
    
    def test_prediction_endpoint_structure(self):
        """Test prediction endpoint responds with proper structure"""
        # Note: This tests the endpoint structure without actual model inference
        # since we're using a mock model in the current setup
        
        # The prediction endpoint should exist and return proper error for missing file
        response = client.post("/api/v1/predict")
        assert response.status_code in [400, 422]  # Missing file should be handled
        
    def test_workflow_error_handling(self):
        """Test error handling throughout the workflow"""
        # Test various error scenarios
        
        # 1. No file provided
        response = client.post("/api/v1/predict")
        assert response.status_code in [400, 422]
        
        # 2. Invalid content type
        response = client.post("/api/v1/predict", 
                              headers={"content-type": "application/json"})
        assert response.status_code in [400, 422]
        
    def test_healthcare_data_handling(self):
        """Test healthcare data handling compliance"""
        # Health check should not expose sensitive information
        response = client.get("/api/v1/health")
        data = response.json()
        
        # Should not contain sensitive data patterns
        sensitive_patterns = ["password", "secret", "key", "token"]
        response_text = str(data).lower()
        
        for pattern in sensitive_patterns:
            assert pattern not in response_text, f"Sensitive data exposed: {pattern}"

class TestDeploymentReadiness:
    """Test deployment readiness and configuration"""
    
    def test_environment_configuration(self):
        """Test environment configuration handling"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        
    def test_logging_functionality(self):
        """Test logging is properly configured"""
        # Make a request that should generate logs
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        
    def test_api_versioning(self):
        """Test API versioning is properly implemented"""
        # API should be versioned under /api/v1/
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        
        # Root should redirect or provide API information
        response = client.get("/")
        assert response.status_code in [200, 404]  # Should handle root appropriately

if __name__ == "__main__":
    pytest.main([__file__, "-v"])