"""
Freespin Frenzy V0.79
By Steve Shambles May 2020.
Work in progress.
---------------------------
pip3 install SoundFile
pip3 install sounddevice
-------------------------
0.79:Fixed highscore not saving sometimes bug. trapped root exit to iconify.
0.78:Added new startup cards instead of blanks.
0.77:Added top up $100 option when broke,or exit.also check credits b4 spin.
0.76:Linted
0.75:Added consolation prize of stake value on losing spins of fsfrenzy.
0.74:Added sound fx on off option in menu.
0.73:Finished adding sound effects.
0.72:Improved a few functions to be more effecient.
0.71:Added sounfx for jackpot, freespins and bonus pot.
0.70:Fixed extra freespins message bug during frenzy.
0.70:Added drop down menu with, about, visit blog and quit options.
0.69:Added auto load and save of players credits so can resume games laater.
0.68:Made bonus pot, min of $100.
0.68:Increased win values of JQKA payouts.
0.67:Updated paytable graphic to reflect new features.
0.67:Added bonus pot
0.66:Added 3 matching suits gets stake-back, x3 stake during feature.
0.65:Fixed minor message bug when get 2 freespin cards during feature.
0.65:Increased freespin frenzy feature to start with 15 freespins, was 10.
"""
import os
from random import randrange
import sys
import time
from tkinter import Tk, Button, Label, LabelFrame, Menu, PhotoImage
from tkinter import messagebox, DISABLED, NORMAL
import webbrowser

import sounddevice as sd
import soundfile as sf


class Glo:
    """Variables, set at defaults for global use.
       Add Glo. to each variable, then it is effectively global."""
    btn1_is_held = False
    btn2_is_held = False
    btn3_is_held = False
    hold_btn1 = None
    hold_btn2 = None
    hold_btn3 = None
    no_card_being_held = True
    random_card = ''
    card_one = ''
    card_two = ''
    card_three = ''
    reel_one = ''
    reel_two = ''
    reel_three = ''
    plyr_stake = 1
    plyr_winnings = 0
    plyr_credits = 200
    bonus_pot = 0
    high_score = 200
    stake_btn = None
    dbl_freespin = False
    freespins_in_play_count = 0
    freespins_in_play = False
    freespins_credits_won = 0
    sound_fx = True


root = Tk()
root.title('Freespin Frenzy V.79. S.Shambles May 2020')
root.resizable(False, False)
root.protocol('WM_DELETE_WINDOW', root.iconify)

def play_sound(filename):
    """Play WAV file.Supply filename when calling this function."""
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    #status = sd.wait()  # Wait until file is done playing.


def check_cards_folder():
    """Check for existence of cards folder which hold vital graphics."""
    cards_check = 'cards'
    check_file = os.path.isdir(cards_check)
    # To do, offer auto download if missing.
    if not check_file:
        root.withdraw()
        messagebox.showwarning('File Error', 'The cards folder'
                               ' is missing.\nCannot continue\n.')
        sys.exit()


check_cards_folder()

# Frame for pay table display.
pay_table_frame = LabelFrame(root)
pay_table_frame.grid(row=0, column=0)

# Load in and display paytable image.
pay_table_lbl = Label(pay_table_frame)
pay_table_img = PhotoImage(file=r'cards/gfx/pay-table-v6-386x260.png')
pay_table_lbl.config(image=pay_table_img)
pay_table_lbl.grid(row=0, column=0, padx=2, pady=2)
pay_table_lbl.photo = pay_table_img

# Frame for messages display.
msg_frame = LabelFrame(root)
msg_frame.grid(row=1, column=0)

# Startup message.
msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                text='Please choose stake, and then click Spin.')
msg_lbl.grid(row=1, column=0)

# Frame for the card images.
cards_frame = LabelFrame(root)
cards_frame.grid(row=2, column=0)

# Frame for bank display.
bank_frame = Label(root, bg='white')
bank_frame.grid(row=4, column=0)

# Frame for bonus pot display.
bpot_frame = Label(root, bg='white')
bpot_frame.grid(row=5, column=0)

# Frame for high score display.
high_score_frame = Label(root, bg='white')
high_score_frame.grid(row=6, column=0)


