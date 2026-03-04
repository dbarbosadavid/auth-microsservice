from database.firebase import ref_users

class UserRepository:
    def get_by_id(self, id: str):
        return ref_users.child(id).get()

    def create(self, data: dict):
        return ref_users.push(data)
    
    def update(self, id: str, data: dict):
        return ref_users.child(id).update(data)

    def delete(self, id: str):
        ref_users.child(id).delete()

    def get_all(self):
        return ref_users.get()