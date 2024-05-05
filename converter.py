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
			results.extend(expr.findall(".//Error"))
			for result in results:
				expr.remove(result)
	
	etree.write(outfile)

def make_worksheet(infile, outfile):
	with zipfile.ZipFile(outfile, 'w') as z:
		z.write(infile, arcname="content.xml")

if __name__ == "__main__":
	filter_results("tests/input_1.cws", "out.cws.xml")