def freespin_msg_box():
    """Pop up to explain details of what to expect from the
       Freespin Frenzy feature."""

    messagebox.showinfo('Freespin Frenzy', 'You have won 15 Freespins.\n\n'
                        'All wins will be tripled in value.\n\n'
                        'For every Freespin card you get during\n'
                        'this feature an extra Freespin will be added\n'
                        'to your total Freespins.\n\n'
                        'Get all 3 Freespins cards in to re-trigger\n'
                        'this feature and add 15 more spins.\n\n'
                        'There is no limit to how many Freespins\n'
                        'you can amass during this feature.\n'
                        'However, a Jackpot, 3 Wildcards, will end\n'
                        'this feature.\n')


def save_high_score():
    """Save current score to file if it beats previous highscore."""
    with open(r'cards/high-score.txt', 'w') as contents:
        if Glo.high_score < Glo.plyr_credits:
            return
        save_hs = str(Glo.high_score)
        contents.write(save_hs)


def save_bank():
    """Save current bank value to resume play newxt session"""
    with open(r'cards/bank.txt', 'w') as contents:
        bank_save = str(Glo.plyr_credits)
        contents.write(bank_save)


def load_bank():
    """Load saved bank value to enable resume playfrom last session."""
    with open(r'cards/bank.txt', 'r') as contents:
        saved_bank = contents.read()
        Glo.plyr_credits = int(saved_bank)
        update_bank()


def update_high_score():
    """Update high score label."""
    high_score_lbl = Label(high_score_frame, font=('Helvetica', 10, 'bold'),
                           fg='blue',
                           text='High Score: $'+str(Glo.high_score)+'     ')
    high_score_lbl.grid(row=6, column=0)
    save_high_score()


def load_high_score():
    """Load back the high score variable from file
       and store in Glo.high_score."""
    with open(r'cards/high-score.txt', 'r') as contents:
        saved_hs = contents.read()
        if saved_hs > '':
            Glo.high_score = int(saved_hs)
            update_high_score()


def update_bank():
    """Update bank label."""
    bank_lbl = Label(bank_frame, font=('Helvetica', 10, 'bold'),
                     fg='green', text='Bank: $'+str(Glo.plyr_credits)+'     ')
    bank_lbl.grid(row=4, column=0)

    # Check if current bank beats highscore, if so then update.
    if Glo.plyr_credits > Glo.high_score:
        Glo.high_score = Glo.plyr_credits
        update_high_score()


def update_bonus_pot():
    """Update bonus pot value."""
    bpot_lbl = Label(bpot_frame, font=('Helvetica', 10, 'bold'),
                     fg='red', text='Bonus Pot: $'+str(round(Glo.bonus_pot))
                     +'   ')
    bpot_lbl.grid(row=5, column=0)


def clear_msg_box():
    """Clears msg box area with 90 blank spaces."""
    msg_lbl = Label(msg_frame, text=' ' * 90)
    msg_lbl.grid(row=1, column=0)
    msg_lbl.update()


def print_msg(message):
    """Creats a small message area for in-game info."""
    clear_msg_box()
    msg_lbl = Label(msg_frame, font=('Helvetica', 10, 'bold'),
                    text=message)
    msg_lbl.grid(row=1, column=0)
    msg_lbl.update()


def disable_hold_btns():
    """De-activate hold buttons."""
    Glo.hold_btn1.configure(state=DISABLED)
    Glo.hold_btn2.configure(state=DISABLED)
    Glo.hold_btn3.configure(state=DISABLED)
    Glo.no_card_being_held = True


def enable_hold_btns():
    """Activate hold buttons."""
    Glo.hold_btn1.configure(state=NORMAL)
    Glo.hold_btn2.configure(state=NORMAL)
    Glo.hold_btn3.configure(state=NORMAL)
    Glo.no_card_being_held = False


def hold_card1():
    """Check if can hold or unhold card one, if so toogle it and update it."""
    # No holds allowed yet so return.
    if Glo.no_card_being_held:
        return
    # Toggle boolean, so if held, unhold, and vice versa.
    Glo.btn1_is_held = not Glo.btn1_is_held
    if Glo.sound_fx:
        play_sound(r"cards/sounds/hold-btn.wav")

    hold_unhold_btn_img = 'cards/gfx/hold-btn.png'
    if Glo.btn1_is_held:
        hold_unhold_btn_img = 'cards/gfx/held-btn.png'

    Glo.hold_btn1 = Button(cards_frame, width=68, height=35,
                           command=hold_card1)
    hold_image1 = PhotoImage(file=hold_unhold_btn_img)
    Glo.hold_btn1.config(image=hold_image1)
    Glo.hold_btn1.image = hold_image1
    Glo.hold_btn1.grid(row=2, column=1, padx=2, pady=2)


