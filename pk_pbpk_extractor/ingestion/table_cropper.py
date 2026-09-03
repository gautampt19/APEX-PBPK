from PIL import Image
import os

def crop_table_from_image(page_image: Image.Image, bbox: list, dpi: int = 300) -> Image.Image:
    """
    Crops a table using the bounding box [x0, y0, x1, y1] from MinerU.
    """
    # bbox usually [x0, y0, x1, y1]
    # Adjust for DPI if needed, but assuming bbox is relative to image dimensions
    
    # Crop the image
    cropped_image = page_image.crop((bbox[0], bbox[1], bbox[2], bbox[3]))
    
    # Optional: resize or enhance for 300 DPI equivalent if needed
    
    return cropped_image
