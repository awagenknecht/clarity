"""Tests for cec2 baseline enhance module."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import hydra
import numpy as np
import pytest
from omegaconf import DictConfig

from clarity.evaluator.msbg.msbg_utils import read_signal
from clarity.recipes.cec2.baseline.enhance import enhance


@pytest.fixture()
def hydra_cfg(tmp_path: Path):
    """Fixture for hydra config."""
    hydra.core.global_hydra.GlobalHydra.instance().clear()
    hydra.initialize(config_path=".", job_name="test_cec2")
    cfg = hydra.compose(
        config_name="config", overrides=["path.root=.", f"path.exp_folder={tmp_path}"]
    )
    return cfg


def not_tqdm(iterable):
    """
    Replacement for tqdm that just passes back the iterable.

    Useful for silencing `tqdm` in tests.
    """
    return iterable


@patch("clarity.recipes.cec2.baseline.enhance.tqdm", not_tqdm)
def test_enhance(tmp_path: Path, hydra_cfg: DictConfig) -> None:
    """Test run_HL_processing function."""
    np.random.seed(0)

    # Run the enhance function
    enhance(hydra_cfg)

    # Check that the output signal is correct
    filename = tmp_path / "enhanced_signals" / "S06001_L0064_HA-output.wav"
    assert filename.exists()
    signal = read_signal(filename)
    assert np.sum(np.abs(signal)) == pytest.approx(78939.73132324219)
    print(tmp_path)
