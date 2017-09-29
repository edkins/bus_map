temp/m.svg: temp/paths.txt Makefile mk_svg.py
	python3 mk_svg.py temp/paths.txt > $@

temp/paths.txt: temp/shapes.txt Makefile extract_paths.py
	python3 extract_paths.py temp/shapes.txt > $@

temp/shapes.txt: ../app/src/main/res/raw/opendata_ttc_schedules.zip Makefile
	unzip -o $< shapes.txt -d temp
	touch temp/shapes.txt
