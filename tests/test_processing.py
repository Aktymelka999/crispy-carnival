
import pytest
from src.processing import filter_by_state, sort_by_date

class TestProcessing:
    def test_filter_by_state_executed(self, sample_transactions):
        filtered = filter_by_state(sample_transactions, "EXECUTED")
        assert len(filtered) == 3
        assert all(t["state"] == "EXECUTED" for t in filtered)

    def test_filter_by_state_nonexistent(self, sample_transactions):
        filtered = filter_by_state(sample_transactions, "CANCELLED")
        assert len(filtered) == 0

    def test_sort_by_date_ascending(self, sample_transactions):
        sorted_tx = sort_by_date(sample_transactions, reverse=False)
        dates = [t["date"] for t in sorted_tx]
        assert dates == sorted(dates)

    def test_sort_by_date_descending(self, sample_transactions):
        sorted_tx = sort_by_date(sample_transactions, reverse=True)
        dates = [t["date"] for t in sorted_tx]
        assert dates == sorted(dates, reverse=True)