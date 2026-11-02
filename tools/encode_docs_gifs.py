"""Encode the rendered, actual-asset animation frames into portable README GIFs."""
import json

from PIL import Image

from build_docs_media import MEDIA, OUTPUT


def encode() -> None:
    """Use one shared palette per animation to prevent distracting colour flicker."""
    jobs = json.loads((OUTPUT / "manifest.json").read_text(encoding="utf-8"))
    for job in jobs:
        frames = [Image.open(path.replace(".svg", ".png")).convert("RGB") for path in job["frames"]]
        samples = Image.new("RGB", (800, 260*len(frames)))
        for index, frame in enumerate(frames):
            samples.paste(frame, (0, index*260))
        palette = samples.quantize(colors=256)
        indexed = [frame.quantize(palette=palette, dither=0) for frame in frames]
        target = MEDIA / job["name"]
        indexed[0].save(target, save_all=True, append_images=indexed[1:], duration=job["duration"], loop=0, disposal=2, optimize=False)
        with Image.open(target) as result:
            assert result.is_animated and result.n_frames >= 10
            assert result.size == (800, 260)
        print(f"{target.name}: {len(frames)} frames, {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    encode()
