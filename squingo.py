import os
from pathlib import Path
import random
import simpleaudio
import string
from termcolor import colored
import threading
import time

# text to print when the hand is a double payout ("Squingo")
# (text from https://texteditor.com/multiline-text-art/ on setting "Black 7")
TEXT_SQUINGO = '''
 ▄█▀▀▀▄█   ▄▄█▀▀██   ▀██▀  ▀█▀ ▀██▀ ▀█▄   ▀█▀  ▄▄█▀▀▀▄█   ▄▄█▀▀██
 ██▄▄  ▀  ▄█▀    ██   ██    █   ██   █▀█   █  ▄█▀     ▀  ▄█▀    ██
  ▀▀███▄  ██      ██  ██    █   ██   █ ▀█▄ █  ██    ▄▄▄▄ ██      ██
▄     ▀██ ▀█▄  ▀▄ ▀█  ██    █   ██   █   ███  ▀█▄    ██  ▀█▄     ██
█▀▄▄▄▄█▀    ▀█▄▄▄▀█▄   ▀█▄▄▀   ▄██▄ ▄█▄   ▀█   ▀▀█▄▄▄▀█   ▀▀█▄▄▄█▀
'''

# text to print when the hand is a loss ("Not Squingo")
# (text from https://texteditor.com/multiline-text-art/ on setting "Black 7")
TEXT_NOT_SQUINGO = '''
▀█▄   ▀█▀  ▄▄█▀▀██   █▀▀██▀▀█     ▄█▀▀▀▄█   ▄▄█▀▀██   ▀██▀  ▀█▀ ▀██▀ ▀█▄   ▀█▀  ▄▄█▀▀▀▄█   ▄▄█▀▀██
 █▀█   █  ▄█▀    ██     ██        ██▄▄  ▀  ▄█▀    ██   ██    █   ██   █▀█   █  ▄█▀     ▀  ▄█▀    ██
 █ ▀█▄ █  ██      ██    ██         ▀▀███▄  ██      ██  ██    █   ██   █ ▀█▄ █  ██    ▄▄▄▄ ██      ██
 █   ███  ▀█▄     ██    ██       ▄     ▀██ ▀█▄  ▀▄ ▀█  ██    █   ██   █   ███  ▀█▄    ██  ▀█▄     ██
▄█▄   ▀█   ▀▀█▄▄▄█▀    ▄██▄      █▀▄▄▄▄█▀    ▀█▄▄▄▀█▄   ▀█▄▄▀   ▄██▄ ▄█▄   ▀█   ▀▀█▄▄▄▀█   ▀▀█▄▄▄█▀
'''

# text to print when the hand is a triple payout ("Monkey Pirate")
# (text from https://texteditor.com/multiline-text-art/ on setting "Black 7")
TEXT_MONKEY_PIRATE = '''
▀██    ██▀  ▄▄█▀▀██   ▀█▄   ▀█▀ ▀██▀  █▀  ▀██▀▀▀▀█  ▀██▀ ▀█▀   ▀██▀▀█▄  ▀██▀ ▀██▀▀█▄       █     █▀▀██▀▀█ ▀██▀▀▀▀█
 ███  ███  ▄█▀    ██   █▀█   █   ██ ▄▀     ██  ▄      ██ █      ██   ██  ██   ██   ██     ███       ██     ██  ▄
 █▀█▄▄▀██  ██      ██  █ ▀█▄ █   ██▀█▄     ██▀▀█       ██       ██▄▄▄█▀  ██   ██▀▀█▀     █  ██      ██     ██▀▀█
 █ ▀█▀ ██  ▀█▄     ██  █   ███   ██  ██    ██          ██       ██       ██   ██   █▄   ▄▀▀▀▀█▄     ██     ██
▄█▄ █ ▄██▄  ▀▀█▄▄▄█▀  ▄█▄   ▀█  ▄██▄  ██▄ ▄██▄▄▄▄▄█   ▄██▄     ▄██▄     ▄██▄ ▄██▄  ▀█▀ ▄█▄  ▄██▄   ▄██▄   ▄██▄▄▄▄▄█
'''

