def pizzas():
    return [
        {   'id': 1, 'name': 'Margherita', 'price': 12.50,
            'description': 'La classique italienne avec sauce tomate, mozzarella fraîche et basilic. Un équilibre parfait de saveurs méditerranéennes.'},
        {
            'id': 2, 'name': 'Pepperoni', 'price': 15.90,
            'description': 'Généreusement garnie de rondelles de pepperoni légèrement épicé sur un lit de mozzarella fondante et de sauce tomate.'},
        {
            'id': 3,'name': 'Reine','price': 14.80,
           'description': 'Un mélange savoureux de jambon blanc, champignons frais, olives noires, mozzarella et sauce tomate. Un grand classique de la cuisine italienne.'},
        {
            'id': 4,'name': 'Hawaïenne','price': 16.50,
            'description': 'L\'exotique alliance sucrée-salée avec jambon, ananas rôti et mozzarella sur une base sauce tomate.'},
        {
            'id': 5,'name': '4 Fromages','price': 18.90,
            'description': 'Un festin de fromages avec mozzarella, gorgonzola, chèvre et emmental. Le bonheur des amateurs de fromages.'},
        {
            'id': 6,'name': 'Mexicaine','price': 17.50,
            'description': 'Une explosion de saveurs épicées avec bœuf haché, poivrons, oignons, maïs, jalapeños et épices mexicaines.'},
        {
            'id': 7,'name': 'Saumon fumé','price': 23.90,
            'description': 'Raffinée avec saumon fumé norvégien, crème fraîche, aneth frais et oignons rouges. Une touche de citron complète ce délice.'},
        {
            'id': 8,'name': '4 saisons','price': 16.90,
            'description': 'Quatre sections distinctes : artichauts, olives noires, jambon et champignons. Chaque part offre une nouvelle découverte.'},
        {
            'id': 9,'name': 'Pizza Carrée','price': 19.90,
            'description': 'Notre spécialité unique en forme carrée, garnie de légumes grillés, mozzarella di bufala et huile d\'olive extra vierge.'},
        {
            'id': 10,'name': 'Chèvre-miel','price': 15.50,
            'description': 'L\'alliance parfaite du fromage de chèvre crémeux et du miel, relevée de noix et de roquette fraîche. Un mélange sucré-salé délicieux.'}
    ]


def ingredients():
    return [
        {'id': 1, 'name': 'Sauce tomates', 'available': True},
        {'id': 2, 'name': 'Mozzarella', 'available': True},
        {'id': 3, 'name': 'Pepperoni', 'available': True},
        {'id': 4, 'name': 'Jambon', 'available': True},
        {'id': 5, 'name': 'Champignon', 'available': True},
        {'id': 6, 'name': 'Gorgonzola', 'available': True},
        {'id': 7, 'name': 'Chèvre', 'available': True},
        {'id': 8, 'name': 'Miel', 'available': True},
        {'id': 9, 'name': 'Parmesan', 'available': True},
        {'id': 10, 'name': 'Ananas', 'available': True},
        {'id': 12, 'name': 'Poivron', 'available': True},
        {'id': 13, 'name': 'Basilic', 'available': True},
        {'id': 14, 'name': 'Boeuf haché', 'available': True},
        {'id': 15, 'name': 'Jalapenos', 'available': True},
        {'id': 16, 'name': 'Crème fraiche', 'available': True},
        {'id': 17, 'name': 'Saumon fumé', 'available': True},
        {'id': 18, 'name': 'Olives noirs', 'available': True},
        {'id': 19, 'name': 'Maïs', 'available': True},
        {'id': 20, 'name': 'Oignon', 'available': True}]

def recettes():
    return [
        {'id_pizza' : 1, 'id_ingredient': 1}, 
        {'id_pizza' : 1, 'id_ingredient': 2}, 
        {'id_pizza' : 1, 'id_ingredient': 13},
        {'id_pizza' : 2, 'id_ingredient': 1}, 
        {'id_pizza' : 2, 'id_ingredient': 2}, 
        {'id_pizza' : 2, 'id_ingredient': 3},
        {'id_pizza' : 3, 'id_ingredient': 1}, 
        {'id_pizza' : 3, 'id_ingredient': 2}, 
        {'id_pizza' : 3, 'id_ingredient': 4},
        {'id_pizza' : 3, 'id_ingredient': 5}, 
        {'id_pizza' : 4, 'id_ingredient': 1}, 
        {'id_pizza' : 4, 'id_ingredient': 2},
        {'id_pizza' : 4, 'id_ingredient': 4},
        {'id_pizza' : 4, 'id_ingredient': 10}, 
        {'id_pizza' : 5, 'id_ingredient': 1},
        {'id_pizza' : 5, 'id_ingredient': 2}, 
        {'id_pizza' : 5, 'id_ingredient': 6}, 
        {'id_pizza' : 5, 'id_ingredient': 9},
        {'id_pizza' : 5, 'id_ingredient': 7}, 
        {'id_pizza' : 6, 'id_ingredient': 1}, 
        {'id_pizza' : 6, 'id_ingredient': 2},
        {'id_pizza' : 6, 'id_ingredient': 14},
        {'id_pizza' : 6, 'id_ingredient': 15}, 
        {'id_pizza' : 6, 'id_ingredient': 19},
        {'id_pizza' : 7, 'id_ingredient': 2},
        {'id_pizza' : 7, 'id_ingredient': 16}, 
        {'id_pizza' : 7, 'id_ingredient': 17}, 
        {'id_pizza' : 8, 'id_ingredient': 1}, 
        {'id_pizza' : 8, 'id_ingredient': 2},
        {'id_pizza' : 8, 'id_ingredient': 4},
        {'id_pizza' : 8, 'id_ingredient': 5}, 
        {'id_pizza' : 8, 'id_ingredient': 18},
        {'id_pizza' : 9, 'id_ingredient': 1},
        {'id_pizza' : 9, 'id_ingredient': 20}, 
        {'id_pizza' : 9, 'id_ingredient': 18},
        {'id_pizza' : 10, 'id_ingredient': 1},
        {'id_pizza' : 10, 'id_ingredient': 2},
        {'id_pizza' : 10, 'id_ingredient': 7},
        {'id_pizza' : 10, 'id_ingredient': 8}]