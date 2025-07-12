#!/usr/bin/env python3
"""
SoundManager - Audio feedback system for Emphizor
Handles loading and playing sound effects for UI feedback
"""

import os
from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import QSoundEffect
from logger_config import get_logger

# Set up logger for this module
logger = get_logger(__name__)

class SoundManager(QObject):
    """Manages sound effects for the application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sounds = {}
        self.enabled = True
        self.volume = 0.3  # Default volume (30%)
        self.sounds_directory = "sounds"
        
        # Initialize sound effects
        self.init_sounds()
        logger.info("SoundManager initialized")
    
    def init_sounds(self):
        """Initialize all sound effects"""
        # Define sound effects and their file names (minimal set)
        sound_definitions = {
            'click': 'click.wav',        # General UI interactions
            'success': 'success.wav',    # Positive feedback (card added, correct answer, match found)
            'error': 'error.wav',        # Negative feedback (errors, wrong answers)
            'flip': 'flip.wav'           # Card/game interactions
        }
        
        # Create sound effects
        for sound_name, filename in sound_definitions.items():
            try:
                sound_effect = QSoundEffect(self)
                sound_path = os.path.join(self.sounds_directory, filename)
                
                # Check if file exists
                if os.path.exists(sound_path):
                    sound_effect.setSource(QUrl.fromLocalFile(os.path.abspath(sound_path)))
                    sound_effect.setVolume(self.volume)
                    self.sounds[sound_name] = sound_effect
                    logger.debug(f"Loaded sound effect: {sound_name}")
                else:
                    logger.warning(f"Sound file not found: {sound_path}")
                    
            except Exception as e:
                logger.error(f"Failed to load sound effect {sound_name}: {str(e)}")
    
    def play_sound(self, sound_name):
        """Play a sound effect by name"""
        if not self.enabled:
            return
            
        if sound_name in self.sounds:
            try:
                sound_effect = self.sounds[sound_name]
                if sound_effect.status() == QSoundEffect.Status.Ready:
                    sound_effect.play()
                    logger.debug(f"Playing sound: {sound_name}")
                else:
                    logger.warning(f"Sound not ready: {sound_name}")
            except Exception as e:
                logger.error(f"Failed to play sound {sound_name}: {str(e)}")
        else:
            logger.warning(f"Sound effect not found: {sound_name}")
    
    def set_volume(self, volume):
        """Set the volume for all sound effects (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        for sound_effect in self.sounds.values():
            sound_effect.setVolume(self.volume)
        logger.info(f"Volume set to: {self.volume}")
    
    def set_enabled(self, enabled):
        """Enable or disable all sound effects"""
        self.enabled = enabled
        logger.info(f"Sound effects {'enabled' if enabled else 'disabled'}")
    
    def is_enabled(self):
        """Check if sound effects are enabled"""
        return self.enabled
    
    def get_volume(self):
        """Get the current volume level"""
        return self.volume
    
    # Convenience methods for common sounds
    def play_click(self):
        """Play UI click sound"""
        self.play_sound('click')
    
    def play_success(self):
        """Play success sound"""
        self.play_sound('success')
    
    def play_error(self):
        """Play error sound"""
        self.play_sound('error')
    
    def play_flip(self):
        """Play card flip sound"""
        self.play_sound('flip') 