def hold_card2():
    """Check if can hold or unhold card 2."""
    if Glo.no_card_being_held:
        return
    Glo.btn2_is_held = not Glo.btn2_is_held
    if Glo.sound_fx:
        play_sound(r"cards/sounds/hold-btn.wav")

    hold_unhold_btn_img = 'cards/gfx/hold-btn.png'
    if Glo.btn2_is_held:
        hold_unhold_btn_img = 'cards/gfx/held-btn.png'

    Glo.hold_btn2 = Button(cards_frame, width=68, height=35,
                           command=hold_card2)
    hold_image2 = PhotoImage(file=hold_unhold_btn_img)
    Glo.hold_btn2.config(image=hold_image2)
    Glo.hold_btn2.image = hold_image2
    Glo.hold_btn2.grid(row=2, column=2, padx=2, pady=2)


def hold_card3():
    """Check if can hold or unhold card 3."""
    if Glo.no_card_being_held:
        return
    Glo.btn3_is_held = not Glo.btn3_is_held
    if Glo.sound_fx:
        play_sound(r"cards/sounds/hold-btn.wav")

    hold_unhold_btn_img = 'cards/gfx/hold-btn.png'
    if Glo.btn3_is_held:
        hold_unhold_btn_img = 'cards/gfx/held-btn.png'

    Glo.hold_btn3 = Button(cards_frame, width=68, height=35,
                           command=hold_card3)
    hold_image3 = PhotoImage(file=hold_unhold_btn_img)
    Glo.hold_btn3.config(image=hold_image3)
    Glo.hold_btn3.image = hold_image3
    Glo.hold_btn3.grid(row=2, column=3, padx=2, pady=2)


def reset_hold_btns():
    """If any hold buttons are in the held state, then unhold them to reset."""
    if Glo.btn1_is_held:
        hold_card1()
    if Glo.btn2_is_held:
        hold_card2()
    if Glo.btn3_is_held:
        hold_card3()


def get_rnd_cards():
    """Select 3 different random cards for a new game."""
    # Ranks list. Fx is a frespin card and Wx is a wildcard, Bx bonus pot.
    Glo.ranks = ['FH', 'FD', 'FC',
                 'WH', 'WD', 'WC',
                 'JH', 'JD', 'JC', 'JS',
                 'QH', 'QD', 'QC', 'QS',
                 'KH', 'KD', 'KC', 'KS',
                 'AH', 'AD', 'AC', 'AS',
                 'BH', 'BD', 'BC']

    if not Glo.btn1_is_held:
        # Choose a rnd card for card one.
        card_one_rank = randrange(len(Glo.ranks))
        Glo.card_one = (Glo.ranks[card_one_rank])
        # Delete the chosen card from the list
        # so cant be picked again this hand.
        del Glo.ranks[card_one_rank]

    if not Glo.btn2_is_held:
        card_two_rank = randrange(len(Glo.ranks))
        Glo.card_two = (Glo.ranks[card_two_rank])
        del Glo.ranks[card_two_rank]

    if not Glo.btn3_is_held:
        card_three_rank = randrange(len(Glo.ranks))
        Glo.card_three = (Glo.ranks[card_three_rank])
        del Glo.ranks[card_three_rank]

    # Check for duplicate card,
    # If one found do the lot again:get_rnd_hand().
    if Glo.card_one == Glo.card_two or Glo.card_one ==  \
            Glo.card_three or Glo.card_two == Glo.card_three:
        # Calls itself to do this def again from start,if dup.
        get_rnd_cards()


def rnd_hold():
    """Random chance of a hold. No holds allowed during Freespins."""
    Glo.no_card_being_held = True
    reset_hold_btns()
    set_hold_btns()
    disable_hold_btns()

    Glo.btn1_is_held = False
    Glo.btn2_is_held = False
    Glo.btn3_is_held = False

    Glo.stake_btn.config(state=NORMAL)
    rnd_hld = randrange(5)  # 1 in 5 chance of a hold and hold after win.
    # Change the 5 to 1 for testing, holds every go.

    if not rnd_hld:
        enable_hold_btns()
        Glo.no_card_being_held = False
        Glo.stake_btn.config(state=DISABLED)


