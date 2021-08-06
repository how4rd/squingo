```
 ▄█▀▀▀▄█   ▄▄█▀▀██   ▀██▀  ▀█▀ ▀██▀ ▀█▄   ▀█▀  ▄▄█▀▀▀▄█   ▄▄█▀▀██
 ██▄▄  ▀  ▄█▀    ██   ██    █   ██   █▀█   █  ▄█▀     ▀  ▄█▀    ██
  ▀▀███▄  ██      ██  ██    █   ██   █ ▀█▄ █  ██    ▄▄▄▄ ██      ██
▄     ▀██ ▀█▄  ▀▄ ▀█  ██    █   ██   █   ███  ▀█▄    ██  ▀█▄     ██
█▀▄▄▄▄█▀    ▀█▄▄▄▀█▄   ▀█▄▄▀   ▄██▄ ▄█▄   ▀█   ▀▀█▄▄▄▀█   ▀▀█▄▄▄█▀
```

## Background

Squingo is a card game from the future. Its rules are so complicated that real-time play is intractable using unaugmented human cognition. Instead, supercomputers analyze each hand to answer that most burning question: Squingo or Not Squingo?

Squingo was designed as a booth for AstroCamp's casino event during the summer of 2021. Each player places a bet on the outcome of the game. An outcome of "Squingo" yields double the initial bet; an outcome of "Not Squingo" yields nothing; and the rare outcome of "Monkey Pirate" yields triple the initial bet. The outcomes are probabilistic and independent of the input.

Two staff members operate the station under a blacklight while electronic music blasts in the background. One, the host, is dressed in formal clothes and guides campers through the game. The other is the Squingobot, dressed in a robot helmet, who remains silent and types inputs into the Squingo program.

The host instructs campers to perform arbitrary tasks, such as throwing cards at the wall or adding up numbers, and then tells the Squingobot ridiculous text to enter as the card hand. Instead of following those directions, the Squingobot mashes the keyboard before submitting the hand. A series of randomly generated filler strings fill the screen (think "reticulating splines") and ridiculous sounds play while the host builds up hype for the output. Once the output appears, the host pays out the campers' bets.

The campers had a blast!

## Configuration

Squingo is written in Python. If you have `pip` installed, you can install the program's dependencies by running

```
pip install -r requirements.txt
```

from the program's directory. Then, play Squingo by running

```
python squingo.py
```

from the program's directory. The game loops until the user terminates the program.

## Credits

Credit for the initial Squingo concept goes to Max St. Claire, who developed it as a complicated game played with physical cards. He also came up with the idea for this digital version.

Credits for the sound effects are listed in `sfx/sfx_credits.md`.
