from database.firebase import ref_roles

class RoleRepository:
    def get_by_id(self, id: str):
        return ref_roles.child(id).get()

    def create(self, data: dict):
        return ref_roles.push(data)
    
    def update(self, id: str, data: dict):
        return ref_roles.child(id).update(data)

    def delete(self, id: str):
        ref_roles.child(id).delete()

    def get_all(self):
        return ref_roles.get()