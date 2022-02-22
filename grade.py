#Import the Image and ImageFilter classes from PIL (Pillow)
from PIL import Image
from PIL import ImageFilter
import sys
import os
import random
import numpy as np
from scipy import ndimage
from scipy.ndimage import convolve
import math

def edge_Detection(im):
    ########################################
    # This function returns edge image created using pillow's inbuilt filters
    # Input parameters:(im)
    # *im: Pillow image
    ########################################
    
    edge_image = im.filter(ImageFilter.SMOOTH)
    edge_image = edge_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    edge_image = edge_image.filter(ImageFilter.FIND_EDGES)
    edge_image=edge_image.convert('1')
    return edge_image


#reference:https://alyssaq.github.io/2014/understanding-hough-transform/
def hough_trans(region,threshold=0.5):
    ########################################
    # This function returns rhos/thetas and vote accumulator matrix for vertical lines in range [-5 degree,+5 degree]
    # Input parameters:(region,threshold)
    # *region: Binary Pillow image with edges as white pixels and 
    # *threshold: Precision angle in degrees for theta
    ########################################
    
    thetas = np.deg2rad(np.arange(-5.0, 5.0, threshold))
    width, height = region.width,region.height
    D = int(round(math.sqrt(width * width + height * height)))
    rhos = np.linspace(-D, D, D * 2)   
    COSST = np.cos(thetas)
    SINT = np.sin(thetas)
    numtheta = len(thetas)
    accumulator = np.zeros((2 * D, numtheta), dtype=np.uint8)
    edges=[]
    for i in range(0,width):
        for j in range(600,height):
            if(region.getpixel((i,j))==255):
                edges.append((i,j))
    for pixl in edges:
        for thetaindx in range(len(thetas)):
            rho = D + int(round(pixl[0] * COSST[thetaindx] + pixl[1] * SINT[thetaindx]))
            accumulator[rho, thetaindx] += 1
    return accumulator,rhos,thetas

def getangleofcorrection(accumulator, thetas, rhos,thresholdper=1):
    ########################################
    # This function attempts to find the angle of mis-alignment of the document image
    # using the hough_trans function 
    # Input parameters:(accumulator, thetas, rhos,thresholdper)
    # *accumulator: Vote accumulator matrix returned by from hough_trans
    # *thetas: Range matrix of polar coordinate theta 
    # *rhos: Range matrix of polar coordinate rho 
    # *thresholdper: Threshold value in the range (0,1], (thresholdper=0.8 means consider only (rho,theta) -
    # pairs for which votes> (80% of the highest vote count)  
    ########################################
    
    maxi=np.argmax(accumulator)
    maxrhocord,maxthetacord=(maxi+1)//accumulator.shape[1],(maxi+1)%accumulator.shape[1]-1
    maxvotes=accumulator[maxrhocord][maxthetacord]
    threshold=maxvotes if int(thresholdper*maxvotes)<1 else int(thresholdper*maxvotes)
    peaks=np.argwhere(accumulator>=threshold)
    
    # consider the average angle of all peaks as the tiltangle, and return it
    tiltangle=np.rad2deg(np.mean(thetas[peaks[:,1:]]))
    
    return tiltangle

