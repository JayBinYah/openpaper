from datetime import datetime

from app.helpers.parser import (
    _detect_pdf_mime_type,
    get_start_page_from_offset,
    parse_publication_date,
)


# ---------------------------------------------------------------------------
# Tests for get_start_page_from_offset
# ---------------------------------------------------------------------------

class TestGetStartPageFromOffset:
    def test_returns_minus_one_for_empty_offsets(self):
        assert get_start_page_from_offset({}, 0) == -1

    def test_returns_minus_one_for_negative_offset(self):
        offsets = {0: (0, 100), 1: (100, 200)}
        assert get_start_page_from_offset(offsets, -1) == -1

    def test_returns_minus_one_when_offset_equals_last_end(self):
        offsets = {0: (0, 100), 1: (100, 200)}
        assert get_start_page_from_offset(offsets, 200) == -1

    def test_returns_correct_page_for_first_page(self):
        offsets = {0: (0, 100), 1: (100, 200)}
        assert get_start_page_from_offset(offsets, 0) == 0
        assert get_start_page_from_offset(offsets, 99) == 0

    def test_returns_correct_page_for_second_page(self):
        offsets = {0: (0, 100), 1: (100, 200)}
        assert get_start_page_from_offset(offsets, 100) == 1
        assert get_start_page_from_offset(offsets, 199) == 1

    def test_single_page_document(self):
        offsets = {0: (0, 500)}
        assert get_start_page_from_offset(offsets, 0) == 0
        assert get_start_page_from_offset(offsets, 499) == 0
        assert get_start_page_from_offset(offsets, 500) == -1


# ---------------------------------------------------------------------------
# Tests for parse_publication_date
# ---------------------------------------------------------------------------

class TestParsePublicationDate:
    def test_returns_none_for_empty_string(self):
        assert parse_publication_date("") is None

    def test_parses_full_date(self):
        result = parse_publication_date("2024-03-15")
        assert result == datetime(2024, 3, 15)

    def test_parses_year_month(self):
        result = parse_publication_date("2024-03")
        assert result == datetime(2024, 3, 1)

    def test_parses_year_only(self):
        result = parse_publication_date("2024")
        assert result == datetime(2024, 1, 1)

    def test_returns_none_for_invalid_format(self):
        assert parse_publication_date("not-a-date") is None
        assert parse_publication_date("15/03/2024") is None


# ---------------------------------------------------------------------------
# Tests for _detect_pdf_mime_type
# ---------------------------------------------------------------------------

class TestDetectPdfMimeType:
    def test_returns_false_for_non_pdf_bytes(self):
        assert _detect_pdf_mime_type(b"not a pdf") is False

    def test_returns_false_without_enough_markers(self):
        # Has PDF header but only one marker
        data = b"%PDF-1.4 %%EOF"
        assert _detect_pdf_mime_type(data) is False

    def test_returns_true_for_valid_pdf_like_bytes(self):
        data = b"%PDF-1.4 %%EOF /Type /Catalog xref"
        assert _detect_pdf_mime_type(data) is True

    def test_returns_false_for_empty_bytes(self):
        assert _detect_pdf_mime_type(b"") is False

