# Assignment 1 Report
## Authors:
1. Prathmesh Deshmukh
2. Ahmed Shahzad 
3. Anuj Patel

## Image Blob Detector 

The image blob detector algorithm first blurs the images 
to standardize how the input is read 
After that the gray scaled blurred image 
is converted to a numpy array
This numpy array is than passed to the function
scan image which looks for the rgb value 
of line from Hough Transformation 
Then we convert tuple to list
(This function assumes it gets a single answer block)
Then we go through the column index
finding the respective blocks that correspond to each 
choice and then we store that in dictionary 

We then pass the every block in the dictionary and calculate how many zeros exist in the image block (this denotes how filled it is)
We return the count to the main function 
who updates the answer choice in regards to a threshold this threshold 
is set to make sure that answers that aren't filled don't get stored
If there is maxKey the answer Is returned 
if not None is returned 

# Answer Encoding System
To run the codes, use the same commands as given in the assignment:
python3 inject.py form.jpg answers.txt injected.jpg
python3 extract.py injected.jpg output.txt
The input files form.jpg and answers.txt are included in the repo. (form.jpg is the blank form)

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
- Ahmed Shahzad: Formulated approach for both parts (with one other team member for each part), wrote code for image blob detection, did testing for part 3.
- Prathmesh Deshmukh: Formulated approach for part 3 (scanning answers) with Ahmed Shahzad, wrote the remaining code for part 3, wrote report for part 3.
- Anuj Patel: Formulated approach for the encoding system with Ahmed Shahzad, wrote the code (inject.py and extract.py) and report for it.
