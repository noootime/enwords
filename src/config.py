import os
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class AppConfig:
    app_name: str = "ENWORDS"
    app_version: str = "0.0.1"
    exam_dir: str = "exams"
    history_file: str = "history.json"
    config_file: str = "config.json"
    viewport_size: int = 8
    grid_columns: int = 6
    word_max_width: int = 10
    default_encoding: str = "utf-8"
    auto_save_history: bool = True
    theme: str = "default"


class Config:
    def __init__(self):
        self._config_dir = self._get_config_dir()
        self._config_path = os.path.join(self._config_dir, "config.json")
        self._config = AppConfig()
        self._load_config()

    def _get_config_dir(self) -> str:
        if os.name == 'nt':
            config_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), "enwords")
        else:
            config_dir = os.path.join(os.path.expanduser('~'), ".config", "enwords")

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        return config_dir

    def _load_config(self):
        if os.path.exists(self._config_path):
            try:
                with open(self._config_path, 'r', encoding=self._config.default_encoding) as f:
                    config_data = json.load(f)
                    for key, value in config_data.items():
                        if hasattr(self._config, key):
                            setattr(self._config, key, value)
            except Exception as e:
                print(f"Loading config file failed: {str(e)}")

    def save_config(self):
        try:
            with open(self._config_path, 'w', encoding=self._config.default_encoding) as f:
                json.dump(asdict(self._config), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Save config file failed: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self._config, key, default)

    def set(self, key: str, value: Any) -> bool:
        if hasattr(self._config, key):
            setattr(self._config, key, value)
            return True
        return False

    def get_exam_dir(self) -> str:
        if os.path.isabs(self._config.exam_dir):
            exam_dir = self._config.exam_dir
        else:
            app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            exam_dir = os.path.join(app_root, self._config.exam_dir)

        if not os.path.exists(exam_dir):
            os.makedirs(exam_dir)

        return exam_dir