import paddle
import paddleocr

# Prüfe verfügbare Geräte
print("Verfügbare Geräte:", paddle.device.get_available_device())
print("CUDA-Geräte:", paddle.device.cuda.device_count())

# Aktiviere GPU-Nutzung
paddle.device.set_device('gpu')

# Initialisiere PaddleOCR mit GPU
print("Initialisiere PaddleOCR mit GPU...")
ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)

print("PaddleOCR mit GPU wurde erfolgreich initialisiert!")