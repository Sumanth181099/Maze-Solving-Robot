# The driver code was already given and was told not to change it.
# All the functions are written by us to solve the maze by finding the shortest path from start point to end point.

# Global variables:	CELL_SIZE, minpath, minpathlen, visit
# Importing necessary modules
import cv2
import numpy as np
import os


# To enhance the maze image
import image_enhancer


# Maze images in task_1_a images folder have cell size of 20 pixels
CELL_SIZE = 20

visit = []
minpath  = []
minpathlen = float('inf')


def readImage(img_file_path):

	"""
	Purpose:
	---
	the function takes file path of original image as argument and returns it's binary form
	"""

	binary_img = None
	binary_img = cv2.imread(img_file_path, cv2.IMREAD_GRAYSCALE)

	return binary_img

def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):
	
	"""
	Purpose:
	---
	the function takes binary form of original image, start and end point coordinates and solves the maze
	to return the list of coordinates of shortest path from initial_point to final_point
	"""
	global minpathlen
	adjlist = getadjlist(original_binary_img, no_cells_height, no_cells_width)	
	path = []
	path.append(initial_point)
	findpath(initial_point, final_point, adjlist, path, (-1, -1))
	minpathlen = float("inf")
	shortestPath = minpath
	return shortestPath

# Helper functions used to get the shortest path

def getroi(img, i,j):
	return img[i*CELL_SIZE:(i+1)*CELL_SIZE, j*CELL_SIZE:(j+1)*CELL_SIZE]

def getadjlist(img, m, n):
	global visit
	adjlist = [[0]*n for i in range(m)]
	visit = [[False]*n for i in range(m)]
	for i in range(m):
		for j in range(n):
			adjlist[i][j] = []
			cellroi = getroi(img, i, j)
			#up
			if i!=0 and cellroi[0][CELL_SIZE//2]==255 and getroi(img, i-1,j)[CELL_SIZE-1][CELL_SIZE//2]==255:
				adjlist[i][j].append((i-1, j))
			#down
			if i!=m-1 and cellroi[CELL_SIZE-1][CELL_SIZE//2]==255 and getroi(img, i+1,j)[0][CELL_SIZE//2]==255 :
				adjlist[i][j].append((i+1, j))
			#left
			if j!=0 and cellroi[CELL_SIZE//2][0]==255 and getroi(img, i,j-1)[CELL_SIZE//2][CELL_SIZE-1]==255:
				adjlist[i][j].append((i, j-1))
			#right
			if j!=n-1 and cellroi[CELL_SIZE//2][CELL_SIZE-1]==255 and getroi(img, i,j+1) [CELL_SIZE//2][0]==255:
				adjlist[i][j].append((i, j+1))
	return adjlist

def equal(a, b):
	return a[0]==b[0] and a[1]==b[1]

def findpath(src, dst, adjlist, path, previous):
	global minpathlen, minpath
	if equal(src, dst):
		if(len(path)<minpathlen):
			minpathlen = len(path)
			minpath = []
			for i in path:
				minpath.append(i)
		return 1

	for i in adjlist[src[0]][src[1]]:
		if not equal(i, previous) and not visit[i[0]][i[1]]:
			path.append(i)
			visit[i[0]][i[1]] = True
			findpath(i, dst, adjlist, path, src)
			visit[i[0]][i[1]] = False
			path.pop()
 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1a_images' folder or not

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1a_images/'				# path to directory of 'task_1a_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()
	
	no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
	no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
	
	print('\n============================================')
	
	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()
			
			no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
			no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
			
			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
	else:

		print('')


