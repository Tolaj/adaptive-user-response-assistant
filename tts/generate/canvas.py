import numpy as np

LATENT_MARGIN = 3


def build_latent_canvas(
    durations: np.ndarray,
    latent_dim: int,
    chunk_compress_factor: int,
    latent_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Build noisy latent canvas + boolean mask. Adds margin to prevent tail clipping."""
    lat_lens = (durations + latent_size - 1) // latent_size + LATENT_MARGIN
    max_len = lat_lens.max()
    lat_mask = (np.arange(max_len) < lat_lens[:, None]).astype(np.int64)
    batch = durations.shape[0]
    latents = np.random.randn(
        batch, latent_dim * chunk_compress_factor, max_len
    ).astype(np.float32)
    latents *= lat_mask[:, None, :]
    return latents, lat_mask
