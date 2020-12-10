<h1 align="center">OrgPie</h1>
<p align="center">A simple python script to organized your files by tags using Tagbox!</p>

It uses TagBox to generate tags for images using Machine learning and then writes it to the metadata of image (only works for JPEG).

## How to use it?
1. You have to have TagBox installed in your machine. Follow this documentation to install the TagBox with Docker:
https://docs.veritone.com/#/developer/machine-box/boxes/tagbox/recognizing-images

2. You will have to install all the dependencies (``pyexiv2``, ``requests``, ``json``) installed in your machine to run the script.

3. Just use ``python classify.py`` and it will classify your images!
