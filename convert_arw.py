import sys
import rawpy
import imageio

try:
    with rawpy.imread(r'd:\Gore 9-12-2025\assets\dr.ajay-domable.ARW') as raw:
        rgb = raw.postprocess()
    imageio.imsave(r'd:\Gore 9-12-2025\assets\dr.ajay-dombale.jpg', rgb)
    print("Conversion successful!")
except Exception as e:
    print(f"Error during conversion: {e}")
