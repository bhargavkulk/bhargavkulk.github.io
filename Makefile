ADOC_FILES := $(shell find content -name '*.adoc')
FRAG_FILES := $(ADOC_FILES:content/%.adoc=cache/%.html)
META_FILES := $(ADOC_FILES:content/%.adoc=cache/%.json)
HTML_FILES := $(ADOC_FILES:content/%.adoc=public/%.html)
TMPL_FILES := $(wildcard templates/*)
ASST_FILES := $(wildcard assets/*)

BLOG_INDEX := cache/blog_index.json

all: link

compile: $(FRAG_FILES) $(META_FILES) $(BLOG_INDEX)

link: compile copy_assets $(HTML_FILES) $(TMPL_FILES) $(ASST_FILES)

public:
	mkdir -p public

cache:
	mkdir -p cache

cache/%.html: content/%.adoc | cache
	asciidoctor -s -o $@ $<

cache/%.json: content/%.adoc src/extract_metadata.py | cache
	python3 src/extract_metadata.py $<

$(BLOG_INDEX): $(META_FILES) src/generate_index.py
	python3 src/generate_index.py cache/blog cache/blog_index.json /blog

public/%.html: cache/%.html cache/%.json $(BLOG_INDEX) | public
	python3 src/fill_template.py templates cache/$*.json cache/$*.html $@ cache/blog_index.json

copy_assets: $(ASSETS) | public
	@rsync -av assets/ public/

clean:
	rm -rf public cache

.PHONY: all clean

.PRECIOUS: cache/%.json
