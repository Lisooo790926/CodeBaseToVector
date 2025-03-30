"""Pytest configuration file."""

import os
import sys
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# 設置測試環境變量
os.environ['GOOGLE_API_KEY'] = 'test_api_key' 