import pytest
from opencompass.utils import datasets_info

import re
class TestDatasetsInfo:
    """Test cases for the datasets_info module."""

    def test_datasets_mapping_presence(self):
        """Test that DATASETS_MAPPING has expected keys and structure."""
        mapping = datasets_info.DATASETS_MAPPING
        # Ensure the mapping is a dict and not empty.
        assert isinstance(mapping, dict)
        assert len(mapping) > 0, "DATASETS_MAPPING is empty"
        # Sample expected keys to be present.
        expected_keys = [
            "opencompass/advglue-dev",
            "opencompass/agieval",
            "opencompass/ai2_arc-test",
            "opencompass/mmmlu_lite",
        ]
        for key in expected_keys:
            assert key in mapping, f"Expected key '{key}' not found in DATASETS_MAPPING"
            # Verify that each dataset has a 'local' entry.
            assert "local" in mapping[key], f"'local' key missing in dataset {key}"

    def test_datasets_mapping_structure(self):
        """Test that every dataset entry in DATASETS_MAPPING contains 'ms_id', 'hf_id', and 'local'."""
        mapping = datasets_info.DATASETS_MAPPING
        for dataset_key, dataset in mapping.items():
            assert isinstance(dataset, dict), f"Dataset {dataset_key} is not a dict"
            for subkey in ["ms_id", "hf_id", "local"]:
                assert subkey in dataset, f"Key '{subkey}' missing in dataset {dataset_key}"

    def test_datasets_mapping_duplicates(self):
        """Test that duplicate keys in DATASETS_MAPPING result in a single entry.
            For instance, the key 'opencompass/mmmlu_lite' is defined twice and should have the last value.
        """
        mapping = datasets_info.DATASETS_MAPPING
        assert "opencompass/mmmlu_lite" in mapping, "'opencompass/mmmlu_lite' not present in DATASETS_MAPPING"
        # The expected value is the one from the last definition.
        expected_local = "./data/mmmlu_lite"
        actual_local = mapping["opencompass/mmmlu_lite"]["local"]
        assert actual_local == expected_local, f"Expected local '{expected_local}' for 'opencompass/mmmlu_lite', but got '{actual_local}'"

    def test_datasets_url_structure(self):
        """Test that every entry in DATASETS_URL contains 'url' and 'md5'."""
        urls = datasets_info.DATASETS_URL
        assert isinstance(urls, dict), "DATASETS_URL is not a dict"
        for url_key, url_value in urls.items():
            assert isinstance(url_value, dict), f"Value for key '{url_key}' is not a dict"
            for subkey in ["url", "md5"]:
                assert subkey in url_value, f"Key '{subkey}' missing in DATASETS_URL entry '{url_key}'"

    def test_datasets_url_valid_urls(self):
        """Test that each URL in DATASETS_URL starts with the expected base URL."""
        urls = datasets_info.DATASETS_URL
        expected_base = "http://opencompass.oss-cn-shanghai.aliyuncs.com/datasets/data/"
        for url_key, url_value in urls.items():
            url = url_value.get("url", "")
            assert url.startswith(expected_base), f"URL for '{url_key}' does not start with '{expected_base}'"
    def test_datasets_mapping_value_types(self):
        """Test that 'ms_id' and 'hf_id' are either None or a string, and 'local' is a non-empty string."""
        mapping = datasets_info.DATASETS_MAPPING
        for key, dataset in mapping.items():
            local = dataset.get("local")
            ms_id = dataset.get("ms_id")
            hf_id = dataset.get("hf_id")
            assert isinstance(local, str) and local, f"'local' for dataset {key} is not a valid non-empty string"
            if ms_id is not None:
                assert isinstance(ms_id, str), f"'ms_id' for dataset {key} is not a string"
            if hf_id is not None:
                assert isinstance(hf_id, str), f"'hf_id' for dataset {key} is not a string"

    def test_datasets_url_md5_format(self):
        """Test that each 'md5' in DATASETS_URL is a valid 32-character hexadecimal string."""
        urls = datasets_info.DATASETS_URL
        for key, entry in urls.items():
            md5_val = entry.get("md5", "")
            assert isinstance(md5_val, str) and len(md5_val) == 32, f"MD5 for {key} is not a valid 32-character string"
            assert re.fullmatch(r"[0-9a-f]{32}", md5_val), f"MD5 for {key} contains invalid characters"
    def test_datasets_mapping_exact_keys(self):
        """Test that each dataset in DATASETS_MAPPING contains exactly 'ms_id', 'hf_id', and 'local' keys."""
        mapping = datasets_info.DATASETS_MAPPING
        for key, dataset in mapping.items():
            expected_keys = {"ms_id", "hf_id", "local"}
            actual_keys = set(dataset.keys())
            assert actual_keys == expected_keys, f"Dataset {key} has keys {actual_keys}, but expected {expected_keys}"

    def test_datasets_url_zip_extension(self):
        """Test that each URL in DATASETS_URL ends with '.zip'."""
        urls = datasets_info.DATASETS_URL
        for key, entry in urls.items():
            url = entry.get("url", "")
            assert url.endswith(".zip"), f"URL for '{key}' does not end with '.zip': {url}"

    def test_datasets_mapping_none_and_empty(self):
        """Test that there is at least one dataset with ms_id/hf_id as None and one with empty string."""
        mapping = datasets_info.DATASETS_MAPPING
        found_none = False
        found_empty = False
        for key, dataset in mapping.items():
            ms_id = dataset.get("ms_id")
            hf_id = dataset.get("hf_id")
            if ms_id is None or hf_id is None:
                found_none = True
            if ms_id == "" or hf_id == "":
                found_empty = True
        assert found_none, "No dataset found with ms_id or hf_id as None"
        assert found_empty, "No dataset found with ms_id or hf_id as an empty string"

    def test_datasets_url_md5_lowercase(self):
        """Test that each MD5 hash in DATASETS_URL is in lowercase."""
        urls = datasets_info.DATASETS_URL
        for key, entry in urls.items():
            md5_val = entry.get("md5", "")
            assert md5_val == md5_val.lower(), f"MD5 for '{key}' is not lowercase: {md5_val}"
    def test_datasets_url_known_entries(self):
        """Test that known entries in DATASETS_URL have the expected URL and MD5 values."""
        urls = datasets_info.DATASETS_URL
        olympiad = urls.get("/OlympiadBench")
        assert olympiad is not None, "Expected '/OlympiadBench' in DATASETS_URL"
        assert olympiad["url"] == "http://opencompass.oss-cn-shanghai.aliyuncs.com/datasets/data/OlympiadBench.zip", \
            f"Unexpected URL for '/OlympiadBench': {olympiad['url']}"
        assert olympiad["md5"] == "97e8b1ae7f6170d94817288a8930ef00", \
            f"Unexpected MD5 for '/OlympiadBench': {olympiad['md5']}"
        longbench = urls.get("/longbenchv2")
        assert longbench is not None, "Expected '/longbenchv2' in DATASETS_URL"
        assert longbench["url"] == "http://opencompass.oss-cn-shanghai.aliyuncs.com/datasets/data/longbenchv2.zip", \
            f"Unexpected URL for '/longbenchv2': {longbench['url']}"
        assert longbench["md5"] == "09b7e06e6f98c5cca8ad597b3d7b42f0", \
            f"Unexpected MD5 for '/longbenchv2': {longbench['md5']}"

    def test_dataset_keys_non_empty(self):
        """Test that all keys in DATASETS_MAPPING are non-empty strings."""
        mapping = datasets_info.DATASETS_MAPPING
        for key in mapping.keys():
            assert isinstance(key, str) and key.strip(), f"Dataset key '{key}' is empty or not a valid string"

    def test_datasets_url_keys_format(self):
        """Test that all keys in DATASETS_URL do not contain whitespace."""
        urls = datasets_info.DATASETS_URL
        for key in urls.keys():
            assert " " not in key, f"Key '{key}' in DATASETS_URL contains whitespace"

    def test_local_path_format(self):
        """Test that each 'local' path in DATASETS_MAPPING is a non-empty string without leading or trailing whitespace."""
        mapping = datasets_info.DATASETS_MAPPING
        for key, dataset in mapping.items():
            local = dataset.get("local", "")
            assert isinstance(local, str) and local, f"'local' for dataset {key} should be a non-empty string"
            assert local == local.strip(), f"'local' path for dataset {key} contains leading or trailing whitespace"