"""
Unit tests for input validators.

Tests:
- Customer query validation
- Date range validation
- Pagination validation
- Search query validation
- Link creation/update validation
- SQL injection prevention
"""

import pytest
from pydantic import ValidationError
from validators import (
    CustomerQuery,
    DateRangeQuery,
    PaginationQuery,
    SearchQuery,
    LinkCreateValidation,
    LinkUpdateValidation,
    ComparisonQuery,
    sanitize_sql_parameter
)


@pytest.mark.unit
class TestCustomerQuery:
    """Test customer query validation."""

    def test_valid_customer_id(self):
        """Test valid customer ID."""
        query = CustomerQuery(customer_id=117)
        assert query.customer_id == 117

    def test_negative_customer_id(self):
        """Test that negative customer IDs are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            CustomerQuery(customer_id=-1)
        assert 'customer_id' in str(exc_info.value)

    def test_zero_customer_id(self):
        """Test that zero customer ID is rejected."""
        with pytest.raises(ValidationError):
            CustomerQuery(customer_id=0)

    def test_very_large_customer_id(self):
        """Test that unreasonably large IDs are rejected."""
        with pytest.raises(ValidationError):
            CustomerQuery(customer_id=99999999)


@pytest.mark.unit
class TestDateRangeQuery:
    """Test date range validation."""

    def test_valid_date_format(self):
        """Test valid YYYY-MM format."""
        query = DateRangeQuery(from_date='2024-01', to_date='2024-03')
        assert query.from_date == '2024-01'
        assert query.to_date == '2024-03'

    def test_invalid_date_format(self):
        """Test that invalid date formats are rejected."""
        with pytest.raises(ValidationError):
            DateRangeQuery(from_date='2024/01')  # Wrong separator

        with pytest.raises(ValidationError):
            DateRangeQuery(from_date='24-01')  # Wrong year format

    def test_invalid_month(self):
        """Test that invalid months are rejected."""
        with pytest.raises(ValidationError):
            DateRangeQuery(from_date='2024-13')  # Month 13

        with pytest.raises(ValidationError):
            DateRangeQuery(from_date='2024-00')  # Month 0

    def test_invalid_year(self):
        """Test that invalid years are rejected."""
        with pytest.raises(ValidationError):
            DateRangeQuery(from_date='1899-01')  # Before 1900

        with pytest.raises(ValidationError):
            DateRangeQuery(from_date='2101-01')  # After 2100

    def test_from_after_to(self):
        """Test that from_date cannot be after to_date."""
        with pytest.raises(ValidationError):
            DateRangeQuery(from_date='2024-06', to_date='2024-01')

    def test_optional_dates(self):
        """Test that dates are optional."""
        query = DateRangeQuery()
        assert query.from_date is None
        assert query.to_date is None


@pytest.mark.unit
class TestPaginationQuery:
    """Test pagination validation."""

    def test_valid_pagination(self):
        """Test valid pagination parameters."""
        query = PaginationQuery(offset=0, limit=50)
        assert query.offset == 0
        assert query.limit == 50

    def test_negative_offset(self):
        """Test that negative offset is rejected."""
        with pytest.raises(ValidationError):
            PaginationQuery(offset=-1, limit=50)

    def test_zero_limit(self):
        """Test that zero limit is rejected."""
        with pytest.raises(ValidationError):
            PaginationQuery(offset=0, limit=0)

    def test_limit_exceeds_maximum(self):
        """Test that limit > 100 is rejected."""
        with pytest.raises(ValidationError):
            PaginationQuery(offset=0, limit=101)

    def test_very_large_offset(self):
        """Test that unreasonably large offset is rejected."""
        with pytest.raises(ValidationError):
            PaginationQuery(offset=9999999, limit=50)


@pytest.mark.unit
@pytest.mark.security
class TestSearchQuery:
    """Test search query validation and sanitization."""

    def test_valid_search(self):
        """Test valid search term."""
        query = SearchQuery(search_term='seo services')
        assert query.search_term == 'seo services'

    def test_sql_injection_prevention(self):
        """Test that SQL injection attempts are rejected."""
        # Semicolon - SQL statement terminator
        with pytest.raises(ValidationError):
            SearchQuery(search_term="'; DROP TABLE customer_history; --")

        # SQL comments
        with pytest.raises(ValidationError):
            SearchQuery(search_term="test--comment")

        # Block comments
        with pytest.raises(ValidationError):
            SearchQuery(search_term="/* comment */ SELECT")

    def test_xp_sp_procedures_rejected(self):
        """Test that xp_ and sp_ are rejected."""
        with pytest.raises(ValidationError):
            SearchQuery(search_term='xp_cmdshell')

        with pytest.raises(ValidationError):
            SearchQuery(search_term='sp_executesql')

    def test_search_term_too_long(self):
        """Test that very long search terms are rejected."""
        with pytest.raises(ValidationError):
            SearchQuery(search_term='a' * 201)

    def test_case_sensitive_flag(self):
        """Test case sensitive search flag."""
        query = SearchQuery(search_term='SEO', case_sensitive=True)
        assert query.case_sensitive is True


@pytest.mark.unit
class TestLinkValidation:
    """Test link creation and update validation."""

    def test_valid_link_creation(self, sample_link_data):
        """Test valid link creation."""
        link = LinkCreateValidation(**sample_link_data)
        assert link.customer_id == 1
        assert link.pub_domain == 'publisher.com'

    def test_domain_validation(self):
        """Test domain format validation."""
        # Valid domain
        link = LinkCreateValidation(
            customer_id=1,
            canonical_root='example.com',
            brand='Brand',
            pub_domain='valid-domain.com',
            target_url='https://example.com/page',
            anchor_text='text',
            published_at='2024-01-15'
        )
        assert link.pub_domain == 'valid-domain.com'

        # Invalid domain
        with pytest.raises(ValidationError):
            LinkCreateValidation(
                customer_id=1,
                canonical_root='-invalid.com',  # Starts with dash
                brand='Brand',
                pub_domain='publisher.com',
                target_url='https://example.com',
                anchor_text='text',
                published_at='2024-01-15'
            )

    def test_url_validation(self):
        """Test URL validation and auto-correction."""
        # URL without protocol should be auto-corrected
        link = LinkCreateValidation(
            customer_id=1,
            canonical_root='example.com',
            brand='Brand',
            pub_domain='publisher.com',
            target_url='example.com/page',  # No protocol
            anchor_text='text',
            published_at='2024-01-15'
        )
        assert link.target_url.startswith('http')

    def test_future_date_rejected(self):
        """Test that future dates are rejected."""
        with pytest.raises(ValidationError):
            LinkCreateValidation(
                customer_id=1,
                canonical_root='example.com',
                brand='Brand',
                pub_domain='publisher.com',
                target_url='https://example.com',
                anchor_text='text',
                published_at='2099-01-01'  # Future date
            )

    def test_date_before_2000_rejected(self):
        """Test that dates before 2000 are rejected."""
        with pytest.raises(ValidationError):
            LinkCreateValidation(
                customer_id=1,
                canonical_root='example.com',
                brand='Brand',
                pub_domain='publisher.com',
                target_url='https://example.com',
                anchor_text='text',
                published_at='1999-12-31'
            )

    def test_link_update_partial(self):
        """Test that link updates can be partial."""
        update = LinkUpdateValidation(anchor_text='new anchor')
        assert update.anchor_text == 'new anchor'
        assert update.pub_domain is None  # Other fields optional


@pytest.mark.unit
class TestComparisonQuery:
    """Test period comparison validation."""

    def test_valid_comparison(self):
        """Test valid comparison query."""
        query = ComparisonQuery(
            period1_from='2024-01',
            period1_to='2024-03',
            period2_from='2024-04',
            period2_to='2024-06'
        )
        assert query.period1_from == '2024-01'

    def test_period1_from_after_to(self):
        """Test that period1 from cannot be after to."""
        with pytest.raises(ValidationError):
            ComparisonQuery(
                period1_from='2024-06',
                period1_to='2024-01',
                period2_from='2024-01',
                period2_to='2024-03'
            )

    def test_period2_from_after_to(self):
        """Test that period2 from cannot be after to."""
        with pytest.raises(ValidationError):
            ComparisonQuery(
                period1_from='2024-01',
                period1_to='2024-03',
                period2_from='2024-06',
                period2_to='2024-04'
            )


@pytest.mark.unit
@pytest.mark.security
class TestSQLSanitization:
    """Test SQL parameter sanitization."""

    def test_sanitize_removes_dangerous_chars(self):
        """Test that dangerous SQL characters are removed."""
        # Semicolon
        assert ';' not in sanitize_sql_parameter('test; DROP TABLE')

        # SQL comments
        assert '--' not in sanitize_sql_parameter('test--comment')

        # Block comments
        assert '/*' not in sanitize_sql_parameter('test /* comment */')

    def test_sanitize_non_string(self):
        """Test that non-string parameters are returned as-is."""
        assert sanitize_sql_parameter(123) == 123
        assert sanitize_sql_parameter(None) is None
