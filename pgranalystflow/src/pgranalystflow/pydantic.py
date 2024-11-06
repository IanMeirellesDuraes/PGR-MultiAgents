'''
class GheInfo(BaseModel):
	ghes: Dict[str] = Field(..., description="Ghes encontrados no documento, onde a chave é o nome do ghe e o valor é os cargos associados ao respectivo ghe")
	ghes_count: int = Field(..., description="Quantidade de ghes encontrados no documento")
	ghes_pages: List[int] = Field(..., description="Páginas em que os ghes foram encontrados")

class RiskAnalysis(BaseModel):
	risk: Dict[str] = Field(..., description="Grupos de riscos encontrados no documento, onde a chave é o nome do risco e o valor é os tipos de riscos associados ao respectivo grupo")
	risk_levels: List[str] = Field(..., description="Níveis de riscos encontrados no documento")
	risk_count: int = Field(..., description="Quantidade de riscos encontrados no documento")
	risk_pages: List[int] = Field(..., description="Páginas em que os riscos foram encontrados")	
'''
'''
class RiscoModel(BaseModel):
    tipo_do_risco: str = Field(..., description="Tipo do respectivo risco")
    nivel_do_risco: str = Field(..., description="Nível do respectivo risco")

class GrupoDeRiscoModel(BaseModel):
    nome_grupo: Dict[str, RiscoModel] = Field(..., description="Nome do grupo de risco como chave e os riscos associados ao grupo como valor")

class GheModel(BaseModel):
    cargos: str = Field(..., description="Cargos associados ao ghe")
    grupos_de_risco: Dict[str, GrupoDeRiscoModel] = Field(..., description="Grupos de risco associados ao ghe especificado")

class EstruturaModel(RootModel):
    __root__: Dict[str, GheModel] = Field(..., description="Estrutura de ghes e riscos associados, sendo o nome do ghe a chave e os riscos associados ao ghe como valor")
'''