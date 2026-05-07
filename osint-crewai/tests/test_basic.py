"""
Basic tests untuk OSINT CrewAI Tools
"""
import pytest
import sys
sys.path.insert(0, '.')

from src.utils.target_detector import detect_target_type


class TestTargetDetector:
    def test_email_detection(self):
        assert detect_target_type("john.doe@gmail.com") == "email"
        assert detect_target_type("admin@example.co.id") == "email"

    def test_ip_detection(self):
        assert detect_target_type("192.168.1.1") == "ip"
        assert detect_target_type("8.8.8.8") == "ip"

    def test_domain_detection(self):
        assert detect_target_type("google.com") == "domain"
        assert detect_target_type("example.co.id") == "domain"

    def test_username_detection(self):
        assert detect_target_type("johndoe123") == "username"
        assert detect_target_type("john_doe") == "username"

    def test_fullname_detection(self):
        assert detect_target_type("John Doe") == "fullname"
        assert detect_target_type("Budi Santoso") == "fullname"


class TestTools:
    def test_google_dork_tool(self):
        from src.tools.social_tools import GoogleDorkTool
        tool = GoogleDorkTool()
        result = tool._run(target="test_user", dork_type="general")
        assert "Google Dork" in result
        assert "test_user" in result

    def test_email_validate_tool(self):
        from src.tools.email_tools import EmailValidateTool
        tool = EmailValidateTool()
        result = tool._run(email="test@example.com")
        assert "Format valid" in result

    def test_markdown_report_tool(self):
        from src.tools.report_tools import MarkdownReportTool
        tool = MarkdownReportTool()
        result = tool._run(content="Test content", title="Test Report")
        assert "Test Report" in result
        assert "Disclaimer" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
