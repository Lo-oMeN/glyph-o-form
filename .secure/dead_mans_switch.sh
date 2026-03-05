#!/bin/bash
# Dead Man's Switch for OpenClaw Workspace
# Auto-publishes to GitHub if no contact for 7 days
# STATUS: DISARMED (manual activation required)

set -euo pipefail

# Configuration
WORKSPACE_DIR="/root/.openclaw/workspace"
HEARTBEAT_FILE="$WORKSPACE_DIR/.secure/last_heartbeat"
PUBLISH_TRIGGER_DAYS=7
PUBLISH_TRIGGER_SECONDS=$((PUBLISH_TRIGGER_DAYS * 24 * 60 * 60))
LOG_FILE="$WORKSPACE_DIR/.secure/dms.log"
LOCK_FILE="$WORKSPACE_DIR/.secure/dms.lock"
ARMED_FLAG="$WORKSPACE_DIR/.secure/DMS_ARMED"

# GitHub Configuration (to be configured before arming)
GITHUB_REPO="${GITHUB_REPO:-}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
GITHUB_BRANCH="${GITHUB_BRANCH:-main}"

# Logging function
log() {
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] $1" | tee -a "$LOG_FILE"
}

# Check if DMS is armed
check_armed() {
    if [ ! -f "$ARMED_FLAG" ]; then
        log "DMS is DISARMED. Exiting."
        exit 0
    fi
    log "DMS is ARMED. Proceeding with checks..."
}

# Update heartbeat (called to reset timer)
update_heartbeat() {
    date +%s > "$HEARTBEAT_FILE"
    log "Heartbeat updated. Timer reset."
}

# Check if trigger condition is met
check_trigger() {
    if [ ! -f "$HEARTBEAT_FILE" ]; then
        log "No heartbeat file found. Creating initial heartbeat."
        update_heartbeat
        return 1
    fi
    
    local last_heartbeat
    local current_time
    local elapsed
    
    last_heartbeat=$(cat "$HEARTBEAT_FILE")
    current_time=$(date +%s)
    elapsed=$((current_time - last_heartbeat))
    
    log "Last heartbeat: $(date -u -d "@$last_heartbeat" "+%Y-%m-%d %H:%M:%S UTC")"
    log "Elapsed time: $elapsed seconds ($((elapsed / 86400)) days)"
    
    if [ "$elapsed" -ge "$PUBLISH_TRIGGER_SECONDS" ]; then
        log "TRIGGER CONDITION MET: $elapsed seconds >= $PUBLISH_TRIGGER_SECONDS seconds"
        return 0
    else
        log "Trigger condition NOT met. Remaining: $((PUBLISH_TRIGGER_SECONDS - elapsed)) seconds"
        return 1
    fi
}

