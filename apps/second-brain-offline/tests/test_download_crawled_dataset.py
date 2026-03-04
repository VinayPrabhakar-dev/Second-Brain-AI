import json
from pathlib import Path

import pytest

@pytest.mark.integration
class TestDownloadCrawledDataset:
    @pytest.fixture
    def crawled_dir(self) -> Path:
        return Path("data/crawled")
    
    def test_crawled_data_directory_exists(self, crawled_dir: Path) -> None:
        assert crawled_dir.exists(), "Crawled data directory does not exist"
        assert crawled_dir.is_dir(), "Crawled data path is not a directory"


    def test_json_files_in_crawled_dir(self, crawled_dir: Path) -> None:
        json_files = list(crawled_dir.glob("*.json"))
        non_empty_json_files = [f for f in json_files if f.stat().st_size > 0]

        assert len(non_empty_json_files) > 0, (
            "No non-empty JSON files found in crawled directory"
        )

        for json_file in json_files:
            try:
                with open(json_file, "r") as f:
                    json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON file: {json_file}")