# Multiple-Choice-Answer-Scheet-Scanner

We developed a program that scans the answer sheet of a specific format, reads the answers marked by the student and writes the result to a .txt file.

## command to run the script:
Note: This script assumes that the input image is in "test-images/" directory and generates the txt file in "test-images/"
command to run the script is:

python3 grade.py inputimagename.jpg outputfilename.txt

## Approach
The program accepts path of the answer sheet image and a name(string) for the output file.
The image is read as a Pillow image. Since the input is a scanned image, the first step is to correct for any misalignments in the image as it might not be perfectly aligned. Image is processed using pillow's in-built filters for edge enhancements and detection. Edge detected image is then passed to a Hough transform function which detects vertical lines in the range of [-5 degree, +5 degree]. We then find the peaks in the Hough parametric space (which correspond to the lines formed by the boxes). Value of the 'thetas' parameter in the peaks is then averaged, which gives us the misalignment. Original Image is then rotated to fix the alignment issues.

After we fix the alignment of the image, next task we perform is to detect the blobs of ink in-order to detect the marked answer. For that, the image is first converted to 8-bit gray scale, blurred and then converted to a NumPy array. We also detect the position of first question, "1", on the original image. This information is then used to segment the transformed image regions where each region corresponds to a question. 85 segments (or blocks) are then processed to generate an answer string, accounting for any handwritten text to the left of the question. All the answers are stored in a list, and in the written to a .txt file. image below demonstrates the results when the script is run on one of the test images.

![alt text](https://github.com/prathyand/Multiple-Choice-Answer-Scheet-Scanner--Computer-Vision/blob/main/test-images/results_demo.PNG)

## Design Decisions

### Detecting the position of the first question (digit "1")
The algorithm for detecting "1" uses a cross-correlation kernel in a predefined region of the image where it is more likely to detect the digit 1. Function is designed such that it considers only the maximum of cross-correlation corresponding to the lowest X (column) co-ordinate, as it may falsely detect multiple maxima’s in very dark regions near marked answers. 

### Image Blob Detection algorithm
The image blob detector algorithm first blurs the images 
to standardize how the input is read 
After that the gray scaled blurred image 
is converted to a NumPy array. We then pass this NumPy image array along with coordinates of digit "1" to the
function 'scanImage'. We assume that the distance between two rows, two boxes in the same row and the distance between two columns does not change. With this assumption, we define a region for each question which contains 5 boxes(A, B,C,D,E), as shown in the image below:

![alt text](https://github.com/prathyand/Multiple-Choice-Answer-Scheet-Scanner--Computer-Vision/blob/main/test-images/SmallSample.PNG)

This region is then broken down into 5 blocks each containing one box. Pixel values in each block is first normalized using transformation (-block+255)/255) such that in the transformed image 0 corresponds to a white pixel and 1 corresponds to a black pixel. 
If the maximum of sum of all the pixels in the transformed block is below a certain threshold, this indicates that no box is filled. Else, sums of all the 5 blocks are then re-normalized with their MAX, and boxes with value > 75% of the MAX are considered as "filled" and the resulting answer string is then generated. 

Another region of a fixed size is defined to the left of the question, and cross-correlation is used to check if there is any hand-written text.

Each of the 85 rows is processed and answers detected in it are appended to a list, which, in the end is returned by the function.

## Test Results:
Our algorithm accurately detects multiple marked answers as well as any handwritten text to the left of the question. However, for few (2 to 3) rows, it fails to detect the answers marked correctly. This is due to the error accumulated in defining the region for each row/question. 
table below summarizes the accuracy of our program on various test results

![alt text](https://github.com/prathyand/Multiple-Choice-Answer-Scheet-Scanner--Computer-Vision/blob/main/test-images/testresults.PNG)

## Problems Faced:
- Hough Transform implementation was not very accurate in detecting small misalignments in the image, probably due to the issues with edge detection
- Some of the answers marked were not detected correctly by the algorithm due to accumulated error in the region defined for the row

### Further Improvements
- Edge detection can be improved using Canny, which will give better results for the Hough transform line detection
- A more robust mechanism to detect the segments for each row will further improve the accuracy of the program


