#!/usr/bin/env python3

import praw
import re

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     refresh_token='',
                     user_agent='desktop:/r/pokemontrades flair migration for new reddit:v0.1 (by /u/crownofnails and /u/SnowPhoenix9999)')

SUBREDDIT = 'pokemontrades'
BANNED_FLAIR_TEMPLATE = '3edecb3e-2f5e-11ea-88ac-0e3967aa9217'

sub = reddit.subreddit(SUBREDDIT)

flairedusers = sub.flair(limit=None) # remove limit when ready to run on real sub

flair_mappings = {
    'default' : ':0:',
    'gen2' : ':2:',
    'pokeball' : ':10:',
    'premierball' : ':20:',
    'greatball' : ':30:',
    'ultraball' : ':40:',
    'luxuryball' : ':50:',
    'masterball' : ':60:',
    'dreamball' : ':70:',
    'cherishball' : ':80:',
    'ovalcharm' : ':90:',
    'shinycharm' : ':100:',
    'gsball' : ':GS:',
    'pokeball1' : ':10i:',
    'premierball1' : ':20i:',
    'greatball1' : ':30i:',
    'ultraball1' : ':40i:',
    'luxuryball1' : ':50i:',
    'masterball1' : ':60i:',
    'dreamball1' : ':70i:',
    'cherishball1' : ':80i:',
    'ovalcharm1' : ':90i:',
    'shinycharm1' : ':100i:',
    'gsball1' : ':GSi:',
    'upgrade' : ':u:',
    'effortribbon' : ':helper:'
}

# def print_users(users):
#     for u in users:
#         # print(u)

#         username = u['user'].name
#         css_class = u['flair_css_class']
#         text = u['flair_text'] or ''

#         print('Current user: {0}. Flair text: \'{1}\'. Flair class: \'{2}\''.format(username, text, css_class))
#         print('-- Setting flair for {0} as flair_text: \'{1}\', flair_css_class: \'{2}\''.format(username, text, css_class))

#         print()

def remove_elements(array, overage):
    reduction = 0
    print ("Received array {0}".format(str(array)))
    while reduction < overage and len(array) > 1:
        print("Removing element in slot {0}".format(str(len(array)-1)))
        removed = array.pop(len(array)-1)
        reduction += len(removed) + 2
    return array

def shorten_flair(flair_components, overage):
    #print("Shortening flair")
    emoji_string_left = flair_components[1] or ''
    fc_string = flair_components[2]
    ign_string = flair_components[3]
    tsv_string = flair_components[4]
    emoji_string_right = flair_components[5] or ''
    igns = re.split(r"(?<=\)), ", flair_components[3])
    fcs = re.split(r", ", flair_components[2])
    if len(flair_components[3]) - len(igns[0]) >= overage:
        igns = remove_elements(igns, overage)
        ign_string = ", ".join(igns)
        print("Reduced flair to {0}".format(ign_string))
    elif len(flair_components[2]) - len(fcs[0]) >= overage:
        fcs = remove_elements(fcs, overage)
        fc_string = ", ".join(fcs)
        print("Reduced flair to {0}".format(fc_string))
    elif (len(flair_components[3]) - len(igns[0])) + (len(flair_components[2]) - len(fcs[0])) >= overage:
        igns = remove_elements(igns, overage)
        ign_string = ", ".join(igns)
        reduction = len(flair_components[3]) - len(ign_string)
        if reduction < overage:
            fcs = remove_elements(fcs, overage)
        fc_string = ", ".join(fcs)
    else:
        return str(flair_components[1] or '')
    return emoji_string_left + fc_string + " || " + ign_string + (" || " + tsv_string if tsv_string else "") + emoji_string_right

def sanitize_flair_text(flair_text):
    return re.sub(r':[\w]+:', '', flair_text)

def update_users(users):
    count = 0
    for u in users:
        username = u['user'].name
        flair_css_class = u['flair_css_class'] or ''
        flair_text = u['flair_text'] or ''
        flair_template_id = None
        new_additions = ''
        new_flair_text = ''

        count += 1
        
        # 0 = full match, 1 = emoji, 2 = FCs, 3 = IGNs, 4 = TSVs, 5 = right-side emoji
        flair_regex = r"^(:[A-Za-z0-9_\-]+:)?(?:SW-)?(\d{4}-\d{4}-\d{4}(?:, (?:SW-)?\d{4}-\d{4}-\d{4})*) \|\| (.*?)(?: \|\| (XXXX|\d{4}(?:, \d{4})*))?(:[A-Za-z0-9_\-]+:)?$"
        flair_text_match = re.search(flair_regex, flair_text)

        print('#{0} Current user: {1}. Flair text: \'{2}\'. Flair class: \'{3}\''.format(count, username, flair_text, flair_css_class))
        
        # only do anything to the flair if the user doesn't have (full) mod flair
        if flair_css_class and 'mf' in flair_css_class:
            print('- Skipped setting flair for {0} as this user has mod flair.'.format(username))
            print()
        # elif flair_text_match and flair_text_match[1]:
        #     print('- Skipped setting flair for {0} since it appears they already have an emoji flair: {1}'.format(username, flair_text))
        # not a full mod, carry on
        elif flair_text_match:
            if ':' in flair_text:
                flair_text = sanitize_flair_text(flair_text)

            # banned user
            if flair_css_class and 'banned' in flair_css_class:
                new_additions = 'BANNED USER'

                # if "BANNED USER" is not currently in the user's flair text, add it.
                # this check exists in case we need to run the script more than once (if it dies mid-way, avoid appending "BANNED USER" again)
                if new_additions not in flair_text:
                    # join them with a space between them for readability
                    new_flair_text = ' '.join([new_additions, flair_text]) 
                else:
                    new_flair_text = flair_text

                # slice off anything after 64 characters
                if len(new_flair_text) > 64:
                    new_flair_text = new_additions + ' ' + shorten_flair(flair_text_match, len(new_flair_text) - 64)

                flair_template_id = BANNED_FLAIR_TEMPLATE

            # user not mod or banned
            else:
                # go through every flair class they have and build the corresponding emoji additions
                for single_class in flair_css_class.split():
                    if single_class in flair_mappings:
                        new_additions += flair_mappings[single_class]

                # don't need a space between emojis/text
                new_flair_text = new_additions + flair_text

                # set flair text to just emoji if they go over limit
                if len(new_flair_text) >= 64:
                    if flair_text_match:
                        new_flair_text = shorten_flair(re.search(flair_regex, new_flair_text), len(new_flair_text) - 64)
                    else:
                        new_flair_text = new_additions

            # set new flair
            print('-- Setting flair for {0} as flair_text: \'{1}\', flair_css_class: \'{2}\''.format(username, new_flair_text, flair_css_class))
            print()

            #sub.flair.set(
            #    redditor=u['user'], 
            #    text=new_flair_text, 
            #    css_class=flair_css_class,
            #    flair_template_id=flair_template_id
            #    )
        else:
            print("-- Skipping user as flair does not match current pattern.")
            print()

if __name__ == '__main__':
    # print_users(flairedusers)
    update_users(flairedusers)
