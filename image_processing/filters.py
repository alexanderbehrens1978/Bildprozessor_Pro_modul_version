from PIL import Image, ImageFilter, ImageOps, ImageChops, ImageEnhance
from tkinter import messagebox

def apply_filter(img, filter_name, strength=1.0):
    """Apply a filter to an image with the given strength"""
    try:
        if filter_name == "Negativ":
            blend_factor = min(max(strength, 0), 1)
            inverted = ImageOps.invert(img)
            return Image.blend(img, inverted, blend_factor)
        elif filter_name == "Multiplikation":
            blend_factor = min(max(strength, 0), 1)
            overlay_value = int(255 * blend_factor)
            overlay = Image.new("RGB", img.size, (overlay_value, overlay_value, overlay_value))
            return ImageChops.multiply(img, overlay)
        elif filter_name == "Helligkeit":
            enhancer = ImageEnhance.Brightness(img)
            effect = enhancer.enhance(2.0)
            return Image.blend(img, effect, strength)
        elif filter_name == "Kontrast":
            enhancer = ImageEnhance.Contrast(img)
            effect = enhancer.enhance(2.0)
            return Image.blend(img, effect, strength)
        elif filter_name == "Schärfen":
            enhancer = ImageEnhance.Sharpness(img)
            effect = enhancer.enhance(2.0)
            return Image.blend(img, effect, strength)
        elif filter_name == "Weichzeichnen":
            effect = img.filter(ImageFilter.GaussianBlur(radius=5))
            return Image.blend(img, effect, strength)
        elif filter_name == "Graustufen":
            blend_factor = min(max(strength, 0), 1)
            gray = img.convert("L").convert("RGB")
            return Image.blend(img, gray, blend_factor)
        elif filter_name == "Sepia":
            blend_factor = min(max(strength, 0), 1)
            gray = img.convert("L")
            sepia = ImageOps.colorize(gray, "#704214", "#C0A080")
            return Image.blend(img, sepia, blend_factor)
        elif filter_name == "Posterize":
            bits = max(1, min(8, int(round((1 - strength) * 7) + 1)))
            return ImageOps.posterize(img, bits)
        elif filter_name == "Solarize":
            threshold = int((1 - strength) * 255)
            return ImageOps.solarize(img, threshold=threshold)
        elif filter_name == "Kantenerkennung":
            blend_factor = min(max(strength, 0), 1)
            effect = img.filter(ImageFilter.FIND_EDGES)
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Emboss":
            blend_factor = min(max(strength, 0), 1)
            effect = img.filter(ImageFilter.EMBOSS)
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Edge Enhance":
            blend_factor = min(max(strength, 0), 1)
            effect = img.filter(ImageFilter.EDGE_ENHANCE)
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Detail":
            blend_factor = min(max(strength, 0), 1)
            effect = img.filter(ImageFilter.DETAIL)
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Smooth":
            blend_factor = min(max(strength, 0), 1)
            effect = img.filter(ImageFilter.SMOOTH)
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Binarize":
            blend_factor = min(max(strength, 0), 1)
            gray = img.convert("L")
            effect = gray.point(lambda x: 255 if x > 128 else 0).convert("RGB")
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Gamma Correction":
            gamma = 2.0
            inv_gamma = 1.0 / gamma
            table = [int((i / 255.0) ** inv_gamma * 255) for i in range(256)]
            effect = img.point(table * 3)
            blend_factor = min(max(strength, 0), 1)
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Adaptive Threshold":
            blend_factor = min(max(strength, 0), 1)
            effect = ImageOps.autocontrast(img)
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Color Boost":
            enhancer = ImageEnhance.Color(img)
            effect = enhancer.enhance(2.0)
            blend_factor = min(max(strength, 0), 1)
            return Image.blend(img, effect, blend_factor)
        elif filter_name == "Custom":
            return img.copy()
        else:
            return img.copy()
    except Exception as e:
        messagebox.showerror("Error", f"Error applying filter: {str(e)}")
        return img.copy()