.. meta::
   :template: blog.html
   :title: My Website
   :date: 2025-02-18

.. role:: serif

.. role:: mono

Welcome to my website! I think I am finally happy with how it looks and *feels*. I took most of the CSS styling from `protesilaos.com <https://protesilaos.com/>`__ and got a very nice and simple to use color palette from `uchū <https://uchu.style/>`__. I should probably add these attributions to the footer, but I have not done that *yet*.

The layout is responsive to changes in window size and also looks nice on phones and tablets. The info-bar very neatly switches from a sidebar to a header when the width of the window is narrow enought. I am also quite enjoying the fonts. I am using:

- Public Sans, as my sans font. Find it `here <https://fonts.google.com/specimen/Public+Sans>`__.
- :serif:`Inria Serif`, as my serif font. Find it `here <https://fonts.google.com/specimen/Inria+Serif>`__.
- :mono:`Fira Mono`, as my mono-spaced font. Find it `here <https://fonts.google.com/specimen/Fira+Mono>`__.

Moreover, this website is powered by a *bespoke* static site generator that I have called `haya <https://github.com/bhargavkulk/haya>`__. Haya uses `ReStructuredText <https://docutils.sourceforge.io/rst.html>`__ which seems to be the defacto markup language for the Python ecosystem. I like RST; it is so easy to extend with new directives. If I used Markdown I'd have to wrestle with the parser directly; it is not extensible by any means. Extensibility is a necessary feature in any markup language for me to use. I think the markup language with the best extensibility is the `Scribble <https://docs.racket-lang.org/scribble/>`__ system used by Racket, but I was more comfortable quickly writing Python. The main RST parser/writer is the ``docutils`` package.

For HTML templating I used the `mako <https://www.makotemplates.org/>`__ templating engine. Mako is nice to use, because I can just embed arbitrary Python code into the template. This is much more intuitive to me instead of using insane templating DSLs. The Scribble documentation system I mentioned before is even easier and nicer to use for templating but alas it is not in Python (I could have sub-processed into Racket to compile Scribble files).

Haya has the basic features needed to make personal websites with blogs. I will keep adding features to Haya as an when I need. Feel free to contribute to Haya if you end up using it too! I need to add a hot reloading server to haya next so that I am not forced to run ``haya build`` while hosting the site on localhost on the side everytime I make a change.

I plan to add a post to the blog at the end of every month to force myself to improve my writing.
