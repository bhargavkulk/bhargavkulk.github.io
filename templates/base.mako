<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="fediverse:creator" content="@bhargavkk@mastodon.social">
        <title>${title}</title>
        <link rel="me" href="https://mastodon.social/@bhargavkk">
        <link rel="stylesheet" href="/style.css">
        <%block name="head_extra"></%block>
    </head>
    <body>
        <nav>
            <ul>
                <li><a href="/"><code>/home</code></a></li>
                <li><a href="/blog"><code>/blog</code></a></li>
                <li><a href="/garden"><code>/garden</code></a></li>
                <li><a href="/research"><code>/research</code></a></li>
                <li><a href="/resume/"><code>/cv</code></a></li>
            </ul>
        </nav>
        <main>
            <h1>${title}</h1>
            ${self.body()}
        </main>
        <hr>
        <footer>
            <img loading="lazy" width="88" height="31" fetchpriority="low" src="/images/emacs.gif" style="image-rendering: pixelated"/>
            <img loading="lazy" width="88" height="31" fetchpriority="low" src="/images/sanehtml.gif" style="image-rendering: pixelated"/>
            <img loading="lazy" width="88" height="31" fetchpriority="low" src="/images/firefox3.gif" style="image-rendering: pixelated"/>
            <img loading="lazy" width="80" height="15" fetchpriority="low" src="/images/ccby.png" style="image-rendering: pixelated"/>
        </footer>
    </body>
</html>
