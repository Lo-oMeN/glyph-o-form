# Semi-Sovereign Deployment Guide
## Full Autonomous Testing & Deployment

---

## 🚀 QUICK START

### Option 1: Run Locally (Immediate)

```bash
# Start the agent
python3 semi_sovereign_agent.py

# Or run once
python3 semi_sovereign_agent.py --run-once

# Generate report
python3 semi_sovereign_agent.py --report
```

### Option 2: Docker (Recommended)

```bash
# Build image
docker build -t glyphobetics-agent -f docker/Dockerfile .

# Run container
docker run -d \
  -p 8080:8080 \
  -v $(pwd)/reports:/app/reports \
  --name glyph-agent \
  glyphobetics-agent

# View logs
docker logs -f glyph-agent
```

### Option 3: GitHub Actions (Fully Autonomous)

Already configured! Push to master and the pipeline runs automatically.

---

## 📋 WHAT THE AGENT DOES

### Continuous Monitoring
- ✅ Checks for code changes every minute
- ✅ Runs smoke tests on every commit
- ✅ Runs full test suite hourly
- ✅ Generates reports automatically

### Test Coverage
- ✅ HTML validity
- ✅ CSS validity
- ✅ JavaScript syntax
- ✅ Responsive design
- ✅ Accessibility (WCAG)
- ✅ Performance budgets
- ✅ Security scanning

### Auto-Actions
- ✅ Saves detailed reports
- ✅ Sends Telegram notifications
- ✅ Suggests fixes for failures
- ✅ Deploys to staging (optional)

---

## 🔧 CONFIGURATION

Edit `.agent_config.json`:

```json
{
  "autonomous_mode": true,
  "test_on_change": true,
  "auto_deploy_staging": false,
  "alert_on_failure": true,
  "performance_budget": {
    "max_load_time_ms": 2000,
    "max_bundle_size_kb": 500,
    "min_accessibility_score": 0.9
  },
  "notification_channels": ["telegram"],
  "test_schedule": {
    "full_suite": "every_hour",
    "smoke_tests": "every_commit"
  }
}
```

---

## 📊 REPORTS

### Report Location
```
app/reports/
├── report_20260306_120000.json    # Full test report
├── fix_suggestions_20260306.json   # Auto-generated fixes
└── latest_notification.txt         # Latest summary
```

### Report Structure
```json
{
  "timestamp": "2026-03-06T12:00:00",
  "commit": "abc123",
  "summary": {
    "passed": true,
    "score": "95%",
    "duration": "2m30s"
  },
  "tests": {
    "html": {"passed": true, ...},
    "css": {"passed": true, ...},
    "javascript": {"passed": true, ...},
    "responsive": {"passed": true, "score": 0.95},
    "accessibility": {"passed": true, "score": 0.92},
    "performance": {"passed": true, "size_kb": 245},
    "security": {"passed": true, "issues": []}
  },
  "recommendations": [
    "🔧 Add alt text to images...",
    "🔧 Consider lazy loading..."
  ]
}
```

---

## 🔔 NOTIFICATIONS

### Telegram Setup

1. Create bot with @BotFather
2. Get chat ID from @userinfobot
3. Add secrets to GitHub:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### Notification Format
```
🧪 Test Report: ✅ PASS

Score: 95%
Commit: abc1234
Time: 12:00:00

Tests:
✅ Html
✅ Css
✅ Javascript
✅ Responsive
✅ Accessibility
✅ Performance
✅ Security

📝 Recommendations:
🔧 Add alt text to images
```

---

## 🚨 FAILURE HANDLING

### When Tests Fail

1. **Immediate:** Pipeline stops
2. **Report:** Detailed failure saved
3. **Alert:** Telegram notification sent
4. **Suggestions:** Auto-generated fix ideas
5. **Recovery:** Manual fix required

### Common Failures

| Issue | Fix |
|-------|-----|
| JS syntax error | Check semicolons/braces |
| Missing alt text | Add alt="description" |
| Performance budget | Optimize images/bundle |
| Accessibility | Add ARIA labels |

---

## 🎯 PERFORMANCE BUDGETS

### Current Limits
- **Load time:** < 2 seconds
- **Bundle size:** < 500 KB
- **Accessibility:** > 90%
- **Lighthouse Performance:** > 90

### Override
Edit `.agent_config.json`:
```json
"performance_budget": {
  "max_load_time_ms": 3000,
  "max_bundle_size_kb": 1000
}
```

---

## 🔒 SECURITY

### Automated Checks
- ✅ No inline event handlers (XSS)
- ✅ No HTTP links (mixed content)
- ✅ No secrets in code (TruffleHog)
- ✅ Dependency vulnerabilities

### Secrets Management
Use GitHub Secrets:
```
Settings → Secrets → New repository secret
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
- DEPLOY_KEY
```

---

## 🌐 DEPLOYMENT

### Staging (Automatic)
```yaml
# In .github/workflows/semi-sovereign.yml
auto_deploy_staging: true  # After tests pass
```

### Production (Manual)
```bash
# After staging validation
python3 semi_sovereign_agent.py --deploy-production
```

---

## 📈 MONITORING

### Metrics Tracked
- Test pass/fail rate
- Performance trends
- Bundle size over time
- Accessibility score history

### Dashboard
```bash
# View all reports
ls -la app/reports/

# Latest report
cat app/reports/latest_notification.txt
```

---

## 🛠️ TROUBLESHOOTING

### Agent Won't Start
```bash
# Check Python version
python3 --version  # Need 3.10+

# Install dependencies
pip install -r requirements.txt

# Check permissions
chmod +x semi_sovereign_agent.py
```

### Tests Failing
```bash
# Run in debug mode
python3 semi_sovereign_agent.py --run-once --verbose

# Check specific test
python3 -c "
from semi_sovereign_agent import SemiSovereignAgent
agent = SemiSovereignAgent()
result = agent._test_html_validity()
print(result)
"
```

### Notifications Not Sending
```bash
# Check Telegram config
cat .agent_config.json | grep telegram

# Test manually
curl -X POST \
  https://api.telegram.org/bot${TOKEN}/sendMessage \
  -d chat_id=${CHAT_ID} \
  -d text="Test message"
```

---

## 🎓 ADVANCED USAGE

### Custom Tests

Add to `semi_sovereign_agent.py`:
```python
def _test_custom_feature(self):
    """Your custom test"""
    return {
        'passed': True,
        'details': 'Custom check passed'
    }
```

### Webhook Integration

```python
async def _send_webhook(self, report):
    """Send to custom endpoint"""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        await session.post(
            'https://your-webhook.com',
            json=report
        )
```

---

## 📞 SUPPORT

### Status Check
```bash
# Is agent running?
ps aux | grep semi_sovereign

# Latest activity
tail -f app/reports/latest_notification.txt
```

### Emergency Stop
```bash
# Kill agent
pkill -f semi_sovereign_agent

# Disable autonomous mode
python3 -c "
import json
with open('.agent_config.json', 'r') as f:
    config = json.load(f)
config['autonomous_mode'] = False
with open('.agent_config.json', 'w') as f:
    json.dump(config, f)
"
```

---

## 🎉 SUCCESS METRICS

The semi-sovereign agent is working when:
- ✅ Tests run on every commit
- ✅ Reports appear in `app/reports/`
- ✅ Telegram notifications arrive
- ✅ Staging auto-deploys (if enabled)
- ✅ You receive fix suggestions

**Zero manual intervention required.**

---

*"The agent cultivates while you sleep."*
