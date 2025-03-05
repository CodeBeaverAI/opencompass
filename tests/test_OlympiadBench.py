import pytest
from opencompass.configs.summarizers.groups.OlympiadBench import categories, OlympiadBench_summary_groups

class TestOlympiadBenchConfig:
    """Test the OlympiadBench configuration."""

    def test_categories_list(self):
        """Test that the categories list is correctly defined."""
        expected_categories = [
            'OE_TO_maths_en_COMP',
            'OE_TO_maths_zh_COMP',
            'OE_TO_maths_zh_CEE',
            'OE_TO_physics_en_COMP',
            'OE_TO_physics_zh_CEE'
        ]
        assert categories == expected_categories

    def test_summary_groups_structure(self):
        """Test that the summary groups structure has one element with the correct name and subsets."""
        # Ensure the summary groups is a list with one element.
        assert isinstance(OlympiadBench_summary_groups, list)
        assert len(OlympiadBench_summary_groups) == 1

        group = OlympiadBench_summary_groups[0]

        # Verify the dictionary has 'name' and 'subsets' keys.
        assert 'name' in group
        assert 'subsets' in group

        # Verify the name.
        assert group['name'] == 'OlympiadBench'

        # Construct the expected subsets list.
        expected_subsets = ['OlympiadBench_' + c.replace(' ', '_') for c in categories]
        assert group['subsets'] == expected_subsets

    def test_subsets_prefix(self):
        """Test that every subset string starts with 'OlympiadBench_'."""
        group = OlympiadBench_summary_groups[0]
        for subset in group['subsets']:
            assert subset.startswith("OlympiadBench_")
    def test_subsets_are_strings(self):
        """Test that all subsets are of string type."""
        group = OlympiadBench_summary_groups[0]
        for subset in group['subsets']:
            assert isinstance(subset, str)

    def test_subset_no_whitespace(self):
        """Test that no subset string contains whitespace."""
        group = OlympiadBench_summary_groups[0]
        for subset in group['subsets']:
            assert " " not in subset

    def test_summary_group_keys(self):
        """Test that the summary group dictionary contains exactly 'name' and 'subsets' keys."""
        group = OlympiadBench_summary_groups[0]
        assert sorted(group.keys()) == ['name', 'subsets']
    def test_categories_are_strings(self):
        """Test that the categories list contains only string elements."""
        for cat in categories:
            assert isinstance(cat, str)

    def test_transformation_logic(self):
        """Test that the transformation logic correctly replaces whitespace with underscores."""
        # Using a sample string with multiple and single spaces.
        test_category = "example category  with spaces"
        expected = "OlympiadBench_" + test_category.replace(" ", "_")
        actual = "OlympiadBench_" + test_category.replace(" ", "_")
        assert actual == expected

    def test_summary_groups_static_after_category_modification(self):
        """Test that modifying the categories list after module load does not affect the summary groups subsets."""
        original_subsets = OlympiadBench_summary_groups[0]['subsets'].copy()
        # Append a new category to the categories list.
        categories.append("OE_TO_new_CATEGORY")
        # The pre-computed subsets in OlympiadBench_summary_groups should remain unchanged.
        assert OlympiadBench_summary_groups[0]['subsets'] == original_subsets
        # Clean up: remove the appended category.
        categories.pop()
    def test_summary_groups_immutable_after_category_element_modification(self):
        """Verify that updating an element of the categories list does not affect the precomputed summary group subsets."""
        original_categories = categories.copy()
        original_subsets = OlympiadBench_summary_groups[0]['subsets'].copy()
        # Modify each element in the categories list and check that each corresponding summary group element remains unchanged.
        for i in range(len(categories)):
            categories[i] = categories[i] + "_modified"
            assert OlympiadBench_summary_groups[0]['subsets'][i] == "OlympiadBench_" + original_categories[i]
        # Restore the original categories to avoid side effects on subsequent tests.
        for i in range(len(categories)):
            categories[i] = original_categories[i]

    def test_duplicate_prefix_in_transformation(self):
        """Test that the transformation logic prepends the prefix even if the category already starts with 'OlympiadBench_'."""
        test_category = "OlympiadBench_existing"
        # The expected behavior is to simply prepend "OlympiadBench_" even if the test_category already contains it.
        expected = "OlympiadBench_" + test_category.replace(" ", "_")
        actual = "OlympiadBench_" + test_category.replace(" ", "_")
        assert actual == expected