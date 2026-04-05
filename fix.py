cat > ./fix.py << 'SCRIPT'
import glob, os

path = "/Users/swapnil/.cache/huggingface/modules/transformers_modules/icon_caption_florence/modeling_florence2.py"

with open(path) as f:
    src = f.read()

old = "            past_length = past_key_values[0][0].shape[2]"
new = "            past_length = past_key_values[0][0].shape[2] if (past_key_values is not None and past_key_values[0] is not None and past_key_values[0][0] is not None) else 0"

count = src.count(old)
print(f"Found {count} occurrences")
src = src.replace(old, new)

with open(path, "w") as f:
    f.write(src)

pycache = "/Users/swapnil/.cache/huggingface/modules/transformers_modules/icon_caption_florence/__pycache__"
for pyc in glob.glob(f"{pycache}/*.pyc"):
    os.remove(pyc)
    print(f"Deleted {pyc}")

with open(path) as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if "past_key_values[0][0].shape" in l:
        print(f"Line {i+1}: {l.rstrip()}")

print("Done")
SCRIPT

python3 ./fix.py