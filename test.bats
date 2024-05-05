function md5cmp {
	#Check that two files (given as two arguments) have the same md5sum
	test "$(md5sum $1 | cut -d ' ' -f 1)" = "$(md5sum $2 | cut -d ' ' -f 1)"
}

@test "help" {
	python converter.py --help
}

@test "cws to xml" {
	python converter.py --to-xml tests/input_1.cws
	md5cmp out.cws.xml tests/output_1.cws.xml
}
