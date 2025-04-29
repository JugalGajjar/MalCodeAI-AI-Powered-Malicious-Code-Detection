few_shots = {}

few_shots["component_1"] = [
"""
{
  "component_type": "METHOD_DEFINITION",
  "component_name": "FlaskApp.upload",
  "component_code": "def upload(self):\\n    if 'username' not in session:\\n        return redirect(url_for('login'))\\n    if request.method == 'POST':\\n        file = request.files['profile_pic']\\n        if file:\\n            filename = file.filename\\n            file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))\\n            return f\\\"<p>Uploaded successfully: {filename}</p>\\\"\\n    return render_template('upload.html')",
  "component_description": "Handles user profile picture uploads and saves them to a server directory without sanitizing file names."
}
""",
"""
{
  "component_type": "METHOD_DEFINITION",
  "component_name": "FlaskApp.upload",
  "component_code": "def upload(self):\\n    if 'username' not in session:\\n        return redirect(url_for('login'))\\n    if request.method == 'POST':\\n        file = request.files['profile_pic']\\n        if file:\\n            filename = file.filename\\n            file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))\\n            return f\\\"<p>Uploaded successfully: {filename}</p>\\\"\\n    return render_template('upload.html')",
  "component_description": "Handles user profile picture uploads and saves them to a server directory without sanitizing file names.",
  "vulnerabilities": [
    {
      "vul_type": "Unrestricted File Upload",
      "cve_score": 8.6,
      "exploitation_methods": [
        "1. Upload a file named '../../app.py'.\\n2. Server overwrites critical code.\\n3. Gain remote code execution or crash the app.",
        "1. Upload a 'shell.php' or malicious executable.\\n2. Server executes uploaded code if misconfigured.",
        "1. Upload oversized files repeatedly.\\n2. Exhaust disk storage causing Denial of Service (DoS).",
        "1. Upload files with double extensions (e.g., 'profile.php.jpg').\\n2. Bypass extension checks to execute scripts."
      ],
      "developer_fixes": [
        "Sanitize file names to remove special characters and traversal sequences.",
        "Restrict allowed file types to safe image formats only.",
        "Save uploaded files with randomized names (UUIDs) instead of client-provided names.",
        "Store uploads outside of the web-accessible directory structure."
      ]
    }
  ]
}
"""
]

few_shots["component_2"] = [
"""
{
  "component_type": "FUNCTION_DEFINITION",
  "component_name": "renderProfile",
  "component_code": "function renderProfile(user) {\\n  document.getElementById('profile').innerHTML = \\\"<h1>\\\" + user.name + \\\"</h1><p>\\\" + user.bio + \\\"</p>\\\";\\n}",
  "component_description": "Renders user profile information on the page directly from user input without escaping HTML content."
}
""",
"""
{
  "component_type": "FUNCTION_DEFINITION",
  "component_name": "renderProfile",
  "component_code": "function renderProfile(user) {\\n  document.getElementById('profile').innerHTML = \\\"<h1>\\\" + user.name + \\\"</h1><p>\\\" + user.bio + \\\"</p>\\\";\\n}",
  "component_description": "Renders user profile information on the page directly from user input without escaping HTML content.",
  "vulnerabilities": [
    {
      "vul_type": "Cross-Site Scripting (XSS)",
      "cve_score": 6.9,
      "exploitation_methods": [
        "1. Set user.bio to '<script>alert(\\\"XSS\\\")</script>'.\\n2. Script runs when page loads.\\n3. Attacker executes arbitrary JS code.",
        "1. Inject scripts that steal session cookies.\\n2. Hijack user sessions or impersonate users.",
        "1. Inject malicious redirects via DOM manipulation.\\n2. Phish user credentials by sending them to attacker-controlled pages.",
        "1. Alter the website content by injecting arbitrary HTML elements."
      ],
      "developer_fixes": [
        "Escape all user-generated input before injecting into the DOM.",
        "Use DOM APIs like textContent or innerText instead of innerHTML for inserting user data.",
        "Implement Content Security Policy (CSP) headers to restrict script sources."
      ]
    }
  ]
}
"""
]

