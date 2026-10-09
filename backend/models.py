from typing import Optional
from sqlmodel import Field, SQLModel

class Track(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    spotify_id: str = Field(index=True, unique=True, description="ID único da música no Spotify")
    name: str = Field(description="Nome da música")
    artist_name: str = Field(description="Nome do artista principal")
    album_image_url: Optional[str] = Field(default=None, description="URL da capa do álbum")
    preview_url: Optional[str] = Field(default=None, description="URL do trecho de 30 segundos")
