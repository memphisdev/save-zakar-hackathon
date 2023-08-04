import os
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()
ROOT_PATH = Path.cwd().parent
DATA_PATH = ROOT_PATH / "data"
RAW_PATH = DATA_PATH / "raw"
PREPROCESSED_PATH = DATA_PATH / "preprocessed"
DATASET_PATH = DATA_PATH / "dataset"


@dataclass(frozen=True)
class MemphisCredentials:
    HOST: str = os.getenv("HOSTNAME")
    USERNAME: str = os.getenv("CLIENT_USERNAME")
    PASSWORD: str = os.getenv("CLIENT_PASSWORD")
    ACCOUNT_ID: int = int(os.getenv("ACCOUNT_ID"))


class Station(Enum):
    FIRE_ALERTS: str = "zakar-fire-alerts"
    TEMPERATURE_READINGS: str = "zakar-temperature-readings"
    TWEETS: str = "zakar-tweets"


class DataName(StrEnum):
    FIRE_ALERTS: str = auto()
    TEMPERATURE_READINGS: str = auto()
    TWEETS: str = auto()


@dataclass
class ConsumerConfig:
    consumer_name: str = "consumer"
    stations: list[Station] = field(
        default_factory=lambda: [station.value for station in Station]
    )


@dataclass
class RawData:
    fire_alerts_path: Path = RAW_PATH / f"{DataName.FIRE_ALERTS}.json"
    temperature_readings_path: Path = RAW_PATH / f"{DataName.TEMPERATURE_READINGS}.json"
    tweets_path: Path = RAW_PATH / f"{DataName.TWEETS}.json"

    @property
    def exist(self) -> bool:
        return (
            self.fire_alerts_path.exists()
            and self.temperature_readings_path.exists()
            and self.tweets_path.exists()
        )

    @property
    def fire_alerts(self) -> pd.DataFrame:
        if self.fire_alerts_path.exists():
            return pd.read_json(self.fire_alerts_path, lines=True)
        else:
            raise FileNotFoundError(f"Could not find {self.fire_alerts_path}.")

    @property
    def temperature_readings(self) -> pd.DataFrame:
        if self.temperature_readings_path.exists():
            return pd.read_json(self.temperature_readings_path, lines=True)
        else:
            raise FileNotFoundError(f"Could not find {self.temperature_readings_path}.")

    @property
    def tweets(self) -> pd.DataFrame:
        if self.tweets_path.exists():
            return pd.read_json(self.tweets_path, lines=True)
        else:
            raise FileNotFoundError(f"Could not find {self.tweets_path}.")


@dataclass
class PreprocessedData:
    tweets_path: Path = PREPROCESSED_PATH / f"{DataName.TWEETS}_preprocessed.parquet"
    temperature_readings_path: Path = (
        PREPROCESSED_PATH / f"{DataName.TEMPERATURE_READINGS}_preprocessed.parquet"
    )

    @property
    def temperature_readings(self) -> pd.DataFrame:
        if self.temperature_readings_path.exists():
            return pd.read_json(self.temperature_readings_path, lines=True)
        else:
            raise FileNotFoundError(f"Could not find {self.temperature_readings_path}.")

    @property
    def tweets(self) -> pd.DataFrame:
        if self.tweets_path.exists():
            return pd.read_json(self.tweets_path, lines=True)
        else:
            raise FileNotFoundError(f"Could not find {self.tweets_path}.")


@dataclass
class Dataset:
    tweets_train_path: Path = DATASET_PATH / f"{DataName.TWEETS}/train.parquet"
    tweets_test_path: Path = DATASET_PATH / f"{DataName.TWEETS}/test.parquet"
    train_path: Path = DATASET_PATH / "train.parquet"
    test_path: Path = DATASET_PATH / "test.parquet"
    train_days: int = 5 * 365
    test_days: int = 2 * 365
    common_cols: list[str] = field(
        default_factory=lambda: ["day", "geospatial_x", "geospatial_y"]
    )

    @property
    def train_test_split(self) -> float:
        return self.train_days / (self.train_days + self.test_days)

    @property
    def exist(self):
        return (
            self.train_path.exists()
            and self.test_path.exists()
            and self.tweets_train_path.exists()
            and self.tweets_test_path.exists()
        )

    @property
    def tweets_train(self) -> pd.DataFrame:
        if self.tweets_train_path.exists():
            return pd.read_parquet(self.tweets_train_path)
        else:
            raise FileNotFoundError(f"Could not find {self.tweets_train_path}.")

    @property
    def tweets_test(self) -> pd.DataFrame:
        if self.tweets_test_path.exists():
            return pd.read_parquet(self.tweets_test_path)
        else:
            raise FileNotFoundError(f"Could not find {self.tweets_test_path}.")

    @property
    def train(self) -> pd.DataFrame:
        if self.train_path.exists():
            return pd.read_parquet(self.train_path)
        else:
            raise FileNotFoundError(f"Could not find {self.train_path}.")

    @property
    def test(self) -> pd.DataFrame:
        if self.test_path.exists():
            return pd.read_parquet(self.test_path)
        else:
            raise FileNotFoundError(f"Could not find {self.test_path}.")
