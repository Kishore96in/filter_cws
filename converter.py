import defusedxml.ElementTree
import tempfile
import zipfile
import os

def filter_results(infile, outfile):
	tmpdir = tempfile.mkdtemp()
	
	with zipfile.ZipFile(infile, 'r') as z:
		z.extractall(tmpdir)
	
	fname = os.path.join(tmpdir, "content.xml")
	etree = defusedxml.ElementTree.parse(fname)
	
	worksheet = etree.getroot()
	for expr in worksheet.iter():
		if expr.tag == "Expression":
			results = expr.findall(".//Result")
			for result in results:
				expr.remove(result)
	
	etree.write(outfile)
if __name__ == "__main__":
	filter_results("tests/input_1.cws", "out.cws.xml")
