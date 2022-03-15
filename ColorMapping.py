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
        
        mainLayout = cmds.columnLayout()

        #---------------------------------------------------------------------
               
        slidersLayout = cmds.frameLayout('Color Sliders:', collapsable = True)
        cmds.separator(w=300, style='in')    
        
        rowLayoutUI = cmds.rowLayout( bgc=(1,0,0), nc=3)
        
        
        leftColumn = cmds.columnLayout( bgc=(0,0,1))
                
        

        #SLIDERS INDEX SLIDER
        self.widgets['slider'] = cmds.colorIndexSliderGrp (
            label= 'Color Index:',
            min=0,
            max=31,
            value=0,
            cw3 = (65, 30, 130),
            enable = True,
            
        )

        
        cmds.text(l='')
        cmds.text(l='')

        
        #SLIDERS RGB SLIDER
        
        self.widgets['slider'] = cmds.colorSliderGrp (
            label= 'RGB Color:',
            rgb = (0,0,0),
            cw3 = (65, 30, 130),
            enable = True,
            
        ) 
        
        
        cmds.setParent('..')
        middleColumn = cmds.columnLayout(bgc=(0,0,0), cal='right') 

        indexApplyButton = cmds.button(l="Apply", h=20, w=50)
        cmds.text(l='')
        
        cmds.separator(w=10, style='in')
        
        cmds.button(l="Apply", h=20, w=50)     

        cmds.button(l="Save", h=20, w=50)     
        
        
        cmds.setParent('..')
        cmds.setParent(mainLayout)

        #---------------------------------------------------------------------

        buttonsFrameLayout = cmds.frameLayout('Index Colors:', collapsable = True)
        cmds.separator(w=300, style='in')  


        #BUTTONS
        #creamos los botones usando la ColorMapping class que teníamos de antes,
        # le pasamos una variable self llamada self.colors al init de myWindow
        #que ejecute ColorMapping, en concreto el method get all color names, que ya nos los da ordenados
        #la función la metemos fuera del create, va aparte.

        self.widgets['shelfLayout_buttons'] = cmds.shelfLayout(
            spacing=1,
            height = 160,
        )
        #Populate buttons function at the end of Create function
        self.populate_buttons()

        




        #---------------------------------------------------------------------
        
        cmds.setParent(mainLayout)        
              
        customFrameLayout = cmds.frameLayout('Custom Colors:', collapsable = True)
        cmds.separator(w=300, style='in')
        cmds.setParent('..')        
        
        
        
        
        
        
        
        
        #FIN DE LOS UI ELEMENTS

        cmds.showWindow(self.widgets['mainWindow'])






    def on_button_press(self, buttonIndex, buttonColor, *args, **kwargs):

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
                command = partial(self.on_button_press, index, colorOutliner)
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





