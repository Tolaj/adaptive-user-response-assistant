import warnings
from pathlib import Path


def download_from_hf(repo_id: str, dest: Path, filename: str | None = None) -> Path:
    """Download model from HuggingFace Hub into dest/."""
    from huggingface_hub import snapshot_download, hf_hub_download

    dest.mkdir(parents=True, exist_ok=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if filename:
            hf_hub_download(repo_id=repo_id, filename=filename, local_dir=str(dest))
        else:
            snapshot_download(repo_id=repo_id, local_dir=str(dest))
    print(f"[HF] {repo_id} → {dest}")
    return dest


if __name__ == "__main__":
    print("Usage: download_from_hf('org/model', Path('./models/llm/my-model'))")
