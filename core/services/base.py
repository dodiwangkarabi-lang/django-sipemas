class BaseService(object):
    model = None
    
    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)
    
    def update(self, id, **kwargs):
        return self.model.objects.filter(id=id).update(**kwargs)
    
    def delete(self, id):
        return self.model.objects.filter(id=id).delete()