module.exports = {
  apps: [
    {
      name: "propflow-backend",
      script: ".venv/bin/uvicorn",
      args: "backend.main:app --host 127.0.0.1 --port 8000",
      interpreter: "none",
      env: {
        PYTHONPATH: "."
      }
    },
    {
      name: "propflow-frontend",
      cwd: "./web",
      script: "node_modules/next/dist/bin/next",
      args: "dev -p 3000",
      interpreter: "none"
    }
  ]
};
