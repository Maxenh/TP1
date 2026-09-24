import sys
import json
import os


from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem,\
      QMainWindow, QWidget, QVBoxLayout, QLineEdit, QMessageBox, QLabel
from PySide6.QtCore import Qt
#j'imagine que cette commande permet l'ouverture de la fenetre de l'application
    
app = QApplication(sys.argv)

try:
    class Window(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Tableau JSON")
            self.resize(650, 100)
            self.import_json = QLineEdit("Copier le chemin d'accès du fichier JSON ici")
            

            layout = QVBoxLayout()
            layout.addWidget(self.import_json)
            self.setLayout(layout)
            self.import_json.returnPressed.connect(self.chemins_json)

        def chemins_json(self):
            self.path = self.import_json.text()
            self.ouverture_fichier()

         #ouverture du fichier json et lecture de son contenu
        def ouverture_fichier(self):
            try:
               
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                
                self.visuel = Visuel_Tableau(self.data, self.path)
                self.visuel.show()
                self.close()

            except json.JSONDecodeError:
                QMessageBox.critical(None, "Erreur de décodage JSON.", 
                                     "Le fichier JSON est mal formé. Veuillez vérifier son contenu.")   
except FileNotFoundError:
    QMessageBox.critical(None, "Fichier JSON introuvable.", 
                         "Veuillez vérifier le chemin d'accès du fichier JSON.")   



try:

    #creation d'un visuel plus beau pour le tableau en utilisant QMainWindow
    class Visuel_Tableau(QMainWindow):
        def __init__(self, data, path):
            super().__init__()
            self.setWindowTitle("Tableau JSON")
            self.data = data
            self.path = path

            #creation de l'application 
            self.application=QWidget()
            

            # fabrication du tableau
            self.json_tableau = QTableWidget()
            self.json_tableau.setSortingEnabled(True)  # Activer le tri des colonnes

                
            #mise en place des noms des colonnes
            colonnes = [
                "id", "nom", "categorie", "format", 
                "polygones", "statut", "auteur", 
                "date_creation", "prix", "taille_fichier" 
                ]
        

            self.setCentralWidget(self.json_tableau)

            self.json_tableau.setColumnCount(len(colonnes))
            self.json_tableau.setHorizontalHeaderLabels(colonnes)
            self.json_tableau.setRowCount(len(self.data))


            #loop pour ajouter les données du fichier json dans le tableau
            for ligne, objet in enumerate(self.data):

                for colonne, nom_colonne in enumerate(colonnes):

                    #si une valeur dans le fichier json est manquante, on mettra "N/A" dans le tableau
                    try:
                        valeur = objet[nom_colonne]
                    except KeyError:
                        valeur = "N/A"

                #Utilisation de QTableWidgetItem pour régler le problème d'un mauvais tri des nombres dans le tableau
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, valeur)

                    self.json_tableau.setItem(
                        ligne,
                        colonne,
                        item
                    )


            # Ajuster la largeur des colonnes en fonction du contenu        
            self.json_tableau.resizeColumnsToContents() 
            largeur_fenetre =self.json_tableau.horizontalHeader().length()
            self.resize(largeur_fenetre + 70, 600)       

            

            #Barre de recherche créer
            self.recherche = QLineEdit()
            self.recherche.setPlaceholderText("Rechercher...")

            #associe la touche enter a une commande
            self.recherche.returnPressed.connect(self.rechercher)

            #fabrication des alignements de la barre de recherche et du tableau
            apparence_du_tableau=QVBoxLayout()
            apparence_du_tableau.addWidget(self.recherche)
            apparence_du_tableau.addWidget(self.json_tableau)
            

            #association de l'apparence du tableau à l'application
            self.application.setLayout(apparence_du_tableau)

            #mettre le tout a l'écran
            self.setCentralWidget(self.application)

            

            #calcul de la taille du fichier json
            st_taille = os.path.getsize(self.path)
            t_ko = st_taille / 1024

            #obtenir le nom du fichier json
            st_nom_fichier = os.path.basename(self.path)

            #affichage du nom et de la taille du fichier json dans l'application
            info_label = QLabel(
                f" Nom du fichier : {st_nom_fichier}  |  Taille du fichier : {t_ko:.2f} Ko | Nombre d'items : {len(self.data)}"
                )
            apparence_du_tableau.addWidget(info_label)

        try:
            #fonction de recherche dans le tableau, demande au systeme de trouver le mot similaire a celui ecrit
            def rechercher(self):
                texte_recherche = self.recherche.text().lower() #permet d'annuler les maj vs minuscule .lower
                resultats = False

                for ligne in range(self.json_tableau.rowCount()):
                    correspondance = False
                    for colonne in range(self.json_tableau.columnCount()):
                        item = self.json_tableau.item(ligne, colonne)
                        if item and texte_recherche in item.text().lower():
                            correspondance = True
                            resultats = True
                            break
                    self.json_tableau.setRowHidden(ligne, not correspondance)    
                if not resultats:
                    QMessageBox.information(None, "Aucune correspondance trouvée.", 
                                            "Aucun résultat ne correspond à votre recherche.")
                    
           
                           
        except Exception as e:
            QMessageBox.critical(None, "Erreur lors de la recherche.", 
                                 f"Une erreur est survenue lors de la recherche : {str(e)}") 


except Exception as b:
    QMessageBox.critical(None, "Erreur lors de la création du tableau.", 
                         f"Une erreur est survenue lors de la création du tableau : {str(b)}")
  

window = Window()
window.show()


sys.exit(app.exec())