def freespin_frenzy():
    """Freespin Frenzy feature."""
    print_msg('You Win 15 freespins, all wins are tripled!')

    freespin_msg_box()

    Glo.freespins_in_play_count = 15
    Glo.freespins_in_play = True
    Glo.stake_btn.config(state=DISABLED)
    disable_hold_btns()
    time.sleep(2)

    while Glo.freespins_in_play_count > 0:
        print_msg('Freespin Frenzy: '+str(Glo.freespins_in_play_count)
                  + ' Freespins left')

        spin_btn_clkd()

        Glo.freespins_in_play_count -= 1
        Glo.stake_btn.config(state=DISABLED)
        time.sleep(2)

    # Finished freespins.
    Glo.freespins_in_play_count = 0
    Glo.freespins_in_play = False
    display_start_cards()

    print_msg('You won a total of $'+str(Glo.freespins_credits_won))
    Glo.freespins_credits_won = 0


def check_for_win():
    """Check for all winnning combinations."""
    Glo.plyr_winnings = 0
    suit1 = ''
    suit2 = ''
    suit3 = ''
    r1 = (Glo.reel_one[:1])
    r2 = (Glo.reel_two[:1])
    r3 = (Glo.reel_three[:1])

    out_come = r1+r2+r3

    # ===========================tests and cheats===============
    # get freespins feature
