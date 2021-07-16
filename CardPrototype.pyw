# RelicCards.py
# TODO: Implement card sheet generation for use in tabletop sim

import json, PIL, os, sys, textwrap
# Import the custom labeled TK widgets
from minerva_tk_utils import *
# Load all the images we need to create prototype cards, as well as PIL
from minerva_protocard import *
        
class CardEntry:
    def __init__( self, root ):
        self.name = LabeledEntry( root, "Card Name:", 0  )
        self.menu = LabeledOptions( root, "Card Category:", 1, 0, card_categories )
        self.costs = {
            "any"      : LabeledEntry( root, "Generic Cost:",  2, 0, True ),
            "scrap"    : LabeledEntry( root, "Scrap Cost:",    3, 0, True ),
            "ore"      : LabeledEntry( root, "Ore Cost:",      4, 0, True ),
            "research" : LabeledEntry( root, "Research Cost:", 5, 0, True ),
            "alloy"    : LabeledEntry( root, "Alloy Cost:",    6, 0, True ),
            "energy"   : LabeledEntry( root, "Energy Cost:",   7, 0, True ),
        }
        self.rules = LabeledText( root, "Rules Text:", 8  )
        
        # Change the tab ordering
        self.name.lift()
        self.menu.lift()
        for w in self.costs.values():
            w.lift()
        self.rules.lift()
        self.show()
        
        
    def show( self ):
        self.name.grid()
        self.menu.grid()
        for v in self.costs.values():
            v.grid()
        self.rules.grid()
        
        
    def hide( self ):
        self.name.grid_forget()
        self.rules.grid_forget()
        self.menu.grid_forget()
        for v in self.costs.values():
            v.grid_forget()
            
        
    def __str__( self ):
        """ Convert this card to JSON format for saving."""
        return json.dumps( {
            "name"     : str(self.name),
            "category" : self.menu.value.get(),
            "costs"    : { k : str(v) for k,v in self.costs.items() },
            "rules"    : str( self.description )
        }, indent = 4 )
        
    
    def generate_pips( self ):
        """ 
            This function generates a single image containing all the pips required to represent the casting cost for a card. 
            Do not call this function directly, it's intended as a helper function for 'CardEntry.generate_image'
        """    
        
        resources = ['energy','ore','scrap','alloy','research']
        # Lambda to fetch cost value and keep code readable
        cost = lambda k : self.costs[k].value.get()

        # Fetching the appropriate generic pip image
        generic = None if cost('any') == 0 else generic_pips[cost('any')-1].copy()

        # Counts the number of pips that appear in the card's cost.
        total_pips = (1,0)[ cost('any') == 0 ] + sum( [cost(k) for k in resources] )

        # total number of pixels wide with 1 pixel of padding on either side of each pip, and the height of the pip image
        pip_w, pip_h = total_pips * 221, 221 
        
        # Generate a new image to composite our pip images onto
        pip_image = Image.new( 'RGBA', (pip_w,pip_h), (0,0,0,0) )
        
        # Used to collect a list of pip images to use.
        pip_list = []               
        
        # Only append the generic pip if one exists
        if generic: 
            pip_list.append( generic )
            
        # iterate through each resource type other than generic and add N pips for the count of each one.
        for k in resources:
            for n in range( cost(k) ):
                pip_list.append( pip_images[k].copy() )
        
        # Enumerate the pips and paste the respective image to our pip image.
        for pip in enumerate( pip_list ):
            pip_image.paste( pip[1], ( pip[0] * 221, 0 ), pip[1] )
            
        # Save a temporary image... Test to see if this is necessary or if we can just return the image directly.
        pip_image.save(local_path('src\\temp_pips.png'))
        
        # Return the composited pip image.
        return pip_image
        
        
    def generate_rules_text( self ):
        """ 
            This function generates an image containing the rules text for this card. 
            Do not call this function directly. It's merely a helper for 'CardEntry.generate_image'
        """
        rules_font = ImageFont.truetype( local_path( "src\\OptimusPrinceps.ttf" ), 200 )
        img = Image.new("RGBA", (3025,4075), (0,0,0,0) )
        draw = ImageDraw.Draw( img )
        wrap = textwrap.TextWrapper( width = 26, replace_whitespace = False )
        text = wrap.fill( str(self.rules) )
        draw.multiline_text( (0,0), text, font = rules_font, fill=(0,0,0) )
        return img
        
        
        
    def generate_image( self, preview = False ):
        """ This function generates the entire face image for this card. """
        global card_index
        print( "Generating Card Image... " )
        new_image = new_card_image()
        cw, ch = int( new_image.size[0] / 2 ), int( new_image.size[1] / 2 )
        
        # Generate the card name text and center it on top of the card.
        name = ImageDraw.Draw( new_image )        
        text_size = font.getsize(self.name.value.get())
        name.text( ( cw - (text_size[0] / 2), 100 ), self.name.value.get(), fill = "black", font = font )        
        
        # Generate the pip image
        pips = self.generate_pips()
        # Paste the pip image to the card face
        new_image.paste( pips, ( cw-int(pips.size[0]/2), 120 + text_size[1] ), pips )
        
        # Generate the rules text
        rules = self.generate_rules_text()
        rw, rh = int( rules.size[0] / 2 ), int( rules.size[1] / 2 )
        new_image.paste( rules, (cw-rw, 200 + text_size[1] + pips.size[1] ), rules )
        
        # Convert spaces in the card name to underscore:
        filename = self.name.value.get().replace(' ','_') + '.png'
        category = self.menu.value.get()
        
        
        if preview:
            # Show the card for debugging purposes.
            new_image.show()
        else:
            # Save the newly generated card to disk
            new_image.save( local_path( f"img\\{category}\\{filename}") )
        
        
        
        
        
    
    
    
if __name__ == "__main__":

    root = Tk()
    root.title( "Relic Card Entry Tool" )


    card = CardEntry( root )
    quit_button = Button( root, text = "Quit", command = lambda : root.destroy() )
    quit_button.grid( row = 28, column = 0, sticky='ew', padx=2,pady=2 )
    
    json_button = Button( root, text = "Generate JSON", command = lambda : print(card) )
    json_button.grid( row = 28, column = 1, sticky = 'ew', padx = 2, pady = 2 )
    
    preview_button = Button( root, text = "Preview", command = lambda : card.generate_image(True) )
    preview_button.grid( row = 28, column = 2, sticky = 'ew', padx = 2, pady = 2 )
    
    image_button = Button( root, text = "Generate Image", command = lambda : card.generate_image() )
    image_button.grid( row = 29, column = 0, columnspan = 3, sticky = 'ew', padx = 2, pady = 2 )
    
    root.mainloop()