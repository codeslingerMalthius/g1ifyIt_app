
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import cv2
import numpy as np

# Load BLIP for prompt generation
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda")

# Load ControlNet + Stable Diffusion pipeline
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")
pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_xformers_memory_efficient_attention()

# Function to generate a G1-style robot prompt from a vehicle image
def generate_prompt(image: Image.Image) -> str:
    inputs = blip_processor(image, return_tensors="pt").to("cuda")
    output = blip_model.generate(**inputs)
    caption = blip_processor.decode(output[0], skip_special_tokens=True)
    return f"A G1-style Transformer robot that turns into {caption}"

# Function to generate ControlNet image from vehicle photo using Canny edge detection
def get_canny_image(image: Image.Image) -> Image.Image:
    image_cv = np.array(image.convert("RGB"))
    image_cv = cv2.resize(image_cv, (512, 512))
    edges = cv2.Canny(image_cv, 100, 200)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    return Image.fromarray(edges_rgb)

# Main function to process vehicle image and return robot image
def generate_robot_image(vehicle_image_path: str) -> Image.Image:
    original_image = Image.open(vehicle_image_path).convert("RGB").resize((512, 512))
    prompt = generate_prompt(original_image)
    control_image = get_canny_image(original_image)
    output = pipe(prompt, image=control_image, num_inference_steps=30, guidance_scale=8.5).images[0]
    return output
