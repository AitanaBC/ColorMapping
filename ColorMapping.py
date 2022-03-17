#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Aitana Belda VF013 Scripts II


#------------------------------ EX 01 ---------------------------------#
#                                                                      #
#                           COLOR MAPPING                              #
#                                                                      #
#----------------------------------------------------------------------#

import maya.cmds as cmds
from functools import partial


#----------------------------------------------------------------------#
#                         DICTIONARY CLASS                             #   
#----------------------------------------------------------------------#

class ColorMapping(dict):
    def __init__(self):
        
        #Color data
        
        self['data'] = {
            'gray':[0,(0.4,0.4,0.4)],
            'black':[1,(0,0,0)],
            'darkGray':[2,(.35,.35,.35)],
            'lightGray':[3,(.43,.43,.43)],
            'burgundy':[4,(.54,0,.11)],
            'darkBlue':[5,(0,0,.31)],
            'blue':[6,(0,0,1)],
            'darkGreen':[7,(0,.22,0.07)],
            'purple':[8,(.11,0,.2)],
            'pink':[9,(.74,0,.75)],
            'midBrown':[10,(.47,.22,.15)],
            'darkBrown':[11,(.19,.1,.09)],
            'rust':[12,(.53,.09,0)],
            'red':[13,(1,0,0)],
            'green':[14,(0,1,0)],
            'cobalt':[15,(0,.16,.54)], 
            'white':[16,(1,1,1)],
            'yellow':[17,(1,1,0)],
            'turquoise':[18,(.31,.83,1)],
            'springGreen':[19,(.18,1,.56)],
            'lightPink':[20,(1,.62,.62)],
            'sandyBrown':[21,(.87,.62,.39)],
            'paleYellow':[22,(1,1,.27)],
            'jade':[23,(0,.55,.25)],
            'lightbrown':[24,(.56,.34,.13)],
            'olive':[25,(.56,.58,.11)],
            'appleGreen':[26,(.33,.58,.12)],
            'seaGreen':[27,(.13,.58,.29)],
            'teal':[28,(.13,.57,.56)],
            'cerulean':[29,(.14,.32,.57)],
            'darkViolet':[30,(.36,.07,.57)],
            'eggPlant':[31,(.57,.11,.34)]
            }


    #Defining methods to collect all necessary data
    #from the dictionary
    
    #Get data from NAME
    def get_rgb_from_name(self, name):
        return self['data'][name][1]

    def get_index_from_name(self, name):
        return self['data'][name][0]
    
    def get_all_color_names(self):
        return [
        k
        for k,v in sorted(self['data'].items(),
        #data sorted by index
        key=lambda item: item[1] )
        ]    
    
    
    #Get data from INDEX
    def get_rgb_from_index(self, index):
        for c, data in self['data'].items():
            if data[0] == index:
                return data[1]

    def get_color_from_index(self, index):
        for c, data in self ['data'].items():
            if data[0]== index:
                return c




#----------------------------------------------------------------------#
#                             UI CLASS                                 #   
#----------------------------------------------------------------------#


