"""
Tests for the GET /activities endpoint.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_success(self, client):
        """Test successfully retrieving all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Verify response is a dictionary
        assert isinstance(data, dict)
        
        # Verify we have activities
        assert len(data) > 0
        
    def test_get_activities_structure(self, client):
        """Test that activities have the correct structure."""
        response = client.get("/activities")
        data = response.json()
        
        # Pick the first activity and verify its structure
        first_activity_name = list(data.keys())[0]
        activity = data[first_activity_name]
        
        # Verify required fields exist
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        
        # Verify field types
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
        
    def test_get_activities_participants_are_emails(self, client):
        """Test that participants are email strings."""
        response = client.get("/activities")
        data = response.json()
        
        # Check first activity with participants
        for activity_name, activity in data.items():
            if activity["participants"]:
                for participant in activity["participants"]:
                    assert isinstance(participant, str)
                    assert "@" in participant
                break

    def test_get_activities_max_participants_positive(self, client):
        """Test that max_participants is a positive integer."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity in data.items():
            assert activity["max_participants"] > 0

    def test_get_activities_participants_within_max(self, client):
        """Test that participants count does not exceed max_participants."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity in data.items():
            assert len(activity["participants"]) <= activity["max_participants"]
