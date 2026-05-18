import requests
import pandas as pd

USUARIOS_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_URL = "https://jsonplaceholder.typicode.com/posts"


def fetch_usuarios() -> list[dict]:
    """
    Faz GET em https://jsonplaceholder.typicode.com/users
    Retorna lista de usuarios.
    """

    try:
        response = requests.get(USUARIOS_URL, timeout=10)
        response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
        return response.json()
    except Exception as e:
        print(f"Error ao buscar usuário: {e}")
        return []

def fetch_posts() -> list[dict]:
    """
    Faz GET em https://jsonplaceholder.typicode.com/posts
    Retorna lista de posts.
    """

    try:    
        response = requests.get(POSTS_URL, timeout=10)
        response.raise_for_status()  # Verifica se a resposta foi bem-sucedida
        return response.json()
    
    except Exception as e:
        print(f"Error ao buscar posts: {e}")
        return []

def flatten_usuario(usuario: dict) -> dict:
    """
    Achata os campos aninhados do usuario.
    """

    address = usuario.get("address", {}) #
    company = usuario.get("company", {}) #

    return {
        "id": usuario.get("id"),
        "name": usuario.get("name"),
        "username": usuario.get("username"),
        "email": usuario.get("email"),
        "address_street": address.get("street"),
        "address_city": address.get("city"),
        "address_zipcode": address.get("zipcode"),
        "phone": usuario.get("phone"),
        "website": usuario.get("website"),
        "company_name": company.get("name"),
    }

def extract_usuarios() -> pd.DataFrame:
    
    """
    Extrai usuarios, achata campos e retorna DataFrame
    pronto para carga na camada raw.
    """

    usuarios = fetch_usuarios()

    usuarios_achatados = [
        flatten_usuario(usuario)
        for usuario in usuarios
    ]

    df = pd.DataFrame(usuarios_achatados) #

    df["dl_load_timestamp"] = pd.Timestamp.now() #

    return df


def extract_posts() -> pd.DataFrame:
    
    """
    Extrai posts e retorna DataFrame
    pronto para carga na camada raw.
    """

    posts = fetch_posts()

    df = pd.DataFrame(posts)

    if df.empty:
        return df

    df = df.rename(columns={
        "userId": "user_id" # 
    })

    df["dl_load_timestamp"] = pd.Timestamp.now() # 

    df = df[
        [
            "id",
            "user_id",
            "title",
            "body",
            "dl_load_timestamp",
        ]
    ]

    return df