class ColorMappingWindow:
    
    def __init__(self):
        self.window_title = 'Color Control'
        self.window_id = 'colorControlUI'
        self.colors = ColorMapping()


        #Dict containing all UI widgets
        self.widgets = dict()

        #Create the window via the create method below.
        self.create()

    
    
    
    #WINDOW FUNCTIONS
    
    #Used to get all data from diferent widgets and send it to other functions.
    
    
    #INDEX SLIDER
    #----------------------------------------------------------------------#
    #----------------------------------------------------------------------#
    
    
    #GETTING the color value and sending it to their respective functions.
    
    def getIndexColor_VIEWPORT(self, slider, *args):
        '''
        This function gets the slider value of the INDEX slider and passes 
        it onto setIndexColor_VIEWPORT() function.
        It changes the SHAPE'S color, but not the outliner's.
        Used for the ONLY VIEWPORT option in the pop-up menu.
        @slider(str): String with the full name of the RGB Color slider.

        '''
        
        value = cmds.colorIndexSliderGrp(slider, query=True, value=True)
        value = value - 1
        self.setIndexColor_VIEWPORT(value)
        
        
    def getIndexColor_OUTLINER(self, slider, *args):
        '''This function gets the slider value of the INDEX slider and passes 
        it onto setIndexColor_OUTLINER() function.
        It changes the OUTLINER'S color, but not the shape's.
        Used for the ONLY OUTLINER option in the pop-up menu.
        @slider(str): String with the full name of the RGB Color slider.

        '''
        
        value = cmds.colorIndexSliderGrp(slider, query=True, value=True)
        value = value - 1
        self.setIndexColor_OUTLINER(value)
    

    #Apply Button colors both the outliner name and viewport shape.    
    def getIndexColor_SINGLEPRESS(self, slider, *args):
        '''
        On APPLY button press, executes both functions to apply the chosen  
        color to both OUTLINER and SHAPE.
        @slider(str): String with the full name of the RGB Color slider.
        '''
        self.getIndexColor_VIEWPORT(slider)
        self.getIndexColor_OUTLINER(slider)
    
    
    
    
    
    #SETTING the color value for each option, outliner and shape.
      
    def setIndexColor_VIEWPORT(self, shpColor):
        '''Sets the color of a shape using Maya's Index colors.
        Applies the color only to the SHAPE.
        @shpColor(int): Index number of the color we want to set.
        '''
        
        #Save the selection
        selection = cmds.ls(sl=True) 
        i = 0

        # CHANGE SHAPE COLOR
        for shape in selection:
            cmds.setAttr("{}.overrideEnabled".format(shape), True)
            cmds.setAttr("{}.overrideRGBColors".format(shape), False)
            cmds.setAttr("{}.overrideColor".format(shape), shpColor)
            i = i+1

        print ('Index Color ({}) set to SHAPE'.format(shpColor))
        
        
        
        
        
    def setIndexColor_OUTLINER(self, shpColor):
        '''Sets the color of a shape using Maya's Index colors.
        Applies the color only to the OUTLINER.
        @shpColor(int): Index number of the color we want to set.
        '''
    
        # Save the selection
        selection = cmds.ls(sl=True)
        
        #Get the RGB values from the color dictionary
        index = cmds.colorIndexSliderGrp(self.widgets['indexSlider'], query=True, value=True) -1
        colorOutliner = self.colors.get_rgb_from_index(index)             

        for s in selection:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), colorOutliner[0], colorOutliner[1], colorOutliner[2])    
        
        print ('Index Color ({}) set to OUTLINER'.format(colorOutliner) )
    
    
    
    
    #RGB SLIDER
    #----------------------------------------------------------------------#
    #----------------------------------------------------------------------#
    
    
    
    #GETTING the color value and sending it to their respective functions.
    
    def getRGBColor_VIEWPORT(self, slider, *args):
        '''This function gets the slider value of the RGB color and passes it 
        onto setRGBColor_VIEWPORT() function.
        @slider(str): String with the full name of the RGB Color slider.
        '''
        
        value = cmds.colorSliderGrp(self.widgets['rgbSlider'], query=True, rgb=True)
        print(value)
        self.setRGBColor_VIEWPORT(value)


 
    def getRGBColor_OUTLINER(self, slider, *args):
        '''This function gets the slider value of the RGB color and passes it 
        onto setRGBColor_OUTLINER() function.
        @slider(str): String with the full name of the RGB Color slider.
        '''
        
        value = cmds.colorSliderGrp(self.widgets['rgbSlider'], query=True, rgb=True)
        print(value)
        self.setRGBColor_OUTLINER(value)


    #Apply Button colors both the outliner name and viewport shape.    
    def getRGBColor_SINGLEPRESS(self, slider, *args):
        '''
        On APPLY button press, executes both functions to apply the chosen  
        color to both OUTLINER and SHAPE.
        @slider(str): String with the full name of the RGB Color slider.
        '''
        self.getRGBColor_VIEWPORT (slider)
        self.getRGBColor_OUTLINER (slider)
   
    
    
    
    #SETTING the color value for each option, outliner and shape.
    
    def setRGBColor_VIEWPORT(self, shpColor, *args):
        '''Sets the color of a SHAPE using RGB colors.
        Only applies to VIEWPORT.
        @shpColor(list): List with the 3 RGB values of the color we want to set.
        '''
        
        # Save the selection
        selection = cmds.ls(sl=True) 

        # Change the selected shapes colors
        for shape in selection:
            cmds.setAttr("{}.overrideEnabled".format(shape), True)
            cmds.setAttr("{}.overrideRGBColors".format(shape), True)
            cmds.setAttr("{}.overrideColorR".format(shape), shpColor[0])
            cmds.setAttr("{}.overrideColorG".format(shape), shpColor[1])
            cmds.setAttr("{}.overrideColorB".format(shape), shpColor[2])
      
        print ('RGB Color ({}) set to SHAPE'.format(shpColor) )
            
    
   
   
    def setRGBColor_OUTLINER(self, *args):
        '''Sets the color of a shape using RGB colors.
        Only applies to OUTLINER.
        '''
        
        selection = cmds.ls(sl=True)
       
        rgbColor = cmds.colorSliderGrp(self.widgets['rgbSlider'], query=True, rgb=True) 
                     

        for s in selection:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), rgbColor[0], rgbColor[1], rgbColor[2])
    
        print ('RGB Color ({}) set to OUTLINER '.format(rgbColor) )


    



    #CUSTOM LIBRARY APPLY
    #----------------------------------------------------------------------#
    #----------------------------------------------------------------------#
    
    #Sets a saved custom color to the OUTLINER.
    
    def setCustomColor_OUTLINER(self, value, *args):
        '''
        This function sets the saved custom color to the OUTLINER
        @value = (int, int, int) RGB value of the custom color.
        '''
        selection = cmds.ls(sl=True)                     

        for s in selection:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), value[0], value[1], value[2])
            
    
    
    #Sets a saved custom color to the SHAPE.
    
    def setCustomColor_VIEWPORT(self, value, *args):
        selection = cmds.ls(sl=True) 
    
        for shape in selection:
            cmds.setAttr("{}.overrideEnabled".format(shape), True)
            cmds.setAttr("{}.overrideRGBColors".format(shape), True)
            cmds.setAttr("{}.overrideColorR".format(shape), value[0])
            cmds.setAttr("{}.overrideColorG".format(shape), value[1])
            cmds.setAttr("{}.overrideColorB".format(shape), value[2])
      

   
    #Sets the custom color to both the OUTLINER and SHAPE
       
    def setCustomColor_SINGLEPRESS(self, value, *args):
        self.setCustomColor_OUTLINER(value)
        self.setCustomColor_VIEWPORT(value)
    
    
    
    #SAVE CUSTOM COLOR TO THE CUSTOM LIBRARY
    #----------------------------------------------------------------------#
    #----------------------------------------------------------------------#
    
    
    def saveColor(self, ml, slider, *args):
        '''This function saves the current value of the RGB slider and creates 
        a new set of buttons to apply or delete it.
        @ml(str): String with the full name of the main layout to parent the 
                  custom color buttons.
        @slider(str): String with the full name of the RGB Color slider.
        '''
       
        # Get the slider's value         
        value = cmds.colorSliderGrp(slider, query=True, rgb=True)
       
        # Create the button set layout
        parent=ml 
        customColLay = cmds.rowLayout(nc=2, cw2=(20, 600), cal=(2, "left"),  parent=ml)
        cmds.text(l="", al=("left"))
        savedClrsLayout = cmds.rowLayout(nc=3, cw=(23, 23), cal=(2, "right"))
        colorButton = cmds.button(l="", h=20, w=100, bgc=value)
        
        #Create the APPLY button with the secondary button popupMenu, which contains
        #two menu items, for OUTLINER and SHAPE.
        self.widgets['customColorApplyButton'] = cmds.button(l="Apply", h=20, w=50, 
                                 c=partial(self.setCustomColor_SINGLEPRESS, value))
       
       
        cmds.popupMenu(p=self.widgets['customColorApplyButton'] )

        cmds.menuItem(label= 'Apply only to SHAPE',
                      command = partial(self.setCustomColor_VIEWPORT, value) )
       
            
        cmds.menuItem(label= 'Apply only to OUTLINER',
                      command = partial(self.setCustomColor_OUTLINER, value) )
                      
        #Delete button              
        colorButton = cmds.button(l="Delete", h=20, w=50, 
                                  c=partial(self.delCustomColor, customColLay))
        print ('Custom color ({}) successfully saved to Custom Library.'.format(value))


    #Delete button function which deletes the custom saved color.    
    def delCustomColor(self, colBtn, *args):
        '''This function deletes the saved custom color.
        @colBtn(str): String with the full name of the button we want to 
                      delete.
        '''
        self = cmds.deleteUI(colBtn)


    
    #UI CREATION AND MAIN LAYOUT
    #----------------------------------------------------------------------#
    #----------------------------------------------------------------------#


    #Window setup
    def create(self):
        if cmds.window(self.window_id, exists=True):
            cmds.deleteUI(self.window_id)

        self.widgets['mainWindow'] = cmds.window(
            self.window_id,
            title= self.window_title,
            sizeable = False,
            rtf = True,
            mnb = False,
            mxb = False,
            toolbox = True,
            widthHeight = (300,300)
        )

        #UI ELEMENTS
        
        #---------------------------------------------------------------------

        #Main Column layout
        self.widgets['mainLayout'] = cmds.columnLayout()
        cmds.text(l='                     - Right clic for setting options -')
        cmds.text(l='')
        
        #COLOR SLIDERS MENU
        #---------------------------------------------------------------------
       
        #Collapsable Sliders Frame Layout
        slidersLayout = cmds.frameLayout('Color Sliders:', collapsable = True)
        cmds.separator(w=300, style='in')    
        
        
       
        #---------------------------------------------------------------------
        
        rowLayoutUI = cmds.rowLayout(nc=3)

        #Column layout containing the sliders
        leftColumn = cmds.columnLayout()
                
        
        #INDEX Slider
        self.widgets['indexSlider'] = cmds.colorIndexSliderGrp (
            label= 'Index:',
            min=1,
            max=31,
            value=1,
            cw3 = (35, 30, 160),
            enable = True,      
            )

        
        #Misc separators
        cmds.text(l='')
        cmds.separator(w=225, style='in')
        cmds.text(l='')


        #RGB Slider
        self.widgets['rgbSlider'] = cmds.colorSliderGrp (
            label= 'RGB:',
            rgb = (0,0,0),
            cw3 = (35, 30, 160),
            enable = True,
            ) 
        

        #Back to the row Layout to create the second column containing the Buttons
        cmds.setParent('..')

        middleColumn = cmds.columnLayout() 

        #Index Slider Apply Button
        self.widgets['indexApplyButton'] = cmds.button(l="Apply", 
                                                       h=20, 
                                                       w=50, 
                                                       c=partial(self.getIndexColor_SINGLEPRESS, self.widgets['indexSlider']) )
        
        #Index Slider Apply Button sub-menu       
        cmds.popupMenu(p=self.widgets['indexApplyButton'])
        cmds.menuItem(
                label= 'Apply only to SHAPE',
                command = partial(self.getIndexColor_VIEWPORT, self.widgets['indexSlider'] ) )
            
        cmds.menuItem(
                label= 'Apply only to OUTLINER',
                command = partial(self.getIndexColor_OUTLINER, self.widgets['indexSlider']) )        
        
        
        
        #Misc separator
        cmds.text(l='')
                
        
        
        #RGB Slider Apply Button and its sub-menu       
        self.widgets['rgbApplyButton'] = cmds.button(l="Apply", 
                                                    h=20, 
                                                    w=50, 
                                                    c=partial(self.getRGBColor_SINGLEPRESS, self.widgets['rgbSlider']) )     

        
        cmds.popupMenu(p=self.widgets['rgbApplyButton'])
        cmds.menuItem(
                label= 'Apply only to SHAPE',
                command = partial(self.getRGBColor_VIEWPORT, self.widgets['rgbSlider']) )
            
        cmds.menuItem(
                label= 'Apply only to OUTLINER',
                command = partial(self.getRGBColor_OUTLINER, self.widgets['rgbSlider']) )
        
        
        
        
        
        #RGB Slider Save Button     
        self.widgets['rgbSaveButton'] = cmds.button(l="Save", 
                                                    h=20, 
                                                    w=50,
                                                    )     
        
        cmds.setParent('..')
        cmds.setParent(self.widgets['mainLayout'])

        

        #INDEX PICKER MENU
        #---------------------------------------------------------------------

        #Collapsable frame Layout 
        self.widgets['buttonsFrameLayout'] = cmds.frameLayout('Index Picker:', collapsable = True)
        cmds.separator(w=300, style='in')  


        #Shelf Layout which will contain the index buttons.
        self.widgets['shelfLayout_buttons'] = cmds.shelfLayout(
            spacing=1,
            height = 150,
            )
        
        #Populate buttons function to create the index buttons
        self.populate_buttons()
        
        cmds.setParent('..')

        cmds.setParent(self.widgets['mainLayout'])        



        #CUSTOM LIBRARY MENU
        #---------------------------------------------------------------------

        #Collapsable frame layout to collect the custom colors.     
        self.widgets['customFrameLayout'] = cmds.frameLayout('Custom Library:', collapsable = True)
        cmds.separator(w=300, style='in')
        
        
        #Third column Layout.
        self.widgets['customColumnLayout'] = cmds.columnLayout()
        

        #Save Button
        cmds.button (self.widgets['rgbSaveButton'],
                                                    e=True, 
                                                    c=partial(self.saveColor, 
                                                              self.widgets['customColumnLayout'], 
                                                              self.widgets['rgbSlider']))
        
           
        
        cmds.setParent('..')        
        
                
        

        #FIN DE LOS UI ELEMENTS
        #---------------------------------------------------------------------
        cmds.showWindow(self.widgets['mainWindow'])






    #COLOR INDEX PICKER FUNCTIONS
    #----------------------------------------------------------------------#
    #----------------------------------------------------------------------#

    #Left clic on the index picker buttons.
    def on_button_press_SHELF(self, buttonIndex, buttonColor, *args, **kwargs):
        '''
        This function sets the Index picker color to both the SHAPE and OUTLINER.
        '''

        selectedControls = cmds.ls(sl=True)

        for s in selectedControls:
            #Outliner
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), buttonColor[0], buttonColor[1], buttonColor[2])
            #Shape
            cmds.setAttr('{}.overrideEnabled'.format(s), True)
            cmds.setAttr("{}.overrideRGBColors".format(s), False)
            cmds.setAttr('{}.overrideColor'.format(s), buttonIndex)
        print('Set ({}) color to OUTLINER and SHAPE'.format(buttonColor))

        



    #Right clic on the index picker buttons.
    def on_rClic_SHAPE_press(self, buttonIndex, *args, **kwargs):
        '''
        This function sets the Index Picker color ONLY to the SHAPE.
        '''

        selectedControls = cmds.ls(sl=True)

        for s in selectedControls:
            cmds.setAttr('{}.overrideEnabled'.format(s), True)
            cmds.setAttr("{}.overrideRGBColors".format(s), False)
            cmds.setAttr('{}.overrideColor'.format(s), buttonIndex)
        
        print('Set ({}) color to SHAPE'.format(buttonIndex))



    def on_rClic_OUTLINER_press(self, buttonColor, *args, **kwargs):
        '''
        This function sets the Index Picker color ONLY to the OUTLINER.
        '''

        selectedControls = cmds.ls(sl=True)

        for s in selectedControls:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), buttonColor[0], buttonColor[1], buttonColor[2])
        
        print('Set ({}) color to OUTLINER'.format(buttonColor))




    #Creates the actual buttons with the ColorMapping dictionary 
    #and the getting its data functions.
    
    def populate_buttons(self):
        for colorName in self.colors.get_all_color_names():
            index = self.colors.get_index_from_name(colorName)
            colorOutliner = self.colors.get_rgb_from_index(index)
            cmds.button(
                l= ' ',
                bgc = self.colors.get_rgb_from_index(index),
                h=35,
                w=35,


                #Button command
                command = partial(self.on_button_press_SHELF, index, colorOutliner)
            )
            
            #sub-menu
            cmds.popupMenu()
            cmds.menuItem(
                label= 'Apply only to SHAPE',
                command = partial(self.on_rClic_SHAPE_press, index)
            )
            cmds.menuItem(
                label= 'Apply only to OUTLINER',
                command = partial(self.on_rClic_OUTLINER_press, colorOutliner)
            )


StartColorControl = ColorMappingWindow()

#End





