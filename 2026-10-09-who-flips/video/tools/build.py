"""Render the saved Excalidraw timeline and encode the final MP4 and silent GIF."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import wave
from PIL import Image

VIDEO = Path(__file__).resolve().parents[1]
WORK = VIDEO / '.build'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-render', action='store_true', help='Reuse existing .build frames')
    args = parser.parse_args()
    if not args.skip_render:
        subprocess.run([os.environ.get('NODE', 'node'), str(VIDEO / 'tools/render.mjs'), '--animate'], check=True)
    frames = json.loads((WORK / 'frames.json').read_text())
    scenes = json.loads((VIDEO / 'source/scenes.json').read_text())
    expected_ms = round(sum(s['duration'] for s in scenes) * 1000)
    total_ms = sum(f['duration'] for f in frames)
    if total_ms != expected_ms:
        raise ValueError(f'Timeline duration differs: frames={total_ms}, scenes={expected_ms}')
    with wave.open(str(VIDEO / 'audio/narration.wav')) as audio:
        audio_duration = audio.getnframes() / audio.getframerate()
    if abs(audio_duration - total_ms / 1000) > .04:
        raise ValueError('The narration and animation durations differ; update the timing before rebuilding.')
    ffmpeg = os.environ.get('FFMPEG')
    if not ffmpeg:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    # Relative frame paths avoid machine-specific locations in the concat list.
    lines = ['ffconcat version 1.0']
    for frame in frames:
        lines.extend([f"file 'frames/{frame['file']}'", f"duration {frame['duration'] / 1000:.3f}"])
    lines.append(f"file 'frames/{frames[-1]['file']}'")
    concat = WORK / 'frames.ffconcat'
    concat.write_text('\n'.join(lines) + '\n')
    subprocess.run([
        ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-safe', '0', '-i', str(concat),
        '-i', str(VIDEO / 'audio/narration.wav'), '-map', '0:v:0', '-map', '1:a:0',
        '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
        '-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-t', str(total_ms / 1000),
        '-movflags', '+faststart', str(VIDEO / 'who-flips.mp4')
    ], check=True)
    # One palette across frames prevents shimmer around the drawn strokes.
    preview = Image.new('RGB', (540 * 3, 540 * 2), '#fffaf0')
    for i, scene in enumerate(scenes):
        im = Image.open(WORK / 'stills' / (scene['slug'] + '.png')).convert('RGB')
        preview.paste(im.resize((540, 540), Image.Resampling.LANCZOS), ((i % 3) * 540, (i // 3) * 540))
    palette = preview.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    preview.save(VIDEO / 'storyboard-preview.png')
    gif_frames = [Image.open(WORK / 'frames' / f['file']).convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    gif = VIDEO / 'who-flips.gif'
    gif_frames[0].save(gif, save_all=True, append_images=gif_frames[1:],
        duration=[f['duration'] for f in frames], loop=0, optimize=True, disposal=1,
        comment=b'Who Flips? | arxiv.org/abs/2606.16011 | Excalidraw animation')
    with Image.open(gif) as encoded:
        encoded_ms = 0
        for i in range(encoded.n_frames):
            encoded.seek(i)
            encoded_ms += encoded.info['duration']
        if encoded_ms != total_ms:
            raise ValueError(f'GIF duration differs: {encoded_ms} != {total_ms}')
    shutil.copy2(WORK / 'stills' / (scenes[0]['slug'] + '.png'), VIDEO / 'cover.png')
    shutil.copy2(WORK / 'stills' / (scenes[-1]['slug'] + '.png'), VIDEO / 'closing-card.png')
    print(f'Built MP4 + silent GIF: {total_ms / 1000:.1f} seconds, 1080 × 1080')

if __name__ == '__main__':
    main()
