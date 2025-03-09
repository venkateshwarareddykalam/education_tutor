import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

#img_url = 'fighter.jpg' 
#raw_image = Image.open(img_url).convert('RGB')

def get_image_info(raw_image):
	# conditional image captioning
	#text = "a photography of"
	#inputs = processor(raw_image, text, return_tensors="pt")

	#out = model.generate(**inputs)
	#print(processor.decode(out[0], skip_special_tokens=True))
	# >>> a photography of a woman and her dog

	# unconditional image captioning
	inputs = processor(raw_image, return_tensors="pt")

	out = model.generate(**inputs)
	ans = str(processor.decode(out[0], skip_special_tokens=True))
	return ans
	#>>> a woman sitting on the beach with her dog