##    out_come = 'FFF'
##    r1 = 'F'
##    r2 = 'F'
##    r3 = 'F'
##
##    if Glo.freespins_in_play and Glo.freespins_in_play_count == 43:
##        #give test bonuspot on freespin 43
##        out_come = 'FFW'
##        r1 = 'F'
##        r2 = 'F'
##        r3 = 'W'

    #=====================================================

    # Check for 3 of same suit, First find out if any wild or fs cards are out.
    wild_fs = True
    if r1 == 'W' or r2 == 'W' or r3 == 'W' or r1 == 'F' or r2 == 'F'  \
       or r3 == 'F' or r1 == 'B' or r2 == 'B' or r3 == 'B':
        wild_fs = False

    if wild_fs:
        suit1 = (Glo.reel_one[1:-4])  # Get suit letter, i.e H,S,D,C
        suit2 = (Glo.reel_two[1:-4])
        suit3 = (Glo.reel_three[1:-4])

    if Glo.freespins_in_play:
        disable_hold_btns()

    # Check for 3 matching suits.
    suits = suit1+suit2+suit3
    sewts = ['DDD', 'HHH', 'CCC', 'SSS']
    if suits in sewts:
        if Glo.freespins_in_play:
            Glo.plyr_winnings += Glo.plyr_stake * 3
            Glo.freespins_credits_won += Glo.plyr_stake * 3
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-suits.wav")
        else:
            Glo.plyr_winnings += Glo.plyr_stake

        print_msg('3 matching suits - You win $'+str(Glo.plyr_winnings))
        Glo.plyr_credits += Glo.plyr_winnings
        if Glo.sound_fx:
            play_sound(r"cards/sounds/three-suits.wav")
        update_bank()
        update_high_score()
        time.sleep(1)
        return

    # Check for 3 bonus pot cards - wins bonus pot.
    if out_come == 'BBB':
        if Glo.freespins_in_play:
            Glo.plyr_winnings += Glo.bonus_pot
            Glo.freespins_credits_won += Glo.bonus_pot
            print_msg('You win the bonus pot $'+str(Glo.plyr_winnings))
            if Glo.sound_fx:
                play_sound(r"cards/sounds/bonus-pot.wav")
            time.sleep(1)
        else:
            Glo.plyr_winnings += Glo.bonus_pot
            if Glo.sound_fx:
                play_sound(r"cards/sounds/bonus-pot.wav")

        Glo.plyr_credits += Glo.bonus_pot
        update_bank()
        update_high_score()
        print_msg('You win the bonus pot $'+str(Glo.plyr_winnings))
        return

    # Check for 3 wilds - jackpot.
    if out_come == 'WWW':
        if Glo.freespins_in_play:
            Glo.plyr_winnings += Glo.plyr_stake * 600
            Glo.freespins_credits_won += Glo.plyr_stake * 600
            print_msg('3 Wilds - Jackpot! You win $'+str(Glo.plyr_winnings))
            if Glo.sound_fx:
                play_sound(r"cards/sounds/jackpot.wav")
            time.sleep(1)
            # If jackpot then end the freespins feature.
            Glo.freespins_in_play = False
            Glo.freespins_in_play_count = 0
            print_msg('Jackpot ends Freespins...')
            time.sleep(1)

        else:
            Glo.plyr_winnings += Glo.plyr_stake * 200
            if Glo.sound_fx:
                play_sound(r"cards/sounds/jackpot.wav")

        Glo.plyr_credits += Glo.plyr_winnings
        update_bank()
        update_high_score()
        print_msg('3 Wilds - Jackpot! You win $'+str(Glo.plyr_winnings))
        return

    # Check for freespins.
    if out_come == 'FFF':
        disable_hold_btns()
        if not Glo.freespins_in_play:
            if Glo.sound_fx:
                play_sound(r"cards/sounds/freespins.wav")
            freespin_frenzy()
        else:
            Glo.freespins_in_play_count += 15  # add to fs as already in play.
            print_msg('FREESPINS RE-TRIGGERED - 15 more added')
            if Glo.sound_fx:
                play_sound(r"cards/sounds/freespins.wav")
            time.sleep(1)
        return

    mess = ''
    # Checks for 2 fs cards and configures appropriate message.
    if r1 == 'F' and r2 == 'F' or r1 == 'F' and r3 == 'F' \
            or r2 == 'F' and r3 == 'F':
        mess = 'You win two extra Freespins'
    else:
        mess = 'You win an extra Freespin'

    if r1 == 'F':
        if Glo.freespins_in_play:
            Glo.freespins_in_play_count += 1
            if Glo.sound_fx:
                play_sound(r"cards/sounds/extra-fs.wav")
            print_msg(mess)

    if r2 == 'F':
        if Glo.freespins_in_play:
            Glo.freespins_in_play_count += 1
            if Glo.sound_fx:
                play_sound(r"cards/sounds/extra-fs.wav")
            print_msg(mess)

    if r3 == 'F':
        if Glo.freespins_in_play:
            Glo.freespins_in_play_count += 1
            if Glo.sound_fx:
                play_sound(r"cards/sounds/extra-fs.wav")
            print_msg(mess)

    # Check for 3 jacks.
    jacks = ['JJJ', 'WJJ', 'WWJ', 'JWJ', 'JJW', 'WJW', 'JWW']
    if out_come in jacks:
        if Glo.freespins_in_play:
            Glo.plyr_winnings += Glo.plyr_stake * 15
            Glo.freespins_credits_won += Glo.plyr_stake * 15
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-pics.wav")
            print_msg('3 Jacks - You win $'+str(Glo.plyr_winnings))
        else:
            Glo.plyr_winnings += Glo.plyr_stake * 5
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-pics.wav")

        Glo.plyr_credits += Glo.plyr_winnings
        update_bank()
        update_high_score()
        print_msg('3 Jacks - You win $'+str(Glo.plyr_winnings))

    # Check for 3 queens.
    queens = ['QQQ', 'WQQ', 'WWQ', 'QWQ', 'QQW', 'WQW', 'QWW']
    if out_come in queens:
        if Glo.freespins_in_play:
            Glo.plyr_winnings += Glo.plyr_stake * 30
            Glo.freespins_credits_won += Glo.plyr_stake * 30
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-pics.wav")
            print_msg('3 Queens - You win $'+str(Glo.plyr_winnings))
        else:
            Glo.plyr_winnings += Glo.plyr_stake * 10
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-pics.wav")

        Glo.plyr_credits += Glo.plyr_winnings
        update_bank()
        update_high_score()
        print_msg('3 Queens - You win $'+str(Glo.plyr_winnings))

    # Check for 3 kings.
    kings = ['KKK', 'WKK', 'WWK', 'KWK', 'KKW', 'WKW', 'KWW']
    if out_come in kings:
        if Glo.freespins_in_play:
            Glo.plyr_winnings += Glo.plyr_stake * 45
            Glo.freespins_credits_won += Glo.plyr_stake * 45
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-pics.wav")
            print_msg('3 Kings - You win $'+str(Glo.plyr_winnings))
        else:
            Glo.plyr_winnings += Glo.plyr_stake * 15
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-pics.wav")

        Glo.plyr_credits += Glo.plyr_winnings
        update_bank()
        update_high_score()
        print_msg('3 Kings - You win $'+str(Glo.plyr_winnings))

    # Check for 3 aces.
    aces = ['AAA', 'WAA', 'WWA', 'AWA', 'AAW', 'WAW', 'AWW']
    if out_come in aces:
        if Glo.freespins_in_play:
            Glo.plyr_winnings += Glo.plyr_stake * 60
            Glo.freespins_credits_won += Glo.plyr_stake * 60
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-pics.wav")
            print_msg('3 Aces - You win $'+str(Glo.plyr_winnings))
        else:
            Glo.plyr_winnings += Glo.plyr_stake * 20
            if Glo.sound_fx:
                play_sound(r"cards/sounds/three-pics.wav")
        Glo.plyr_credits += Glo.plyr_winnings
        update_bank()
        update_high_score()
        print_msg('3 Aces - You win $'+str(Glo.plyr_winnings))

    if not Glo.plyr_winnings and not Glo.freespins_in_play:
        print_msg('No Win')
        if Glo.sound_fx:
            play_sound(r"cards/sounds/lose.wav")

    if not Glo.plyr_winnings and Glo.freespins_in_play  \
            and 'F' not in out_come:
        Glo.plyr_winnings += Glo.plyr_stake
        Glo.freespins_credits_won += Glo.plyr_stake
        Glo.plyr_credits += Glo.plyr_winnings
        print_msg('Consolation prize $'+str(Glo.plyr_stake))
        if Glo.sound_fx:
            play_sound(r"cards/sounds/consolation.wav")
        update_bank()
        update_high_score()


