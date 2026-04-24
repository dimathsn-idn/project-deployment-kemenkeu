from __future__ import annotations

from typing import Literal

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

GapSize = Literal["small", "medium", "large"]


def three_columns_layout(
	ratios: tuple[int, int, int] = (1, 1, 1),
	gap: GapSize = "medium",
) -> tuple[DeltaGenerator, DeltaGenerator, DeltaGenerator]:
	"""Return 3 columns for equal or custom-width content sections."""
	col1, col2, col3 = st.columns(list(ratios), gap=gap)
	return col1, col2, col3


def sidebar_main_layout(
	sidebar_ratio: int = 1,
	main_ratio: int = 3,
	gap: GapSize = "large",
) -> tuple[DeltaGenerator, DeltaGenerator]:
	"""Return 2 columns where left behaves as sidebar and right as main content."""
	sidebar, main = st.columns([sidebar_ratio, main_ratio], gap=gap)
	return sidebar, main


def full_content_layout() -> DeltaGenerator:
	"""Return a full-width container for single-column content."""
	return st.container()
