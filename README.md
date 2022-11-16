# Youtube Scrapper

## Description

Ce script permet de scrapper une liste de vidéos Youtuve et de stocker certaines informations dans un fichier au format JSON  

## Installation

```sh
python3.8 -m venv .venv  
source .venv/bin/activate  
pip install --upgrade pip
pip install -r requirements.txt 
``` 

## Utilisation

`python scrapper.py --input input.json --output output.json`

Avec 

- [`input.json`](./input.json) : la liste des vidéos Youtube, ayant le format :   
```json
{
    "videos_id": [
        "youtube_id1",
        "youtube_id2",
        ...
    ]
}
```

- [`output.json`](./output.json) : fichier de sortie avec les informations

### Tests

Pour exécuter les tests :  
```sh
pytest
```

Attention, deux tests sont dépendant du nombres de likes, ils peuvent ainsi changer au cours du temps.  

## Données scrappées

- Title : Titre de la vidéo
- Author : Auteur de la vidéo 
- NbLikes : Nombre de likes 
- Description : Description complète de la vidéo
- Links : Liens et timestamps présent dans la description
- Comments : Commentaires de la vidéo

### Exemple de sortie du script

```json
[
    {
        "Title": "Vidéo intéressante",
        "Author": "Créateur de contenu",
        "NbLikes": 1000,
        "Description": " ... ",
        "Links": [
            "abc.com",
            ...
        ],
        "Comments": [
            {
                "Author": "Commentateur",
                "Content": " ... ",
                "NbLikes": "10"
            },
            ...
        ],
        "Id": "000000000"
    },
    {
        ...
    }
]
```  