def spin_reels():
    """Pseudo spin,pretty poor, but best I can do for now."""

    spinner = ['FH', 'FD', 'FC',
               'WH', 'WD', 'WC',
               'JH', 'JD', 'JC', 'JS',
               'QH', 'QD', 'QC', 'QS',
               'KH', 'KD', 'KC', 'KS',
               'AH', 'AD', 'AC', 'AS',
               'BH', 'BD', 'BC']

    r_one = Label(cards_frame)
    r_two = Label(cards_frame)
    r_three = Label(cards_frame)

    Glo.hold_btn1.configure(state=DISABLED)
    Glo.hold_btn2.configure(state=DISABLED)
    Glo.hold_btn3.configure(state=DISABLED)

    for spins in range(4):

        for spinr in range(18):
        # spinr represents how many symbols to display for the spin.
        # the bigger the value the longer the spin will take.
        
            rnd_symb1 = randrange(len(spinner))
            symb1 = spinner[rnd_symb1]+'.png'

            rnd_symb2 = randrange(len(spinner))
            symb2 = spinner[rnd_symb2]+'.png'

            rnd_symb3 = randrange(len(spinner))
            symb3 = spinner[rnd_symb3]+'.png'

            if spins < 1 and not Glo.btn1_is_held:  # Check reel not held.
                # r_one is a temp variable for duratiion of spin.
                r_one = Label(cards_frame)
                PHOTO = PhotoImage(file='cards/gfx/'+str(symb1))
                r_one.config(image=PHOTO)
                r_one.grid(row=0, column=1, padx=2, pady=2)
                r_one.photo = PHOTO
                r_one.update()

            if spins == 1 and not Glo.btn1_is_held:
                # card_lbl_one is what symbol reel 1 stops on.
                card_lbl_one = Label(cards_frame)
                PHOTO = PhotoImage(file='cards/gfx/'+str(Glo.reel_one))
                card_lbl_one.config(image=PHOTO)
                card_lbl_one.grid(row=0, column=1, padx=2, pady=2)
                card_lbl_one.photo = PHOTO
                r_one.update()

            if spins < 2 and not Glo.btn2_is_held:
                r_two = Label(cards_frame)
                PHOTO = PhotoImage(file='cards/gfx/'+str(symb2))
                r_two.config(image=PHOTO)
                r_two.grid(row=0, column=2, padx=2, pady=2)
                r_two.photo = PHOTO
                r_two.update()

            if spins == 2 and not Glo.btn2_is_held:
                card_lbl_two = Label(cards_frame)
                PHOTO = PhotoImage(file='cards/gfx/'+str(Glo.reel_two))
                card_lbl_two.config(image=PHOTO)
                card_lbl_two.grid(row=0, column=2, padx=2, pady=2)
                card_lbl_two.photo = PHOTO
                r_two.update()

            if spins < 3 and not Glo.btn3_is_held:
                r_three = Label(cards_frame)
                PHOTO = PhotoImage(file='cards/gfx/'+str(symb3))
                r_three.config(image=PHOTO)
                r_three.grid(row=0, column=3, padx=2, pady=2)
                r_three.photo = PHOTO
                r_three.update()

            if spins == 3 and not Glo.btn3_is_held:
                spins = 99
                card_lbl_three = Label(cards_frame)
                PHOTO = PhotoImage(file='cards/gfx/'+str(Glo.reel_three))
                card_lbl_three.config(image=PHOTO)
                card_lbl_three.grid(row=0, column=3, padx=2, pady=2)
                card_lbl_three.photo = PHOTO
                r_three.update()

            time.sleep(0.025)
            # Destroy temp vars holding images that were spun.
            r_one.destroy()
            r_two.destroy()
            r_three.destroy()

    
    check_for_win()
    rnd_hold()
    save_bank()


