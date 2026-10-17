# WebTravel

Application web d'agence de voyages développée avec **Django**, dans le cadre d'un projet académique (IUT, BUT3).

## Objectif du projet

WebTravel simule le portail d'une agence de voyages :

- **Visiteurs et clients** : ils consultent le catalogue des voyages (titre, prix, photo) et le détail de chaque itinéraire, c'est-à-dire les étapes par ville avec le nombre de jours. Un visiteur peut créer un compte client.
- **Membres du personnel** (`is_staff`) : ils gèrent le catalogue directement depuis l'interface publique. Ils peuvent créer, modifier et supprimer des villes, des voyages (avec leur photo) et les étapes d'un voyage.

Le back-office Django (`/admin/`) reste disponible pour les super-utilisateurs.

## Technologies

| Élément | Version / détail |
| :--- | :--- |
| Langage | Python 3.11 ou plus récent |
| Framework | Django 5.2 |
| Images | Pillow (requis par `ImageField`) |
| Base de données | SQLite 3 (fichier `webtravel/db.sqlite3`, non versionné) |
| Interface | Templates Django, Bootstrap 5.0.2 et Bootstrap Icons (via CDN) |

## Arborescence

```text
webtravel/                      ← racine du dépôt
├── README.md
├── requirements.txt            ← dépendances Python
├── .gitignore
└── webtravel/                  ← dossier du projet Django (contient manage.py)
    ├── manage.py
    ├── images/imagesVoyage/    ← photos des voyages (MEDIA_ROOT)
    ├── webtravel/              ← configuration (settings.py, urls.py)
    ├── applicompte/            ← connexion, déconnexion, inscription, barre de navigation
    └── applitravel/            ← modèles Ville / Voyage / Etape, vues, templates, CSS
```

---

## Installation

### 1. Installer Python (s'il n'est pas déjà installé)

Vérifiez d'abord si Python est présent :

```bash
python --version      # Windows
python3 --version     # Linux / macOS
```

Si la commande affiche `Python 3.11` ou une version plus récente, passez à l'étape 2. Sinon :

- **Windows** : téléchargez l'installateur sur <https://www.python.org/downloads/>. Au premier écran, **cochez « Add python.exe to PATH »**, puis cliquez sur « Install Now ». Fermez et rouvrez ensuite le terminal.
  Autre possibilité : `winget install Python.Python.3.12`
- **macOS** : téléchargez l'installateur sur <https://www.python.org/downloads/>, ou passez par Homebrew : `brew install python@3.12`
- **Linux (Debian / Ubuntu)** :
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip
  ```
- **Linux (Fedora)** : `sudo dnf install python3 python3-pip`

> Dans la suite, remplacez `python` par `python3` si vous êtes sous Linux ou macOS.

### 2. Récupérer le projet

```bash
git clone https://git.iut-orsay.fr/irabeha/webtravel.git
cd webtravel
```

### 3. Créer et activer l'environnement virtuel

L'environnement virtuel isole les dépendances du projet de celles du reste du système. Créez-le **à la racine du dépôt** (le dossier qui contient `requirements.txt`) :

```bash
python -m venv .venv
```

Puis activez-le :

| Système | Commande d'activation |
| :--- | :--- |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| Linux / macOS | `source .venv/bin/activate` |

Une fois l'environnement activé, `(.venv)` apparaît au début de l'invite de commande. Pour le désactiver plus tard, tapez `deactivate`.

> **Windows, PowerShell :** si l'activation est refusée avec un message du type « l'exécution de scripts est désactivée », lancez une fois la commande ci-dessous, puis réessayez :
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### 4. Installer les dépendances

L'environnement virtuel doit être activé :

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Pour vérifier l'installation :

```bash
python -m django --version     # doit afficher 5.2.x
```

### 5. Préparer la base de données

Les commandes Django se lancent depuis le dossier qui contient `manage.py` :

```bash
cd webtravel
```

Le projet lit sa configuration dans des variables d'environnement. En développement, il suffit d'activer le mode debug.

| Système | Commande |
| :--- | :--- |
| Windows (PowerShell) | `$env:DJANGO_DEBUG="True"` |
| Windows (cmd) | `set DJANGO_DEBUG=True` |
| Linux / macOS | `export DJANGO_DEBUG=True` |

> Cette variable ne vaut que pour le terminal en cours : il faut la redéfinir à chaque nouveau terminal.

Appliquez ensuite les migrations, puis créez un compte administrateur (staff) :

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

Ouvrez ensuite <http://127.0.0.1:8000/> dans un navigateur ; la page redirige vers la liste des voyages.

---

## Utilisation

| Page | Adresse | Accès |
| :--- | :--- | :--- |
| Liste des voyages | `/voyages/` | Tout le monde |
| Détail d'un voyage | `/voyages/<id>` | Tout le monde |
| Connexion | `/login/` | Tout le monde |
| Inscription | `/register/` | Visiteurs |
| Liste des villes | `/villes/` | Staff |
| Créer une ville / un voyage | `/villes/add`, `/voyages/add` | Staff |
| Back-office Django | `/admin/` | Super-utilisateur |

Un compte créé par `/register/` est un compte **client**. Pour qu'un compte accède aux fonctions de gestion, cochez « Statut équipe » sur cet utilisateur dans `/admin/`.

## Lancer les tests

Depuis le dossier `webtravel/` (celui de `manage.py`), avec l'environnement virtuel activé et `DJANGO_DEBUG=True` :

```bash
python manage.py test
```

## Variables d'environnement

| Variable | Rôle | Valeur par défaut |
| :--- | :--- | :--- |
| `DJANGO_DEBUG` | `True` pour le développement | `False` |
| `DJANGO_SECRET_KEY` | Clé secrète Django, **obligatoire** quand `DJANGO_DEBUG` n'est pas à `True` | clé de développement si le debug est activé |
| `DJANGO_ALLOWED_HOSTS` | Noms d'hôte autorisés, séparés par des virgules | `localhost,127.0.0.1` |

Pour générer une clé secrète :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Problèmes fréquents

| Symptôme | Solution |
| :--- | :--- |
| `ImproperlyConfigured: ... DJANGO_SECRET_KEY ...` | Définissez `DJANGO_DEBUG=True` (étape 5) dans le terminal en cours. |
| `ModuleNotFoundError: No module named 'django'` | L'environnement virtuel n'est pas activé (étape 3), ou les dépendances ne sont pas installées (étape 4). |
| `python` introuvable sous Windows | Réinstallez Python en cochant « Add python.exe to PATH », ou utilisez la commande `py` à la place de `python`. |
| Les photos des voyages ne s'affichent pas | Le serveur de développement ne sert les images qu'avec `DJANGO_DEBUG=True`. |
| `no such table` | Lancez `python manage.py migrate`. |