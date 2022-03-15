#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Aitana Belda VF013 Scripts II

import maya.cmds as cmds
from functools import partial


#DICTIONARY
class ColorMapping(dict):
    def __init__(self):
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


#creamos methods para recoger los diferentes valores del diccionario
    def get_rgb_from_name(self, name):
        return self['data'][name][1]

    def get_index_from_name(self, name):
        return self['data'][name][0]

    def get_rgb_from_index(self, index):
        for c, data in self['data'].items():
            if data[0] == index:
                return data[1]

    def get_color_from_index(self, index):
        for c, data in self ['data'].items():
            if data[0]== index:
                return c

#estamos usando el primer item del diccionario (el index) en el lambda para ordenar la lista que devuelva el method
#lambda va con el sorted, es una manera entre otras de ordenar
    def get_all_color_names(self):
        return [
        k
        for k,v in sorted(self['data'].items(),
        key=lambda item: item[1] )
        ]

#INTERFACES are the perfect place to use classes, empezamos definiendo la class de la ventana para el colormapper





class MyWindow:
    def __init__(self):
        self.window_title = 'Color Control'
        self.window_id = 'colorControlUI'
        self.colors = ColorMapping()

        #creamos el dict donde ir metiendo todos los elementos de la ui

        self.widgets = dict()

        #este create lo usamos para ejecutar el method que viene ahora, como __init__ se ejecuta siempre este también se ejecutará siempre
        self.create()

    
    
    #WINDOW FUNCTIONS

    def getIndexColor_VIEWPORT(self, slider, *args):
        '''This function gets the slider value of the Index color and passes 
        it onto setIndexColor() function.
        @slider(str): String with the full name of the Index Color slider.
        '''
        
        value = cmds.colorIndexSliderGrp(slider, query=True, value=True)
        value = value - 1
        self.setIndexColor_VIEWPORT(value)
        
        
    def getIndexColor_OUTLINER(self, slider, *args):
        '''This function gets the slider value of the Index color and passes 
        it onto setIndexColor() function.
        @slider(str): String with the full name of the Index Color slider.
        '''
        
        value = cmds.colorIndexSliderGrp(self.widgets['indexSlider'], query=True, value=True)
        value = value - 1
        self.setIndexColor_OUTLINER(value)
    
    
    def getIndexColor_SINGLEPRESS(self, slider, *args):
        self.getIndexColor_VIEWPORT(slider)
        self.getIndexColor_OUTLINER(slider)
    
    
    
    
    
    def setIndexColor_VIEWPORT(self, shpColor):
        '''Sets the color of a shape using Maya's Index colors.
        @shpColor(int): Index number of the color we want to set.
        '''
        
        # Save the selection
        selection = cmds.ls(sl=True) 
        i = 0

    
        # CHANGE SHAPE COLOR
        for obj in selection:
            # Verify and save the shapes in a list
            if cmds.nodeType(selection[i]) == "transform":
                shapeList = cmds.listRelatives(selection[i], c=1, s=1, f=1)
            else:
                shapeList.append(selection[i])
            # Change the selected shapes colors
            for shape in shapeList:
                cmds.setAttr("{}.overrideEnabled".format(shape), True)
                cmds.setAttr("{}.overrideRGBColors".format(shape), False)
                cmds.setAttr("{}.overrideColor".format(shape), shpColor)
            i = i+1
        
        
        
        
        
    def setIndexColor_OUTLINER(self, shpColor):
        '''Sets the color of a shape using Maya's Index colors.
        @shpColor(int): Index number of the color we want to set.
        '''
    
        # Save the selection
        selection = cmds.ls(sl=True)
        
        index = cmds.colorIndexSliderGrp(self.widgets['indexSlider'], query=True, value=True) -1
        colorOutliner = self.colors.get_rgb_from_index(index)
        
        print(colorOutliner)
             

        for s in selection:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), colorOutliner[0], colorOutliner[1], colorOutliner[2])    
    
    
    
    
    
    
    
    
    def getRGBColor_VIEWPORT(self, slider, *args):
        '''This function gets the slider value of the RGB color and passes it 
        onto setIndexColor() function.
        @slider(str): String with the full name of the RGB Color slider.
        '''
        
        value = cmds.colorSliderGrp(self.widgets['rgbSlider'], query=True, rgb=True)
        print(value)
        self.setRGBColor_VIEWPORT(value)


 
    def getRGBColor_OUTLINER(self, slider, *args):
        '''This function gets the slider value of the RGB color and passes it 
        onto setIndexColor() function.
        @slider(str): String with the full name of the RGB Color slider.
        '''
        
        value = cmds.colorSliderGrp(self.widgets['rgbSlider'], query=True, rgb=True)
        print(value)
        self.setRGBColor_OUTLINER(value)


    def getRGBColor_SINGLEPRESS(self, slider, *args):
        self.getRGBColor_VIEWPORT (slider)
        self.getRGBColor_OUTLINER (slider)
   
   
   
    
    
            
            
    

    
    
    
    
    
    
    def setRGBColor_VIEWPORT(self, shpColor, *args):
        '''Sets the color of a shape using RGB colors.
        @shpColor(list): List with the 3 RGB values of the color we want 
                         to set.
        '''
        
        # Save the selection
        selection = cmds.ls(sl=True) 
        i = 0
    
        # CHANGE SHAPE COLOR
        for obj in selection:
            # Verify and save the shapes in a list
            if cmds.nodeType(selection[i]) == "transform":
                shapeList = cmds.listRelatives(selection[i], c=1, s=1, f=1)
            else:
                shapeList.append(selection[i])
            # Change the selected shapes colors
            for shape in shapeList:
                cmds.setAttr("{}.overrideEnabled".format(shape), True)
                cmds.setAttr("{}.overrideRGBColors".format(shape), True)
                cmds.setAttr("{}.overrideColorR".format(shape), shpColor[0])
                cmds.setAttr("{}.overrideColorG".format(shape), shpColor[1])
                cmds.setAttr("{}.overrideColorB".format(shape), shpColor[2])
            i = i + 1
            
    
    def setRGBColor_OUTLINER(self, shpColor, *args):
        '''Sets the color of a shape using RGB colors.
        @shpColor(list): List with the 3 RGB values of the color we want 
                         to set.
        '''
        

        selection = cmds.ls(sl=True)
        
        rgbColor = cmds.colorSliderGrp(self.widgets['rgbSlider'], query=True, rgb=True) 
                     

        for s in selection:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), rgbColor[0], rgbColor[1], rgbColor[2])
    
    
    

    def setCustomColor_OUTLINER(self, value, *args):
        selection = cmds.ls(sl=True)                     

        for s in selection:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), value[0], value[1], value[2])
            
    def setCustomColor_VIEWPORT(self, value, *args):
        selection = cmds.ls(sl=True) 
        i = 0
    
        # CHANGE SHAPE COLOR
        for obj in selection:
            # Verify and save the shapes in a list
            if cmds.nodeType(selection[i]) == "transform":
                shapeList = cmds.listRelatives(selection[i], c=1, s=1, f=1)
            else:
                shapeList.append(selection[i])
            # Change the selected shapes colors
            for shape in shapeList:
                cmds.setAttr("{}.overrideEnabled".format(shape), True)
                cmds.setAttr("{}.overrideRGBColors".format(shape), True)
                cmds.setAttr("{}.overrideColorR".format(shape), value[0])
                cmds.setAttr("{}.overrideColorG".format(shape), value[1])
                cmds.setAttr("{}.overrideColorB".format(shape), value[2])
            i = i + 1        

    def setCustomColor_SINGLEPRESS(self, value, *args):
        self.setCustomColor_OUTLINER(value)
        self.setCustomColor_VIEWPORT(value)
    
    
    
    
    
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
        customColLay = cmds.rowLayout(nc=2, cw2=(20, 600), cal=(2, "left"), 
                    parent=ml)
        cmds.text(l="", al=("left"))
        savedClrsLayout = cmds.rowLayout(nc=3, cw=(23, 23), cal=(2, "right"))
        colorButton = cmds.button(l="", h=20, w=100, bgc=value)
        self.widgets['customColorApplyButton'] = cmds.button(l="Apply", h=20, w=50, 
                   
                   
                   c=partial(self.setCustomColor_SINGLEPRESS, value))
       
       
        cmds.popupMenu(p=self.widgets['customColorApplyButton'] )

        cmds.menuItem(label= 'Apply only to SHAPE',
                      command = partial(self.setCustomColor_VIEWPORT, value) )
       
            
        cmds.menuItem(label= 'Apply only to OUTLINER',
                      command = partial(self.setCustomColor_OUTLINER, value) )
                      
                      
        colorButton = cmds.button(l="Delete", h=20, w=50, 
                                  c=partial(self.delCustomColor, customColLay))


    
    def delCustomColor(self, colBtn, *args):
        '''This function deletes the saved custom color.
        @colBtn(str): String with the full name of the button we want to 
                      delete.
        '''
        
        self = cmds.deleteUI(colBtn)



    def printie(self, *args):
        print:'ayuda'
    #este method es para el lio de crear y borrar la ventana cada vez
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

        #entre aquí y el show window metemos todos los elementos de la ui
        
        #---------------------------------------------------------------------
        #---------------------------------------------------------------------

        
        self.widgets['mainLayout'] = cmds.columnLayout()

        
        #---------------------------------------------------------------------
        #---------------------------------------------------------------------
       
        slidersLayout = cmds.frameLayout('Color Sliders:', collapsable = True)
        cmds.separator(w=300, style='in')    
        
        
        #----------
        rowLayoutUI = cmds.rowLayout(nc=3)
        
        
        #
        leftColumn = cmds.columnLayout()
                
        

        #SLIDERS INDEX SLIDER
       
        self.widgets['indexSlider'] = cmds.colorIndexSliderGrp (
            label= 'Index:',
            min=1,
            max=31,
            value=1,
            cw3 = (35, 30, 160),
            enable = True,
            
        )

        
        cmds.text(l='')
        cmds.separator(w=225, style='in')
        
        cmds.text(l='')


        #SLIDERS RGB SLIDER
        
        self.widgets['rgbSlider'] = cmds.colorSliderGrp (
            label= 'RGB:',
            rgb = (0,0,0),
            cw3 = (35, 30, 160),
            enable = True,
            
        ) 
        
        
        cmds.setParent('..')
        
        
        #
        middleColumn = cmds.columnLayout() 

        self.widgets['indexApplyButton'] = cmds.button(l="Apply", 
                                                       h=20, 
                                                       w=50, 
                                                       c=partial(self.getIndexColor_SINGLEPRESS, self.widgets['indexSlider']) )
        
        
        cmds.popupMenu(p=self.widgets['indexApplyButton'])
        cmds.menuItem(
                label= 'Apply only to SHAPE',
                command = partial(self.getIndexColor_VIEWPORT, self.widgets['indexSlider'] ) )
            
        cmds.menuItem(
                label= 'Apply only to OUTLINER',
                command = partial(self.getIndexColor_OUTLINER, self.widgets['indexSlider']) )        
        
        
        
        
        
        
        
        cmds.text(l='')
                
        
        
        
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
        
        self.widgets['rgbSaveButton'] = cmds.button(l="Save", 
                                                    h=20, 
                                                    w=50,
                                                    )     
        
        cmds.setParent('..')
        cmds.setParent(self.widgets['mainLayout'])

        
        #---------------------------------------------------------------------
        #---------------------------------------------------------------------


        self.widgets['buttonsFrameLayout'] = cmds.frameLayout('Index Picker:', collapsable = True)

        cmds.separator(w=300, style='in')  


        #BUTTONS
        #creamos los botones usando la ColorMapping class que teníamos de antes,
        # le pasamos una variable self llamada self.colors al init de myWindow
        #que ejecute ColorMapping, en concreto el method get all color names, que ya nos los da ordenados
        #la función la metemos fuera del create, va aparte.

        self.widgets['shelfLayout_buttons'] = cmds.shelfLayout(
            spacing=1,
            height = 150,
        )
        #Populate buttons function at the end of Create function
        self.populate_buttons()
        
        cmds.setParent('..')
        cmds.text(l='Rclic for options')


        #---------------------------------------------------------------------
        #---------------------------------------------------------------------

        cmds.setParent(self.widgets['mainLayout'])        
              
        self.widgets['customFrameLayout'] = cmds.frameLayout('Custom Library:', collapsable = True)
        cmds.separator(w=300, style='in')
        
        self.widgets['customColumnLayout'] = cmds.columnLayout()
        

        cmds.button (self.widgets['rgbSaveButton'],
                                                    e=True, 
                                                    c=partial(self.saveColor, 
                                                              self.widgets['customColumnLayout'], 
                                                              self.widgets['rgbSlider']))
        
           
        
        cmds.setParent('..')        
        
                
        

        #FIN DE LOS UI ELEMENTS

        cmds.showWindow(self.widgets['mainWindow'])






    def on_button_press_SHELF(self, buttonIndex, buttonColor, *args, **kwargs):

        selectedControls = cmds.ls(sl=True)

        for s in selectedControls:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), buttonColor[0], buttonColor[1], buttonColor[2])

            cmds.setAttr('{}.overrideEnabled'.format(s), True)
            cmds.setAttr('{}.overrideColor'.format(s), buttonIndex)

        




    def on_rClic_SHAPE_press(self, buttonIndex, *args, **kwargs):

        selectedControls = cmds.ls(sl=True)

        for s in selectedControls:
            cmds.setAttr('{}.overrideEnabled'.format(s), True)
            cmds.setAttr('{}.overrideColor'.format(s), buttonIndex)


    def on_rClic_OUTLINER_press(self, buttonColor, *args, **kwargs):

        selectedControls = cmds.ls(sl=True)

        for s in selectedControls:
            cmds.setAttr('{}.useOutlinerColor'.format(s), True)
            cmds.setAttr('{}.outlinerColor'.format(s), buttonColor[0], buttonColor[1], buttonColor[2])



    def populate_buttons(self):
        #los diccionarios no tienen orden de entradas, así que para que salgan los
        #botones en orden usamos el lambda el el ColorMapping(get_all_color_names)
        for colorName in self.colors.get_all_color_names():
            index = self.colors.get_index_from_name(colorName)
            colorOutliner = self.colors.get_rgb_from_index(index)
            cmds.button(
                l= ' ',
                bgc = self.colors.get_rgb_from_index(index),
                h=35,
                w=35,


                #BUTTON PRESS
                command = partial(self.on_button_press_SHELF, index, colorOutliner)
            )
            cmds.popupMenu()
            cmds.menuItem(
                label= 'Apply only to SHAPE',
                command = partial(self.on_rClic_SHAPE_press, index)
            )
            cmds.menuItem(
                label= 'Apply only to OUTLINER',
                command = partial(self.on_rClic_OUTLINER_press, colorOutliner)
            )


windowcm = MyWindow()





