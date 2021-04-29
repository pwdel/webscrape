import re

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
