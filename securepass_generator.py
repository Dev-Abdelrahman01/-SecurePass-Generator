#!/usr/bin/env python3
"""
SecurePass Generator - A Password Generation Utility
A beginner-friendly Python project demonstrating:
- String manipulation and character sets
- Random module for secure password generation
- User input validation
- Functions and modular programming
- Command-line interface design
"""

import random
import string
import secrets

def display_banner():
    """Display the application banner."""
    print("=" * 50)
    print("        SECUREPASS GENERATOR")
    print("     Strong Password Generator")
    print("=" * 50)
    print()

def get_password_length():
    """Get the desired password length from the user."""
    while True:
        try:
            length = int(input("Enter the desired password length (8-128): "))
            if 8 <= length <= 128:
                return length
            else:
                print("Password length must be between 8 and 128 characters.")
        except ValueError:
            print("Please enter a valid number.")

def get_user_preferences():
    """Get user preferences for password composition."""
    print("\nPassword Composition Options:")
    print("(Press Enter for default 'yes' or type 'n' for no)")
    
    # Get preferences with default values
    include_uppercase = get_yes_no_input("Include uppercase letters (A-Z)?", default=True)
    include_lowercase = get_yes_no_input("Include lowercase letters (a-z)?", default=True)
    include_numbers = get_yes_no_input("Include numbers (0-9)?", default=True)
    include_symbols = get_yes_no_input("Include symbols (!@#$%^&*)?", default=True)
    
    # Ensure at least one character type is selected
    if not any([include_uppercase, include_lowercase, include_numbers, include_symbols]):
        print("\nAt least one character type must be selected!")
        print("Defaulting to include all character types.")
        return True, True, True, True
    
    return include_uppercase, include_lowercase, include_numbers, include_symbols

def get_yes_no_input(prompt, default=True):
    """Get a yes/no input from the user with a default value."""
    default_text = " [Y/n]" if default else " [y/N]"
    user_input = input(prompt + default_text + ": ").strip().lower()
    
    if user_input == "":
        return default
    elif user_input in ['y', 'yes']:
        return True
    elif user_input in ['n', 'no']:
        return False
    else:
        print("Invalid input. Using default.")
        return default

def build_character_set(include_uppercase, include_lowercase, include_numbers, include_symbols):
    """Build the character set based on user preferences."""
    characters = ""
    
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    return characters

def generate_password(length, characters):
    """Generate a secure password using the specified character set."""
    # Use secrets module for cryptographically secure random generation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def generate_multiple_passwords(length, characters, count=5):
    """Generate multiple password options."""
    passwords = []
    for i in range(count):
        password = generate_password(length, characters)
        passwords.append(password)
    return passwords

def calculate_password_strength(password):
    """Calculate and display password strength information."""
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    # Calculate character set size
    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_symbol:
        charset_size += 23
    
    # Estimate entropy (bits of randomness)
    import math
    entropy = length * math.log2(charset_size) if charset_size > 0 else 0
    
    # Determine strength level
    if entropy < 30:
        strength = "Very Weak"
    elif entropy < 50:
        strength = "Weak"
    elif entropy < 70:
        strength = "Moderate"
    elif entropy < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return {
        'length': length,
        'has_lower': has_lower,
        'has_upper': has_upper,
        'has_digit': has_digit,
        'has_symbol': has_symbol,
        'charset_size': charset_size,
        'entropy': entropy,
        'strength': strength
    }

def display_password_analysis(password):
    """Display detailed password analysis."""
    analysis = calculate_password_strength(password)
    
    print(f"\n{'='*50}")
    print("PASSWORD ANALYSIS")
    print(f"{'='*50}")
    print(f"Length: {analysis['length']} characters")
    print(f"Character Set Size: {analysis['charset_size']}")
    print(f"Estimated Entropy: {analysis['entropy']:.1f} bits")
    print(f"Strength Level: {analysis['strength']}")
    print()
    print("Character Types Used:")
    print(f"  ✓ Lowercase letters: {'Yes' if analysis['has_lower'] else 'No'}")
    print(f"  ✓ Uppercase letters: {'Yes' if analysis['has_upper'] else 'No'}")
    print(f"  ✓ Numbers: {'Yes' if analysis['has_digit'] else 'No'}")
    print(f"  ✓ Symbols: {'Yes' if analysis['has_symbol'] else 'No'}")

