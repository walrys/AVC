###What it does
classify a given audio/video clip into predefined venue categories based on acoustic/visual/textual features

##Given
Tools and Datasets: https://drive.google.com/file/d/0BzCduZQhBlNybURhWlBsRGcwUjA/view?usp=sharing
  - Training set: 30 categories of 100 micro-videos each
  - Test set (query): 900 micro-videos
  - Tools: that extract keyframes and audio track of videos for analysis
  - Audio Features:
    - Zero-crossing Rate
    - Energy
    - Magnitude Spectrum
    - MFCC
  - Visual Features:
    - Tools used in A1 to analyse keyframes
  - A basic UI template to extract simple acoustic features

##Implementation
###Audio Classification (70%)
####1. Feature Extraction
Extract features using feature extractor tools given.
Combine features based on appropriate weights (early fusion vs late fusion).

####2. Venue Categorising
Audio-based classification using machine-learning (softmax, svm, kNN, leanear regression)

####3. UI
Work on example UI provided. Simple UI.
Input: A micro-video file. Adjustable hyperparameters for weightage of features
Output: Estimated venue labels (categories)

####4. Evaluation
Evaluate performance of classifier with appropriate feature combination using F1 or MAP

####5. Analysis
Analysis and aggregation of results. Do systematic tests for different combination of acoustic features to analyse performance.

###Visual/Text Classification (30%)
####Video frame analysis
Pull 1 or more frames from micro-videos along with their textual features to enhance audio classifier
####Analysis
Test different combination of audio/visual/textual features

###Extra Grades (???%)
Extra Grades will be given for implementing additional innovative features or design