few_shots["component_3"] = [
"""
{
  "component_type": "CLASS_DEFINITION",
  "component_name": "UserAuth",
  "component_code": "<?php\\nclass UserAuth {\\n    private $db;\\n\\n    public function __construct($dbConnection) {\\n        $this->db = $dbConnection;\\n    }\\n\\n    public function login($username, $password) {\\n        $query = \\\"SELECT * FROM users WHERE username = '$username' AND password = '$password'\\\";\\n        $result = mysqli_query($this->db, $query);\\n\\n        if (mysqli_num_rows($result) > 0) {\\n            $_SESSION['user'] = $username;\\n            return true;\\n        }\\n        return false;\\n    }\\n}\\n?>",
  "component_description": "PHP user authentication class interacting with a MySQL database using raw SQL queries and storing plaintext passwords."
}
""",
"""
{
  "component_type": "CLASS_DEFINITION",
  "component_name": "UserAuth",
  "component_code": "<?php\\nclass UserAuth {\\n    private $db;\\n\\n    public function __construct($dbConnection) {\\n        $this->db = $dbConnection;\\n    }\\n\\n    public function login($username, $password) {\\n        $query = \\\"SELECT * FROM users WHERE username = '$username' AND password = '$password'\\\";\\n        $result = mysqli_query($this->db, $query);\\n\\n        if (mysqli_num_rows($result) > 0) {\\n            $_SESSION['user'] = $username;\\n            return true;\\n        }\\n        return false;\\n    }\\n}\\n?>",
  "component_description": "PHP user authentication class interacting with a MySQL database using raw SQL queries and storing plaintext passwords.",
  "vulnerabilities": [
    {
      "vul_type": "SQL Injection",
      "cve_score": 9.8,
      "exploitation_methods": [
        "1. Supply username as ' OR '1'='1.\\n2. SQL query always evaluates true.\\n3. Bypass authentication without valid credentials.",
        "1. Inject 'UNION SELECT' payloads.\\n2. Extract data from other tables (e.g., user emails, passwords).",
        "1. Inject DROP TABLE statements.\\n2. Corrupt or destroy application database."
      ],
      "developer_fixes": [
        "Use prepared statements with parameter binding for SQL queries.",
        "Sanitize and validate all user inputs before database interaction.",
        "Apply least privilege principles on database accounts."
      ]
    },
    {
      "vul_type": "Plaintext Password Storage",
      "cve_score": 7.1,
      "exploitation_methods": [
        "1. Database breach reveals plaintext passwords.\\n2. Use leaked passwords for credential stuffing on other services.",
        "1. Attacker instantly knows users' real passwords without needing to crack any hashes."
      ],
      "developer_fixes": [
        "Hash passwords using secure algorithms like bcrypt or Argon2 before storage.",
        "Never store or transmit passwords in plaintext."
      ]
    }
  ]
}
"""
]

few_shots["component_4"] = [
"""
{
  "component_type": "METHOD_DEFINITION",
  "component_name": "FileDownloader.downloadFile",
  "component_code": "public void downloadFile(String filename) throws IOException {\\n    File file = new File(\\\"/var/www/uploads/\\\" + filename);\\n    if (file.exists()) {\\n        Files.copy(file.toPath(), new FileOutputStream(\\\"downloaded_\\\" + filename));\\n    }\\n}",
  "component_description": "Java method for downloading files from a server directory based on user-supplied filenames without validation."
}
""",
"""
{
  "component_type": "METHOD_DEFINITION",
  "component_name": "FileDownloader.downloadFile",
  "component_code": "public void downloadFile(String filename) throws IOException {\\n    File file = new File(\\\"/var/www/uploads/\\\" + filename);\\n    if (file.exists()) {\\n        Files.copy(file.toPath(), new FileOutputStream(\\\"downloaded_\\\" + filename));\\n    }\\n}",
  "component_description": "Java method for downloading files from a server directory based on user-supplied filenames without validation.",
  "vulnerabilities": [
    {
      "vul_type": "Path Traversal",
      "cve_score": 7.6,
      "exploitation_methods": [
        "1. Supply filename '../../etc/passwd'.\\n2. Server reads sensitive OS files.\\n3. Disclosure of critical system information.",
        "1. Traverse to application source code files.\\n2. Steal intellectual property or discover vulnerabilities."
      ],
      "developer_fixes": [
        "Normalize and validate user-supplied paths.",
        "Restrict file access strictly within allowed directories.",
        "Reject filenames containing '../' or similar traversal sequences."
      ]
    },
    {
      "vul_type": "Information Exposure",
      "cve_score": 6.5,
      "exploitation_methods": [
        "1. Download .env files with API keys and credentials.",
        "2. Download configuration backups revealing sensitive internal data."
      ],
      "developer_fixes": [
        "Ensure that sensitive files are not stored alongside user-uploaded data.",
        "Apply server-side file access control mechanisms."
      ]
    }
  ]
}
"""
]

