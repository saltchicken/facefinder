import os, sys
from facefinder.analyze import get_embedding
from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt()

directory = "." # Current directory
entries = os.listdir(directory)

# files = [f for f in entries if os.path.isfile(os.path.join(directory, f))]
files = [os.path.normpath(os.path.join(directory, f)) for f in entries if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

selected_image = fzf.prompt(files, '--multi --cycle')
# selected_image = fzf.prompt(files, '--multi --cycle --preview hello')
if len(selected_image) == 0:
    print("No selection made")
    sys.exit(1)
elif len(selected_image) == 1:
    selected_image_path = os.path.join(directory, selected_image[0])
    selected_image_path = os.path.normpath(selected_image_path)
else:
    print("Multiple files not implemented")

print(f"Image: {selected_image_path}")

get_embedding(selected_image_path)
