"""
Member D (Dhawal) - Diagnostics Engine Module
White-Box Testing: Basis Path Testing

Student ID: member_d_dhawal
Testing Technique: Basis Path Coverage
Module: diagnostics_engine.py
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from member_d_dhawal.diagnostics_engine import DiagnosticsEngine
from src.domain.league import League
from src.domain.team import Team


class TestDiagnosticsEngineBasisPath:
    """Basis Path Testing for DiagnosticsEngine"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = DiagnosticsEngine()
        self.league = League("Test League", "2024-2025")
    
    def test_detect_anomalies_path1_with_data(self):
        """Path 1: Anomaly detection with league data"""
        self.league.add_team(Team("Team A", "Stadium A"))
        anomalies = self.engine.detect_scheduling_anomalies(self.league, save_results=False)
        assert isinstance(anomalies, list)
    
    def test_detect_anomalies_path2_empty(self):
        """Path 2: Anomaly detection with empty league"""
        anomalies = self.engine.detect_scheduling_anomalies(self.league, save_results=False)
        assert isinstance(anomalies, list)
    
    def test_generate_report_path1(self):
        """Path 1: Report generation succeeds"""
        self.league.add_team(Team("Team A", "Stadium A"))
        self.league.add_team(Team("Team B", "Stadium B"))
        report = self.engine.generate_season_summary(self.league, save_results=False)
        assert isinstance(report, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
