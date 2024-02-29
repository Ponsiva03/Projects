import numpy as np 

# Creating array from list with type float 
a = np.array([[1, 2, 4], [5, 8, 7]], dtype = 'float') 
print ("Array created using passed list:\n", a) 

# Creating array from tuple 
b = np.array((1 , 3, 2)) 
print ("\nArray created using passed tuple:\n", b)

# ------------------------------x----------------------
# 2. Often, the element is of an array is originally unknown, but its size is known. Hence, NumPy offers several functions to create arrays with initial placeholder content. These minimize the necessity of growing arrays, an expensive operation. For example: np.zeros, np.ones, np.full, np.empty, etc.

# To create sequences of numbers, NumPy provides a function analogous to the range that returns arrays instead of lists.
# Creating a 3X4 array with all zeros 
c = np.zeros((3, 4)) 
print ("An array initialized with all zeros:\n", c) 

# Create a constant value array of complex type 
d = np.full((3, 3), 6, dtype = 'complex') 
print ("An array initialized with all 6s."
			"Array type is complex:\n", d) 

# Create an array with random values 
e = np.random.random((2, 2)) 
print ("A random array:\n", e)
# -------------------------------x--------------------
# 3. arange: This function returns evenly spaced values within a given interval. Step size is specified.


# Create a sequence of integers 
# from 0 to 30 with steps of 5 
f = np.arange(0, 30, 5) 
print ("A sequential array with steps of 5:\n", f)
# -----------------------------------------x---------------------------------
# 
# 4. linspace: It returns evenly spaced values within a given interval.
# Create a sequence of 10 values in range 0 to 5 
g = np.linspace(0, 5, 10) 
print ("A sequential array with 10 values between"
								"0 and 5:\n", g)
# ----------------------------------------x-----------------------------------------------
#  Reshaping array: We can use reshape method to reshape an array. Consider an array with shape 
# (a1, a2, a3, &#x2026, aN). We can reshape and convert it into another array with shape (b1, b2, b3, &#x2026,
#  bM). The only required condition is a1 x a2 x a3 &#x2026 x aN = b1 x b2 x b3 &#x2026 x bM. (i.e. the origina
# l size of the array remains unchanged.)
# Reshaping 3X4 array to 2X2X3 array 
arr = np.array([[1, 2, 3, 4], 
				[5, 2, 4, 2], 
				[1, 2, 0, 1]]) 

newarr = arr.reshape(2, 2, 3) 

print ("Original array:\n", arr) 
print("---------------") 
print ("Reshaped array:\n", newarr)



# ------------------------------------x--------------------------

# Flatten array: We can use flatten method to get a copy of the array collapsed into one dimension. 
# It accepts order argument. # The default value is &#x2018C&#x2019 (for row-major order).
#  Use &#x2018F&#x2019 for column-major order.


# Flatten array 
arr = np.array([[1, 2, 3], [4, 5, 6]]) 
flat_arr = arr.flatten() 

print ("Original array:\n", arr) 
print ("Fattened array:\n", flat_arr)


# -------------------------------------x----------------------------------------
# NumPy Array Indexing
# Knowing the basics of NumPy array indexing is important for analyzing and manipulating the array object.
#  NumPy in Python offers many ways to do array indexing.

# Slicing: Just like lists in Python, NumPy arrays can be sliced. As arrays can be multidimensional,
#  you need to specify a slice for each dimension of the array.
# Integer array indexing: In this method, lists are passed for indexing for each dimension.
#  One-to-one mapping of corresponding elements is done to construct a new arbitrary array.
# Boolean array indexing: This method is used when we want to pick elements from the array 
# which satisfy some condition.



# Python program to demonstrate 
# indexing in numpy 
import numpy as np 

# An exemplar array 
arr = np.array([[-1, 2, 0, 4], 
				[4, -0.5, 6, 0], 
				[2.6, 0, 7, 8], 
				[3, -7, 4, 2.0]]) 

# Slicing array 
temp = arr[:2, ::2] 
print ("Array with first 2 rows and alternate"
					"columns(0 and 2):\n", temp) 

# Integer array indexing example 
temp = arr[[0, 1, 2, 3], [3, 2, 1, 0]] 
print ("\nElements at indices (0, 3), (1, 2), (2, 1),"
									"(3, 0):\n", temp) 

# boolean array indexing example 
cond = arr > 0 # cond is a boolean array 
temp = arr[cond] 
print ("\nElements greater than 0:\n", temp) 


# ---------------------------------x-------------------------------------------
# NumPy Basic Operations
# The Plethora of built-in arithmetic functions is provided in Python NumPy.

# Operations on a single NumPy array
# We can use overloaded arithmetic operators to do element-wise operations on the array to create a new array.
#  In the case of +=, -=, *= operators, the existing array is modified.


# Python program to demonstrate 
# basic operations on single array 
import numpy as np 

a = np.array([1, 2, 5, 3]) 

# add 1 to every element 
print ("Adding 1 to every element:", a+1) 

# subtract 3 from each element 
print ("Subtracting 3 from each element:", a-3) 

# multiply each element by 10 
print ("Multiplying each element by 10:", a*10) 

# square each element 
print ("Squaring each element:", a**2) 

# modify existing array 
a *= 2
print ("Doubled each element of original array:", a) 

# transpose of array 
a = np.array([[1, 2, 3], [3, 4, 5], [9, 6, 0]]) 

print ("\nOriginal array:\n", a) 
print ("Transpose of array:\n", a.T) 

# ----------------------------------------------------x-----------------------------

# NumPy – Unary Operators
# Many unary operations are provided as a method of ndarray class. 
# This includes sum, min, max, etc. These functions can also be applied row-wise or
#  column-wise by setting an axis parameter.







