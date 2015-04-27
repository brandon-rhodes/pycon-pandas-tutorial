TABLE_HTML := $(wildcard *.html)
TABLE_IMG := $(addsuffix .png, $(basename $(TABLE_HTML)))

tmp.png: tmp.dot $(TABLE_IMG)
	dot -Tpng -o tmp.png tmp.dot

$(TABLE_IMG): %.png: %.html ../style-table.css
	(echo '<style>'; cat ../style-table.css; echo '</style>'; cat $<) |\
		wkhtmltoimage - tmp.png && convert -trim tmp.png $@

