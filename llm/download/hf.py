import warnings
from pathlib import Path
from huggingface_hub import hf_hub_download


def download_from_hf(repo_id: str, dest: Path, filename: str) -> Path:
    """
    Download a single GGUF file from a HuggingFace repo into dest/.

    Parameters
    ----------
    repo_id  : HuggingFace repo, e.g. "Qwen/Qwen2.5-3B-Instruct-GGUF"
    dest     : local directory to save into  (models/llm/<model-name>/)
    filename : exact filename in the repo,   e.g. "qwen2.5-3b-instruct-q4_k_m.gguf"
    """
    print(f"[HF] Downloading {repo_id}/{filename} → {dest}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        local_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=str(dest),
        )
    print(f"[HF] Done: {local_path}")
    return Path(local_path)
