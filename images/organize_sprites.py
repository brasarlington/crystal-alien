"""
Sprite Organizer for Crystal Quest
Automatically copies and renames Kenney sprites to the correct structure

INSTRUCTIONS:
1. Download Kenney's New Platformer Pack from:
   https://kenney.nl/assets/new-platformer-pack

2. Extract the ZIP file (you'll get a folder like "images" or similar)

3. Edit KENNEY_PATH below to point to the extracted folder

4. Run: python organize_sprites.py

5. Run your game: python game_with_sprites.py
"""

import os
import shutil
from pathlib import Path

# ============================================================================
# CONFIGURATION - EDIT THIS!
# ============================================================================

# Path to your extracted Kenney pack
# Example Windows: "C:/Users/YourName/Downloads/images"
# Example Mac/Linux: "/Users/YourName/Downloads/images"
# IMPORTANT: This should point to the "images" folder that contains Sprites/
KENNEY_PATH = "images"

# Your images folder (relative to this script)
IMAGES_PATH = "images"

# ============================================================================
# FUNCTIONS
# ============================================================================

def create_images_folder():
    """Create the images folder if it doesn't exist"""
    Path(IMAGES_PATH).mkdir(exist_ok=True)
    print(f"✓ Created/verified images folder: {IMAGES_PATH}")

def copy_sprite(source_path, dest_name):
    """Copy and rename a sprite file"""
    source = Path(KENNEY_PATH) / source_path
    dest = Path(IMAGES_PATH) / dest_name
    
    if not source.exists():
        print(f"⚠️  Not found: {source_path}")
        print(f"   Looking for: {source}")
        return False
    
    try:
        shutil.copy2(source, dest)
        print(f"✓ Copied: {dest_name}")
        return True
    except Exception as e:
        print(f"✗ Error copying {source_path}: {e}")
        return False

def verify_kenney_path():
    """Check if the Kenney path exists"""
    if not Path(KENNEY_PATH).exists():
        print("=" * 70)
        print("ERROR: Kenney pack not found!")
        print("=" * 70)
        print(f"Looking for: {KENNEY_PATH}")
        print()
        print("Please:")
        print("1. Download the pack from: https://kenney.nl/assets/new-platformer-pack")
        print("2. Extract the ZIP file")
        print("3. Edit KENNEY_PATH in this script to point to the 'images' folder")
        print()
        print("Example paths:")
        print("  Windows: 'C:/Users/YourName/Downloads/images'")
        print("  Mac:     '/Users/YourName/Downloads/images'")
        print("  Linux:   '/home/yourname/Downloads/images'")
        print()
        print("The path should contain the 'Sprites' folder inside.")
        print("=" * 70)
        return False
    
    # Verify Sprites folder exists
    sprites_path = Path(KENNEY_PATH) / "Sprites"
    if not sprites_path.exists():
        print("=" * 70)
        print("ERROR: 'Sprites' folder not found!")
        print("=" * 70)
        print(f"Looking for: {sprites_path}")
        print()
        print("Your KENNEY_PATH should point to the 'images' folder that contains:")
        print("  - Sprites/")
        print("  - Vector/")
        print("  - Spritesheets/")
        print("  - etc.")
        print()
        print("Current KENNEY_PATH: " + str(Path(KENNEY_PATH).absolute()))
        print("=" * 70)
        return False
    
    return True

