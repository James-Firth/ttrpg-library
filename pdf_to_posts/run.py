import sys
from pathlib import Path
from wand.image import Image 
from wand.color import Color
from thefuzz import fuzz
from thefuzz import process
import inquirer

# TODO: WIP, lots to do

DRY_RUN = True

def generate_template(name):
	return f'''---
title: "{name}"
draft: true
genre: "fantasy"
complication: "medium"
tags: []
pageCount: 0 
author: N/A 
publisher: N/A
features: 
- Notable Feature
---

## Pitch

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Scelerisque eu ultrices vitae auctor. Enim diam vulputate ut pharetra sit. Porttitor leo a diam sollicitudin tempor id eu nisl nunc. Arcu odio ut sem nulla pharetra diam sit. Aliquam nulla facilisi cras fermentum odio. Pretium lectus quam id leo in. Id aliquet risus feugiat in ante metus. Platea dictumst vestibulum rhoncus est. Auctor urna nunc id cursus. Vitae tortor condimentum lacinia quis vel eros donec ac odio.
'''

def generate_game(file_path, name):
	source_file_path_str = str(file_path.resolve())

	game_path = output_path / name
	game_path.mkdir(parents=True, exist_ok=True)
	(game_path/'index.md').write_text(generate_template(name))

	print("generating ", source_file_path_str )


	with Image(filename=source_file_path_str+'[0]', resolution=300) as src:
		src.alpha_channel = 'remove'
		src.background_color = Color('white')
		src.save(filename=str(game_path/'cover.jpg'))

def is_likely_corebook(file_path):
	# info
	folder_name = str(file_path.parent).lower()
	file_name = str(file_path.name).lower()


	name_score = fuzz.ratio(folder_name, file_name)
	core_score = fuzz.ratio(file_name, f"{folder_name}_core.pdf")
	singles_score = fuzz.ratio(file_name, f"{folder_name}_singles.pdf")
	print(f"name Score {name_score} for file {file_name}")
	print(f"core Score {core_score} for file {file_name}")
	print(f"single  Score {singles_score} for file {file_name}")
	return True 

#  "SMART" version
# for p in Path(root_path).iterdir():
# 	print("Folder ", p.name)
# 	if p.is_dir():
# 		for f in p.glob('*.pdf'):
# 			if is_likely_corebook(f):
# 				generate_game(f, p.name)

def run(root_path, output_path):
	# TODO: should ask for select not just a single choice in case multiple are wanted
	# Should ask for adventures or not
	for p in sorted(Path(root_path).iterdir()):
		print("Folder ", p.name)
		if p.is_dir():
			# file_list = list(p.glob('*.pdf'))
			core_gamebook = None
			file_list = [str(x.name) for x in p.glob('*.pdf')]
			if len(file_list) > 1:
				default_selected = filter(lambda x: x.lower() == p.name.lower(), file_list)
				questions = [
						inquirer.Checkbox('corebook',
							message="Which book should be used for the thumbnail(s)?",
							choices=file_list,
						),
				]
				answers = inquirer.prompt(questions)
				print("SELECTED FILE: ", str(p/answers['corebook']))
				core_gamebook = p/answers['corebook']
			elif len(file_list) == 1:
				print("AUTO SELECTED FILE:", str(p/file_list[0]))
				core_gamebook = p/file_list[0]
			else:
				print("no PDFs found")

			if DRY_RUN:
				print(f"[DRY] {core_gamebook} for game {p.name}")
			
			# if core_gamebook is not None:
			# 	print(f"generate info for {str(p.name)}...")
			# 	generate_game(core_gamebook, str(p.name))

if __name__ == "__main__":
	print("Welcome to the Game Library Generator!")
	# TODO: Accept as Commandline args
	root_path = Path("/Volumes/RPGs/")
	output_path = Path("../content/games/")

	print(f"Input {str(root_path)} output {str(output_path)}")
	run(root_path, output_path)
