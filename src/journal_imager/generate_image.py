import requests
import base64
import io
from PIL import Image

def generate_image(ngrok_url, prompt, guidance_scale, num_inference_steps, img_path):
    """ Given a prompt, generate an image.

    Args:
        ngrok_url (str): The URL of the ngrok server.
        prompt (str): The prompt to generate the image from.
        guidance_scale (float): The guidance scale to use when generating the image.
        num_inference_steps (int): The number of inference steps to use when generating the image.
        img_path (str): The path to save the generated image to.

    Returns:
        None
    """
    
    # Send a request to the Colab notebook
    response = requests.post(ngrok_url + '/generate',
                             json = {
                                 'prompt': prompt,
                                 'guidance_scale': guidance_scale,
                                 'num_inference_steps': num_inference_steps
                                 }
    )

    # Get the image string from the response
    img_str = dict(response.json())['image']

    # base64 to image
    img_bytes = base64.b64decode(img_str[2::])
    img = Image.open(io.BytesIO(img_bytes))
    img.save(img_path)