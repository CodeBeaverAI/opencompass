import pytest
from opencompass.utils.datasets_info import DATASETS_MAPPING, DATASETS_URL

def test_datasets_mapping_structure():
    """Test that DATASETS_MAPPING has expected structure and that each entry is a dict containing a 'local' key."""
    # Check that DATASETS_MAPPING is a dict
    assert isinstance(DATASETS_MAPPING, dict)
    # Ensure each key is a string and its value a dict with a 'local' key (a string)
    for key, info in DATASETS_MAPPING.items():
            assert isinstance(key, str)
            assert isinstance(info, dict)
            assert 'local' in info
            assert isinstance(info['local'], str)

def test_mmmlu_lite_duplicate_key():
    """Test that duplicate key 'opencompass/mmmlu_lite' ends up with the last definition."""
    # The key "opencompass/mmmlu_lite" appears twice.
    # It should hold the last defined value, that is local = "./data/mmmlu_lite"
    value = DATASETS_MAPPING.get("opencompass/mmmlu_lite")
    assert value is not None
    assert value['local'] == "./data/mmmlu_lite"

def test_datasets_url_structure():
    """Test that DATASETS_URL has proper structure and each value has a nonempty 'url' and 'md5'."""
    assert isinstance(DATASETS_URL, dict)
    for key, data in DATASETS_URL.items():
            assert isinstance(key, str)
            assert isinstance(data, dict)
            assert 'url' in data
            assert 'md5' in data
            assert isinstance(data['url'], str) and data['url']
            assert isinstance(data['md5'], str) and data['md5']

def test_specific_dataset_url():
    """Test that a specific dataset in DATASETS_URL (humaneval zip) has the expected URL."""
    key = "/humaneval/"
    assert key in DATASETS_URL
    data = DATASETS_URL[key]
    expected_url = "http://opencompass.oss-cn-shanghai.aliyuncs.com/datasets/data/humaneval.zip"
    assert data['url'] == expected_url

def test_nonexistent_dataset():
    """Test that a non-existent dataset key in DATASETS_MAPPING returns None."""
    assert DATASETS_MAPPING.get("nonexistent/dataset") is None
def test_dataset_optional_fields():
    """Test that 'ms_id' and 'hf_id' in each DATASETS_MAPPING entry are either None or a string."""
    for key, info in DATASETS_MAPPING.items():
        for field in ["ms_id", "hf_id"]:
            # Every dataset should include the optional fields, even if they are None or empty strings.
            assert field in info, f"Missing key '{field}' in dataset '{key}'"
            if info[field] is not None:
                assert isinstance(info[field], str), f"Field '{field}' in dataset '{key}' is not a string or None."

def test_datasets_url_md5_format():
    """Test that the MD5 values in DATASETS_URL are valid lowercase hex strings of length 32."""
    import re
    md5_pattern = re.compile(r'^[a-f0-9]{32}$')
    for key, data in DATASETS_URL.items():
        md5 = data.get('md5')
        assert isinstance(md5, str), f"MD5 for key '{key}' is not a string."
        assert md5_pattern.match(md5), f"MD5 for key '{key}' does not match expected format: {md5}"

def test_datasets_local_paths():
    """Test that every 'local' path in DATASETS_MAPPING starts with './data'."""
    for key, info in DATASETS_MAPPING.items():
        local = info.get("local")
        assert isinstance(local, str), f"'local' value for dataset '{key}' is not a string."
        assert local.startswith("./data"), f"'local' path for dataset '{key}' does not start with './data'."
def test_specific_dataset_values():
    """Test that specific datasets in DATASETS_MAPPING have the expected ms_id, hf_id, and local values."""
    # Test the ADVGLUE dataset: ms_id and hf_id should be None and local should match expected path.
    advglue = DATASETS_MAPPING.get("opencompass/advglue-dev")
    assert advglue is not None
    assert advglue["ms_id"] is None, "Expected ms_id to be None for ADVGLUE-dev"
    assert advglue["hf_id"] is None, "Expected hf_id to be None for ADVGLUE-dev"
    assert advglue["local"] == "./data/adv_glue/dev_ann.json", "Incorrect local path for ADVGLUE-dev"

    # Test the CMNLI dataset: check that local path matches the expected one.
    cmnli = DATASETS_MAPPING.get("opencompass/cmnli-dev")
    assert cmnli is not None
    assert cmnli["local"] == "./data/CLUE/cmnli/cmnli_public/dev.json", "Incorrect local path for CMNLI-dev"

    # Test the KORBENCH dataset: ms_id and hf_id are expected to be empty strings.
    korbench = DATASETS_MAPPING.get("opencompass/korbench")
    assert korbench is not None
    assert korbench["ms_id"] == "", "Expected ms_id to be an empty string for korbench"
    assert korbench["hf_id"] == "", "Expected hf_id to be an empty string for korbench"
    assert korbench["local"] == "./data/korbench", "Incorrect local path for korbench"

def test_datasets_mapping_keys_nonempty():
    """Test that all keys in DATASETS_MAPPING are non-empty strings."""
    for key in DATASETS_MAPPING.keys():
        assert isinstance(key, str) and key.strip() != "", f"Empty key found in DATASETS_MAPPING: '{key}'"

def test_datasets_url_keys_nonempty():
    """Test that all keys in DATASETS_URL are non-empty strings."""
    for key in DATASETS_URL.keys():
        assert isinstance(key, str) and key.strip() != "", f"Empty key found in DATASETS_URL: '{key}'"
def test_datasets_url_http_prefix():
    """Test that every dataset URL in DATASETS_URL starts with 'http://' or 'https://'."""
    for key, data in DATASETS_URL.items():
        url = data.get("url", "")
        assert isinstance(url, str) and url, f"URL for key '{key}' is missing or not a string."
        assert url.startswith("http://") or url.startswith("https://"), (
            f"URL for key '{key}' does not start with http:// or https://"
        )

def test_dataset_local_paths_no_trailing_whitespace():
    """Test that no local path in DATASETS_MAPPING has trailing whitespace."""
    for key, info in DATASETS_MAPPING.items():
        local = info.get("local", "")
        assert isinstance(local, str) and local, f"'local' for dataset '{key}' is missing or not a string."
        # Check that the local path does not have trailing whitespace
        assert local == local.rstrip(), f"Local path for dataset '{key}' has trailing whitespace."