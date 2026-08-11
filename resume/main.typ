#import "lib.typ": *

#show: resume

= #context document.author.first()

#urls(
    (("bhargavkishork@gmail.com", "mailto:bhargavkishork@gmail.com"),
    ("github.com/bhargavkulk", "https://github.com/bhargavkulk"),
    ("linkedin.com/bhargavkulk", "https://linkedin.com/in/bhargavkulk"),
    ("bhargavkulk.github.io", "https://bhargavkulk.github.io"),
))

== Education

#education([University of Utah], [2023---Present], [PhD, Computer Science])
- Advised by #link("https://pavpanchekha.com")[Pavel Panchekha]

#education([BITS Pilani], [2019---2023], [BEng, Computer Science])

== Publications

#publication(
    [Semantics for 2D Rasterization],
    [OOPSLA'26],
    [#underline[Bhargav Kulkarni], Henry Whiting, Pavel Panchekha],
)
- Formalized Skia's 2D rasterization semantics in Lean and built a verified optimizer that achieves
  an average speedup of 18.7% across the top 100 websites by traffic.

#publication(
    [Mixing Condition Numbers and Oracles for Accurate Floating-point Debugging],
    [IEEE ARITH'25],
    [#underline[Bhargav Kulkarni], Pavel Panchekha]
)
- Built a floating-point debugger combining double-double arithmetic, condition numbers, and
  logarithmic oracles, achieving 80.0% precision and 96.1% recall on 546 difficult numeric
  benchmarks.

== Employment

#employment([Adobe Inc.], [2026], [Graduate Research Intern])
- Building an optimizer for scene-graphs in Adobe Photoshop

#employment([University of Utah], [2023---Present], [Research Assistant])
- Currently building a verified optimizer for the Skia vector graphics engine that powers Chrome
  rendering.
- Previously adapted floating-point static analysis techniques to build an accurate floating-point
  debugger.

#employment([NASA Langley Formal Methods Group], [2024], [Research Intern])
- Worked on generating proof certificates for the PVS automated theorem prover to verify Herbie’s (a
  floating-point superoptimizer) accuracy-aware optimizations

== Skills and Projects
- *General Programming*: Python, Racket, Java
- *Systems Programming*: C/C++, Bash, Rust
- *Hardware*: Verilog, x86
#v(0.25em)
- *Trinity Game Engine*: A game engine and byte code VM for scripting.
   #link("github.com/bhargavkulk/trinity")[\[source\]]
- *Logic in Coq*: Classical propositional logic and natural deduction in
   Coq/Rocq. #link("github.com/bhargavkulk/logic-in-Coq")[\[source\]]
- *CheemScheme*: Scheme dialect in C++ with tail recursion and error reporting.
   #link("github.com/bhargavkulk/cheem-scheme/tree/C%2B%2B")[\[source\]]
