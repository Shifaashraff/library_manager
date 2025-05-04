import json
import os
from typing import List, Dict

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("Welcome to your Personal Library Manager!")
    print("="*50)
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")
    print("="*50)

def get_valid_input(prompt: str, input_type=str, valid_options=None):
    """Get validated user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                raise ValueError("Input cannot be empty")
            
            if input_type == int:
                user_input = int(user_input)
            elif input_type == bool:
                user_input = user_input.lower()
                if user_input not in ['yes', 'no', 'y', 'n']:
                    raise ValueError("Please enter 'yes' or 'no'")
                user_input = user_input in ['yes', 'y']
            
            if valid_options and user_input not in valid_options:
                raise ValueError(f"Please enter one of: {', '.join(map(str, valid_options))}")
            
            return user_input
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def add_book(library: List[Dict]) -> None:
    """Add a new book to the library"""
    print("\n" + "="*50)
    print("Add a New Book")
    print("="*50)
    
    book = {
        'title': get_valid_input("Enter the book title: "),
        'author': get_valid_input("Enter the author: "),
        'year': get_valid_input("Enter the publication year: ", int),
        'genre': get_valid_input("Enter the genre: "),
        'read': get_valid_input("Have you read this book? (yes/no): ", bool)
    }
    
    library.append(book)
    print("\nBook added successfully!")

def remove_book(library: List[Dict]) -> None:
    """Remove a book from the library"""
    if not library:
        print("\nYour library is empty!")
        return
    
    print("\n" + "="*50)
    print("Remove a Book")
    print("="*50)
    
    title = get_valid_input("Enter the title of the book to remove: ")
    found_books = [book for book in library if book['title'].lower() == title.lower()]
    
    if not found_books:
        print(f"\nNo book found with title '{title}'")
        return
    
    if len(found_books) > 1:
        print("\nMultiple books found with that title:")
        for i, book in enumerate(found_books, 1):
            print(f"{i}. {book['title']} by {book['author']} ({book['year']})")
        
        choice = get_valid_input(
            "Enter the number of the book to remove: ",
            int,
            range(1, len(found_books)+1)
        )
        book_to_remove = found_books[choice-1]
    else:
        book_to_remove = found_books[0]
    
    library.remove(book_to_remove)
    print("\nBook removed successfully!")

def search_books(library: List[Dict]) -> None:
    """Search for books by title or author"""
    if not library:
        print("\nYour library is empty!")
        return
    
    print("\n" + "="*50)
    print("Search for a Book")
    print("="*50)
    print("Search by:")
    print("1. Title")
    print("2. Author")
    
    choice = get_valid_input("Enter your choice: ", int, [1, 2])
    search_term = get_valid_input(
        "Enter the search term: " if choice == 1 else "Enter the author's name: "
    )
    
    if choice == 1:
        results = [book for book in library if search_term.lower() in book['title'].lower()]
    else:
        results = [book for book in library if search_term.lower() in book['author'].lower()]
    
    if not results:
        print("\nNo matching books found.")
        return
    
    print(f"\nFound {len(results)} matching book(s):")
    for i, book in enumerate(results, 1):
        status = "Read" if book['read'] else "Unread"
        print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_all_books(library: List[Dict]) -> None:
    """Display all books in the library"""
    if not library:
        print("\nYour library is empty!")
        return
    
    print("\n" + "="*50)
    print("Your Library")
    print("="*50)
    
    for i, book in enumerate(library, 1):
        status = "Read" if book['read'] else "Unread"
        print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_statistics(library: List[Dict]) -> None:
    """Display library statistics"""
    if not library:
        print("\nYour library is empty!")
        return
    
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    
    print("\n" + "="*50)
    print("Library Statistics")
    print("="*50)
    print(f"Total books: {total_books}")
    print(f"Percentage read: {percentage_read:.1f}%")
    
    # Additional statistics
    genres = {}
    authors = {}
    for book in library:
        genres[book['genre']]= genres.get(book['genre'], 0) + 1
        authors[book['author']] = authors.get(book['author'], 0) + 1
    
    print("\nBooks by genre:")
    for genre, count in genres.items():
        print(f"- {genre}: {count}")
    
    print("\nBooks by author:")
    for author, count in authors.items():
        print(f"- {author}: {count}")

def save_library(library: List[Dict], filename: str = "library.json") -> None:
    """Save the library to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(library, f, indent=4)
    except Exception as e:
        print(f"Error saving library: {e}")

def load_library(filename: str = "library.json") -> List[Dict]:
    """Load the library from a JSON file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading library: {e}")
    return []

def main():
    """Main program loop"""
    library = load_library()
    
    while True:
        clear_screen()
        display_menu()
        
        choice = get_valid_input("\nEnter your choice: ", int, range(1, 7))
        
        if choice == 1:
            add_book(library)
        elif choice == 2:
            remove_book(library)
        elif choice == 3:
            search_books(library)
        elif choice == 4:
            display_all_books(library)
        elif choice == 5:
            display_statistics(library)
        elif choice == 6:
            save_library(library)
            print("\nLibrary saved to file. Goodbye!")
            break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()