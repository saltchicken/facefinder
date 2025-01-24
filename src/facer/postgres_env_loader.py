from pathlib import Path
import os
from dotenv import load_dotenv

def get_env_file_path():
    if os.name == "nt":  # Windows
        config_dir = Path(os.getenv("APPDATA", "C:\\Users\\Default\\AppData\\Roaming")) / "facer"
    else:  # Linux/macOS
        config_dir = Path(os.getenv("XDG_CONFIG_HOME", "~/.config")).expanduser() / "facer"

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / ".env"

def load_custom_env():
    env_file_path = get_env_file_path()
    # Load the .env file from the custom location
    if env_file_path.exists():
        load_dotenv(env_file_path)  # Explicitly pass the path to the .env file
        print(f"✅ Loaded environment variables from {env_file_path}")
        return True
    else:
        print(f"⚠️  No .env file found at {env_file_path}. Please create one.")
        return False

def check_or_create_env():
    env_file_path = get_env_file_path()

    # List of required environment variables (you can add more as needed)
    required_vars = [
        ("DB_HOST", "localhost"),
        ("DB_PORT", "5432"),
        ("DB_USER", "postgres"),
        ("DB_NAME", "postgres"),
        # ("DB_PASSWORD", "password"),
    ]

    # Check if the .env file exists
    if not load_custom_env():
        user_input = input("Would you like to create one now? (y/n): ").strip().lower()

        if user_input == "y":
            # Open the .env file for writing
            with open(env_file_path, "w") as env_file:
                print(f"✅ .env file created at {os.path.abspath(env_file_path)}")

                # Prompt the user for each variable
                for var_name, default_value in required_vars:
                    user_value = input(
                        f"Please set the value for {var_name} (default: {default_value}): "
                    ).strip()

                    # Use the default if the user provides no input
                    if not user_value:
                        user_value = default_value

                    # Write the variable to the .env file
                    env_file.write(f"{var_name}={user_value}\n")
                    print(f"✅ {var_name} set.")

                print("All variables have been set.")
            print("Edit this file with your configuration.")
            load_custom_env()
        else:
            print("❌ Running in offline mode. Use command `connect` to go to online mode with database")
            exit(1)  # Exit if the user does not want to create the file

