import pytest
from manager import get_offline_protocol
from campus_dispatch import dispatch_emergency_sos

def test_offline_fallback():
    res = get_offline_protocol("cpr needed")
    assert "Rescue breaths" in res or "Chest" in res or "Call" in res

def test_mock_dispatch():
    res = dispatch_emergency_sos(28.6, 77.2, "Test Hazard", "HIGH")
    assert res["status"] in ["sent", "mock_sent"]