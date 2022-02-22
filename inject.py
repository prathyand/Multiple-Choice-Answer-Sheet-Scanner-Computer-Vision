"""
Created on Fri Feb 15 16:56:28 2022

@author: Anuj Patel
"""
from PIL import Image, ImageDraw
import sys

if __name__ == '__main__':
    #Load the blank form 
    im = Image.open(sys.argv[1])
    
    #Load the correct answers
    file = open(sys.argv[2], 'r')
    answers = file.readlines()
    alphabet_to_number = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5}
    
    i=669   #This is the chosen pixel column number from which the code will be printed. 
    #Since all answer sheets are of the given format, this space will always be empty for the code to be printed.
    
    draw = ImageDraw.Draw(im) 
    draw.line([(i,450),(i,500)], fill=0)               #start line to signal beginning of the bar code
    i+=1
    for answer in answers:
        ans = list(answer.split(" ")[1].rstrip())      #extract the answer alphabets
        num_ans = [alphabet_to_number[x] for x in ans] #convert into integers using the dictionary 
        for n in num_ans:
            draw = ImageDraw.Draw(im) 
            draw.line([(i+n,450),(i+n,500)], fill=0)   #vertical length of the bar code (rows 450 to 500)
        i+=5
            
    #im.show()
    im.save(sys.argv[3])