# ASCII graphic to print when the hand is a triple payout ("Monkey Pirate")
GRAPHIC_MONKEY_PIRATE = '''
                                       .*,                         
                                  %@%@@@@@@@@@@(                   
                                #&&@@@@@@@@@@@@@@#                 
                    ./(#(//(&@&%&@@ %@@@@@@@@@@%(@@                
                 @@%%%%%&@@@@@@@@(.&       (@@. @@@@               
                  @%%@@%@@@@@@@@@@@( .@* &@  #@/&@@@@@@.           
                   .@@%@@@@@@@@@/ /.   */    @@@@@@@@@@&@@@@(      
                   #%%@@@@@@@@@@@ @@# , .   (  (@@@@@@@@@@%%@@(    
                  %%%%,,(@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&%%&&      
             ,    %%%,,,*%%%%%%%%%%%%@%%%%%%%&@@@@@@@@@@&(         
           ,,,     &%&,%%%%%%%,,*,,&%%%%%%%%%%%%%%#,*,.&%%%        
          ,,,,        /%%%%%,,,,/@*,,,%(,,,,,,%%%%%%,,,,%%%.       
         ,,,,,,       (%%*,,,,&@/,,,,,,,,,,,,,,/%%%%(,#%%(,        
         ,,,,,,        %%,,,@@@@*,,,,,,,,,,,,,,*%%%%//*            
         .,,,,,        .#%@,,,*,,,***,,,,,*,,,,,(%%%      ,*.      
          ,,,.*,         (#,,,,,,(,,,,,,,,,,,,,,(%/   %&%%,.#%%%#  
           ,,,,,            &*,,,,,,,**,,,,,,,#%,    %%        .%% 
             ,.,            %####%#(*,,*/#%%#*        %%%*      /%&
             ,((//,/%%%#%%%%#######*,,,##(####%%                (%%
              ,,/(,%%%%%%%%######%#,,,,%//#####%%%%,           ,%% 
                ///      (#####//##,,,,#%###%###%%%%/,,,      #%%  
                         *%###%%(%*,,,,(#%%#####%%(/,,,,,   (%%.   
                           &%%*,,,,,,,,,,/####*     .,*, (%#%      
                            %%%%*,,,,,,/%%%%%#      *#%%%(         
                           #%%%%%%%%%%%%%#%%%%%%%%%%/              
                           &%%%%%%%%%%%%%%%%%%%                    
                           &%%%%%        .%%%%%%,                  
                           /%%%%#          /##*,,,                 
                            *,,,,,          .,,,,,                 
                            .,,,,.

                HE DO BE TERRORIZING THE SEVEN SEAS THOUGH 👀
'''

# possible filler texts to use when processing a hand

TEXT_FILLER_VERBS = [
    'Reticulating',
    'Degaussing',
    'Repiping',
    'Rebooting',
    'Differentiating with respect to',
    'Consuming',
    'Flummoxing',
    'Derezzing',
    'Applying the Fourier transform to',
    'Defibrillating',
    'Sublimating',
    'Arming',
    'Energizing',
    'Aerosolizing',
    'Exterminating',
    'Traversing',
    'Minifying',
    'Compressing',
    'Warming up',
    'Neutralizing',
    'Quantifying',
    'Vectorizing',
    'Rasterizing',
    'Kerning',
    'Parallelizing',
    'Hashing',
    'Encrypting',
    'Decrypting'
]

TEXT_FILLER_NOUNS = [
    'splines',
    'boron wave shift-scoop',
    'plasma',
    'beryllium antigravity turbine bracket',
    'chromium dorsal crystal core',
    'Higgs bosons',
    'dilithium',
    'kyber crystals',
    'energized protodermis',
    'exsidian layer',
    'psionic unit',
    'moon device',
    'REDACTED',
    'adamantium shell',
    'cockroaches',
    'droid brains',
    'hyperdrive',
    'big data',
    'blockchain',
    'Gaussian surface',
    'vector field',
    'flux',
    'ad impressions',
    'social graph',
    'kerning',
    'ligatures',
    'GPUs',
    'graphene nanotubes'
]

