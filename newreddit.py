#!/usr/bin/env python3

import praw
import re

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     refresh_token='',
                     user_agent='/r/pokemontrades flair migration for new reddit by /u/crownofnails')

#REAL_SUBREDDIT = 'pokemontrades'
TEST_SUBREDDIT = 'notpokemontrades'

sub = reddit.subreddit(TEST_SUBREDDIT)

flairedusers = sub.flair(limit=50) # remove limit when ready to run on real sub

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

def sanitize_flair_text(flair_text):
    return re.sub(r':[\w]+:', '', flair_text)

def update_users(users):
    for u in users:
        username = u['user'].name
        flair_css_class = u['flair_css_class']
        flair_text = u['flair_text'] or ''
        new_additions = ''
        new_flair_text = ''

        print('Current user: {0}. Flair text: \'{1}\'. Flair class: \'{2}\''.format(username, flair_text, flair_css_class))

        # only do anything to the flair if the user doesn't have (full) mod flair
        if 'mf' in flair_css_class:
            print('- Skipped setting flair as this user has mod flair.')
            print()

        # not a full mod, carry on
        else:
            if ':' in flair_text:
                flair_text = sanitize_flair_text(flair_text)

            # banned user
            if 'banned' in flair_css_class:
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
                    new_flair_text = new_flair_text[:64]

                flair_css_class = 'banned'

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
                    new_flair_text = new_additions

            # set new flair
            print('-- Setting flair for {0} as flair_text: \'{1}\', flair_css_class: \'{2}\''.format(username, new_flair_text, flair_css_class))
            print()

            sub.flair.set(
                redditor=u['user'], 
                text=new_flair_text, 
                css_class=flair_css_class
                )

if __name__ == '__main__':
    # print_users(flairedusers)
    update_users(flairedusers)
