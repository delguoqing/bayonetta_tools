import os
import shutil
import glob
import lxml.etree
	
def gen(fmt, output_path):
	xml = lxml.etree.parse("codegen/%s.xml" % fmt)
	xslt = lxml.etree.parse("codegen/parser.xsl")
	transform = lxml.etree.XSLT(xslt)
	transform(xml)
	xslt = lxml.etree.parse("codegen/fields.xsl")
	transform = lxml.etree.XSLT(xslt)
	transform(xml)
	
	fields = None
	tmp_modules = ("g_fields", )
	for m in tmp_modules:
		f = __import__(m).DATA
		if fields is None:
			fields = f
		else:
			for k, v in f.iteritems():
				if k in fields:
					fields[k].update(v)
				else:
					fields[k] = v
	
	MARK_BEG = '"""BEG FIELDS"""'
	MARK_END = '"""END FIELDS"""'
	LINE_END = "\n"
	for cls_name, cls_fields in fields.iteritems():
		ex_m_name = "ex_" + cls_name
		fname = os.path.join(output_path, ex_m_name + ".py")
		if os.path.exists(fname):
			f = open(fname, "r")
			data = f.read()
			f.close()
			a = data.find(MARK_BEG)
			b = data.find(MARK_END, a)
			
			data_out = data[:a] + MARK_BEG + LINE_END
			for field_name in sorted(cls_fields):
				data_out += "\t\tself.%s = None%s"  % (field_name, LINE_END)
			data_out += "\t\t" + data[b:]
			f = open(fname, "w")
			f.write(data_out)
			f.close()
			
	for filepath in glob.glob("g_*.py"):
		if filepath.endswith("g_fields.py"):
			continue
		os.system("move /Y %s %s" % (filepath, output_path))
	
def clean_up():
	os.system("del g_*.py")
	os.system("del g_*.pyc")
	
if __name__ == '__main__':
	gen("wmb", "wmb_parser")
	clean_up()