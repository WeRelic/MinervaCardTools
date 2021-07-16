# minerva_tk_utils.py

from tkinter import Tk, Entry, Label, Button, StringVar, IntVar, OptionMenu, BooleanVar, Text


class Labeled:
    def __init__( self, root, label_text, row = 0, column = 0):
        self.label = Label( root, text = label_text )
        self.row = row
        self.column = column
        
        
    def grid( self, padx = 2, pady = 2, sticky = 'w' ):
        self.label.grid( row = self.row, column = self.column, padx = padx, pady = pady, sticky = sticky )

    def grid_forget( self ):
        self.label.grid_forget()
        
        
        

class LabeledOptions( Labeled ):
    def __init__( self, root, label_text, row = 0, column = 0, options = [] ):
        super().__init__( root, label_text, row, column )
        self.opts = options
        self.value = StringVar(root)
        self.value.set(options[0])
        self.menu = OptionMenu( root, self.value, *options )        
    
    def grid( self, padx = 2, pady = 2, sticky = 'w' ):
        super().grid( padx, pady, sticky )
        self.menu.grid( row = self.row, column = self.column + 1, padx = padx, pady = pady, sticky = 'ew' )
    
    def grid_forget( self ):
        super().grid_forget()
        self.menu.grid_forget()
        
    def lift( self ):
        self.menu.lift()
        
    
class LabeledEntry( Labeled ):
    def __init__( self, root, label_text, row = 0, column = 0, is_int = False ):
        super().__init__( root, label_text, row, column )
        self.value = IntVar(root) if is_int else StringVar( root )
        self.entry = Entry( root, textvariable = self.value )
        
    def __str__( self ):
        return f"{self.value.get()}"
        
    def grid( self, padx = 2, pady = 2, sticky = 'w' ):    
        super().grid( padx, pady, sticky )
        self.entry.grid( row = self.row, column = self.column+1, columnspan = 2, sticky='ew', padx = 2, pady = 2 )
        
    def grid_forget(self):
        super().grid_forget()
        self.entry.grid_forget()
        
    def lift( self ):
        self.entry.lift()
        
        
        
        
          
class LabeledText( Labeled ):
    def __init__( self, root, label_text, row = 0, column = 0 ):
        super().__init__( root, label_text, row, column )
        self.entry = Text( root, height = 20, width = 48 )
        
    def __str__( self ):
        return self.entry.get("1.0","end")
        
    def grid( self, padx = 2, pady = 2, sticky = 'w' ): 
        super().grid( padx, pady, sticky )
        self.entry.grid( row = self.row+1, column = self.column, columnspan = 3, padx = 2, pady = 2, sticky = 'ew' )
                
    def grid_forget( self ):
        super().grid_forget()
        self.entry.grid_forget()
        
    def lift(self):
        self.entry.lift()