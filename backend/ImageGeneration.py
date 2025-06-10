import asyncio
import os
import re
from time import sleep
from dotenv import load_dotenv
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

# Load API key (still needed for Hugging Face model download)
load_dotenv()
API_KEY = os.getenv("Hugging_Face_API")

if not API_KEY:
    raise EnvironmentError("API Key not found in .env file.")

# Load the pipeline locally
print("[*] Loading Stable Diffusion pipeline...")
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2",
    use_auth_token=API_KEY,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
pipe = pipe.to(device)
print(f"[+] Pipeline loaded on {device}")

# Generate and save a single image
def generate_image_local(prompt, index):
    try:
        result = pipe(prompt)
        image = result.images[0]
        safe_prompt = re.sub(r'[\\/*?:"<>|]', "_", prompt)
        os.makedirs("Data", exist_ok=True)
        filename = os.path.join("Data", f"{safe_prompt}_{index}.png")
        image.save(filename)
        print(f"[+] Saved: {filename}")
        return filename
    except Exception as e:
        print(f"[!] Error generating image: {e}")
        return None

# Async wrapper for parallel image generation
async def generate_images(prompt):
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, generate_image_local, prompt, i + 1) for i in range(4)]
    await asyncio.gather(*tasks)

# Open images after generation
def open_images(prompt):
    safe_prompt = re.sub(r'[\\/*?:"<>|]', "_", prompt)
    for i in range(1, 5):
        file_path = os.path.join("Data", f"{safe_prompt}_{i}.png")
        if os.path.exists(file_path):
            try:
                img = Image.open(file_path)
                img.show()
                sleep(1)
            except Exception as e:
                print(f"[!] Error opening image {file_path}: {e}")
        else:
            print(f"[!] File not found: {file_path}")

# Combined generator and viewer
def WrapperImages(prompt):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Monitor for new prompts
def monitor():
    file_path = os.path.join("Frontend", "Files", "ImageGeneration.data")
    print("🧠 Local Image Generator is running...")

    while True:
        try:
            with open(file_path, "r") as f:
                data = f.read().strip()

            if not data:
                sleep(1)
                continue

            parts = data.split(",", 1)
            if len(parts) != 2:
                print(f"[!] Invalid format: '{data}' — expected 'prompt,True'")
                sleep(1)
                continue

            prompt, status = parts[0].strip(), parts[1].strip()
            if status == 'True':
                print(f"[*] Generating images for: '{prompt}'")
                WrapperImages(prompt)

                # Clear the file after generation
                with open(file_path, "w") as f:
                    f.write("")
            else:
                sleep(1)

        except Exception as e:
            print(f"[!] Monitor error: {e}")
            sleep(1)

# Run monitor loop
if __name__ == "__main__":
    monitor()
