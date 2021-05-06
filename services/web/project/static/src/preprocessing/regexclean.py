# regex removal
import re
# cleantext
from cleantext import clean

# compile int a regular expression object given instructions
# remove first layer of tags, characters
htmltags_re = re.compile(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]')
# compile and remove newline tags
htmltags_nre = re.compile(r'\n\\n')


# empty text tags removed list
text_tagsremovedlist = []

# removetags function
# input a list of scraped websites, output text with regex removed
def remove_tags(titlelist,textlist):

    # do this for all items in text list
    for counter in range(0,len(textlist)):
        # remove characters for a particular textlist item
        text_htmltags_removed = htmltags_re.sub('', str(textlist[counter]))
        # remove newline function on that list item
        text_ntags_removed = htmltags_nre.sub('', text_htmltags_removed)
        # append to list
        text_tagsremovedlist.append(text_ntags_removed)

    return(text_tagsremovedlist)

def clean_text(text_tagsremovedlist):

    cleanedtags = []

    for counter in range(0,len(text_tagsremovedlist)):
        cleanedtags.append(
        clean(
            text_tagsremovedlist[counter],  # iterate over list
            fix_unicode=True,               # fix various unicode errors
            to_ascii=True,                  # transliterate to closest ASCII representation
            lower=True,                     # lowercase text
            no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
            no_urls=False,                  # replace all URLs with a special token
            no_emails=False,                # replace all email addresses with a special token
            no_phone_numbers=False,         # replace all phone numbers with a special token
            no_numbers=False,               # replace all numbers with a special token
            no_digits=False,                # replace all digits with a special token
            no_currency_symbols=False,      # replace all currency symbols with a special token
            no_punct=False,                 # remove punctuations
            replace_with_punct="",          # instead of removing punctuations you may replace them
            replace_with_url="<URL>",
            replace_with_email="<EMAIL>",
            replace_with_phone_number="<PHONE>",
            replace_with_number="<NUMBER>",
            replace_with_digit="0",
            replace_with_currency_symbol="<CUR>",
            lang="en"                        # set to 'de' for German special handling
            )
            )

    return()
