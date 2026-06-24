import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image, ImageOps, ImageTk, ImageFilter
# from img_treatment import creation_d_image
# from circle_flatter import aplanir
# from clarity import lisible

root = ctk.CTk() # Main window in tkinter (like a big box)
root.geometry("750x450") # Size of the window
root.title("Serial Number Reader") # Title of the window
root.resizable(False, False)

chemin_fichier = '' # Path to the image

est_nette = True
est_circulaire = False
image = ''

def upload_image():
    """ Fonction pour obtenir l'image et la mettre dans le canva """
    global chemin_fichier
    chemin_fichier = filedialog.askopenfilename(initialdir="img_traitee") # To open the directory to search the image

    image = Image.open(chemin_fichier) # To open the image
    width, height = int(image.width), int(image.height)
    if width < 550 or height < 250 :
        pass
    elif width >= 550 or height >= 250 :
        width, height = int(image.width/2), int(image.height/2) # To resize image to make it file the canvas et not overflow it
    elif width >= 1050 or height >= 750 :
        width, height = int(image.width/4), int(image.height/4) # To resize image to make it file the canvas et not overflow it
    elif width >= 1550 or height >= 1250 :
        width, height = int(image.width/6), int(image.height/6) # To resize image to make it file the canvas et not overflow it
    elif width >= 2050 or height >= 1750 :
        width, height = int(image.width/8), int(image.height/8) # To resize image to make it file the canvas et not overflow it
    else :
        width, height = int(image.width/16), int(image.height/16) # To resize image to make it file the canvas et not overflow it
    image = image.resize((width, height), Image.Resampling.LANCZOS) # Resize the image
    canvas.config(width=image.width, height=image.height) # Adapt the size of the canvas to image size

    global image_tk
    image_tk = ImageTk.PhotoImage(image) # To make a sutaible image for tkinter
    canvas.image = image_tk # set to canvas
    canvas.create_image(0, 0, image=image_tk, anchor="nw") # coordinates of canvas to put img in the center
    print("1")
    global est_nette
    est_nette = lisible(chemin_fichier)
    if est_nette == True :
        est_circulaire = pop_up()
        if est_circulaire :
            print("Redressment en cours")
            image_redressee = redressement(est_circulaire, chemin_fichier)
            print("Fin du redressement")
            print("création du jeu d'image")
            creation_d_image(image_redressee)
            print("Jeu d'image crée")
            print("2")
        else:
            creation_d_image(chemin_fichier)
            print("3")
    else :
        popup_bool = ctk.CTkToplevel(root)
        popup_bool.title('Serial Number Reader') # Titre de la fenêtre
        popup_bool.geometry("350x150") # Taille de la fenêtre
        popup_bool.resizable(False, False) # Ne peux pas être redimensionner
        popup_bool.grab_set() # On ne peux plus cliquer derrière la fenêtre

        label = ctk.CTkLabel(popup_bool, text="L'image n'est pas nette,", font=ctk.CTkFont(size=16, weight="bold"))
        label2 = ctk.CTkLabel(popup_bool, text="veuillez changer d'image", font=ctk.CTkFont(size=16, weight="bold"))
        label.pack(pady=(20,0))
        label2.pack(pady=(0,20))
        print("4")



def pop_up():
    popup_bool = ctk.CTkToplevel(root)
    popup_bool.title('Serial Number Reader') # Titre de la fenêtre
    popup_bool.geometry("350x150") # Taille de la fenêtre
    popup_bool.resizable(False, False) # Ne peux pas être redimensionner
    popup_bool.grab_set() # On ne peux plus cliquer derrière la fenêtre
    print("5")

    def clic_oui():
        global est_circulaire # Permet de modifier le variable
        est_circulaire = True
        popup_bool.destroy()
        print("6")

    def clic_non():
        global est_circulaire
        est_circulaire = False
        popup_bool.destroy()
        print("7")

    popup_bool.protocol("WM_DELETE_WINDOW", clic_non) # Sécurité, si on clique sur la croix rouge alors c'est condidéré comme False

    label = ctk.CTkLabel(popup_bool, text="Le texte est il circulaire ?", font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(pady=(20,20))

    btn_oui = ctk.CTkButton(popup_bool, text="Oui", command=clic_oui)
    btn_oui.pack(side="left", padx=20, pady=10, expand=True)

    btn_non = ctk.CTkButton(popup_bool, text="Non", command=clic_non)
    btn_non.pack(side="right", padx=20, pady=10, expand=True)

    popup_bool.wait_window()
    return est_circulaire

def redressement(booleen, chemin):
    """ Fonction qui redresse l'image circulaire """
    if booleen == True :
        return aplanir(chemin)
    else :
        print('False')

def OCR_image():
    """ Fonction qui appelle l'OCR et renvoie le texte lu par celui-ci """
    pass

title_label = ctk.CTkLabel(root, text='Serial Number Reader', font=ctk.CTkFont(size=30, weight="bold")) # To create a title label inside the window
title_label.pack(padx = 0, pady=(40,20)) # To position the title lable in the window / padx = pading on the x axe pady = padding on the y axe / pady=(40,20) => 40 on top, 20 on bottom

upload_button = ctk.CTkButton(root, text="Upload Image", width=500, command=upload_image, bg_color='white') # To create a button to upload image
upload_button.pack(pady = 20)

canvas = ctk.CTkCanvas(root, width=350, height=210)
canvas.pack()


root.mainloop() # loop to make the interface