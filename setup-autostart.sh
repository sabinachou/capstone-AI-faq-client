#!/bin/bash

# Setup Auto-Start for AI FAQ System
# Setup auto-start for AI FAQ system on boot

echo "🚀 Setting up Auto-Start for AI FAQ System"
echo "=========================================="

# Check if it's macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Detected macOS, setting up LaunchAgent..."
    
    # Create LaunchAgent directory
    LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
    mkdir -p "$LAUNCH_AGENTS_DIR"
    
    # Get absolute path of current script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    AUTO_START_SCRIPT="$SCRIPT_DIR/auto-start.sh"
    
    # Create LaunchAgent plist file
    cat > "$LAUNCH_AGENTS_DIR/com.aifaq.autostart.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aifaq.autostart</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$AUTO_START_SCRIPT</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/logs/launchd_error.log</string>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF
    
    # Set permissions
    chmod 644 "$LAUNCH_AGENTS_DIR/com.aifaq.autostart.plist"
    
    # Load LaunchAgent
    launchctl load "$LAUNCH_AGENTS_DIR/com.aifaq.autostart.plist"
    
    echo "✅ LaunchAgent created and loaded successfully!"
    echo "📁 LaunchAgent file: $LAUNCH_AGENTS_DIR/com.aifaq.autostart.plist"
    echo "🔄 The system will now start automatically on login"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detected Linux, setting up systemd service..."
    
    # Get absolute path of current script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    AUTO_START_SCRIPT="$SCRIPT_DIR/auto-start.sh"
    
    # Create systemd service file
    sudo tee /etc/systemd/system/aifaq.service > /dev/null << EOF
[Unit]
Description=AI FAQ System
After=network.target

[Service]
Type=forking
User=$USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=/bin/bash $AUTO_START_SCRIPT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd configuration
    sudo systemctl daemon-reload
    
    # Enable service
    sudo systemctl enable aifaq.service
    
    echo "✅ Systemd service created and enabled successfully!"
    echo "📁 Service file: /etc/systemd/system/aifaq.service"
    echo "🔄 The system will now start automatically on boot"
    echo "📋 To manage the service:"
    echo "   Start: sudo systemctl start aifaq"
    echo "   Stop: sudo systemctl stop aifaq"
    echo "   Status: sudo systemctl status aifaq"
    
else
    echo "❌ Unsupported operating system: $OSTYPE"
    echo "💡 Please manually set up auto-start for your OS"
    exit 1
fi

# Create log directory
mkdir -p logs

echo ""
echo "🎉 Auto-start setup completed!"
echo "📝 Logs will be saved in the logs/ directory"
echo "🔄 Your AI FAQ system will now start automatically"
echo ""
echo "📋 Manual commands:"
echo "   Start: ./auto-start.sh"
echo "   Stop: ./stop-services.sh"
echo "   Check status: ps aux | grep -E 'python3 app.py|npm start'"