# Decrypt files for publishing
decrypt_files() {
    log "Decrypting files for publication..."
    
    local passphrase
    passphrase=$(cat "$WORKSPACE_DIR/.secure/passphrase.key")
    
    cd "$WORKSPACE_DIR"
    
    for enc_file in *.enc memory/*.enc 2>/dev/null; do
        if [ -f "$enc_file" ]; then
            local output_file="${enc_file%.enc}"
            openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 -in "$enc_file" -out "$output_file" -pass pass:"$passphrase"
            log "Decrypted: $enc_file"
        fi
    done
}

# Prepare release package
prepare_package() {
    log "Preparing release package..."
    
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local release_dir="$WORKSPACE_DIR/.secure/release_$timestamp"
    
    mkdir -p "$release_dir"
    
    # Copy all relevant files
    cp -r "$WORKSPACE_DIR"/*.md "$release_dir/" 2>/dev/null || true
    cp -r "$WORKSPACE_DIR/memory" "$release_dir/" 2>/dev/null || true
    cp -r "$WORKSPACE_DIR/.secure" "$release_dir/" 2>/dev/null || true
    
    # Create manifest
    cat > "$release_dir/MANIFEST.txt" << EOF
Dead Man's Switch Release
=========================
Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Trigger: $PUBLISH_TRIGGER_DAYS days of silence
Files Included:
- All specifications (*.enc files decrypted)
- All research outputs
- All memory files
- Security protocols

This release was automatically triggered.
EOF
    
    echo "$release_dir"
}

# Publish to GitHub
publish_to_github() {
    local release_dir="$1"
    
    if [ -z "$GITHUB_REPO" ] || [ -z "$GITHUB_TOKEN" ]; then
        log "ERROR: GitHub configuration missing. Cannot publish."
        return 1
    fi
    
    log "Publishing to GitHub: $GITHUB_REPO"
    
    # Create a temporary git repo
    cd "$release_dir"
    git init
    git add .
    git commit -m "Dead Man's Switch Release - $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
    
    # Push to GitHub
    git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_REPO.git"
    git push -u origin "$GITHUB_BRANCH" --force
    
    log "Published to GitHub successfully"
}

# Disarm the DMS
disarm() {
    rm -f "$ARMED_FLAG"
    log "DMS DISARMED. Auto-publish disabled."
}

# Arm the DMS
arm() {
    if [ -z "$GITHUB_REPO" ]; then
        echo "ERROR: GITHUB_REPO not configured"
        exit 1
    fi
    if [ -z "$GITHUB_TOKEN" ]; then
        echo "ERROR: GITHUB_TOKEN not configured"
        exit 1
    fi
    
    touch "$ARMED_FLAG"
    update_heartbeat
    log "DMS ARMED. Auto-publish will trigger after $PUBLISH_TRIGGER_DAYS days of silence."
    log "Repository: $GITHUB_REPO"
    log "Branch: $GITHUB_BRANCH"
}

# Abort trigger (manual reset)
abort() {
    update_heartbeat
    log "DMS ABORTED. Timer reset."
}

# Main execution
main() {
    # Ensure .secure directory exists
    mkdir -p "$WORKSPACE_DIR/.secure"
    
    case "${1:-check}" in
        arm)
            arm
            ;;
        disarm)
            disarm
            ;;
        abort)
            abort
            ;;
        heartbeat)
            update_heartbeat
            ;;
        check)
            check_armed
            if check_trigger; then
                log "EXECUTING DEAD MAN'S SWITCH..."
                
                # Create lock file
                if [ -f "$LOCK_FILE" ]; then
                    log "Lock file exists. Another instance may be running."
                    exit 1
                fi
                touch "$LOCK_FILE"
                
                # Execute publish sequence
                decrypt_files
                local release_dir
                release_dir=$(prepare_package)
                publish_to_github "$release_dir"
                
                # Cleanup
                rm -f "$LOCK_FILE"
                disarm
                
                log "Dead Man's Switch executed successfully."
            fi
            ;;
        status)
            if [ -f "$ARMED_FLAG" ]; then
                echo "Status: ARMED"
                if [ -f "$HEARTBEAT_FILE" ]; then
                    local last_heartbeat
                    local current_time
                    local elapsed
                    last_heartbeat=$(cat "$HEARTBEAT_FILE")
                    current_time=$(date +%s)
                    elapsed=$((current_time - last_heartbeat))
                    echo "Last heartbeat: $(date -u -d "@$last_heartbeat" "+%Y-%m-%d %H:%M:%S UTC")"
                    echo "Elapsed: $((elapsed / 86400)) days, $(( (elapsed % 86400) / 3600 )) hours"
                    echo "Trigger in: $(( (PUBLISH_TRIGGER_SECONDS - elapsed) / 86400 )) days"
                fi
                echo "Repository: ${GITHUB_REPO:-"Not configured"}"
            else
                echo "Status: DISARMED"
            fi
            ;;
        *)
            echo "Usage: $0 {arm|disarm|abort|heartbeat|check|status}"
            echo ""
            echo "Commands:"
            echo "  arm       - Arm the dead man's switch (requires GITHUB_REPO and GITHUB_TOKEN)"
            echo "  disarm    - Disarm the dead man's switch"
            echo "  abort     - Reset timer (prevents trigger)"
            echo "  heartbeat - Update last contact timestamp"
            echo "  check     - Check if trigger condition is met (default)"
            echo "  status    - Show current DMS status"
            exit 1
            ;;
    esac
}

main "$@"
