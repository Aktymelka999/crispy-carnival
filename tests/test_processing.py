from src.processing import filter_by_state, sort_by_date


class TestProcessing:
    def test_filter_by_state_executed(self, sample_transactions):
        filtered = filter_by_state(sample_transactions, "EXECUTED")
        assert len(filtered) == 2
        assert all(t["state"] == "EXECUTED" for t in filtered)

    def test_filter_by_state_nonexistent(self, sample_transactions):
        filtered = filter_by_state(sample_transactions, "CANCELLED")
        assert len(filtered) == 0

    def test_sort_by_date_ascending(self, sample_transactions):
        sorted_tx = sort_by_date(sample_transactions, reverse=False)
        dates = [t["date"] for t in sorted_tx if "date" in t]
        assert dates == sorted(dates)

    def test_sort_by_date_descending(self, sample_transactions):
        sorted_tx = sort_by_date(sample_transactions, reverse=True)
        dates = [t["date"] for t in sorted_tx if "date" in t]
        assert dates == sorted(dates, reverse=True)


class TestFilterByState:
    def test_filter_executed_only(self):
        data = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
            {"id": 2, "state": "PENDING", "date": "2024-01-02"},
            {"id": 3, "state": "EXECUTED", "date": "2024-01-03"},
        ]
        result = filter_by_state(data, "EXECUTED")

        assert len(result) == 2
        ids = {t["id"] for t in result}
        assert ids == {1, 3}

    def test_filter_non_existent_state(self):
        data = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
        ]
        result = filter_by_state(data, "CANCELLED")
        assert result == []

    def test_filter_invalid_input_not_list(self):
        result = filter_by_state("not a list", "EXECUTED")
        assert result == []

    def test_filter_dict_validation(self):
        data = [
            {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
            "invalid_item",
            None,
            {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
        ]
        result = filter_by_state(data, "EXECUTED")
        assert len(result) == 2


class TestSortByDate:
    def test_sort_ascending_default(self):
        data = [
            {"id": 3, "date": "2024-01-03"},
            {"id": 1, "date": "2024-01-01"},
            {"id": 2, "date": "2024-01-02"},
        ]
        result = sort_by_date(data)  # reverse=False

        ids = [t["id"] for t in result]
        assert ids == [1, 2, 3]

    def test_sort_descending(self):
        data = [
            {"id": 1, "date": "2024-01-01"},
            {"id": 2, "date": "2024-01-02"},
            {"id": 3, "date": "2024-01-03"},
        ]
        result = sort_by_date(data, reverse=True)

        ids = [t["id"] for t in result]
        assert ids == [3, 2, 1]

    def test_sort_missing_date_field(self):
        data = [
            {"id": 1, "date": "2024-01-01"},
            {"id": 2},  # Нет поля date
            {"id": 3, "date": "2024-01-03"},
        ]
        result = sort_by_date(data)

        valid_ids = [t["id"] for t in result if "date" in t]
        valid_dates = [t["date"] for t in result if "date" in t]
        assert valid_dates == sorted(valid_dates)
        assert set(valid_ids) == {1, 3}

    def test_sort_invalid_input_not_list(self):
        result = sort_by_date("not a list")
        assert result == []

    def test_sort_iso_format_correctness(self):

        data = [
            {"id": 1, "date": "2024-12-31"},
            {"id": 2, "date": "2024-01-01"},
            {"id": 3, "date": "2023-12-31"},
        ]
        result = sort_by_date(data)

        ids = [t["id"] for t in result]

        assert ids == [3, 2, 1]
