from pymongo import MongoClient


class MongoDatabase:
    def __init__(self, db_name, collection_name, uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, document):
        """
        Добавляет новый документ в коллекцию.
        Аргумент document должен быть словарем.
        """
        result = self.collection.insert_one(document)
        return result.inserted_id

    def read_document(self, document_id):
        """
        Читает документ по его ID.
        """
        document = self.collection.find_one({"_id": document_id})
        return document

    def read_all_documents(
            self,
            search_filter: dict = {}
    ):
        """
        Читает все документы, соответствующие фильтру.
        Аргумент filter должен быть словарем (по умолчанию пустой, чтобы вернуть все документы).
        """
        documents = self.collection.find(search_filter)
        return list(documents)

    def update_document(self, document_id, update_fields):
        """
        Обновляет документ по его ID.
        Аргумент update_fields должен быть словарем с полями, которые нужно обновить.
        """
        result = self.collection.update_one(
            {"_id": document_id},
            {"$set": update_fields}
        )
        return result.modified_count

    def delete_document(self, document_id):
        """
        Удаляет документ по его ID.
        """
        result = self.collection.delete_one({"_id": document_id})
        return result.deleted_count

    def delete_all_documents(
            self,
            search_filter: dict = {}
    ):
        """
        Удаляет все документы, соответствующие фильтру (по умолчанию удаляет все документы).
        """
        result = self.collection.delete_many(search_filter)
        return result.deleted_count


db_actuals = MongoDatabase("HyanProject", "Actuals")
db_unnamed = MongoDatabase("HyanProject", "Unnamed")
