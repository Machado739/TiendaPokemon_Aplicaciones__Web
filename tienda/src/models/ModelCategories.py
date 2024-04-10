class Categories:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
class ModelCategories:

    @staticmethod
    def add_category(mysql, category):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", (category.name, category.description))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def update_category(mysql, category):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE categories SET name = %s, description = %s WHERE id = %s", (category.name, category.description, category.id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def delete_category(mysql, category_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_all_categories(mysql):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM categories")
        categories_data = cursor.fetchall()
        categories = []
        for category_data in categories_data:
            category = Categories(id=category_data[0], name=category_data[1], description=category_data[2])
            categories.append(category)
        cursor.close()
        return categories
