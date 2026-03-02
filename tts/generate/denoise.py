import numpy as np


def run_denoiser(
    latents: np.ndarray,
    lat_mask: np.ndarray,
    style: np.ndarray,
    hidden: np.ndarray,
    attn: np.ndarray,
    steps: int,
    model: dict,
) -> np.ndarray:
    """Run latent diffusion denoiser for `steps` steps."""
    batch = latents.shape[0]
    n_steps = np.full(batch, steps, dtype=np.float32)
    for step in range(steps):
        ts = np.full(batch, step, dtype=np.float32)
        latents = model["latent_denoiser"].run(
            None,
            {
                "noisy_latents": latents,
                "latent_mask": lat_mask,
                "style": style,
                "encoder_outputs": hidden,
                "attention_mask": attn,
                "timestep": ts,
                "num_inference_steps": n_steps,
            },
        )[0]
    return latents
