#!/usr/bin/env python3
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hbreeze <hbreeze@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/13 21:49:44 by hbreeze           #+#    #+#              #
#    Updated: 2024/09/13 21:49:44 by hbreeze          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
import os
import sys
import json
import colorama
import subprocess
from colorama import Fore, Style, Back


def load_settings():
	script_dir = os.path.dirname(os.path.realpath(__file__))
	settings_path = os.path.join(script_dir, "settings.json")
	with open(settings_path, "r") as f:
		settings = json.load(f)
	return settings

settings = load_settings()

def cprint(string, color):
	print(f"{color}{string}{Style.RESET_ALL}")

def cinput(string, color):
	return input(f"{color}{string}{Style.RESET_ALL}")

def check_updates():
	cprint("Checking for updates...", Fore.GREEN)
	cwd = os.getcwd()
	script_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(script_path)
	pipe = subprocess.Popen(["git", "fetch", "--dry-run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = pipe.communicate()
	if pipe.returncode == 0:
		if stdout:
			cprint("Updates available.", Fore.YELLOW)
			if cinput("Update? (y/n): ", Fore.BLUE) == "y":
				os.system("git stash")
				os.system("git pull")
				os.system("git stash apply")
				if (cinput("Restart? (y/n): ", Fore.BLUE) == "y"):
					os.execl(sys.executable, sys.executable, *sys.argv)
	os.chdir(cwd)

def setup_project(*args):
	colorama.init()
	cprint("Setting up a new project...", Fore.GREEN)
	os.system(f"git init {os.getcwd()}")
	os.system(f"git add .")
	os.system(f"git commit -m 'Initial commit'")
	cprint("Initial commit done.", Fore.GREEN)

	remote_added = False
	for i in args:
		if i[0:len("remote=")] == "remote=":
			remote_url = i[len("remote="):]
			remote_name = input("Enter the remote name: ")
			code = os.system(f"git remote add {remote_name} {remote_url}")
			if code == 0:
				cprint(f"Added remote '{remote_name}'.", Fore.GREEN)
			else:
				cprint("Failed to add remote.", Fore.RED)
			remote_added = True

	if not remote_added and cinput("Add remote? (y/n): ", Fore.BLUE) == "y":
		cprint("https://github.com/new", Fore.BLUE)
		remote_url = cinput("Enter the remote URL: ", Fore.YELLOW)
		remote_name = cinput("Enter the remote name: ", Fore.YELLOW)
		code = os.system(f"git remote add {remote_name} {remote_url}")
		if code == 0:
			cprint(f"Added remote '{remote_name}'.", Fore.GREEN)
		else:
			cprint("Failed to add remote.", Fore.RED)

	branch_created = False
	for i in args:
		if i[0:len("branch=")] == "branch=":
			branch_name = i[len("branch="):]
			code = os.system(f"git checkout -b {branch_name}")
			if code == 0:
				cprint(f"Branch '{branch_name}' created.", Fore.GREEN)
			else:
				cprint("Failed to create branch.", Fore.RED)
			branch_created = True

	while not branch_created and cinput("Create branch? (y/n): ", Fore.BLUE) == "y":
		branch_name = input("Enter branch name: ")
		code = os.system(f"git checkout -b {branch_name}")
		if code == 0:
			cprint(f"Branch '{branch_name}' created.", Fore.GREEN)
		else:
			cprint("Failed to create branch.", Fore.RED)
		default_branch = os.system('git config --global init.defaultBranch')
		os.system(f"git checkout {'master' if not default_branch else default_branch}")

	if "readme" in args or cinput("Add README.md? (y/n): ", Fore.BLUE) == "y":
		code = os.system("touch README.md")
		if code == 0:
			cprint("README.md created.", Fore.GREEN)
		else:
			cprint("Failed to create README.md.", Fore.RED)
	
	if "gitignore" in args or cinput("Add .gitignore? (y/n): ", Fore.BLUE) == "y":
		code = os.system("touch .gitignore")
		if code == 0:
			cprint(".gitignore created.", Fore.GREEN)
			with open(".gitignore", "w") as f:
				f.write('\n'.join(settings["gitignore"]))
		else:
			cprint("Failed to create .gitignore.", Fore.RED)

	if settings["libft"] and ("libft" in args or cinput("Add libft? (y/n): ", Fore.BLUE) == "y"):
		code = os.system(f"git submodule add {settings['libft']} libft")
		if code == 0:
			cprint("libft added.", Fore.GREEN)
		else:
			cprint("Failed to add libft.", Fore.RED)

	while settings["tag_dir"] and cinput("Add to tag? (y/n): ", Fore.BLUE) == "y":
		tag_list = [f.path for f in os.scandir(settings["tag_dir"]) if f.is_dir()]
		for i, tag in enumerate(tag_list):
			cprint(f"{i+1}. {tag}", Fore.YELLOW)
		tag_choice = int(input(f"{Fore.BLUE}Enter tag number: {Style.RESET_ALL}"))
		code = os.system(f"ln -s {os.getcwd()} {tag_list[tag_choice-1]}")
		if code == 0:
			cprint("Added to tag.", Fore.GREEN)
		else:
			cprint("Failed to add to tag.", Fore.RED)

if __name__ == "__main__":
	keywords = sys.argv
	setup_project(*keywords[1:])

