import pytest
from opencompass.configs.datasets.OlympiadBench.OlympiadBench_categories import categories
import re

def test_categories_list_is_correct():
    """Test that 'categories' is a list with the expected length (5)."""
    assert isinstance(categories, list), "'categories' should be a list"
    # Verify that there are exactly 5 category entries
    assert len(categories) == 5, f"Expected 5 categories, but got {len(categories)}"

def test_categories_content():
    """Test that the contents of 'categories' match the expected exact values."""
    expected = [
        'OE_TO_maths_en_COMP',
        'OE_TO_maths_zh_COMP',
        'OE_TO_maths_zh_CEE',
        'OE_TO_physics_en_COMP',
        'OE_TO_physics_zh_CEE'
    ]
    assert categories == expected, f"Expected categories {expected}, but got {categories}"

def test_all_elements_are_non_empty_strings():
    """Test that every element in 'categories' is a non-empty string and follows the expected naming convention."""
    for cat in categories:
        assert isinstance(cat, str), f"Category {cat} is not a string"
        assert cat, "Category should not be an empty string"
        parts = cat.split('_')
        # Expected format: OE_TO_subject_language_COMP/CEE
        # Hence, there should be exactly 5 parts, e.g., ["OE", "TO", "maths", "en", "COMP"]
        assert len(parts) == 5, f"Category {cat} does not split into 5 parts"
        assert parts[0] == 'OE', f"First part of {cat} should be 'OE'"
        assert parts[1] == 'TO', f"Second part of {cat} should be 'TO'"

def test_category_validity():
    """Test that each category has valid subject, language, and exam board values."""
    valid_subjects = {'maths', 'physics'}
    valid_languages = {'en', 'zh'}
    valid_boards = {'COMP', 'CEE'}
    for cat in categories:
        parts = cat.split('_')
        # The expected parts: [ "OE", "TO", subject, language, exam board ]
        subject = parts[2]
        language = parts[3]
        board = parts[4]
        assert subject in valid_subjects, f"Invalid subject '{subject}' in category '{cat}'"
        assert language in valid_languages, f"Invalid language '{language}' in category '{cat}'"
        assert board in valid_boards, f"Invalid board '{board}' in category '{cat}'"

def test_no_duplicates_in_categories():
    """Test that there are no duplicate entries in the categories list."""
    unique_categories = set(categories)
    assert len(categories) == len(unique_categories), f"Found duplicates in categories: {categories}"

def test_category_regex():
    """Test that each category matches the expected regex pattern: OE_TO_(maths|physics)_(en|zh)_(COMP|CEE)."""
    pattern = re.compile(r'^OE_TO_(maths|physics)_(en|zh)_(COMP|CEE)$')
    for cat in categories:
        assert pattern.match(cat), f"Category {cat} does not match the expected pattern"

def test_category_no_whitespace():
    """Test that no category string has leading or trailing whitespace."""
    for cat in categories:
        assert cat == cat.strip(), f"Category {cat} has leading or trailing whitespace"
def test_category_starts_with_prefix():
    """Test that every category string starts with 'OE_TO_'."""
    for cat in categories:
        assert cat.startswith("OE_TO_"), f"Category {cat} does not start with 'OE_TO_'"

def test_category_underscore_count():
    """Test that every category string contains exactly 4 underscores."""
    for cat in categories:
        count = cat.count('_')
        assert count == 4, f"Category {cat} contains {count} underscores, expected 4"

def test_category_parts_are_alphabetic():
    """Test that each component of the category string (when split by '_') is alphabetic."""
    for cat in categories:
        parts = cat.split('_')
        for part in parts:
            # Although subjects (maths, physics) and exam boards (COMP, CEE) may have a mix of case,
            # we expect them to be fully alphabetic.
            assert part.isalpha(), f"Part '{part}' in category '{cat}' contains non-alphabetic characters"

def test_category_case_consistency():
    """Test that the initial components 'OE' and 'TO' are in uppercase as expected."""
    for cat in categories:
        parts = cat.split('_')
        assert parts[0] == parts[0].upper(), f"First part '{parts[0]}' of category '{cat}' should be uppercase"
        assert parts[1] == parts[1].upper(), f"Second part '{parts[1]}' of category '{cat}' should be uppercase"

@pytest.mark.parametrize("category", categories)
def test_category_split_structure(category):
    """Test that splitting a category string results in exactly 5 parts and that parts match expected patterns."""
    parts = category.split('_')
    assert len(parts) == 5, f"Category {category} did not split into 5 parts; got {len(parts)} parts"
    # Check that subject is either 'maths' or 'physics'
    assert parts[2] in {'maths', 'physics'}, f"Subject {parts[2]} in category {category} is invalid"
    # Check that language is either 'en' or 'zh'
    assert parts[3] in {'en', 'zh'}, f"Language {parts[3]} in category {category} is invalid"
    # Check that board is either 'COMP' or 'CEE'
    assert parts[4] in {'COMP', 'CEE'}, f"Exam board {parts[4]} in category {category} is invalid"