def setup_result():
    """Set up the next game, preloading the next spin."""
    get_rnd_cards()

    Glo.reel_one = Glo.card_one+'.png'
    Glo.card1_val = Glo.random_card

    Glo.reel_two = Glo.card_two+'.png'
    Glo.card2_val = Glo.random_card

    Glo.reel_three = Glo.card_three+'.png'
    Glo.card3_val = Glo.random_card


def set_hold_btns():
    """Load and display hold buttons."""
    hold_btn_img = PhotoImage(file='cards/gfx/hold-btn.png')

    Glo.hold_btn1 = Button(cards_frame, width=68, height=35,
                           command=hold_card1)
    Glo.hold_btn1.config(image=hold_btn_img)
    Glo.hold_btn1.image = hold_btn_img
    Glo.hold_btn1.grid(row=2, column=1, padx=2, pady=2)

    Glo.hold_btn2 = Button(cards_frame, width=68, height=35,
                           command=hold_card2)
    Glo.hold_btn2.config(image=hold_btn_img)
    Glo.hold_btn2.image = hold_btn_img
    Glo.hold_btn2.grid(row=2, column=2, padx=2, pady=2)

    Glo.hold_btn3 = Button(cards_frame, width=68, height=35,
                           command=hold_card3)
    Glo.hold_btn3.config(image=hold_btn_img)
    Glo.hold_btn3.image = hold_btn_img
    Glo.hold_btn3.grid(row=2, column=3, padx=2, pady=2)


def spin_btn_clkd():
    """Spin button clicked."""
    if Glo.plyr_credits < Glo.plyr_stake:
        messagebox.showinfo('Freespin Frenzy', 'Not enough credits\n')
        return

    if Glo.sound_fx:
        play_sound(r"cards/sounds/spin-btn.wav")
    spin_btn.configure(state=DISABLED)
    spin_btn.update()
    Glo.stake_btn.config(state=DISABLED)

    # Choose a random value for bonus pot, based on stake, max x50 stake.
    Glo.bonus_pot = randrange(Glo.plyr_stake * 150)
    Glo.bonus_pot += 100  # Min $100 pot
    update_bonus_pot()

    if not Glo.freespins_in_play:
        Glo.plyr_credits -= Glo.plyr_stake  # Not freespins so charge credit.

        # Choose a random value for bonus pot, based on stake, max x50 stake.
        Glo.bonus_pot = randrange(Glo.plyr_stake * 150)
        Glo.bonus_pot += 100  # Min $100 pot
        update_bonus_pot()

        update_bank()

    setup_result()

    if not Glo.freespins_in_play:
        clear_msg_box()

    spin_reels()
    if not Glo.freespins_in_play:
        spin_btn.configure(state=NORMAL)

    if Glo.plyr_credits < 1:
        ask_yn = messagebox.askyesno('Credits', 'You do not have enough'
                               '\ncredits left to play another game\n\n'
                               'Would you like a $100 top-up?.')
        if ask_yn is False:
            root.destroy()
            sys.exit()

        Glo.plyr_credits = 100
        update_bank()


