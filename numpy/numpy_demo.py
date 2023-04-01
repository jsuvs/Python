#python -m pip install numpy
import numpy

#core type is ndarray

#easy way to create an ndarray from an array like object
array = numpy.array([1,2,3,4,5])
print("shape (dimensions): {}".format(array.shape))              
#returns (5,) single dimension size 5
#in python a tuple with only one element has to include a comma after that element to indicate it is a tuple
#otherwise it would think it was the value 5
print("dtype (data type): {}".format(array.dtype))  
#returns int32

array = numpy.array([1,2,3,4,5], dtype=float)
print("dtype (data type): {}".format(array.dtype))  #float64

array = numpy.array([1,2.0,3,4,5])
print("dtype (data type): {}".format(array.dtype))  #float64

array = numpy.array([[1,2],[3,4]])
print("shape (dimensions): {}".format(array.shape))    #(2,2)

array1 = numpy.array([1, 2, 3])
array2 = numpy.array([4, 5, 6])
array1 = numpy.concatenate((array1, array2))
print(array1) #[1,2,3,4,5,6]

#https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
