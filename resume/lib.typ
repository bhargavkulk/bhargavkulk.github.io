#let author = "Bhargav Kulkarni"

#let html-css = ```css
  body {
    box-sizing: border-box;
    max-width: 8.5in;
    margin: 0 auto;
    padding: 0.5in;
    color: #000;
    font-family: "CharisW", serif;
    font-size: 11pt;
    line-height: 1.15;
  }
  h1.resume-name {
    margin: 0 0 0.3em;
    font-family: "Cooper Hewitt", sans-serif;
    font-size: 20pt;
    font-weight: 400;
    text-align: center;
  }
  nav.contact-links {
    margin: 0 0 1em;
    font-family: "Fira Mono", monospace;
    font-size: 0.8em;
    text-align: center;
  }
  nav.contact-links a {
    color: inherit;
    text-decoration: underline;
  }
  h2.resume-section {
    margin: 1em 0 0.35em;
    border-top: 1.2pt solid currentColor;
    padding-top: 0.35em;
    font-family: "Cooper Hewitt", sans-serif;
    font-size: 1.35em;
    font-weight: 400;
  }
  .quad {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    column-gap: 1em;
    row-gap: 0;
    margin: 0.35em 0;
  }
  .quad-tr,
  .quad-br {
    text-align: right;
  }
  ul {
    margin: 0.25em 0 0.6em;
    padding-left: 1.25em;
  }
  ul ul {
    margin-top: 0;
    margin-bottom: 0;
  }
  li > p {
    margin: 0;
  }
  .pdf-link {
    margin: 0 0 0.5em;
    text-align: left;
    font-family: "Fira Mono", monospace;
    font-size: 0.8em;
  }
  a {
    color: inherit;
  }
```.text

#let quad(top-left, top-right, bottom-left, bottom-right) = context {
  if target() == "html" {
    html.elem("div", attrs: (class: "quad"))[
      #html.elem("div", attrs: (class: "quad-tl"))[#top-left]
      #html.elem("div", attrs: (class: "quad-tr"))[#top-right]
      #html.elem("div", attrs: (class: "quad-bl"))[#bottom-left]
      #html.elem("div", attrs: (class: "quad-br"))[#bottom-right]
    ]
  } else {
    [#top-left #h(1fr) #top-right \
    #bottom-left #h(1fr) #bottom-right]
  }
}

#let education(location, time, position) = quad(
  strong(location),
  emph(time),
  emph(position),
  [],
)

#let publication(title, conf, authors) = quad(
  strong(title),
  emph(conf),
  authors,
  [],
)

#let employment(company, time, position) = quad(
  strong(company),
  emph(time),
  emph(position),
  [],
)

#let urls(urls_map) = context {
  if target() == "html" {
    html.elem("nav", attrs: (class: "contact-links"))[
      #(urls_map.map(url => link(url.at(1))[#url.at(0)]).join("·"))
    ]
  } else {
    align(center)[
      #(
        urls_map
          .map(url => text(font: "Fira Mono", size: 0.8em)[
            #link(url.at(1))[#url.at(0)]
          ])
          .join("·")
      )
    ]
  }
}

#let resume(body) = [
  #set document(
    author: author,
    title: author,
  )

  #set text(
    font: "Charis",
    size: 11pt,
    lang: "en",
    ligatures: false,
  )

  #set page(
    margin: 0.5in,
    paper: "us-letter",
  )

  #context {
    if target() == "html" {
      html.elem("link", attrs: (rel: "stylesheet", href: "/fonts.css"))
      html.style(html-css)
    }
  }

  #context {
    if target() == "html" {
      html.elem("p", attrs: (class: "pdf-link"))[
      #html.elem("a", attrs: (href: "resume.pdf"))[View as PDF]
      ]
    }
  }

  #show link: underline

  #show heading.where(level: 1): it => context {
    if target() == "html" {
      html.elem("h1", attrs: (class: "resume-name"))[#it.body]
    } else {
      set text(font: "Cooper Hewitt", weight: 705, size: 20pt)
      set align(center)
      pad(it.body)
    }
  }

  #show heading.where(level: 2): it => context {
    if target() == "html" {
      html.elem("h2", attrs: (class: "resume-section"))[#it.body]
    } else {
      set text(font: "Cooper Hewitt", weight: 705)
      line(length: 100%, stroke: 1pt)
      pad(top: -10pt, bottom: 5pt, [#it.body])
    }
  }

  #set list(marker: ([•]))

  #body
]
