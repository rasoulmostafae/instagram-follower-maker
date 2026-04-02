#!/usr/bin/env python3
# Inshackle v2.1 (2026) - Fixed Rate Limit & Follow Issues
# Powered by instagrapi

import os
import json
import time
import random
import getpass
from instagrapi import Client
from instagrapi.exceptions import *
from colorama import init, Fore
from tqdm import tqdm

init(autoreset=True)

SESSION_FILE = "session.json"
CELEB_IDS = ["460563723", "26669533", "7719696", "247944034", "173560420", "18428658", "6380930",
             "232192182", "12281817", "305701719", "427553890", "12331195", "325734299",
             "212742998", "407964088", "7555881", "177402262", "19596899", "181306552",
             "1506607755", "184692323", "11830955", "25025320"]

def banner():
    print(f"{Fore.RED}M\"\"M {Fore.WHITE} dP dP dP")
    print(f"{Fore.RED}M  M {Fore.WHITE} 88 88 88")
    print(f"{Fore.RED}M  M {Fore.WHITE} 88d888b. .d8888b. 88d888b. .d8888b.")
    print(f"{Fore.RED}M  M {Fore.WHITE} 88'  `88 88'  `88 88'  `88 88ooood8")
    print(f"{Fore.RED}M  M {Fore.WHITE} 88    88 88.  .88 88.  .88 88. ...")
    print(f"{Fore.RED}M  M {Fore.WHITE} dP    dP `88888P' dP    dP `88888P'")
    print(f"{Fore.RED}MMMMM")
    print(f"\n{Fore.RED}[{Fore.WHITE}v2.1 2026{Fore.RED}] {Fore.WHITE}Python Edition - Powered by instagrapi")
    print(f"{Fore.YELLOW}WARNING: Heavy use can get your account banned. Use at your own risk!\n")

def handle_rate_limit():
    wait = random.randint(180, 420)  # 3 to 7 minutes
    print(f"{Fore.RED}[!] 429 Rate Limit detected. Waiting {wait//60} minutes...")
    time.sleep(wait)

def login():
    cl = Client()
    cl.delay_range = [3, 8]
    cl.request_timeout = 15

    if os.path.exists(SESSION_FILE):
        print(f"{Fore.GREEN}[+] Loading saved session...")
        cl.load_settings(SESSION_FILE)
        try:
            cl.get_timeline_feed()
            print(f"{Fore.GREEN}[+] Login successful with saved session!")
            return cl
        except:
            print(f"{Fore.YELLOW}[!] Session expired. Logging in again...")

    username = input(f"{Fore.CYAN}[+] Username: {Fore.WHITE}")
    password = getpass.getpass(f"{Fore.CYAN}[+] Password: {Fore.WHITE}")

    try:
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        print(f"{Fore.GREEN}[+] Login Successful! Session saved.")
        return cl
    except ChallengeRequired:
        code = input(f"{Fore.YELLOW}Enter code (6 digits): {Fore.WHITE}")
        cl.challenge_resolve(code)
        cl.dump_settings(SESSION_FILE)
        print(f"{Fore.GREEN}[+] Challenge passed. Login successful.")
        return cl
    except Exception as e:
        print(f"{Fore.RED}[!] Login error: {e}")
        exit(1)

def increase_followers(cl, username):
    print(f"{Fore.RED}⚠️  EXTREME WARNING (2026):")
    print(f"{Fore.RED}   This old 'follow/unfollow celebs' trick barely works anymore and is very likely to get your account action-blocked.")
    print(f"{Fore.YELLOW}   I will run only 2 very slow cycles with realistic delays.\n")
    
    confirm = input(f"{Fore.YELLOW}Do you still want to continue? (y/n): {Fore.WHITE}")
    if confirm.lower() != "y":
        return

    for cycle in range(2):
        print(f"\n{Fore.CYAN}=== Starting Cycle {cycle+1}/2 ===")
        
        # Follow phase
        print(f"{Fore.CYAN}[+] Following celebrities slowly...")
        for cid in tqdm(CELEB_IDS):
            try:
                cl.follow(cid)
                time.sleep(random.uniform(35, 55))   # Very slow & human-like
            except (RateLimitError, PleaseWaitFewMinutes, Exception) as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    handle_rate_limit()
                    break
                continue

        print(f"{Fore.YELLOW}[*] Follow phase done. Sleeping 20-30 minutes...")
        time.sleep(random.uniform(1200, 1800))

        # Unfollow phase
        print(f"{Fore.CYAN}[+] Unfollowing celebrities slowly...")
        for cid in tqdm(CELEB_IDS):
            try:
                cl.unfollow(cid)
                time.sleep(random.uniform(35, 55))
            except (RateLimitError, PleaseWaitFewMinutes, Exception) as e:
                if "429" in str(e) or "rate limit" in str(e).lower():
                    handle_rate_limit()
                    break
                continue

        print(f"{Fore.YELLOW}[*] Cycle {cycle+1} finished. Long sleep before next cycle...")
        time.sleep(random.uniform(1800, 3600))  # 30-60 minutes

    print(f"{Fore.GREEN}[+] Finished 2 cycles. Check your followers manually.")
    print(f"{Fore.YELLOW}Note: This method usually gives very few or zero new followers in 2026.")

