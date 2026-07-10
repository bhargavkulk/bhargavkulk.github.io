local first_heading_processed = false

-- Strip the synthetic page title section header from the first Djot section.
function Div(el)
  if not first_heading_processed and el.classes:includes('section') then
    local first = el.content[1]
    if first and first.t == 'Header' and first.level == 1 then
      table.remove(el.content, 1)
      first_heading_processed = true
      return el.content
    end
  end
end

-- Render Djot spans with an explicit class attribute as keyboard input.
function Span(el)
  local class_attr = el.attributes and el.attributes["class"]
  if class_attr and class_attr:match("(^|%s)kbd($|%s)") then
    local content = pandoc.List(el.content)
    content:insert(1, pandoc.RawInline("html", "<kbd>"))
    content:insert(pandoc.RawInline("html", "</kbd>"))
    return content
  end
end
