from huggingface_hub import InferenceClient
from IPython.display import display

client = InferenceClient(
    provider="hf-inference",
    api_key="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"
)
def Genarate_img(prompt):
    try:
        image = client.text_to_image(
            "genrate relavent images of the discussion given below \n\n "+prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )
        
        display(image)
        image.save("astronaut_riding_horse.png")
        print("Image successfully generated and saved!")
        
    except Exception as e:
        print(f"Error with first model: {e}")
        
        try:
            image = client.text_to_image(
                "genrate relavent images of the discussion given below \n\n "+prompt,
                model="runwayml/stable-diffusion-v1-5"
            )
            
            display(image)
            image.save("astronaut_riding_horse.png")
            print("Image successfully generated with backup model!")
            
        except Exception as e2:
            print(f"Error with second model: {e2}")
            print("Suggestion: Try during off-peak hours or with a Pro subscription")