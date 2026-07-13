# Security Policy

Thank you for helping keep the **Shop Billing System** secure.

We take the security of this project seriously and appreciate responsible disclosure of potential vulnerabilities.

---

# Supported Versions

The following table shows which versions of the project currently receive security updates.

| Version | Supported |
| ------- | --------- |
| 1.x.x   | ✅ Yes     |
| 0.x.x   | ❌ No      |

Please upgrade to the latest supported version before reporting an issue that may already have been fixed.

---

# Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public GitHub Issue.

Instead, report it privately by contacting the project maintainer.

Include as much information as possible:

* Vulnerability description
* Steps to reproduce
* Expected behavior
* Actual behavior
* Affected version
* Operating system
* Python version
* Flask version
* Browser (if applicable)
* Screenshots or logs (if available)
* Suggested fix (optional)

Providing complete information helps us investigate and resolve the issue more quickly.

---

# Response Process

After receiving a security report, we will:

1. Acknowledge receipt of the report.
2. Investigate the reported issue.
3. Confirm whether the vulnerability is valid.
4. Develop and test a fix.
5. Release a security update if necessary.
6. Notify the reporter once the issue has been addressed.

---

# Responsible Disclosure

To help protect users, please:

* Do not publicly disclose the vulnerability before it has been fixed.
* Give maintainers a reasonable amount of time to investigate and resolve the issue.
* Avoid sharing exploit code that could put users at risk before a fix is available.

We appreciate responsible disclosure and collaboration.

---

# Security Best Practices

If you deploy this project, consider the following recommendations:

* Use a strong and unique `SECRET_KEY`.
* Store secrets in a `.env` file and never commit it to version control.
* Use strong MySQL credentials.
* Keep Python, Flask, and dependencies up to date.
* Restrict database access to trusted hosts.
* Use HTTPS in production.
* Validate and sanitize all user input.
* Protect against SQL injection and cross-site scripting (XSS).
* Regularly back up your database.
* Review logs for suspicious activity.

---

# Dependency Security

Regularly check for outdated or vulnerable packages.

Recommended commands:

```bash
pip list --outdated
```

Upgrade packages as needed:

```bash
pip install --upgrade package_name
```

---

# Supported Environment

Recommended software versions:

| Component | Version               |
| --------- | --------------------- |
| Python    | 3.10 or later         |
| Flask     | 2.3 or later          |
| MySQL     | 8.0 or later          |
| Bootstrap | 5.x                   |
| Chart.js  | Latest stable release |

---

# Security Updates

Security fixes will be included in future releases and documented in the project's `CHANGELOG.md`.

Users are encouraged to update to the latest version whenever possible.

---

# Contact

If you have questions about this security policy or need to report a vulnerability, please contact the project maintainer through the appropriate private communication channel rather than creating a public issue.

Thank you for helping keep the **Shop Billing System** secure.
