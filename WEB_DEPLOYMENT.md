# Bytecode Interpreter Web Interface

A simple web frontend for the bytecode interpreter that mimics the GUI functionality.

## Features

- **Web-based Editor**: Write and edit bytecode directly in the browser
- **Real-time Execution**: Run bytecode and see immediate results
- **Code Optimization**: Optimize bytecode with a single click
- **Example Programs**: Pre-built examples to learn from
- **State Inspection**: View stack, variables, and execution state
- **Responsive Design**: Works on desktop and mobile devices

## Local Development

### Prerequisites
- Python 3.8 or higher
- pip

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   python app.py
   ```

3. Open your browser to `http://localhost:5000`

## Deployment to Fly.io

### Prerequisites
- [Fly.io CLI](https://fly.io/docs/hands-on/install-flyctl/) installed
- Fly.io account

### Deploy Steps

1. **Login to Fly.io**:
   ```bash
   flyctl auth login
   ```

2. **Launch the app** (first time only):
   ```bash
   flyctl launch
   ```
   - Choose app name (or use `bytecode-interpreter`)
   - Select region closest to your users
   - Don't add a database
   - Don't deploy immediately

3. **Deploy the application**:
   ```bash
   flyctl deploy
   ```

4. **Open your deployed app**:
   ```bash
   flyctl open
   ```

### Configuration

The app is configured via `fly.toml`:
- **Port**: 8080 (internal), 443/80 (external)
- **Memory**: 512MB
- **CPU**: 1 shared CPU
- **Auto-scaling**: Enabled (0 minimum machines)

### Environment Variables

Set environment variables for production:
```bash
flyctl secrets set FLASK_ENV=production
flyctl secrets set SECRET_KEY=your-secret-key-here
```

## API Endpoints

The web interface also provides JSON API endpoints:

- `POST /api/run` - Run bytecode and return JSON results
- `POST /api/optimize` - Optimize bytecode and return JSON results
- `GET /health` - Health check endpoint

### API Usage Example

```javascript
// Run bytecode
fetch('/api/run', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        code: 'PUSH 10\nPUSH 20\nADD\nPRINT\nHALT'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Security Considerations

- **Input Validation**: All bytecode input is validated
- **Error Handling**: Graceful error handling for malformed code
- **Resource Limits**: File upload limits and timeout protection
- **HTTPS**: Forced HTTPS in production

## Monitoring

- Health check endpoint: `/health`
- Fly.io provides built-in metrics and logging
- View logs: `flyctl logs`
- Monitor status: `flyctl status`

## Troubleshooting

### Common Issues

1. **App won't start**:
   ```bash
   flyctl logs
   ```

2. **Memory issues**:
   ```bash
   flyctl scale memory 1024
   ```

3. **Performance issues**:
   ```bash
   flyctl scale count 2
   ```

### Useful Commands

- View app status: `flyctl status`
- Scale resources: `flyctl scale`
- View secrets: `flyctl secrets list`
- SSH into app: `flyctl ssh console`

## License

This project is part of the Bytecode Interpreter educational toolkit.
