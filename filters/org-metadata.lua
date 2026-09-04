local json = require 'pandoc.json'
local metadata = {}

function RawBlock(raw)
  if raw.format ~= 'org' then
    return nil
  end

  local name, value = raw.text:match('#%+(%w+):%s*(.+)$')
  if name and value then
    metadata[name:lower()] = value
  end
end

function Meta(meta)
  if meta.title then
    metadata.title = pandoc.utils.stringify(meta.title)
  end

  if meta.date then
    metadata.date = pandoc.utils.stringify(meta.date)
  end

  if meta.author then
    metadata.author = pandoc.utils.stringify(meta.author)
  end

  if meta.description then
    metadata.description = pandoc.utils.stringify(meta.description)
  end

  metadata.template = metadata.template or 'page.mako'

  local input = PANDOC_STATE.input_files[1]
  local relative = input:match('content/(.+)$') or pandoc.path.filename(input)
  metadata.path = relative:gsub('%.org$', '.html')
  metadata.link = '/' .. metadata.path
  metadata.slug = pandoc.path.split_extension(pandoc.path.filename(input))

  io.stdout:write(json.encode(metadata))
  os.exit(0)
end
