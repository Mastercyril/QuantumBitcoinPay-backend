# QUANTUM A.I. DEPLOYMENT GUIDE
## Complete Step-by-Step Instructions

**Created by:** Joseph Dougherty, 13th Chamber LLC  
**Date:** January 16, 2026

## STEP 1: PREPARE YOUR SYSTEM

### 1.1 Check OneDrive Setup
1. Open OneDrive on your Dell
2. Verify it's syncing properly (green checkmark on taskbar icon)
3. Note your OneDrive path (usually `C:\Users\[YourName]\OneDrive`)
4. Create folder: `OneDrive\quantum Ai`

### 1.2 Check Google Drive Setup
1. Open Google Drive Desktop app
2. Verify it's syncing properly
3. Note your Google Drive path (usually `C:\Users\[YourName]\Google Drive`)
4. Create folder: `Google Drive\quantum Ai`

### 1.3 Install Python (if needed)
1. Download Python 3.11 from python.org
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Complete installation

## STEP 2: ORGANIZE YOUR FILES

### 2.1 Create Main Directory
1. Open File Explorer
2. Navigate to `C:\`
3. Create folder: `QuantumAI`

### 2.2 Create Subdirectories
Inside `C:\QuantumAI\`, create these folders:
- `core`
- `gui`
- `config`
- `storage`
- `logs`

### 2.3 Place Files in Correct Locations

**In `C:\QuantumAI\`:**
- QuantumAI_Installer.py
- QuantumAI.py (main launcher)
- README.md

**In `C:\QuantumAI\core\`:**
- quantum_ai_core.py
- personality_system.py
- memory_manager.py
- learning_engine.py
- ethics_framework.py

**In `C:\QuantumAI\gui\`:**
- chat_interface.py

## STEP 3: INSTALL DEPENDENCIES

### 3.1 Open Command Prompt
1. Press Windows Key + R
2. Type: `cmd`
3. Press Enter

### 3.2 Navigate to QuantumAI Directory
```
cd C:\QuantumAI
```

### 3.3 Install Required Packages
```
pip install requests
pip install tkinter
```

## STEP 4: RUN INSTALLATION SCRIPT

### 4.1 Execute Installer
In Command Prompt:
```
python QuantumAI_Installer.py
```

### 4.2 Verify Installation
You should see:
```
✓ Created: C:\QuantumAI\core
✓ Created: C:\QuantumAI\storage\local_memory
... (more lines)
✓ Configuration files created
✓ Desktop shortcut ready
INSTALLATION COMPLETE ✓
```

## STEP 5: FIRST LAUNCH

### 5.1 Launch the Application
**Option A:** Double-click desktop shortcut "Quantum A.I."
**Option B:** In Command Prompt:
```
cd C:\QuantumAI
python QuantumAI.py
```

### 5.2 First Launch Behavior
The system will:
1. Initialize memory banks
2. Create personality profiles
3. Generate ethical framework
4. Connect to OneDrive and Google Drive
5. Open GUI chat interface

## STEP 6: USING THE SYSTEM

### 6.1 Chat Interface Overview
- **Top Panel:** Instructions & Web Learning
  - URL input: Add websites for AI to learn from
  - Command input: Execute system commands
- **Middle Panel:** Chat conversation area
- **Bottom Panel:** Your message input
- **Bottom Buttons:** 
  - New Conversation: Start fresh with new personality
  - View Memory: See memory statistics
  - Learning Stats: View learning progress
  - Exit: Close application

### 6.2 Starting First Conversation
1. Type "hello" in input box
2. Press Enter or click "Send"
3. AI will respond with random personality
4. Personality stays same until conversation ends
5. Click "New Conversation" for different personality

### 6.3 Teaching the AI
**From Websites:**
1. Paste URL in "Learn from URL" field
2. Click "Load"
3. AI extracts and stores knowledge

**From Conversation:**
- AI automatically learns from every interaction
- Builds pattern recognition
- Improves responses over time

## STEP 7: CLOUD SYNC VERIFICATION

### 7.1 Check OneDrive
1. Open OneDrive folder
2. Navigate to `quantum Ai`
3. Should see `memory_backup` folder
4. Check for `memory_database.json` file

### 7.2 Check Google Drive
1. Open Google Drive folder
2. Navigate to `quantum Ai`
3. Should see `memory_backup` folder
4. Check for `memory_database.json` file

### 7.3 Auto-Sync Behavior
- Memory syncs after every conversation
- Syncs to both OneDrive and Google Drive
- Can restore from either location

## STEP 8: CREATING EXE FILE (Optional)

### 8.1 Install PyInstaller
```
pip install pyinstaller
```

### 8.2 Create EXE
```
cd C:\QuantumAI
pyinstaller --onefile --windowed --name="QuantumAI" QuantumAI.py
```

### 8.3 Find Your EXE
- Located in: `C:\QuantumAI\dist\QuantumAI.exe`
- Can move this anywhere
- Double-click to run

## TROUBLESHOOTING

### Problem: "Module not found"
**Solution:** Reinstall dependencies:
```
pip install --upgrade requests tkinter
```

### Problem: "Can't connect to OneDrive"
**Solution:** 
1. Verify OneDrive is running
2. Check folder path in `config/cloud_paths.json`
3. Manually update path if needed

### Problem: "Personality not changing"
**Solution:** Click "New Conversation" button

### Problem: "Memory not syncing"
**Solution:**
1. Check OneDrive/Google Drive are running
2. Verify folder permissions
3. Check internet connection

## CUSTOMIZATION

### Editing Personalities
Edit: `C:\QuantumAI\core\personality_system.py`
- Modify greetings
- Change traits
- Add new personalities (keep total at 10)

### Adjusting Ethics
Edit: `C:\QuantumAI\core\ethics_framework.py`
- Modify core principles
- Add/remove prohibited topics
- Adjust priority levels

### Changing Cloud Paths
Edit: `C:\QuantumAI\config\cloud_paths.json`
- Update OneDrive path
- Update Google Drive path
- Add additional backup locations

## SUPPORT

For issues or questions:
- Contact: 13th Chamber LLC
- Email: [Your email]
- GitHub: github.com/[your-repo]/quantum-ai-core

## FILE CHECKLIST

Before deployment, verify you have:
- [ ] QuantumAI_Installer.py
- [ ] QuantumAI.py (main launcher)
- [ ] quantum_ai_core.py
- [ ] personality_system.py
- [ ] memory_manager.py
- [ ] learning_engine.py
- [ ] ethics_framework.py
- [ ] chat_interface.py
- [ ] README.md
- [ ] This deployment guide

## NEXT STEPS

1. Save all files to OneDrive and Google Drive `quantum Ai` folders
2. Follow Step 1-7 above
3. Start using your AI system
4. Monitor learning progress
5. Customize as needed

**System is ready for deployment!**
