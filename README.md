# tenzor-parser
This program is used to scraping web-sites and getting article content without extra information.

Usage
-----
    python3 parser.py URL

Result of work
-----
This program creates two files:
 - examples/URL/original.html -- Very original HTML-page
 - examples/URL/parsed.txt -- Scraped text from webpage

Example
-----
    # python3.exe parser.py http://www.example.ru/index.html
    # ls ./examples/www.example.ru/index.html/*
    > ./examples/www.example.ru/index.html/oroginal.html
    > ./examples/www.example.ru/index.html/parsed.html

Algorythm
-----
 - This program check page for *div* tags with specified class name or property name ([schema.org](http://schema.org))
 - Then it find all tags *p* and add text to resulting string
 - In the end the program format string using rules: 80 characters for line, 2 line breaks between sections, links in square brackets
 
 Note
 ----
 The best result is for sites using ([schema.org](http://schema.org)).
