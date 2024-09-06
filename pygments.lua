function CodeBlock(el)
    if el.classes[1] then
        local result = pandoc.pipe("pygmentize", { "-f", "html", "-O", "style=bw", "-l", el.classes[1] }, el.text)
        if type(result) == "string" then
            return pandoc.RawBlock("html", result)
        else
            return el
        end
    else
        return el
    end
end

function Math(el)
    if el.mathtype == "InlineMath" then
        return pandoc.Span(el.text, { class = "math" })
    else
        return el
    end
end