def update_stake():
    """Update stake amount image button when changed, 1-5."""
    load_file = 'cards/gfx/stake-btn'+str(Glo.plyr_stake)+'.png'

    Glo.stake_btn = Button(cards_frame, width=68, height=35,
                           command=bet_one)
    stake_image = PhotoImage(file=load_file)
    Glo.stake_btn.config(image=stake_image)
    Glo.stake_btn.image = stake_image
    Glo.stake_btn.grid(row=2, column=0, padx=2, pady=2)

    Glo.bonus_pot = 100 * Glo.plyr_stake
    update_bonus_pot()


def bet_one():
    """Change stake amount, $1 to $5."""
    if Glo.sound_fx:
        play_sound(r"cards/sounds/stake-btn.wav")
    if Glo.plyr_stake == 5:  # Roll around to 1, if = 5.
        Glo.plyr_stake = 1
        update_stake()
        return
    Glo.plyr_stake += 1
    update_stake()


# Create stake btn.
load_file = 'cards/gfx/stake-btn1.png'

Glo.stake_btn = Button(cards_frame, width=68, height=35, command=bet_one)
stake_image = PhotoImage(file=load_file)
Glo.stake_btn.config(image=stake_image)
Glo.stake_btn.image = stake_image
Glo.stake_btn.grid(row=2, column=0, padx=2, pady=2)

# Create spin btn.
spin_btn = Button(cards_frame, width=68, height=35, command=spin_btn_clkd)
spin_image = PhotoImage(file=r'cards/gfx/spin-btn2.png')
spin_btn.config(image=spin_image)
spin_btn.image = spin_image
spin_btn.grid(row=2, column=5, padx=2, pady=2)


def display_start_cards():
    """For new game start, show cards face down."""
    if Glo.sound_fx:
        play_sound(r"cards/sounds/startup.wav")
    for plc_crds in range(3):
        c_one = Button(cards_frame)
        PHOTO = PhotoImage(file='cards/gfx/blank-'+str(plc_crds+1)+'.png')
        c_one.config(image=PHOTO)
        c_one.grid(row=0, column=plc_crds+1, padx=2, pady=2)
        c_one.photo = PHOTO
        c_one.update()


def start_game():
    """Start off the whole show here."""
    load_high_score()
    load_bank()
    update_bank()
    update_high_score()
    display_start_cards()
    set_hold_btns()
    Glo.no_card_being_held = True
    disable_hold_btns()
    Glo.bonus_pot = 100 * Glo.plyr_stake
    update_bonus_pot()
    # The program now loops, waiting for either the spin btn, holds,
    # or stake btn to be clicked.


def about_menu():
    """About program menu text."""
    messagebox.showinfo('Program Information', 'Freespin Frenzy V0.79 '
                        'May 17th 2020\n\n'
                        'Freeware. By Steve Shambles.\n\n')


def visit_blog():
    """Visit my python blog, you know it makes sense."""
    webbrowser.open('https://stevepython.wordpress.com/python-posts-quick-index/')


def exit_app():
    """Yes-no requestor to exit program."""
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to Quit?')
    if ask_yn is False:
        return
    save_high_score()
    save_bank()
    root.destroy()
    sys.exit()


def sound_off():
    """Switch sound effects off from drop down menu."""
    Glo.sound_fx = False


def sound_on():
    """Switch sound effects on from drop down menu."""
    Glo.sound_fx = True


# Drop-down menu.
MENU_BAR = Menu(root)
FILE_MENU = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label='Menu', menu=FILE_MENU)
FILE_MENU.add_command(label='Sound fx ON', command=sound_on)
FILE_MENU.add_command(label='Sound fx OFF', command=sound_off)
FILE_MENU.add_command(label='About', command=about_menu)
FILE_MENU.add_separator()
FILE_MENU.add_command(label='Visit blog', command=visit_blog)
FILE_MENU.add_command(label='Exit', command=exit_app)
root.config(menu=MENU_BAR)

start_game()

root.mainloop()