few_shots["component_5"] = [
"""
{
  "component_type": "FUNCTION_DEFINITION",
  "component_name": "SafeLogin",
  "component_code": "func SafeLogin(username, password string, db *sql.DB) (bool, error) {\\n    stmt, err := db.Prepare(\\\"SELECT id FROM users WHERE username=? AND password_hash=?\\\")\\n    if err != nil {\\n        return false, err\\n    }\\n    defer stmt.Close()\\n\\n    row := stmt.QueryRow(username, password)\\n    var id int\\n    err = row.Scan(&id)\\n    if err != nil {\\n        if err == sql.ErrNoRows {\\n            return false, nil\\n        }\\n        return false, err\\n    }\\n    return true, nil\\n}",
  "component_description": "Go function that safely authenticates users against a database using prepared statements to prevent SQL injection."
}
""",
"""
{
  "component_type": "FUNCTION_DEFINITION",
  "component_name": "SafeLogin",
  "component_code": "func SafeLogin(username, password string, db *sql.DB) (bool, error) {\\n    stmt, err := db.Prepare(\\\"SELECT id FROM users WHERE username=? AND password_hash=?\\\")\\n    if err != nil {\\n        return false, err\\n    }\\n    defer stmt.Close()\\n\\n    row := stmt.QueryRow(username, password)\\n    var id int\\n    err = row.Scan(&id)\\n    if err != nil {\\n        if err == sql.ErrNoRows {\\n            return false, nil\\n        }\\n        return false, err\\n    }\\n    return true, nil\\n}",
  "component_description": "Go function that safely authenticates users against a database using prepared statements to prevent SQL injection.",
  "vulnerabilities": []
}
"""
]

few_shots["component_6"] = [
"""
{
  "component_type": "METHOD_DEFINITION",
  "component_name": "notes_page",
  "component_code": "def notes_page(self):\\n        if 'username' not in session:\\n            return redirect(url_for('login'))\\n        user_notes = self.notes.get(session['username'], [])\\n        return render_template_string(self.notes_template, username=session['username'], notes=user_notes)",
  "component_description": "Notes page route displaying user notes, requiring login and rendering the notes template with user-specific data."
}
""",
"""
{
  "component_type": "METHOD_DEFINITION",
  "component_name": "notes_page",
  "component_code": "def notes_page(self):\\n        if 'username' not in session:\\n            return redirect(url_for('login'))\\n        user_notes = self.notes.get(session['username'], [])\\n        return render_template_string(self.notes_template, username=session['username'], notes=user_notes)",
  "component_description": "Notes page route displaying user notes, requiring login and rendering the notes template with user-specific data.",
  "vulnerabilities": []
}
"""
]

