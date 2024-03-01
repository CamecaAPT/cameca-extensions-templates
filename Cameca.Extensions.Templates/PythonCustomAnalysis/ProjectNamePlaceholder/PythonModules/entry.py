import typing
import numpy as np
import pyapsuite

def main(context: pyapsuite.APSuiteContext) -> typing.Optional[np.ndarray[np.uint64]]:
	# Return a collection of ion indices to filter to that selection in AP Suite
	# For best performance, return a np.ndarray(dtype=np.uint64)
	return None