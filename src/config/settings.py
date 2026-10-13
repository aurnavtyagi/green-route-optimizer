import os
from pathlib import Path


def _load_local_env() -> None:
	"""Load environment variables from the project .env file if present."""

	env_path = Path(__file__).resolve().parents[2] / ".env"

	if not env_path.exists():
		return

	with env_path.open("r", encoding="utf-8") as env_file:
		for line in env_file:
			stripped = line.strip()

			if not stripped or stripped.startswith("#") or "=" not in stripped:
				continue

			key, value = stripped.split("=", 1)
			key = key.strip()
			value = value.strip().strip('"').strip("'")

			if key and key not in os.environ:
				os.environ[key] = value


_load_local_env()


def _load_streamlit_secret(name: str) -> str:
	"""Return a Streamlit secret if the app is running in Streamlit."""

	try:
		import streamlit as st

		if hasattr(st, "secrets") and name in st.secrets:
			return str(st.secrets[name]).strip()
	except Exception:
		return ""

	return ""


AQICN_API_TOKEN = (
	os.getenv("AQICN_API_TOKEN", "").strip()
	or _load_streamlit_secret("AQICN_API_TOKEN")
)
