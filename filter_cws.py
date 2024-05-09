#!/usr/bin/env python3

import defusedxml.ElementTree
import tempfile
import zipfile
import os
import argparse

invalid_characters = [
	#List of characters that are not allowed in an XML file, but which Cantor's files contain.
	chr(0x6), #Cantor seems to use this to mark EmbeddedMath in Markdown cells
	]

def filter_results(infile, outfile):
	tmpdir = tempfile.mkdtemp()
	
	with zipfile.ZipFile(infile, 'r') as z:
		z.extractall(tmpdir)
	
	with open(os.path.join(tmpdir, "content.xml")) as f:
		data = f.read()
	
	for char in invalid_characters:
		data = data.replace(char, chr(0xFFFD))
	
	worksheet = defusedxml.ElementTree.fromstring(data)
	for expr in worksheet.iter():
		results = []
		
		if expr.tag == "Expression":
			results.extend(expr.findall(".//Result"))
			results.extend(expr.findall(".//Error"))
		elif expr.tag == "Markdown":
			results.extend(expr.findall(".//HTML"))
			results.extend(expr.findall(".//EmbeddedMath"))
		elif expr.tag == "Latex":
			expr.attrib.pop('filename')
			expr.attrib.pop('image')
		
		for result in results:
			expr.remove(result)
	
	with open(outfile, 'w') as f:
		f.write(defusedxml.ElementTree.tostring(
			worksheet,
			encoding='unicode',
			))

def make_worksheet(infile, outfile):
	with zipfile.ZipFile(outfile, 'w') as z:
		z.write(infile, arcname="content.xml")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = "Given a Cantor worksheet, create an XML file with the results stripped (or convert such a file to an Cantor worksheet)",
		formatter_class = argparse.ArgumentDefaultsHelpFormatter,
		epilog = "Example: %(prog)s calc.cws",
		)
	parser.add_argument(
		'filename',
		type=str,
		help="The path to the file to handle",
		)
	parser.add_argument(
		'--to-xml',
		default=False,
		action='store_true',
		help="Convert the given file to a result-less XML",
		)
	parser.add_argument(
		'--to-cws',
		default=False,
		action='store_true',
		help="Convert the given XML file to a CWS file",
		)
	parser.add_argument(
		'--force',
		'-f',
		default=False,
		action='store_true',
		help="Use with --to-cws; if a file with the same name as the output exists, overwrite it",
		)
	
	args = parser.parse_args()
	
	if args.to_xml and args.to_cws:
		raise ValueError("Only one of --to-xml and --to-cws should be specified")
	elif args.to_xml:
		filter_results(args.filename, f"{args.filename}.xml")
	elif args.to_cws:
		outfile = args.filename.replace(".cws.xml", ".cws")
		if outfile == args.filename:
			raise RuntimeError(f"Could not generate filename for output file; input: {args.filename}; output: {outfile}")
		
		if args.force or not os.path.isfile(outfile):
			make_worksheet(args.filename, outfile)
		elif os.path.isfile(outfile):
			raise FileExistsError("Use the --force option to overwriting an existing file.")
	else:
		raise ValueError("Specify one of --to-xml and --to-cws")
