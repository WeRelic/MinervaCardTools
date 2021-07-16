# minerva_protocard_images.py
# imports and loads all prototyping images.

from PIL import Image, ImageDraw, ImageFont
import os, sys

from os.path import dirname, join


def local_path( *args ):
    return os.path.join( os.path.dirname( sys.argv[0] ), *args )


# Generates a basic card image
new_card_image = lambda : Image.open( local_path( f"src\\CardFront.png" ) )
card_back = Image.open( local_path( f"src\\CardBack.png" ) )

# Generic pip images for 1-10
generic_pips = [ Image.open( local_path( f"src\\GenericPip{n}.png" ) ) for n in range(1,11) ]
font = ImageFont.truetype( local_path( "src\\OptimusPrinceps.ttf" ), 244 )

# Used to categorize card images into various files. Better organization.
card_categories = [ 'misc', 'economic', 'edicts', 'units', 'logistics', 'draw_cards', 'interaction' ]

# Check that all category directories exist and create them if they don't.
for c in card_categories:
    if not os.path.isdir( local_path( f"img\\{c}" ) ):
        os.mkdir( local_path(f"img\\{c}") )
    
# Pip images for each "colored" pip
pip_images = { 
    k.lower() : Image.open( 
        local_path( f"src\\{k}Pip.png" ) 
        ) for k in [ "Alloy", "Research", "Energy", "Ore", "Scrap" ] 
}
