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

function Link(el)
  el.target = org_to_html(el.target)
  return el
end

function Image(el)
  el.src = strip_file_scheme(el.src)
  return el
end