def save_password_to_file(password, filename="generated_password.txt"):
    """Save the generated password to a file."""
    try:
        with open(filename, 'w') as file:
            file.write(f"Generated Password: {password}\n")
            file.write(f"Generated on: {get_current_timestamp()}\n")
        print(f"\nPassword saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving password: {e}")
        return False

def get_current_timestamp():
    """Get the current timestamp as a string."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def display_security_tips():
    """Display password security tips."""
    print(f"\n{'='*50}")
    print("PASSWORD SECURITY TIPS")
    print(f"{'='*50}")
    tips = [
        "• Never reuse passwords across multiple accounts",
        "• Use a password manager to store your passwords securely",
        "• Enable two-factor authentication when available",
        "• Change passwords regularly, especially for important accounts",
        "• Never share your passwords with others",
        "• Avoid using personal information in passwords",
        "• Use different passwords for work and personal accounts"
    ]
    
    for tip in tips:
        print(tip)
    print()

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Generate a single password")
        print("2. Generate multiple password options")
        print("3. View security tips")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            generate_single_password()
        elif choice == '2':
            generate_multiple_password_options()
        elif choice == '3':
            display_security_tips()
        elif choice == '4':
            print("\nThank you for using SecurePass Generator!")
            print("Stay secure!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

def generate_single_password():
    """Generate and display a single password."""
    print(f"\n{'='*50}")
    print("SINGLE PASSWORD GENERATION")
    print(f"{'='*50}")
    
    # Get user preferences
    length = get_password_length()
    include_upper, include_lower, include_numbers, include_symbols = get_user_preferences()
    
    # Build character set and generate password
    characters = build_character_set(include_upper, include_lower, include_numbers, include_symbols)
    password = generate_password(length, characters)
    
    # Display results
    print(f"\n{'='*50}")
    print("GENERATED PASSWORD")
    print(f"{'='*50}")
    print(f"Your password: {password}")
    
    # Show analysis
    display_password_analysis(password)
    
    # Ask if user wants to save
    save_choice = get_yes_no_input("\nSave password to file?", default=False)
    if save_choice:
        save_password_to_file(password)

def generate_multiple_password_options():
    """Generate and display multiple password options."""
    print(f"\n{'='*50}")
    print("MULTIPLE PASSWORD OPTIONS")
    print(f"{'='*50}")
    
    # Get user preferences
    length = get_password_length()
    include_upper, include_lower, include_numbers, include_symbols = get_user_preferences()
    
    # Build character set and generate passwords
    characters = build_character_set(include_upper, include_lower, include_numbers, include_symbols)
    passwords = generate_multiple_passwords(length, characters, count=5)
    
    # Display results
    print(f"\n{'='*50}")
    print("PASSWORD OPTIONS")
    print(f"{'='*50}")
    for i, password in enumerate(passwords, 1):
        print(f"{i}. {password}")
    
    # Let user select one for analysis
    while True:
        try:
            choice = int(input(f"\nSelect a password for analysis (1-5): "))
            if 1 <= choice <= 5:
                selected_password = passwords[choice - 1]
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nSelected password: {selected_password}")
    display_password_analysis(selected_password)
    
    # Ask if user wants to save
    save_choice = get_yes_no_input("\nSave selected password to file?", default=False)
    if save_choice:
        save_password_to_file(selected_password)

def main():
    """Main application entry point."""
    display_banner()
    print("Welcome to SecurePass Generator!")
    print("Create strong, secure passwords for all your accounts.")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please restart the program.")

if __name__ == "__main__":
    main()

