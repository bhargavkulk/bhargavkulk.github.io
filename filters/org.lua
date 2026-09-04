local function strip_file_scheme(path)
  if path:match('^file:///') then
    return path:gsub('^file://', '')
  end
  return path
end

local function org_to_html(path)
  path = strip_file_scheme(path)
  return path:gsub('%.org$', '.html')
end

local denote_links = {}

local function load_denote_links(meta)
  local links = meta['denote-links']
  if links then
    for identifier, link in pairs(links) do
      -- Smart punctuation turns the `--` in Denote filenames into an en dash
      -- when it reads the JSON metadata file.
      denote_links[identifier] = pandoc.utils.stringify(link):gsub('–', '--')
    end
  end
end

local function resolve_link(el)
  local identifier = el.target:match('^denote:([%w]+)$')
  if identifier and denote_links[identifier] then
    el.target = denote_links[identifier]
    return el
  end

  el.target = org_to_html(el.target)
  return el
end

function Link(el)
  return resolve_link(el)
end

function Pandoc(doc)
  load_denote_links(doc.meta)
  return doc:walk({Link = resolve_link})
end

function Image(el)
  el.src = strip_file_scheme(el.src)
  return el
end

-- Convert Org's aside div into a semantic HTML aside element.
function Div(el)
  if el.classes:includes('aside') then
    return {
      pandoc.RawBlock('html', '<aside>'),
      table.unpack(el.content),
      pandoc.RawBlock('html', '</aside>')
    }
  end
  return el
end
