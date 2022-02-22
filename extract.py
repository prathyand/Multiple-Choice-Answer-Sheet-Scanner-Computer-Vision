"""
Created on Fri Feb 15 18:59:36 2022

@author: Anuj Patel
"""
import numpy as np
from PIL import Image
import sys

if __name__ == '__main__':
    #Load the injected image
    injected = Image.open(sys.argv[1])  #sys.argv[1]
    injected = injected.convert("L")
    
    total_bar = {}       #Stores all column values where the line is detected, values are number of pixels detected in that column.
    for i in range(525,1225):     #Our code starts from column 669, so we will search for the code in a 
        for j in range(400,550):  #bounding box around the known position of the code. This also accounts for changes in the position due to printing/scanning.
            pix = injected.getpixel((i,j))
            if pix<50:            #Looking for dark pixels 
                if i in total_bar.keys(): 
                    total_bar[i]+=1  #counting number of dark pixels for that column in the bounding box
                else:
                    total_bar[i]=1        
    
    total_bar = {k:l for k,l in total_bar.items() if l>40}    #removing columns with low count for dark pixels (since they will not be the code columns)
    
    answers_net = np.array(list(total_bar.keys()))[1:] - np.array(list(total_bar.keys()))[0] - 2  #remove the first line (the identifier line)
    questions = np.floor(answers_net/5)+1    #all questions (duplicates allowed for multiple answers)
    answers_per_q = (answers_net)%5          #all answers
    
    multiples={}      #Stores all questions with more than one answer, values are the number of answers for that question.
    for i in np.unique(questions):
        if np.count_nonzero(questions==i)>1:
            multiples[int(i)] = np.count_nonzero(questions==i)
    
    number_to_alphabet = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E'}
    curr_question = questions[0]    #first question, keeps track of current question number in the loop.
    str_ans = str(int(curr_question)) + ' ' + str(number_to_alphabet[answers_per_q[0]])   #first answer to the first question (could be multiple but only selecting the first correct option here)
    file = open(sys.argv[2], "w")
    for i in range(1,len(questions)):
        answer = number_to_alphabet[answers_per_q[i]]
        if questions[i] == curr_question:
            str_ans += answer    #Keep building the answer string if there are multiple answers to the question
        else:
            file.write(str_ans+"\n")
            curr_question = questions[i]
            str_ans = str(int(curr_question)) + ' ' + str(number_to_alphabet[answers_per_q[i]]) #Build the base string (eg. "2 A") for next question 
    file.write(str_ans+"\n")
    file.close()