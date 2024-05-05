@test "can run" {
	python converter.py
}

@test "cws to xml" {
	python converter.py
	echo "$(md5sum out.cws.xml)"
	echo "$(md5sum tests/output_1.cws.xml)"
	test "$(md5sum out.cws.xml | cut -d ' ' -f 1)" = "$(md5sum tests/output_1.cws.xml | cut -d ' ' -f 1)"
}
