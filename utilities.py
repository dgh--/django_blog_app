import re


"""
You don't really need to roll your own utility for removing HTML tags; Django
supplies its own (django.utils.html.strip_tags): 
https://docs.djangoproject.com/en/1.10/ref/utils/#django.utils.html.strip_tags

As the documentation notes, this isn't guaranteed to strip *all* HTML, so
caution should be exercised - it's possible that somebody cleverer than myself
might find a way of exploiting it.

Bleach provides a more robust solution: https://pypi.python.org/pypi/bleach
(but that's probably overkill for what you're doing here); as long as you're
not intending to mark the outputted content as safe in a template 
(i.e. a tag reading <h1> wouldn't be converted to &lt;h1&gt; )
you should be fine.

But yeah. Personally I'd remove it and use Django's implementation; one less
bit of code to maintain. :)
"""


def remove_html(string):
    """Expurgate HTML from string data."""
    result = string
    result = re.sub(
        '<.*/?>|<.*>.*<.*>',
        '',
        result
    )
    return result
