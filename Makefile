# - Directories ------------------------------------------------------------------------------------
content := content
cache := cache
www := www
filters := filters
templates := templates
assets := assets

# - # Files ----------------------------------------------------------------------------------------
DJOT_FILES := $(shell find $(content) -name '*.dj')
FRAGMENTS := $(patsubst $(content)/%.dj,$(cache)/%.html,$(DJOT_FILES))
METADATA := $(patsubst $(content)/%.dj,$(cache)/%.json,$(DJOT_FILES))
PAGES := $(patsubst $(cache)/%.html,$(www)/%.html,$(FRAGMENTS))
TEMPLATE_FILES := $(shell find $(templates) -type f)
ASSET_FILES := $(shell find $(assets) -type f)
COPIED_ASSETS := $(patsubst $(assets)/%,$(www)/%,$(ASSET_FILES))
COLLECTION_DIRS := $(shell find $(content) -mindepth 1 -maxdepth 1 -type d)
COLLECTION_INDEXES := $(patsubst $(content)/%,$(cache)/%_index.json,$(COLLECTION_DIRS))
EXTRA_METADATA_ARGS := $(if $(COLLECTION_INDEXES),-e $(COLLECTION_INDEXES),)
BLOG_FEED_FILES := $(www)/blog_index_atom.xml $(www)/blog_index_rss.xml

all: compile link

clean:
	rm -rf $(cache) $(www)

.PHONY: all clean compile link serve init

init:
	mkdir -p $(content) $(templates) $(assets)

# - Compile ----------------------------------------------------------------------------------------
# Fills `./$(cache)/` with html fragments and JSON metadata
compile: $(FRAGMENTS) $(METADATA) $(COLLECTION_INDEXES)

cache:
	mkdir -p cache

$(cache)/%.html: $(content)/%.dj $(filters)/djot.lua | cache
	@mkdir -p $(dir $@)
	pandoc -f djot -t html --mathml --lua-filter $(filters)/djot.lua $< -o $@

$(cache)/%.json: $(content)/%.dj $(filters)/djot-metadata.lua | cache
	@mkdir -p $(dir $@)
	pandoc -f djot --lua-filter $(filters)/djot-metadata.lua $< > $@

define COLLECTION_INDEX_RULE
$(cache)/$(1)_index.json: $(wildcard $(content)/$(1)/*.dj) $(patsubst $(content)/%.dj,$(cache)/%.json,$(wildcard $(content)/$(1)/*.dj)) scripts/generate_index.py | cache
	uv run python scripts/generate_index.py $(content)/$(1) $$@
endef

$(foreach collection,$(notdir $(COLLECTION_DIRS)),$(eval $(call COLLECTION_INDEX_RULE,$(collection))))

# - Link -------------------------------------------------------------------------------------------
# Uses cached data to build actual website
link: $(PAGES) $(COPIED_ASSETS) $(BLOG_FEED_FILES)

serve:
	uv run python scripts/serve.py $(www) -w $(content) $(filters) $(templates) $(assets) Makefile scripts

www:
	mkdir -p www

$(www)/%.html: $(cache)/%.html $(cache)/%.json scripts/fill_template.py $(TEMPLATE_FILES) $(COLLECTION_INDEXES) | www
	@mkdir -p $(dir $@)
	uv run python scripts/fill_template.py $< $(cache)/$*.json $(templates) $@ $(EXTRA_METADATA_ARGS)

$(BLOG_FEED_FILES) &: cache/blog_index.json scripts/generate_feed.py | www
	uv run python scripts/generate_feed.py cache/blog_index.json cache $(www)

$(www)/%: $(assets)/% | www
	@mkdir -p $(dir $@)
	cp $< $@
