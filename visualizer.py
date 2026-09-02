from PIL import Image, ImageDraw
import io

def draw_bounding_boxes(image_bytes: bytes, boxes: list) -> Image.Image:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for box in boxes:
        if len(box) >= 4:
            ymin, xmin, ymax, xmax = box[:4]
            left = xmin * width if xmax <= 1.0 else (xmin / 1000.0) * width
            top = ymin * height if ymax <= 1.0 else (ymin / 1000.0) * height
            right = xmax * width if xmax <= 1.0 else (xmax / 1000.0) * width
            bottom = ymax * height if ymax <= 1.0 else (ymax / 1000.0) * height

            draw.rectangle([left, top, right, bottom], outline="red", width=4)

    return image