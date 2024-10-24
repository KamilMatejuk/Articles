import sys
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


DAY = int(sys.argv[1])
MAX_DAYS = 92


def draw_rounded_rectangle(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    if fill:
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)  # Top and bottom middle sections
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)  # Left and right middle sections
        draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)  # Top-left corner
        draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)  # Top-right corner
        draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)  # Bottom-left corner
        draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)    # Bottom-right corner
    if outline:
        draw.arc([x1 - 1, y1 - 1, x1 + 2 * radius, y1 + 2 * radius+1], 180, 270, fill=outline, width=width)  # Top-left corner
        draw.arc([x2 - 2 * radius + 1, y1-1, x2, y1 + 2 * radius+1], 270, 360, fill=outline, width=width)  # Top-right corner
        draw.arc([x1 - 1, y2 - 2 * radius + 1, x1 + 2 * radius, y2+1], 90, 180, fill=outline, width=width)   # Bottom-left corner
        draw.arc([x2 - 2 * radius + 1, y2 - 2 * radius + 1, x2, y2+1], 0, 90, fill=outline, width=width)     # Bottom-right corner
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)  # Top
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)  # Bottom
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)  # Left
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)  # Right
    return draw


image = Image.open('winter_arc_progress.png') # 1914 x 690
x, y = image.size
draw = ImageDraw.Draw(image)

# progress bar
margin_left = 75
margin_bottom = 100
outer_size = 30
padding = 5
max_size = x - 2 * margin_left - 2 * padding - 4
size = int(DAY / MAX_DAYS * max_size)
draw = draw_rounded_rectangle(draw, radius=outer_size/2, fill=None, outline='white', width=5,
        xy=[margin_left, y-margin_bottom-outer_size, x-margin_left, y-margin_bottom])
draw = draw_rounded_rectangle(draw, radius=outer_size/2-padding, fill='white', width=1,
        xy=[margin_left+padding+2, y-margin_bottom-outer_size+padding, margin_left+padding+2+size, y-margin_bottom-padding])

# runner
runner = Image.open('winter_arc_runner.png')
runner = runner.resize((runner.size[0] // 2, runner.size[1] // 2))
image.paste(runner, (margin_left+padding+2+size-runner.size[0]//2, y-margin_bottom-outer_size-runner.size[1]-5), runner)

# text
text = f'{DAY/MAX_DAYS:.2%}'
font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-BI.ttf", 100)
text_width = draw.textsize(text, font=font)[0]
draw.text(((x - text_width) // 2, 50), text, fill=(255, 255, 255, 255), font=font)

# save
image.save('winter_arc_progress_daily.png', format="PNG")