# easter egg filler text (appears with odds given by EASTER_EGG_FILLER_PERCENTAGE)
TEXT_FILLER_EASTER_EGG = 'SOMEBODY PLEASE HELP ME I AM STUCK IN THE COMPUTER OPEN TH'

# possible filler sound effects to play immediately after input is entered
SFX_DIR_PATH_INPUT = 'sfx/input'

# possible beep sound effects to play when a processing a hand
SFX_DIR_PATH_BEEP = 'sfx/beep'

# possible miscellanous filler sound effects to play when processing a hand
SFX_DIR_PATH_MISC = 'sfx/misc'

# possible sound effects to play when a hand is squingo
SFX_DIR_PATH_SQUINGO = 'sfx/squingo'

# possible sound effects to play when a hand is not squingo
SFX_DIR_PATH_NOT_SQUINGO = 'sfx/not_squingo'

# possible sound effects to play when a hand is monkey pirate
SFX_DIR_PATH_MONKEY_PIRATE = 'sfx/monkey_pirate'

# the number of chars that progress bars should be
FULL_PROGRESS_BAR_LENGTH_CHARS = 75

# how long the progress bar should freeze in the late 90th percentages
PROGRESS_BAR_FREEZE_TIME_SECONDS = 5

# odds of the round ending in each outcome; these should all add to 100
ODDS_SQUINGO_PERCENTAGE = 46
ODDS_NOT_SQUINGO_PERCENTAGE = 44
ODDS_MONKEY_PIRATE_PERCENTAGE = 10

# outputs of get_outcome() indicating how the round played out
OUTCOME_SQUINGO = 'squingo'
OUTCOME_NOT_SQUINGO = 'not squingo'
OUTCOME_MONKEY_PIRATE = 'monkey pirate'

# odds of each given filler message being the easter egg message
EASTER_EGG_FILLER_PERCENTAGE = 1

def play_random_wave_sfx_from_dir(dir):
    '''
    Given a directory (as a string) containing .wav sfx files, randomly select and play a sound in
    that directory then return after the sound finishes.
    '''

    # glob handles hidden files across OSes
    sfx_path = random.choice([str(path) for path in Path(dir).glob('*')])
    simpleaudio.WaveObject.from_wave_file(sfx_path).play().wait_done()

def get_outcome(hand):
    '''
    Given the int value of a squingo hand, return a string indicating the hand's outcome (squingo,
    not squingo, monkey pirate)
    '''

    possible_outputs_weighted = [OUTCOME_SQUINGO] * ODDS_SQUINGO_PERCENTAGE + \
        [OUTCOME_NOT_SQUINGO] * ODDS_NOT_SQUINGO_PERCENTAGE + \
        [OUTCOME_MONKEY_PIRATE] * ODDS_MONKEY_PIRATE_PERCENTAGE
    return random.choice(possible_outputs_weighted)

def print_ellipsis(num_ellipses):
    '''
    Print out an ellipsis one dot at a time then clear it. Repeat the number of specified times,
    then complete with an ellipsis followed by ' done.' and a newline.
    '''

    # print dummy frame so the cursor is positioned correctly during the actual frames that follow
    print('   ', end='', flush=True)

    for _ in range(num_ellipses):
        for frame in ['   ', '.  ', '.. ', '...']:
            print('\b' * 3 + frame, end='', flush=True)
            time.sleep(0.1)

    print(' done.', flush=True)

def print_matrix_junk():
    '''
    Print out a bunch of junk characters.
    '''

    for i in range(random.randint(800, 1000)):
        for j in range(0, 100):
            if random.randint(0, 3) == 0 or abs(i - j) < 30:
                print(random.choice(string.printable), end='', flush=True)
            else:
                print(' ', end='', flush=True)

    time.sleep(1)

