class Mano:
    def __init__(self,Indice,Corazon,Anular,mañique,pulgar):
        self.Indice=Indice
        self.Corazon=Corazon
        self.Anular=Anular
        self.mañique=mañique
        if(pulgar==None):
            self.pulgar=pulgar

    def setIndice(self,indice):
        self.Indice=indice
    def setCorazon(self,Corazon):
        self.Corazon=Corazon
    def setAnular(self,Anular):
        self.Anular=Anular
    def setMeñique(self,mañique):
        self.mañique=mañique
    def setPulgar(self,pulgar):
        self.pulgar=pulgar
