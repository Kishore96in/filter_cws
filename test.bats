function md5cmp {
	#Check that two files (given as two arguments) have the same md5sum
	test "$(md5sum $1 | cut -d ' ' -f 1)" = "$(md5sum $2 | cut -d ' ' -f 1)"
}

@test "help" {
	python filter_cws.py --help
}

@test "args clash" {
	#Use `not` to check that it fails.
	not python filter_cws.py --to-xml --to-cws tests/input_1.cws
}

@test "cws to xml" {
	python filter_cws.py --to-xml tests/input_1.cws
	md5cmp tests/input_1.cws.xml tests/output_1.cws.xml
}

@test "xml to cws (output not tested)" {
	python filter_cws.py --to-cws tests/output_1.cws.xml
	#NOTE: md5 won't work since even the file modification time will change the md5 of the zip file.
 	#md5cmp output_1.cws tests/output_1.cws
}

@test "xml to cws: fail on existing file" {
	touch tests/output_1_.cws
	cp tests/output_1.cws.xml tests/output_1_.cws.xml
	not python filter_cws.py --to-cws tests/output_1_.cws.xml
	rm tests/output_1_.cws
}


@test "xml to cws : force overwriting" {
	touch tests/output_1_.cws
	cp tests/output_1.cws.xml tests/output_1_.cws.xml
	python filter_cws.py --to-cws tests/output_1_.cws.xml --force
	rm tests/output_1_.cws
}
