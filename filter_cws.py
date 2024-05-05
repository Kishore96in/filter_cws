#!/usr/bin/env python3

import defusedxml.ElementTree
import tempfile
import zipfile
import os
import argparse

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
	parser = argparse.ArgumentParser(
		description = "Given a Cantor worksheet, create an XML file with the results stripped (or convert such a file to an Cantor worksheet)",
		formatter_class = argparse.ArgumentDefaultsHelpFormatter,
		epilog = "Example: %(prog)s calc.cws",
		)
	parser.add_argument('filename', type=str)
	parser.add_argument('--to-xml', default=False, action='store_true' )
	parser.add_argument('--to-cws', default=False, action='store_true' )
	
	args = parser.parse_args()
	
	if args.to_xml and args.to_cws:
		raise ValueError("Only one of --to-xml and --to-cws should be specified")
	elif args.to_xml:
		filter_results(args.filename, "out.cws.xml")
	elif args.to_cws:
		make_worksheet(args.filename, "output_1.cws")
	else:
		raise ValueError("Specify one of --to-xml and --to-cws")