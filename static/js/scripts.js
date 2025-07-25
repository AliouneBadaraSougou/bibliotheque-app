// Fonction pour récupérer les livres populaires depuis l'API
function fetchFeaturedBooks() {
  return fetch('/api/featured_books')
    .then(response => {
      if (!response.ok) {
        throw new Error('Réponse du réseau non valide');
      }
      return response.json();
    });
}

// Fonction pour afficher les livres populaires
function displayFeaturedBooks() {
  const bookGrid = document.querySelector('#featured-books .grid');

  fetchFeaturedBooks()
    .then(books => {
      books.forEach(book => {
        const bookElement = createBookElement(book);
        bookGrid.appendChild(bookElement);
      });
    })
    .catch(error => {
      console.error('Erreur lors de la récupération des livres populaires :', error);
    });
}

// Fonction pour créer un élément de livre
function createBookElement(book) {
  const bookElement = document.createElement('div');
  bookElement.classList.add('bg-white', 'shadow', 'rounded-lg', 'overflow-hidden');

  // Ajouter les informations du livre (titre, auteur, image, etc.)
  bookElement.innerHTML = `
    <img src="/static/images/${book.imageUrl}" alt="Couverture du livre" class="w-full h-48 object-cover">
    <div class="p-4">
      <h3 class="text-xl font-bold mb-2">${book.title}</h3>
      <p class="text-gray-600 mb-4">${book.author}</p>
      <p class="mb-4">${book.description}</p>
      <div class="flex justify-between items-center">
        <button class="bg-indigo-600 text-white font-medium py-2 px-4 rounded-lg hover:bg-indigo-700">Commander</button>
        <button class="favorite-button text-indigo-600 hover:text-indigo-800" data-book-id="${book.id}"><i class="fas fa-star"></i></button>
      </div>
    </div>
  `;

  return bookElement;
}

// Écouter les événements au chargement du DOM
document.addEventListener('DOMContentLoaded', () => {
  displayFeaturedBooks();

  // Gestion des boutons favoris
  const favoriteButtons = document.querySelectorAll('.favorite-button');

  favoriteButtons.forEach(button => {
    button.addEventListener('click', () => {
      const bookId = button.getAttribute('data-book-id');
      const icon = button.querySelector('i');

      // Ajouter la logique pour enregistrer les favoris dans la base de données ou faire une action en conséquence
      // Exemple: mettre en favori un livre

      if (icon.classList.contains('text-yellow-400')) {
        icon.classList.remove('text-yellow-400');
        icon.classList.add('text-indigo-600');
      } else {
        icon.classList.remove('text-indigo-600');
        icon.classList.add('text-yellow-400');
      }
    });
  });
});
