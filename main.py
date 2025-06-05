from num2words import num2words
import flet as ft
import asyncio
import os

class Parametre:
    def __init__(self,debut:int,fin:int,saut:int,sc:float):
        self.debut = debut
        self.fin = fin
        self.saut = saut
        self.sc =sc

class Application_compteur:
    def __init__(self,page:ft.Page):
        
        # proprietes de la page
        self.page = page
        self.page.title= "Simple Compteur"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER


        # HEADER
        # la barre de l'application
        self.page.appbar = ft.AppBar(
            title=ft.Text('Simple Compteur',color="white",weight="w600"),
            leading=ft.Icon(name=ft.Icons.COMPUTER,size=40,color="white"),
            bgcolor='blue',
            actions=[
                ft.IconButton(icon=ft.Icons.INFO_SHARP,icon_size=20,icon_color="white",on_click=self.about),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Toute lettre français", checked=False, on_click=self.check_item_clicked
                        ),
                        ft.PopupMenuItem(
                            text="Toute lettre Anglais", checked=False, on_click=self.check_item_clicked
                        ),
                    ],
                    icon_color='white'
                ),
            ]
        )

        # BODY
        self.compteur = ft.Text(value="0",size=100)
        self.compter_fr = ft.Text(size=30,color="blue",weight="bolod")
        self.compter_en = ft.Text(size=30,color="green",weight="bolod")

        # champs de saisies
        self.debut_compteur = ft.TextField(value="0",hint_text="debut",label="Sebut",expand=1,text_size=12,hint_style=ft.TextStyle(size=12),label_style=ft.TextStyle(size=12),on_blur=self.verifie_input)
        self.fin_compteur = ft.TextField(value="10",hint_text="fin",label="Fin",expand=1,text_size=12,hint_style=ft.TextStyle(size=12),label_style=ft.TextStyle(size=12),on_blur=self.verifie_input)
        self.saut_compteur = ft.TextField(value="1",hint_text="Sauter de",label="Saut",expand=1,text_size=12,hint_style=ft.TextStyle(size=12),label_style=ft.TextStyle(size=12),on_blur=self.verifie_input)
        self.second_to_sleep = ft.TextField(value="1",hint_text="seconde d'intervalle",label="Seconde",expand=1,text_size=12,hint_style=ft.TextStyle(size=12),label_style=ft.TextStyle(size=12),on_blur=self.verifie_input)

        # parametre data
        self.parametre = Parametre(
            debut = int(self.debut_compteur.value),
            fin = int(self.fin_compteur.value),
            saut = int(self.saut_compteur.value),
            sc = float(self.second_to_sleep.value)
        )

        # options
        self.incrementer_decrementer = ft.RadioGroup(content=ft.Column([
            ft.Radio(value="incrementer", label="Incrementer",label_style=ft.TextStyle(size=13,weight="w500")),
            ft.Radio(value="decrementer", label="Décrementer",label_style=ft.TextStyle(size=13,weight="w500")),
        ]),value="incrementer")

       # information user text
        self.info = ft.Text("",font_family="seoge ui",color='red')

        # fênetre modale pour les paramettres
        self.options = ft.AlertDialog(
            modal=True,
            title=ft.Text("Paramètres du compteur",size=14,weight='w500'),
            icon=ft.Icon(ft.Icons.MANAGE_SEARCH),
            content=ft.Column(
                [self.incrementer_decrementer,
                ft.Container(height=10),
                ft.Row([
                    self.debut_compteur,
                    self.fin_compteur,
                    self.saut_compteur,
                    self.second_to_sleep,
                ]),
                ft.Container(height=20),
                self.info
                ]
                
            ),
            actions=[
                ft.FilledButton(text="Commencer",bgcolor="blue",color="white",icon=ft.Icons.RUN_CIRCLE_SHARP, on_click=self.close),
                ft.FilledButton(text="Fermer",bgcolor="red",color="white",icon=ft.Icons.CLOSE,on_click=self.close_exit_dialog),
            ]
        )

        # buttons
        self.regrage_butons = ft.TextButton("Reglage Du Compteur",icon=ft.Icons.SETTINGS,icon_color="blue",on_click=lambda e:self.page.open(self.options))
        self.run = ft.IconButton(icon=ft.Icons.PLAY_ARROW_ROUNDED,icon_size=60, on_click=self.lancer)

        # toute lettre tableau de visualisation
        self.toute_lettre = ft.DataTable(
            columns=[
                ft.DataColumn(
                    label=ft.Text("Français"),
                    tooltip="Nombre en toute lettres"
                ),
                
                ft.DataColumn(
                    label=ft.Text("English"),
                    tooltip="All lettes of numbers"
                ),
               
                
            ],
            
            rows=[
                 ft.DataRow(
                    cells=[
                        ft.DataCell(
                            content=self.compter_fr
                        ),
                        
                        ft.DataCell(
                            content=self.compter_en,
                        ),
                    ]
                ),
            ],
            
        )
        
        # detais sur le compteur
        self.detail = ft.Text(value=f"Debut 1 - Fin 10 - Pas {self.parametre.saut} - Secondes 1",size=15,italic=True)

        self.body = ft.Container(
            width=500,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    self.toute_lettre,
                    self.compteur,
                    ft.Container(height=30),
                    self.detail,
                    self.run,
                    ft.Container(height=20),
                    self.regrage_butons
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        # page appropos
        self.about_page = ft.Container(
            content=ft.Column([
                ft.Text("Apropos de l'application",size=30,font_family="segoe ui",weight='w900'),
                ft.Container(height=20),
                ft.Text("Materiel didactique et exemple de compteur dans le context de la structure repetitive (iterative) en programmation\n\n Il montre un exemple d'utilisation des boucles dans des choses pratique \nDans notre cas l'application qui apprend aux enfants à compter et à visualiser dans different langue leurs montre un interêt de comprendre vraiment comment le developêur a proceder pour concevoir une telle applicatque\n\n l'application est la première version la prochaine prendra en compte d'autre aspect de la programmation \n\ndéveloppé par NTWALI LWABOSHI YVES",size=15,font_family="segoe ui",weight='w400'),
                ft.Container(height=20),
                ft.TextButton("Retourner à la page principale",icon=ft.Icons.ARROW_BACK_IOS,icon_color="blue",on_click=self.goback_principal_page)
            ],alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=500,
            alignment=ft.alignment.center,

        )

        # ajout des composents à la page
        self.page.add(
            self.body
        )

        # declancheur et ..
        self.tourne = False
        self.task = None

    # FONCTIONS
    # _____________________________________

    def about(self,e):
        self.page.controls.clear()
        self.page.controls.append(self.about_page)
        self.page.update()

    def goback_principal_page(self,e):
        self.page.controls.clear()
        self.page.controls.append(self.body)
        self.page.update()

    def check_item_clicked(self,e):
        e.control.checked = not e.control.checked
        self.page.update()

    def verifie_input(self,e):
        content = e.control.value
        try:
            content_float = float(content)
            e.control.border_color = None
            self.info.value = ""
        except Exception as ex:
            e.control.border_color = "red"
            self.info.value = "ce champ est requi et doit contenir que des nombres entier ou decimaux"
        self.page.update()

    def verifier_champ_vide_et_carractere_indesirable(self)->bool:
        try:
            self.initialiser_parametre()
            self.info.value = ""

        except Exception as ex:
            self.info.value = "ces champ est requi et doit contenir que des nombres entier ou decimaux"
            return False
        
        self.page.update()
        return True

    def verifie_ordre(self,)->bool:
        if not self.verifier_champ_vide_et_carractere_indesirable():
            return False

        p = self.parametre

        if p.debut >= 0 and p.fin > 0 and p.saut > 0 and p.sc > 0:
            if p.debut > p.fin:
                return False
            elif p.debut+p.saut > p.fin:
                return False

        else : return False

        return True
        
    def close(self,e):
        if self.verifie_ordre() == True:
            self.page.close(self.options)
            self.page.update
        else:
            self.info.value ="Erreur de validation vérifier si aucun champ n'es à zéro sauf celui du debut et si la somme de debut et de fin est inférieur au saut ou si debut est superieur à la fin, "
            self.page.update()
    
    def initialiser_parametre(self):
        # parametre data
        self.parametre = Parametre(
            debut = int(self.debut_compteur.value),
            fin = int(self.fin_compteur.value),
            saut = int(self.saut_compteur.value),
            sc = float(self.second_to_sleep.value)
        )
        self.detail.value = f"Debut {self.parametre.debut} - Fin {self.parametre.fin} - Pas {self.parametre.saut} - Secondes {self.parametre.sc}"

    async def compter(self):
        if not self.verifie_ordre():
            return

        try:
            p = self.parametre
            if self.incrementer_decrementer.value == "incrementer":
                for i in range(p.debut,p.fin+1,p.saut):
                    if not self.tourne:
                        break
                    self.compteur.value = str(i)
                    self.compter_fr.value = num2words(i,lang="fr")
                    self.compter_en.value =num2words(i,lang="en")
                    await asyncio.sleep(p.sc)
                    self.page.update()

            elif self.incrementer_decrementer.value == "decrementer":
                for i in range(p.fin+1,p.debut,-p.saut):
                    if not self.tourne:
                        break
                    self.compteur.value = str(i)
                    self.compter_fr.value = num2words(i,lang="fr")
                    self.compter_en.value =num2words(i,lang="en")
                    await asyncio.sleep(p.sc)
                    self.page.update()
            
            self.run.icon = ft.Icons.PLAY_ARROW_ROUNDED            
            self.page.update()

        except Exception as ex:
            pass
    
    async def lancer(self,e):
        if not self.tourne:
            self.tourne = True
            self.run.icon = ft.Icons.PAUSE_CIRCLE
            asyncio.create_task(self.compter())
        else:
            self.tourne = False
            self.run.icon = ft.Icons.PLAY_ARROW_ROUNDED

        self.page.update()

    def close_exit_dialog(self,e):
        if not self.verifie_ordre() == True:
            # parametre data
            self.parametre = Parametre(
                debut = 1,
                fin = 10,
                saut = 0,
                sc = 1
            )
        
        self.page.close(self.options)
        self.page.update

    print("application lancée")


async def main(page:ft.Page):
    Application_compteur(page)
    

ft.app(target=main,port=os.environ.get("PORT",8080))
