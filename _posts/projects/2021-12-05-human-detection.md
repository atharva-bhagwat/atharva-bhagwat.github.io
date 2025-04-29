---
layout: post
title: Human Detection using HOG Feature
categories: projects
permalink: projects/hog-human-detection
author: Atharva Bhagwat
---

# Steps

- Read image. Convert to grayscale using: Gray = round(0.299Red + 0.587Green + 0.114*Blue)
- Gradient calculation using prewitt's operator, magnitude calculation (sqrt(Gx^2+Gy^2)) and normalization.
- Gradient angle calculation.
- Calculate histogram bins for every cell (unsigned format/9 bins).
- Calculate normalized bins for every block (l2 norm).
- Flatten and concatenate normalized bins for every block to get a descriptor of length 7524.
- 3NN implementations using similarity formula: sum(min(input, train))/sum(train)

---

[Here](https://github.com/atharva-bhagwat/CSGY-6643/tree/main/human_detection) is the link to the code.
