import requests
import os

from PIL import Image

api_key = input("Enter your API Key: ").strip()

while True:
	output_directory = input("Enter the output directory: ").strip()

	if os.path.isfile(output_directory):
		print("❌ Error: Please enter a valid directory path.")
		continue

	os.makedirs(output_directory, exist_ok=True)
	break

url = "https://api.remove.bg/v1.0/removebg"

while True:
	picture_path = input("Enter the image path (or type 'ok' to finish): ").strip()

	if picture_path.lower() == "ok":
		print("✅ All images processed. Exiting...")
		break

	if not os.path.exists(picture_path):
		print("❌ Error: The specified file does not exist. Try again.")
		continue

	original_image = Image.open(picture_path)
	width, height  = original_image.size

	with open(picture_path, 'rb') as img_file:
		files = {'image_file': img_file}
		head  = {'X-Api-Key':  api_key}
		data  = {'size':       'auto'}

		response = requests.post(url, files=files, headers=head, data=data)

	if response.status_code == requests.codes.ok:
		base_name = os.path.splitext(os.path.basename(picture_path))[0]
		outp_path = os.path.join(output_directory, f"{base_name}.png")

		with open(outp_path, 'wb') as out:
			out.write(response.content)

		result_image = Image.open(outp_path)
		result_image = result_image.resize((width, height), Image.Resampling.LANCZOS)

		result_image.save(outp_path, format="PNG", quality=100, compress_level=0)

		print(f"✅ Processed: {outp_path}")

	else:
		print("❌ Error: ", response.status_code, response.text)
