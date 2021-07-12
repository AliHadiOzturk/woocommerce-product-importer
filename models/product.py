class Product:
    def __init__(self, SKU: str, color: str, categoryName: str, name: str, description: str, regularPrice: int, salePrice: int, stock: int, images: str):
        self.SKU = SKU,
        self.color = color,
        self.categoryName = categoryName,
        self.name = name,
        self.description = description,
        self.regularPrice = regularPrice,
        self.salePrice = salePrice,
        self.stock = stock,
        self.images = images
