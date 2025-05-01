
import gradio as gr
from transformers import BlipProcessor, BlipForConditionalGeneration
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
import torch, cv2
import numpy as np
from PIL import Image

# Load models
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to("cuda")
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
).to("cuda")
pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_xformers_memory_efficient_attention()

def generate(image):
    image = image.convert("RGB").resize((512, 512))
    inputs = blip_processor(image, return_tensors="pt").to("cuda")
    caption = blip_processor.decode(blip_model.generate(**inputs)[0], skip_special_tokens=True)
    prompt = f"A G1-style Transformer robot that turns into {caption}"

    image_cv = np.array(image)
    edges = cv2.Canny(image_cv, 100, 200)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    control_image = Image.fromarray(edges_rgb)

    result = pipe(prompt, image=control_image, num_inference_steps=30, guidance_scale=8.5).images[0]
    return result

gr.Interface(fn=generate, inputs=gr.Image(type="pil"), outputs=gr.Image(type="pil"), title="G1 Transformer Generator").launch()