few_shots["component_7"] = [
"""
{
  "component_type": "FUNCTION_DEFINITION",
  "component_name": "create_post",
  "component_code": "async fn create_post(req: HttpRequest, body: String) -> impl Responder {\\n    let post: serde_json::Value = serde_json::from_str(&body).unwrap();\\n    let title = post[\\\"title\\\"].as_str().unwrap();\\n    let content = post[\\\"content\\\"].as_str().unwrap();\\n    sqlx::query(format!(\\\"INSERT INTO posts (title, content) VALUES ('{}', '{}')\\\", title, content))\\n        .execute(&*DB_POOL)\\n        .await\\n        .unwrap();\\n    HttpResponse::Ok().body(\\\"Post created\\\")\\n}",
  "component_description": "Rust async web API to create blog posts, vulnerable to SQL Injection and lacking input validation."
}
""",
"""
{
  "component_type": "FUNCTION_DEFINITION",
  "component_name": "create_post",
  "component_code": "async fn create_post(req: HttpRequest, body: String) -> impl Responder {\\n    let post: serde_json::Value = serde_json::from_str(&body).unwrap();\\n    let title = post[\\\"title\\\"].as_str().unwrap();\\n    let content = post[\\\"content\\\"].as_str().unwrap();\\n    sqlx::query(format!(\\\"INSERT INTO posts (title, content) VALUES ('{}', '{}')\\\", title, content))\\n        .execute(&*DB_POOL)\\n        .await\\n        .unwrap();\\n    HttpResponse::Ok().body(\\\"Post created\\\")\\n}",
  "component_description": "Rust async web API to create blog posts, vulnerable to SQL Injection and lacking input validation.",
  "vulnerabilities": [
    {
      "vul_type": "SQL Injection",
      "cve_score": 9.5,
      "exploitation_methods": [
        "1. Supply title with a malicious payload like \\\"'; DROP TABLE posts;--\\\".\\n2. Corrupt or delete critical database tables.",
        "1. Inject SQL statements to leak sensitive database information."
      ],
      "developer_fixes": [
        "Always use parameterized queries rather than string interpolation for SQL.",
        "Validate user input strictly before using it in queries."
      ]
    },
    {
      "vul_type": "Denial of Service (DoS) - Panic on Invalid JSON",
      "cve_score": 5.5,
      "exploitation_methods": [
        "1. Send malformed JSON payloads.\\n2. Cause server panics or crashes due to unhandled unwrap() calls."
      ],
      "developer_fixes": [
        "Handle JSON parsing errors gracefully without using `.unwrap()`.",
        "Return appropriate HTTP 400 responses on invalid input instead of crashing."
      ]
    }
  ]
}
"""
]

few_shots["component_8"] = [
"""
{
  "component_type": "CLASS_DEFINITION",
  "component_name": "EmailQueueWorker",
  "component_code": "using System;\\nusing System.Threading.Tasks;\\n\\npublic class EmailQueueWorker\\n{\\n    private readonly IEmailService _emailService;\\n\\n    public EmailQueueWorker(IEmailService emailService)\\n    {\\n        _emailService = emailService;\\n    }\\n\\n    public async Task ProcessQueueAsync(Queue<EmailMessage> queue)\\n    {\\n        while (queue.Count > 0)\\n        {\\n            var message = queue.Dequeue();\\n            try\\n            {\\n                await _emailService.SendEmailAsync(message);\\n            }\\n            catch (Exception ex)\\n            {\\n                Console.WriteLine($\\\"Failed to send email: {ex.Message}\\\");\\n            }\\n        }\\n    }\\n}",
  "component_description": "C# background worker that processes a queue of email messages and handles exceptions securely."
}
""",
"""
{
  "component_type": "CLASS_DEFINITION",
  "component_name": "EmailQueueWorker",
  "component_code": "using System;\\nusing System.Threading.Tasks;\\n\\npublic class EmailQueueWorker\\n{\\n    private readonly IEmailService _emailService;\\n\\n    public EmailQueueWorker(IEmailService emailService)\\n    {\\n        _emailService = emailService;\\n    }\\n\\n    public async Task ProcessQueueAsync(Queue<EmailMessage> queue)\\n    {\\n        while (queue.Count > 0)\\n        {\\n            var message = queue.Dequeue();\\n            try\\n            {\\n                await _emailService.SendEmailAsync(message);\\n            }\\n            catch (Exception ex)\\n            {\\n                Console.WriteLine($\\\"Failed to send email: {ex.Message}\\\");\\n            }\\n        }\\n    }\\n}",
  "component_description": "C# background worker that processes a queue of email messages and handles exceptions securely.",
  "vulnerabilities": []
}
"""
]