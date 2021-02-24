# Align-Image-And-Select-ROI
Align image, using an image as template and select ROI's coordinates


## Requirements
- pip install numpy
- pip install opencv-python
- pip install argparse
- pip install imutils
- pip install scipy
- pip install pytesseract

## USAGE
```
python config_image.py --template data/templatecnh.jpg --image data/testecnh.png
```

- "Enter" to move to the next step
- "Drag and drop" to select ROI (only 1)
- "C" to clear the selected area
- "Enter" to crop the ROI to get the coordinates and apply OCR to get text value
