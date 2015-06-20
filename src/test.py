import os
import glob
import sys
from util import iter_path, \
				 beep_error, beep_finish

def iter_all_wmb():
	return glob.glob(r"..\..\..\bayonetta\*\*\*\*.wmb")

def make_common_test(wmb_files, dump_obj=False):
	def test_common():
		import gen_all
		import parse	
		for wmb_path in iter_path(wmb_files):
			print "parsing %s" % wmb_path
			f = open(wmb_path, "rb")
			try:
				parse.parse(f, dump_obj)
			except Exception:
				beep_error()
		import g_wmb_parser_xb
		g_wmb_parser_xb.print_value_statistic()
		
		# test me if the work is finished
		beep_finish()
		
	return test_common
		
####################
# all test cases
####################
test_all_wmb = make_common_test(iter_all_wmb)
test_bm0020 = make_common_test(r"..\..\..\bayonetta\data01_files\bm\bm0020\bm0020.wmb",
							   dump_obj=False)
test_em001f = make_common_test(r"..\..\..\bayonetta\data01_files\em\em001f\em001f.wmb",
							   dump_obj=False)

ACTIVE_TEST = test_em001f

if __name__ == '__main__':
	
	if len(sys.argv) == 1:
		test = ACTIVE_TEST
	else:
		test = getattr(sys.modules[__name__], "test_%s" % sys.argv[1])
	test()