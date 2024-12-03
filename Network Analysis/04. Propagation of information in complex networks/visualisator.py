import imageio
import numpy as np


class Visualisator:
    @classmethod
    def generate_gif(cls, images: list[np.ndarray], path: str, duration_ms: int, reverse: bool = False, interpolate_frames: int = 0):
        if reverse:
            images.extend(image.copy() for image in reversed(images[1:-1]))
        else:
            images.append(images[-1].copy())

        if interpolate_frames > 0:
            interpolated = []
            for image1, image2 in zip(images[:-1], images[1:]):
                interpolated.extend(cls.interpolate(image1, image2, interpolate_frames))
            images = interpolated
            duration_ms /= (interpolate_frames + 1)

        imageio.mimsave(path, images, loop=0, duration=duration_ms)

    @classmethod
    def interpolate(cls, image1: np.ndarray, image2: np.ndarray, frames: int) -> list[np.ndarray]:
        frames += 1
        interpolated = []
        for i in range(frames):
            alpha = (frames - i) / frames
            blended_image = image1.astype(np.float32) * alpha + image2.astype(np.float32) * (1-alpha)
            blended_image = np.clip(blended_image, 0, 255).astype(np.uint8)
            interpolated.append(blended_image)
        return [image1] + interpolated + [image2]
    