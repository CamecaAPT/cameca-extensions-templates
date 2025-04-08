import typing
import pyapsuite

def main(context: pyapsuite.APSuiteContext) -> typing.Optional[typing.Iterable[int]]:
	# Return a collection of ion indices to filter to that selection in AP Suite
	# For best performance, return a np.ndarray(dtype=np.uint64)
	return None