def getpos1(im):
    ########################################
    # this function returns the (x,y) position of "1" from the image-
    # using  cross correlation kernel 
    # Input parameters:(im)
    # *im: Pillow image
    ########################################
    
    # Processing the image for noise and binarizing it 
    img = im.filter(ImageFilter.SMOOTH)
    img = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    img=img.convert('1')
    
    # region in the image space where the kernel runs 
    box = (200,650,250,710)
    region = img.crop(box)
    npimage=~np.array(region)
    npimage=npimage.astype(int)
    
    #Correlation kernel to find x,y coordinates of "1"
    kn=np.ndarray(shape=(21,12), dtype=np.uint8,buffer=np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
       [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
       [0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.uint8))
    
    
    conimg=ndimage.correlate(npimage,kn,output=int).astype(int)
    
    maxind=np.unravel_index(np.argmax(conimg),conimg.shape)
    
    ########################################
    # Code snippet below finds the most likely position of "1" in the region and returns its coordinates in the image space
    ########################################
    
    maxx=np.argmax(conimg,axis=0)
   
    for i in range(50):
        if conimg[maxx[i]][i]>50:
            break
    if(i<maxind[1]):
        maxind=(maxx[i],i)
    max_x=maxind[1]+200
    max_y=maxind[0]+650
    return(max_x,max_y)

def scanImage(image_array,one_cords):
    ########################################
    # this function detects the marked answers on the answer sheet and returns the-
    # answers as a list
    # Input parameters:(image_array,one_cords)
    # *image_array: Pillow image converted to a numpy array
    # *one_cords: tuple (x1,y1) representing the coordinates of "1" in the image [returned by getpos1 function]
    ########################################
    
    # Offsets for moving to the next row/column
    ROWSHIFTDOWN=48
    COLSHIFTRIGHT=433
    Qcols=[i for i in range(0,COLSHIFTRIGHT*3,COLSHIFTRIGHT)]
    Qrows=[i for i in range(0,ROWSHIFTDOWN*29,ROWSHIFTDOWN)]
    
    x1,y1=one_cords
    outputbuffer=[]
    counter=1
    breakloop=False
    choicesList = list("ABCDE")
    
    for coladjust in Qcols:
        x_new=x1+coladjust
        for rowadjust in Qrows:
            # Condition that checks if we have reached the last question in the 3rd column
            if(coladjust==Qcols[2] and rowadjust==Qrows[27]):
                breakloop=True
                break
                
            y_new=y1+rowadjust
            output=""
            
            # This snippet of code checks for any hand written text to the left of the question
            digitbox=image_array[y_new-16:y_new+16,x_new-75:x_new-25]
            hdsum=np.sum((-digitbox+255)/255)
            
            # Creating bounds for partitioning the scanning window into rectangles
            column_index_list = [x_new+15,x_new+75,x_new+135,x_new+195,x_new+255,x_new+315]
            row_index_list = [y_new-24,y_new+24]
            
            # scanning window where we search for marked answers
            answer_block = image_array[(y_new-25):(y_new+25),(x_new-20):(x_new+335)]
            
            IIMM = []
            for second in range(1, len(column_index_list)):
                first = second - 1
                lower_bound_c = column_index_list[first] + 1
                upper_bound_c = column_index_list[second]
                block = image_array[row_index_list[0]:row_index_list[1], lower_bound_c:upper_bound_c]
                
                # Normalizing the image pixels in the range(0,1) where 0 is "white" and 1 is "black"-
                # sum is stored in IIMM array
                IIMM.append(np.sum((-block+255)/255))

            maxiimm=max(IIMM)
            
            if(maxiimm<500):
                # If the max of all reactangle is below threshold, assume no answer is marked
                # Handles no answer marked case
                
                output=""
                
            else:
                
                # Normalize sums for each rectangle with max value and consider the rectangle as "marked" if -
                # value is greater than 75% of the max
                
                IIMM2=IIMM/maxiimm
                IIMM2=IIMM2>0.75
                output=""
                for i in range(len(IIMM2)):
                    if IIMM2[i]:
                        output+=choicesList[i]
                        
            if(hdsum>60):
                # If handwritten text is detected using threshold, add "x" to the answer string
                output+=" x"
                
            outputbuffer.append(str(counter)+" "+output)
            counter+=1
            
        if breakloop:
            break
    return outputbuffer
    

if __name__ == '__main__':
    
    DICT="test-images/"
    
    imgname=sys.argv[1]
    ImgPATH=DICT+imgname
    outputPATH=DICT+sys.argv[2]
    
    # Delete the .txt file if already exists, to avoid conflicts
    if os.path.exists(outputPATH):
        os.remove(outputPATH)
        
    # Load an image 
    im = Image.open(ImgPATH) 
    
    # Detecting edges
    edge_image=edge_Detection(im)
    
    # Applying hough transform to find vertical lines
    accumulator,rhos,thetas=hough_trans(edge_image)
    
    # Correcting the image to adjust for mis-alignments
    Correction_angle=getangleofcorrection(accumulator, thetas, rhos,thresholdper=1)
    ag_corr=im.rotate(Correction_angle)
    
    # Scanning the image to detect marked answers
    gray_im = ag_corr.convert("L")
    blur_im = gray_im.filter(ImageFilter.BLUR)
    gray_array = np.array(blur_im)
    ans = scanImage(gray_array,getpos1(ag_corr))
    
    # Writing the results to the .txt file
    with open(outputPATH, 'w') as f:
        f.write('\n'.join(ans))
    f.close()