# ====================== Other functions remain the same ======================
# (get_saved, get_story, track_unfollowers, etc. - I kept them unchanged for brevity)

def get_saved(cl, username):
    print(f"{Fore.CYAN}[+] Downloading your Saved posts...")
    os.makedirs(f"{username}/saved", exist_ok=True)
    try:
        medias = cl.saved_medias()
        for i, media in enumerate(tqdm(medias, desc="Downloading")):
            if media.media_type == 1:
                cl.photo_download(media.pk, f"{username}/saved/image_{i}.jpg")
            elif media.media_type == 2:
                cl.video_download(media.pk, f"{username}/saved/video_{i}.mp4")
        print(f"{Fore.GREEN}[+] Saved to {username}/saved/")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Could not fetch saved: {e}")

def get_story(cl, username):
    target = input(f"{Fore.CYAN}[+] Account (leave blank for your own): {Fore.WHITE}") or username
    try:
        user_id = cl.user_id_from_username(target)
        stories = cl.user_stories(user_id)
        os.makedirs(f"{target}/story", exist_ok=True)
        print(f"{Fore.CYAN}[+] Found {len(stories)} stories")
        for story in tqdm(stories, desc="Downloading stories"):
            if story.media_type == 1:
                cl.story_download(story.pk, f"{target}/story/story_{story.pk}.jpg")
            else:
                cl.story_download(story.pk, f"{target}/story/story_{story.pk}.mp4")
        print(f"{Fore.GREEN}[+] Stories saved in {target}/story/")
    except Exception as e:
        print(f"{Fore.RED}[!] Error downloading stories: {e}")

# ... (keep the rest of your original functions: save_list, load_list, get_following_list, etc.)

def menu(cl, username):
    while True:
        print(f"\n{Fore.CYAN}=== Inshackle v2.1 Menu ===")
        print(f"{Fore.WHITE}01 {Fore.YELLOW}Unfollow Tracker")
        print(f"{Fore.WHITE}02 {Fore.YELLOW}Increase Followers (Risky - Slowed)")
        print(f"{Fore.WHITE}03 {Fore.YELLOW}Download Stories")
        print(f"{Fore.WHITE}04 {Fore.YELLOW}Download Saved Content")
        print(f"{Fore.WHITE}05 {Fore.YELLOW}Download Following List")
        print(f"{Fore.WHITE}06 {Fore.YELLOW}Download Followers List")
        print(f"{Fore.WHITE}07 {Fore.YELLOW}Download Profile Info")
        print(f"{Fore.WHITE}08 {Fore.YELLOW}Mass Unfollower (Limited)")
        print(f"{Fore.WHITE}00 {Fore.YELLOW}Exit")
        choice = input(f"\n{Fore.CYAN}[::] Choose option: {Fore.WHITE}")

        if choice == "1": track_unfollowers(cl, username)
        elif choice == "2": increase_followers(cl, username)
        elif choice == "3": get_story(cl, username)
        elif choice == "4": get_saved(cl, username)
        elif choice == "5": get_following_list(cl, username)
        elif choice == "6": get_followers_list(cl, username)
        elif choice == "7": get_profile_info(cl, username)
        elif choice == "8": unfollower_mass(cl, username)
        elif choice in ("00", "0"):
            print(f"{Fore.GREEN}Goodbye!")
            break
        else:
            print(f"{Fore.RED}[!] Invalid option")
        input(f"\n{Fore.WHITE}Press Enter to continue...")

# ====================== START ======================
banner()
cl = login()
username = cl.username
menu(cl, username)