def copy_and_duplicate_sprites():
    """Copy sprites and create duplicates for animation frames"""
    
    # First, copy unique sprites
    unique_sprites = {
        # Player - unique files
        "Sprites/Characters/Default/character_yellow_idle.png": "player_idle_right_0.png",
        "Sprites/Characters/Default/character_yellow_front.png": "player_idle_right_1.png",
        "Sprites/Characters/Default/character_yellow_walk_a.png": "player_walk_right_0.png",
        "Sprites/Characters/Default/character_yellow_walk_b.png": "player_walk_right_1.png",
        "Sprites/Characters/Default/character_yellow_jump.png": "player_jump_right_0.png",
        "Sprites/Characters/Default/character_yellow_duck.png": "player_jump_right_1.png",
        
        # Enemies - unique files
        "Sprites/Enemies/Default/slime_normal_walk_a.png": "slime_move_right_0.png",
        "Sprites/Enemies/Default/slime_normal_walk_b.png": "slime_move_right_1.png",
        "Sprites/Enemies/Default/slime_normal_rest.png": "slime_move_right_2.png",
        "Sprites/Enemies/Default/slime_normal_flat.png": "slime_move_right_3.png",
        "Sprites/Enemies/Default/fly_a.png": "bat_fly_0.png",
        "Sprites/Enemies/Default/fly_b.png": "bat_fly_1.png",
        "Sprites/Enemies/Default/fly_rest.png": "bat_fly_2.png",
        
        # Items
        "Sprites/Tiles/Default/gem_blue.png": "crystal.png",
        "Sprites/Tiles/Default/heart.png": "heart.png",
        "Sprites/Tiles/Default/terrain_grass_block_top.png": "platform_tile.png",
        "Sprites/Tiles/Default/flag_blue_b.png": "goal_flag.png",
        
        # Backgrounds
        "Sprites/Backgrounds/Default/background_solid_sky.png": "background_game.png",
        "Sprites/Backgrounds/Default/background_color_hills.png": "background_menu.png",
    }
    
    success_count = 0
    fail_count = 0
    
    # Copy unique sprites
    for source, dest in unique_sprites.items():
        if copy_sprite(source, dest):
            success_count += 1
        else:
            fail_count += 1
    
    # Now create duplicates for looping animations
    duplicates = [
        # Player idle frames (loop idle animation)
        ("player_idle_right_0.png", "player_idle_right_2.png"),
        ("player_idle_right_1.png", "player_idle_right_3.png"),
        
        # Player walk frames (loop walk animation)
        ("player_walk_right_0.png", "player_walk_right_2.png"),
        ("player_walk_right_1.png", "player_walk_right_3.png"),
        ("player_walk_right_0.png", "player_walk_right_4.png"),
        ("player_walk_right_1.png", "player_walk_right_5.png"),
        
        # Bat fly frames (loop fly animation)
        ("bat_fly_0.png", "bat_fly_3.png"),
    ]
    
    print()
    print("Creating duplicate frames for animation loops...")
    print("-" * 70)
    
    for source_name, dest_name in duplicates:
        source = Path(IMAGES_PATH) / source_name
        dest = Path(IMAGES_PATH) / dest_name
        
        if source.exists():
            try:
                shutil.copy2(source, dest)
                print(f"✓ Duplicated: {source_name} → {dest_name}")
                success_count += 1
            except Exception as e:
                print(f"✗ Error duplicating {source_name}: {e}")
                fail_count += 1
        else:
            print(f"⚠️  Source not found for duplication: {source_name}")
            fail_count += 1
    
    print("-" * 70)
    
    return success_count, fail_count
def main():
    """Main function to organize sprites"""
    print("=" * 70)
    print("Crystal Quest - Sprite Organizer")
    print("=" * 70)
    print()
    
    # Verify Kenney pack exists
    if not verify_kenney_path():
        return
    
    print(f"✓ Found Kenney pack at: {Path(KENNEY_PATH).absolute()}")
    print()
    
    # Create images folder
    create_images_folder()
    print()
    
    # Copy all sprites and create duplicates
    print("Copying sprites from Kenney pack...")
    print("-" * 70)
    
    success_count, fail_count = copy_and_duplicate_sprites()
    
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"✓ Successfully copied: {success_count} files")
    if fail_count > 0:
        print(f"⚠️  Failed/Not found: {fail_count} files")
        print()
        print("Note: Some files might have different names in your pack version.")
        print("The game will use colored rectangles as fallback for missing sprites.")
    print()
    
    # Next steps
    print("=" * 70)
    print("Next Steps")
    print("=" * 70)
    print("1. Run the game:")
    print("   python game_with_sprites.py")
    print()
    print("2. If sprites don't appear:")
    print("   - Check that 'images' folder contains .png files")
    print("   - Verify file names match exactly")
    print("   - Make sure images are at: images/sprite_name.png")
    print()
    print("3. To add more sprites:")
    print("   - Browse the Kenney pack")
    print("   - Add entries to SPRITE_MAP in this script")
    print("   - Run this script again")
    print()
    print("=" * 70)
    print("Happy gaming! 🎮")
    print("=" * 70)

if __name__ == "__main__":
    main()