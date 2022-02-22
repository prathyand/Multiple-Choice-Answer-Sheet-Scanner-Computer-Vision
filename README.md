# Multiple-Choice-Answer-Scheet-Scanner

We developed a program that scans the answer sheet of a specific format, reads the answers marked by the student and writes the result to a .txt file.

## command to run the script:
Note: This script assumes that the input image is in "test-images/" directory and generates the txt file in "test-images/"
command to run the script is:

python3 grade.py inputimagename.jpg outputfilename.txt

## Approach
The program accepts path of the answer sheet image and a name(string) for the output file.
The image is read as a Pillow image. Since the input is a scanned image, the first step is to correct for any misalignments in the image as it might not be perfectly aligned. Image is processed using pillow's in-built filters for edge enhancements and detection. Edge detected image is then passed to a Hough transform function which detects vertical lines in the range of [-5 degree, +5 degree]. We then find the peaks in the Hough parametric space (which correspond to the lines formed by the boxes). Value of the 'thetas' parameter in the peaks is then averaged, which gives us the misalignment. Original Image is then rotated to fix the alignment issues.

After we fix the alignment of the image, next task we perform is to detect the blobs of ink in-order to detect the marked answer. For that, the image is first converted to 8-bit gray scale, blurred and then converted to a NumPy array. We also detect the position of first question, "1", on the original image. This information is then used to segment the transformed image regions where each region corresponds to a question. 85 segments (or blocks) are then processed to generate an answer string, accounting for any handwritten text to the left of the question. All the answers are stored in a list, and in the written to a .txt file.

## Design Decisions

### Detecting the position of the first question (digit "1")
The algorithm for detecting "1" uses a cross-correlation kernel in a predefined region of the image where it is more likely to detect the digit 1. Function is designed such that it considers only the maximum of cross-correlation corresponding to the lowest X (column) co-ordinate, as it may falsely detect multiple maxima’s in very dark regions near marked answers. 

### Image Blob Detector
The image blob detector algorithm first blurs the images 
to standardize how the input is read 
After that the gray scaled blurred image 
is converted to a NumPy array. We then pass this NumPy image array along with coordinates of digit "1" to the
function 'scanImage'. We assume that the distance between two rows, two boxes in the same row and the distance between two columns does not change. With this assumption, we define a region for each question which contains 5 boxes(A, B,C,D,E). This region is then broken down into 5 blocks each containing one box. Pixel values in each block is first normalized using transformation (-block+255)/255) such that in the transformed image 0 corresponds to a white pixel and 1 corresponds to a black pixel. 
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

# PART-2 | Answer Encoding System
To run the codes, use the same commands as given in the assignment:  
python3 inject.py form.jpg answers.txt injected.jpg  
python3 extract.py injected.jpg output.txt  
The input files form.jpg and answers.txt are included in the repo, assumed to be in test-images folder (form.jpg is the blank form).
The output files injected.jpg and output.txt are saved in the working directory itself (also included in the repo).

* Brief Description:
    - The encoding system we have designed is kind of a simplified barcode.
    - Each answer is repsented using 5 vertical bars, one for each option in order. Black line means the option is correct, and white means it's incorrect. So the lines represent: Q1 A, Q1 B, Q1 C, ..., Q85 D, Q85 E. 
    - 85 questions means total number of lines is 85\*5 = 425 +1 identifier line which is a black line printed immediately preceding the first line (Q1 A). This signals the beginning of the barcode.
    - This encoding will not reveal the answer to the students. Even if a student somehow figures out the system, it will be quite improbable for them to count pixelwise. Additionally, the identifier line may also throw some off.

- Further implementation details are in the two python programs' decriptions as follows:

1. inject.py 
    - We have chosen a fixed region of the form to print the barcode as shown in the image. Since we are only dealing with the same format forms, this region will always be blank.
    - The program first draws the identifier line (at column 669), and then the answers for all questions in order. It is necessary to keep this line since Q1 may or may not have 'A' as an answer. It wouldn't be necessary if we also choose to print the incorrect option lines in some other colour, but that might risk revealing the answers to some smart students.
    - The vertical length of the barcode is kept at 50 pixels.

![alt text](https://github.iu.edu/cs-b657-sp2022/pdeshmuk-aap1-ahshahz-a1/blob/main/injected.jpg)

2. extract.py
    - Although we know the exact location of the barcode, we search for the code in a rectangular area enveloping the known position of the code (125 extra pixels left and right, 50 extra pixels up and down). This accounts for changes in the position of the code from the original injected image due to printing and scanning. 
    - The rectangular region is searched for dark pixels (<50 intensity) in a grayscale image (converted). This accounts for any color distortions from the original image.
    - All columns in the region who have more than 40 dark pixels are indentified to be our barcode lines. The lines were made 50 pixels long, but again, some room is given for distortions. 
    - False positives are highly unlikely since the region should be completely blank apart from the barcode. Despite that, a margin is kept from the region to the nearest text to ensure this.
    - The first line is treated as the identifier line, then we start decoding all the answers.
    - Once decoded, the output.txt file is created and answers added to it line by line.
    - answers.txt and output.txt completely match for all test cases tried.
  
 - Further Improvements:
    To make the system more robust, the vertical lines width can be increased to more pixels. This will deal with minor rotation of the image as well. This is quite simple to implement since we only need to draw extra lines, change the recangular region pixel values accordingly and increase the count threshold to qualify as a line. 
    We decided against this for now to limit the total width of the barcode.


## Contributions of the Authors
- Ahmed Shahzad: Formulated approach for both parts (with one other team member for each part), wrote code for image blob detection and report with Prathmesh, did testing for part 1.
- Prathmesh Deshmukh: Formulated approach for part 1 (scanning answers) with Ahmed Shahzad, wrote the remaining code for part 1, wrote report for part 1.
- Anuj Patel: Formulated approach for the encoding system with Ahmed Shahzad, wrote the code (inject.py and extract.py) and report for it.
