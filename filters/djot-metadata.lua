local json = require 'pandoc.json'
local metadata = {}
local first_heading_processed = false

-- TODO WTF is the diff between slug, link and path
-- Capture page metadata from the first top-level Djot section and its heading.
function Div(el)
  if first_heading_processed then
    return
  end

  if el.classes:includes('section') and el.content[1] and el.content[1].t == 'Header' and el.content[1].level == 1 then
    for k, v in pairs(el.attributes) do
      metadata[k] = v
    end

    if el.identifier ~= "" then
      metadata.id = el.identifier
    end

    metadata.title = pandoc.utils.stringify(el.content[1].content)
    first_heading_processed = true

    local input = PANDOC_STATE.input_files[1]
    local relative = pandoc.path.make_relative(input, 'content')
    metadata.path = relative:gsub('%.dj$', '.html')

    metadata.link = '/' .. metadata.path

    metadata.slug = pandoc.path.split_extension(pandoc.path.filename(input))
  end
end

-- Emit the collected metadata as JSON and stop further document processing.
function Pandoc(doc)
  io.stdout:write(json.encode(metadata))
  os.exit(0)
end