def print_progress_bar():
    '''
    Print out a progress bar ranging from 0-100 that progresses randomly. The bar freezes for a bit
    somewhere in the late 90th percentages.
    '''

    percentage_to_freeze = random.randint(96, 100)

    for percentage in range(101):
        current_progress_bar_length_chars = round(FULL_PROGRESS_BAR_LENGTH_CHARS * percentage / 100)
        current_progress_bar = '\u25A0' * current_progress_bar_length_chars

        print(
            f'\r{current_progress_bar.ljust(FULL_PROGRESS_BAR_LENGTH_CHARS)}   {percentage}%',
            end='',
            flush=True
        )

        if percentage == percentage_to_freeze:
            time.sleep(PROGRESS_BAR_FREEZE_TIME_SECONDS)
        else:
            time.sleep(random.randint(0, 100) / 700)

    time.sleep(1)

class WaveSfxThread(threading.Thread):
    '''
    The WaveSfxThread takes in a path (as a string) to a directory of wav sound effects and plays
    them in random order with random pauses until the thread is closed.
    '''

    # the min and max (both inclusive) amount of time to wait between playing sfx
    MIN_SFX_PAUSE_SECONDS = 1
    MAX_SFX_PAUSE_SECONDS = 3

    def __init__(self, sfx_dir):
        '''
        sfx_paths: a list of paths to possible sfx
        '''

        threading.Thread.__init__(self)
        self.should_stop = threading.Event()
        self.sfx_dir = sfx_dir

    def stop(self):
        '''
        Shut down the WaveSfxThread.
        '''

        self.should_stop.set()

    def run(self):
        '''
        Keep playing sound effects at random intervals until the thread is told to stop.
        '''

        while not self.should_stop.is_set():
            play_random_wave_sfx_from_dir(self.sfx_dir)

            delay = random.randint(
                self.MIN_SFX_PAUSE_SECONDS,
                self.MAX_SFX_PAUSE_SECONDS
            )
            time.sleep(delay)

def main():
    while True:
        hand = input('Enter the card hand: ')
        play_random_wave_sfx_from_dir(SFX_DIR_PATH_INPUT)
        # accept input and clear console;
        # see https://stackoverflow.com/a/2084628
        os.system('cls' if os.name == 'nt' else 'clear')


        print_matrix_junk()
        os.system('cls' if os.name == 'nt' else 'clear')

        # run filler

        sfx_thread_misc = WaveSfxThread(SFX_DIR_PATH_MISC)
        sfx_thread_misc.start()
        time.sleep(1)
        sfx_thread_beep = WaveSfxThread(SFX_DIR_PATH_BEEP)
        sfx_thread_beep.start()

        num_filler_texts = random.randint(4, 10)
        for _ in range(num_filler_texts):
            if random.randint(0, 99) < EASTER_EGG_FILLER_PERCENTAGE:
                print(TEXT_FILLER_EASTER_EGG)
            else:
                filler_text = random.choice(TEXT_FILLER_VERBS) + ' ' + random.choice(TEXT_FILLER_NOUNS)
                print(filler_text, end='', flush=True)
                print_ellipsis(random.randint(1, 3))
            time.sleep(0.5)

        sfx_thread_beep.stop()
        sfx_thread_misc.stop()
        time.sleep(1)

        print()
        print('Postprocessing...')
        print_progress_bar()
        os.system('cls' if os.name == 'nt' else 'clear')

        print('Survey says...')
        time.sleep(1)

        outcome = get_outcome(hand)
        if outcome == OUTCOME_SQUINGO:
            print(colored(TEXT_SQUINGO, 'green', attrs=['blink']))
            play_random_wave_sfx_from_dir(SFX_DIR_PATH_SQUINGO)
        elif outcome == OUTCOME_NOT_SQUINGO:
            print(colored(TEXT_NOT_SQUINGO, 'red', attrs=['blink']))
            play_random_wave_sfx_from_dir(SFX_DIR_PATH_NOT_SQUINGO)
        else:  # monkey pirate
            print(colored(TEXT_MONKEY_PIRATE, 'magenta', attrs=['blink']))
            print(colored(GRAPHIC_MONKEY_PIRATE, 'magenta'))
            play_random_wave_sfx_from_dir(SFX_DIR_PATH_MONKEY_PIRATE)

if __name__ == '__main__':
    main()
