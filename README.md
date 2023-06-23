# GramDrop
GramDrop is a terminal-based uploader for Instagram, built using Python. 

It allows you to upload images directly to Instagram feed from your local machine. 
The uploader utilizes the instabot library to handle the upload process.

## Installation

Follow these steps to set up the Gram Drop application:

1. Clone the repository:
	
   		git clone https://github.com/gv1shnu/GramDrop.git

2. Navigate to the project directory:
	
   		cd GramDrop

3. To run this project, make sure you have Python 3.11 and pip installed on your system. Install the required dependencies using:
	
		pip install -r requirements.txt

## Usage

1. Run the main python program:

		python gramdrop.py

2. Follow the prompts in the terminal to provide the required information:

   - Enter the path to the folder containing the images you want to upload.
   - Enter your Instagram username.
   - Enter your Instagram password.

3. GramDrop will automatically convert any images in the folder to proper format and upload them to your Instagram account.

## Acknowledgments 

This project utilizes the [instabot](https://pypi.org/project/instabot/) library, which provides the Instagram upload functionality. I extend my gratitude to the instabot community for their contribution.

Happy uploading! (if it works)

**Note**: It is recommended to use GramDrop responsibly and in compliance with Instagram's terms of service. 

## License

This project is licensed under the [MIT License](LICENSE).