local function strip_file_scheme(path)
  if path:match('^file:///') then
    return path:gsub('^file://', '')
  end
  return path
end

function Link(el)
  el.target = strip_file_scheme(el.target)
  return el
end

function Image(el)
  el.src = strip_file_scheme(el.src)
  return el
end
