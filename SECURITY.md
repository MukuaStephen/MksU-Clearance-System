# Security Checklist - MKSU Clearance System

## ✅ Completed Security Measures

### 1. Git Ignore Configuration
- [x] `.env` files are excluded from git tracking
- [x] Database files (`*.sqlite3`, `*.db`) are excluded
- [x] Media uploads directory excluded (contains student data)
- [x] SSH keys and certificates excluded (`*.pem`, `*.key`, `*.crt`)
- [x] Credentials files excluded (`credentials.json`, `secrets.json`)
- [x] Backup files excluded (`*.bak`, `*.backup`)
- [x] Log files excluded (`*.log`)
- [x] Python cache excluded (`__pycache__/`, `*.pyc`)

### 2. Environment Files
- [x] `.env` removed from git tracking (if it was tracked)
- [x] `.env.example` created as template (safe to commit)
- [x] `.env.mysql.example` exists as reference

### 3. Database Security
- [x] `db.sqlite3` removed from git tracking
- [x] MySQL database used (more secure than SQLite for production)
- [x] Database credentials stored in `.env` file only

### 4. Sensitive Data Protection
- [x] Student uploads directory (`media/`, `evidence/`, `receipts/`) excluded
- [x] All uploaded files are protected from git tracking

---

## 🔐 Files Currently Protected

The following sensitive files are **NOT** tracked by git:

1. **Environment & Configuration**
   - `BACKEND/.env` (contains DB password, JWT secret, email password)
   - Any `.env.*` files (except `.example` files)

2. **Database Files**
   - `db.sqlite3`
   - `*.db`, `*.sqlite`, `*.sqlite3`
   - `*.sql` (database dumps)

3. **Uploaded Documents**
   - `media/` (all media files)
   - `receipts/` (payment receipts)
   - `fee_statements/` (student fee documents)
   - `evidence/` (clearance evidence files)

4. **Security Credentials**
   - `*.pem`, `*.key`, `*.pub` (SSH keys)
   - `*.crt`, `*.cer` (certificates)
   - `credentials.json`, `secrets.json`

5. **Backup & Temporary Files**
   - `*.bak`, `*.backup`, `*.old`
   - Log files (`*.log`)

---

## 📋 Before Pushing to GitHub - Checklist

Run these commands before every push:

```bash
# 1. Check what files are staged
git status

# 2. Verify no .env files are tracked
git ls-files | Select-String "\.env$"
# Should only show: BACKEND/.env.example, BACKEND/.env.mysql.example

# 3. Verify no database files are tracked
git ls-files | Select-String "\.sqlite3$|\.db$"
# Should show nothing

# 4. Check for any accidentally staged sensitive files
git diff --cached --name-only | Select-String "\.env$|\.sqlite|password|secret|key\.json"
# Should show nothing
```

---

## ⚠️ What to NEVER Commit

**NEVER** commit files containing:

1. **Passwords & Secrets**
   - Database passwords
   - JWT secret keys
   - Email passwords
   - API keys (M-PESA, SSO)
   - Any credentials

2. **Personal/Sensitive Data**
   - Student uploaded documents
   - Payment receipts
   - Personal information
   - Database dumps with real data

3. **Environment-Specific Config**
   - `.env` files
   - `local_settings.py`
   - Production configuration files

---

## 🛡️ Additional Security Recommendations

### For Development
- [x] Use `.env` for all sensitive configuration
- [ ] Rotate JWT secret keys regularly
- [ ] Use strong database passwords (minimum 16 characters)
- [ ] Never use default passwords in production
- [ ] Keep `DEBUG=False` in production

### For Production
- [ ] Use environment variables (not `.env` files)
- [ ] Enable HTTPS only (`SECURE_SSL_REDIRECT=True`)
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Use strong `SECRET_KEY` (minimum 50 characters)
- [ ] Restrict `ALLOWED_HOSTS` to your domain only
- [ ] Enable database backups (encrypted)
- [ ] Monitor for security vulnerabilities
- [ ] Keep dependencies updated
- [ ] Use Redis with password authentication
- [ ] Configure proper firewall rules

### For Team Collaboration
- [ ] Each developer should have their own `.env` file
- [ ] Never share `.env` files via Slack/Email/etc.
- [ ] Use a secure password manager for sharing credentials
- [ ] Rotate shared secrets when team members leave
- [ ] Use different credentials for dev/staging/production

---

## 🔍 Regular Security Audits

Run these checks monthly:

```bash
# Check for exposed secrets in git history
git log --all --full-history --source -- "**/.env"

# Check for accidentally committed sensitive files
git log --all --full-history --source -- "**/*.env" "**/*.pem" "**/*.key"

# Scan for hardcoded secrets in code
git grep -i "password.*=.*['\"]" -- "*.py" "*.js"
git grep -i "secret.*=.*['\"]" -- "*.py" "*.js"
```

---

## 📞 If Credentials are Exposed

If you accidentally commit sensitive data:

1. **Immediately rotate all exposed credentials:**
   - Change database passwords
   - Regenerate JWT secret
   - Reset email passwords
   - Invalidate API keys

2. **Remove from git history:**
   ```bash
   # Remove file from history (dangerous - backup first!)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch BACKEND/.env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (if repository is private and you're the only user)
   git push origin --force --all
   ```

3. **Contact your team and GitHub support if needed**

---

## ✅ Current Status

- **Git Ignore**: ✅ Comprehensive (covers all sensitive files)
- **Environment Files**: ✅ Protected
- **Database Files**: ✅ Protected
- **Uploads Directory**: ✅ Protected
- **Credentials**: ✅ Not in repository

**Your repository is now secure! 🔒**

---

## 📚 Additional Resources

- [Django Security Best Practices](https://docs.djangoproject.com/en/4.2/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
