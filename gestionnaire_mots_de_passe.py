"""
=============================================================
 Gestionnaire de Mots de Passe - Password Manager
=============================================================
 Guide d'utilisation :
   1. Remplissez les champs Service, Identifiant et Mot de passe
   2. Cliquez sur "Ajouter" pour sauvegarder une entrée
   3. Sélectionnez une entrée dans la liste pour la voir ou la supprimer
   4. Cliquez sur l'icône "👁" pour afficher/masquer le mot de passe
   5. Les données sont sauvegardées automatiquement dans passwords.json

 Auteur : Projet Start Up - SNT
 Python : 3.10+
 Bibliothèques : tkinter, json, os
=============================================================
"""

import tkinter as tk
from tkinter import messagebox
import json
import os

# --- Fichier de sauvegarde local ---
FICHIER_JSON = "passwords.json"


# --- Charger les mots de passe depuis le fichier JSON ---
def charger_mots_de_passe():
    """Lit le fichier JSON et retourne la liste des entrées."""
    if os.path.exists(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# --- Sauvegarder les mots de passe dans le fichier JSON ---
def sauvegarder_mots_de_passe(liste):
    """Écrit la liste des entrées dans le fichier JSON."""
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(liste, f, ensure_ascii=False, indent=2)


# --- Rafraîchir l'affichage de la Listbox ---
def rafraichir_liste():
    """Vide et reremplit la Listbox avec les données actuelles."""
    listbox.delete(0, tk.END)
    for entree in mots_de_passe:
        listbox.insert(tk.END, f"🔑 {entree['service']}  —  {entree['identifiant']}")


# --- Ajouter un nouveau mot de passe ---
def ajouter():
    """Récupère les champs, valide, puis ajoute l'entrée à la liste."""
    service = champ_service.get().strip()
    identifiant = champ_identifiant.get().strip()
    mdp = champ_mdp.get().strip()

    # Vérification que tous les champs sont remplis
    if not service or not identifiant or not mdp:
        messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
        return

    # Création de l'entrée et ajout à la liste
    entree = {"service": service, "identifiant": identifiant, "mot_de_passe": mdp}
    mots_de_passe.append(entree)
    sauvegarder_mots_de_passe(mots_de_passe)
    rafraichir_liste()

    # Vider les champs après ajout
    champ_service.delete(0, tk.END)
    champ_identifiant.delete(0, tk.END)
    champ_mdp.delete(0, tk.END)
    messagebox.showinfo("Succès", f"Mot de passe pour '{service}' ajouté !")


# --- Afficher le mot de passe de l'entrée sélectionnée ---
def afficher():
    """Affiche dans une boîte de dialogue le mot de passe de l'entrée choisie."""
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une entrée.")
        return

    index = selection[0]
    entree = mots_de_passe[index]
    messagebox.showinfo(
        "Mot de passe",
        f"Service : {entree['service']}\n"
        f"Identifiant : {entree['identifiant']}\n"
        f"Mot de passe : {entree['mot_de_passe']}"
    )


# --- Supprimer l'entrée sélectionnée ---
def supprimer():
    """Supprime l'entrée sélectionnée après confirmation."""
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une entrée.")
        return

    index = selection[0]
    service = mots_de_passe[index]["service"]

    # Demander confirmation avant suppression
    confirmer = messagebox.askyesno("Confirmation", f"Supprimer '{service}' ?")
    if confirmer:
        mots_de_passe.pop(index)
        sauvegarder_mots_de_passe(mots_de_passe)
        rafraichir_liste()
        messagebox.showinfo("Supprimé", f"'{service}' a été supprimé.")


# --- Afficher/Masquer le mot de passe dans le champ de saisie ---
def basculer_visibilite():
    """Alterne entre affichage masqué (***) et visible du mot de passe."""
    if champ_mdp.cget("show") == "*":
        champ_mdp.config(show="")
        btn_oeil.config(text="🙈")
    else:
        champ_mdp.config(show="*")
        btn_oeil.config(text="👁")


# =============================================
#  CONSTRUCTION DE L'INTERFACE GRAPHIQUE
# =============================================

# Charger les données existantes
mots_de_passe = charger_mots_de_passe()

# Fenêtre principale
fenetre = tk.Tk()
fenetre.title("🔐 Gestionnaire de Mots de Passe")
fenetre.geometry("520x430")
fenetre.resizable(False, False)
fenetre.config(bg="#1e1e2e")

# --- Titre ---
tk.Label(
    fenetre, text="🔐 Gestionnaire de Mots de Passe",
    font=("Helvetica", 14, "bold"), bg="#1e1e2e", fg="#cdd6f4"
).grid(row=0, column=0, columnspan=3, pady=(15, 10))

# --- Champ Service ---
tk.Label(fenetre, text="Service :", bg="#1e1e2e", fg="#a6adc8").grid(row=1, column=0, sticky="e", padx=10, pady=5)
champ_service = tk.Entry(fenetre, width=30, bg="#313244", fg="#cdd6f4", insertbackground="white")
champ_service.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

# --- Champ Identifiant ---
tk.Label(fenetre, text="Identifiant :", bg="#1e1e2e", fg="#a6adc8").grid(row=2, column=0, sticky="e", padx=10, pady=5)
champ_identifiant = tk.Entry(fenetre, width=30, bg="#313244", fg="#cdd6f4", insertbackground="white")
champ_identifiant.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)

# --- Champ Mot de passe avec bouton œil ---
tk.Label(fenetre, text="Mot de passe :", bg="#1e1e2e", fg="#a6adc8").grid(row=3, column=0, sticky="e", padx=10, pady=5)
champ_mdp = tk.Entry(fenetre, width=25, show="*", bg="#313244", fg="#cdd6f4", insertbackground="white")
champ_mdp.grid(row=3, column=1, sticky="w", pady=5)
btn_oeil = tk.Button(fenetre, text="👁", command=basculer_visibilite, bg="#313244", fg="#cdd6f4", bd=0, cursor="hand2")
btn_oeil.grid(row=3, column=2, sticky="w")

# --- Boutons d'action ---
frame_boutons = tk.Frame(fenetre, bg="#1e1e2e")
frame_boutons.grid(row=4, column=0, columnspan=3, pady=10)

tk.Button(frame_boutons, text="➕ Ajouter", command=ajouter, bg="#a6e3a1", fg="#1e1e2e", font=("Helvetica", 10, "bold"), width=12, cursor="hand2").pack(side="left", padx=5)
tk.Button(frame_boutons, text="👁 Afficher", command=afficher, bg="#89b4fa", fg="#1e1e2e", font=("Helvetica", 10, "bold"), width=12, cursor="hand2").pack(side="left", padx=5)
tk.Button(frame_boutons, text="🗑 Supprimer", command=supprimer, bg="#f38ba8", fg="#1e1e2e", font=("Helvetica", 10, "bold"), width=12, cursor="hand2").pack(side="left", padx=5)

# --- Liste des mots de passe ---
tk.Label(fenetre, text="Vos entrées :", bg="#1e1e2e", fg="#a6adc8", font=("Helvetica", 10)).grid(row=5, column=0, columnspan=3, pady=(5, 2))

listbox = tk.Listbox(fenetre, width=60, height=8, bg="#313244", fg="#cdd6f4", selectbackground="#585b70", font=("Courier", 10))
listbox.grid(row=6, column=0, columnspan=3, padx=20, pady=5)

# --- Charger les données au démarrage ---
rafraichir_liste()

# --- Lancer l'application ---
fenetre.mainloop()
