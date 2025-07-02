from base_classes import App, FullCard
from fsrs import Card

def main():
    print("=== Emphizor App Demo ===")
    
    app = App()
    
    while True:
        print("\n1. Login/Signup")
        print("2. Add card")
        print("3. View cards")
        print("4. Save user")
        print("5. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            try:
                name = input("Name (for new users): ").strip()
                if not name:
                    name = None
                
                app.login_or_signup(email, password, name)
                if app.user:
                    print(f"Successfully logged in as {app.user.name}")
                else:
                    print("Login failed")
                
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            if not app.user:
                print("Please login first")
                continue
                
            question = input("Question: ").strip()
            answer = input("Answer: ").strip()
            tags_input = input("Tags (comma-separated): ").strip()
            tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            
            card = Card()
            full_card = FullCard(card, question, answer, tags)
            app.user.full_cards.append(full_card)
            print("Card added successfully")
        
        elif choice == "3":
            if not app.user:
                print("Please login first")
                continue
                
            if not app.user.full_cards:
                print("No cards found")
            else:
                print(f"\n{app.user.name}'s Cards:")
                for i, card in enumerate(app.user.full_cards, 1):
                    print(f"{i}. Q: {card.question}")
                    print(f"   A: {card.answer}")
                    print(f"   Tags: {', '.join(card.tags)}")
        
        elif choice == "4":
            if not app.user:
                print("Please login first")
                continue
                
            try:
                app.save_user()
                print("User data saved successfully")
            except Exception as e:
                print(f"Error saving: {e}")
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()


