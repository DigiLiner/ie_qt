
#todo : 

Zoom 
  Mouse tekerleğine zoom bağla gitsin

Pan
  orta butonla pan moduna girsin
  move ile slider değeri değişsin
  butonu bırakınca öyle kalsın
Fikir: Recolor , target color ile renklerin değişmesini sağlayın
Fikir: Renklerde Cyclic özelliği eklenebilir. Spray güzel durur
Fikir: Ayna ile çizim
Şekiller , yıldız, üçgen , yuvarlak  dikdörtgen, ay, elips,ok falan
curve , eğriler
select tools
move tools
rotate tools
png brush
Fix:
  pen line cap falan


Next : 
- [X] Fix Color Palette position
- [ ] Correct slider values


dark mode

Renk kutusu absuttrik
Filtre için kutu yapılacak
Filtreler ile effektler ayrı menülere konabilir
Mouse hareketi ile araçların yanına açıklama , koordinat gibi detaylar
Zoom ortalamıyor
Silgi yapılacak
Copy-paste
Mark - move - selection
Spray güzel değil
Alpha kanalı ne olacak
Layer mümkün olabilir belki
Statusbar yapılacak
Rotate yapılacak
Mirror - Bekli
Resim şifreleme gelişebilir
Print
Splash about gelişmeli
Dockpanel daha sonra silinebilir
Şablon - stencil eklenebilir
Resmin etrafına Cetvel 
Resim bilgileri
Histogram
RGB ayarı
Blend
Pen köşeli çiziyor



# FUNCTIONALITIES
- [x] basic drawing functionality -ok
- [x] undo/redo functionality 
- [x] zoom in/out functionality
- [ ] import/export functionality
- [ ] multiple layers functionality
- [x] multiple documents functionality
- [ ] multiple users functionality
- [ ] real-time collaboration functionality
- [ ] image filters functionality
- [ ] image effects functionality
- [ ] image adjustments functionality
- [ ] image color palette functionality
- [ ] image crop functionality
- [ ] image resize functionality
- [ ] image rotation functionality
- [ ] image flip functionality
- [ ] image layer functionality
- [ ] image file functionality

# TOOLS
- [x] pen tool -ok  
  - [ ] TODO: Add more customization options for the pen tool (e.g., stroke width, opacity).

- [x] line tool -ok
- [ ] brush tool
- [x] eraser tool
- [x] fill tool
- [x] spray tool - needsoptimize
- [x] circle tool
- [x] rectangle tool
- [ ] polyline tool
- [ ] select tool
- [x] wand tool
- [ ] circular select tool
- [ ] move tool
- [ ] rotate tool
- [ ] scale tool
- [ ] text tool
- [x] color picker


# FILTERS
- [ ] grayscale filter
- [ ] sepia filter
- [ ] invert filter
- [ ] blur filter
- [ ] sharpen filter
- [ ] emboss filter
- [ ] edge detect filter
- [ ] colorize filter

# EFFECTS
- [ ] color balance effect
- [ ] color swap effect

# BORDERS
- [ ] border tool
- [ ] frame tool
- [ ] erode border tool
- [ ] dilate border tool

# IMAGE MANIPULATION
- [ ] crop tool
- [ ] resize tool
- [ ] rotate tool
- [ ] flip tool

# ADJUSTMENTS
- [ ] brightness tool
- [ ] contrast tool
- [ ] saturation tool
- [ ] hue tool

# COLOR PALETTE
- [x] color picker tool
- [ ] color palette tool

# LAYERS
- [ ] layer tool
- [ ] layer mask tool
- [ ] layer opacity tool
- [ ] layer blend tool

# FILE
- [ ] open file
- [ ] save file

# HELP
- [ ] about tool
- [ ] help tool

2025
Here's a list of potential missing features, tools, and filters:

1. Core Image Manipulation / Filters: * Color Adjustments: Brightness/Contrast, Hue/Saturation, Color Balance, Levels, Curves. * Image Filters: Blur/Sharpen (Gaussian, Motion, Unsharp Mask), Artistic (Oil Paint, Watercolor, Pixelate), Distort (Twirl, Pinch, Wave), Noise (Add, Reduce), Stylize (Find Edges, Solarize). * Transformations: Arbitrary Rotate, Resize/Scale, Perspective/Skew. * Image Adjustments: Grayscale, Sepia, Invert Colors.

2. Drawing/Painting Tools: * Brush Customization: Advanced brush shapes, textures, dynamics (flow, jitter). * Gradient Tool. * Text Tool. * Shape Tools: Polygon, Star, Custom Shapes. * Retouching Tools: Clone Stamp, Healing Brush, Dodge/Burn.

3. Selection Tools: * Lasso Tools: Freehand, Polygonal, Magnetic. * Color Range Selection. * Quick Selection Tool. * Refine Edge/Masking.

4. Layer Management: * Layer Opacity/Blending Modes. * Layer Grouping, Masks, Adjustment Layers, Styles/Effects. * Rasterize, Merge, Duplicate, Delete, Reorder Layers.

5. UI/UX Enhancements: * Advanced Color Picker Dialog. * History Panel. * Dedicated Tool Options Panel. * Grid/Guides, Rulers. * Zoom to Fit/Actual Pixels. * Comprehensive Keyboard Shortcuts. * Preferences/Settings Dialog.

6. File Formats: * Support for more image file formats (e.g., TIFF, BMP).

7. Performance: * Optimization for large images and complex operations.

Specific to current code:

ie_globals.pen_opacity and ie_globals.pen_blur sliders are not implemented.
The rotate function in main.py is empty.
The ie_tool_crop is defined but its functionality is not implemented.