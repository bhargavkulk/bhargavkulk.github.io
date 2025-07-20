<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>${metadata['title']}</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Bitter:ital,wght@0,100..900;1,100..900&family=Public+Sans:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
        <link href="https://iosevka-webfonts.github.io/iosevka/Iosevka.css" rel="stylesheet" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/charter-webfont@4/charter.min.css" />
        <link rel="stylesheet" href="/style.css">
    </head>
    <body>
        <header>
            <h1><a href="/">Bhargav Kulkarni</a></h1>
            <nav class="navbar">
                <ul>
                    <li><a href="/">/home</a></li>
                    <li><a href="/research.html">/research</a></li>
                    <li><a href="/blog/">/blog</a></li>
                    <li><a href="/cv.html">/cv</a></li>
                    <li><a href="/contact.html">/contact</a></li>
                </ul>
            </nav>
        </header>
        <hr/>
        <main>
            <%block name="content">
            </%block>
        </main>
    </body>
</html>
